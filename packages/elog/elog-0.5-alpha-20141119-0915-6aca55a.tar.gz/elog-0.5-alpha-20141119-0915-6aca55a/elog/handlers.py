import sys
import threading
import queue
import socket
import requests
import requests.exceptions
import json
import logging
import traceback
import datetime
import time


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Public classes #####
class ElasticHandler(logging.Handler, threading.Thread):  # pylint: disable=R0902,R0904
    """
        Example config:
            ...
            elastic:
                level: DEBUG
                class: elog.handlers.ElasticHandler
                time_field: "@timestamp"
                time_format: "%Y-%m-%dT%H:%M:%S.%f"
                url: http://example.com:9200
                index: log-{@timestamp:%Y}-{@timestamp:%m}-{@timestamp:%d}
                doctype: gns2
                fields:
                    logger:    name
                    level:     levelname
                    msg:       msg
                    args:      args
                    file:      pathname
                    line:      lineno
                    pid:       process
            ...

        Required arguments:
            url
            index
            doctype

        Optional arguments:
            fields         -- A dictionary with mapping LogRecord fields to ElasticSearch fields
            time_field     -- Timestamp field name
            time_format    -- Timestamp format
            queue_size     -- The maximum size of the send queue, after which the caller thread is blocked
            bulk_size      -- Number of messages in one session
            retries        -- If the bulk will not be sent to N times, it will be lost
            retry_interval -- Delay between attempts to send
            url_timeout    -- Socket timeout
            log_timeout    -- Maximum waiting time of sending
            respawn_delay  -- If loop in the main thread a fails, it is restarted after X seconds, by default - 1
            blocking       -- Block logging, if the queue is full, by default - False

        The class does not use any formatters.
    """
    def __init__(  # pylint: disable=R0913
            self,
            url,
            index,
            doctype,
            fields=None,
            time_field="time",
            time_format="%s",
            queue_size=512,
            bulk_size=512,
            retries=5,
            retry_interval=1,
            url_timeout=socket._GLOBAL_DEFAULT_TIMEOUT,  # pylint: disable=W0212
            log_timeout=5,
            respawn_delay=1,
            blocking=False,
        ):
        logging.Handler.__init__(self)
        threading.Thread.__init__(self)

        self._url = url
        self._index = index
        self._doctype = doctype
        self._fields = ( fields or {} )
        self._time_field = time_field
        self._time_format = time_format
        self._bulk_size = bulk_size
        self._retries = retries
        self._retry_interval = retry_interval
        self._url_timeout = url_timeout
        self._log_timeout = log_timeout
        self._respawn_delay = respawn_delay
        self._blocking = blocking

        self._queue = queue.Queue(queue_size)

        # XXX: http://docs.python-requests.org/en/latest/user/advanced/
        # Thanks to urllib3, keep-alive is 100% automatic within a session. Any requests that you
        # make within a session will automatically reuse the appropriate connection.
        self._session = requests.Session()

        self.start()


    ### Public ###

    def emit(self, record):
        # Formatters are not used
        if self.continue_processing():
            # While the application works - we accept the message to send
            message = self._make_message(record)
            if self._blocking:
                try:
                    self._queue.put(message, block=False)
                except queue.Full:
                    _exc_stderr("Can't log the message: '{}'. Queue is full.".format(message))
            else:
                self._queue.put(message)

    def continue_processing(self):  # pylint: disable=R0201
        # This thread must be one of the last live threads. Usually, MainThread lives up to the
        # completion of all the rest. We need to determine when it is completed and to stop sending
        # and receiving messages. For our architecture that is enough. In other cases, you can
        # override this method.

        if hasattr(threading, "main_thread"):  # Python >= 3.4
            main_thread = threading.main_thread()  # pylint: disable=E1101
        else:  # Dirty hack for Python <= 3.3
            main_thread = threading._shutdown.__self__  # pylint: disable=W0212,E1101

        return main_thread.is_alive()


    ### Override ###

    def run(self):
        wait_until = time.time() + self._log_timeout
        while self.continue_processing() or not self._queue.empty():
            # After sending a message in the log, we get the main thread object
            # and check if he is alive. If not - stop sending logs.
            # If the queue still have messages - process them.

            if not self.continue_processing():
                # If application is dead, quickly dismantle the remaining queue and break the cycle.
                wait_until = 0

            items = []
            try:
                while len(items) < self._bulk_size:
                    items.append(self._queue.get(timeout=max(wait_until - time.time(), 0)))
            except queue.Empty:
                wait_until = time.time() + self._log_timeout

            if len(items) != 0:
                try:
                    self._send_messages(items)
                except Exception:
                    _exc_stderr("Exception occurred in the ElasticHandler loop, "
                        "the process will be restarted in {} seconds".format(self._respawn_delay))
                    self._session = requests.Session()  # Drop old session
                    time.sleep(self._respawn_delay)


    ### Private ###

    def _make_message(self, record):
        msg = {
            name: getattr(record, item)
            for (name, item) in self._fields.items()
            if hasattr(record, item)
        }
        msg[self._time_field] = datetime.datetime.utcfromtimestamp(record.created)
        return msg

    def _send_messages(self, messages):
        # See for details:
        #   http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-bulk.html
        bulks = []
        for msg in messages:
            bulks.append({  # Data metainfo: index, doctype
                    "index": {
                        "_index": self._index.format(**msg),
                        "_type":  self._doctype.format(**msg),
                    },
                })
            bulks.append(msg)  # Log record
        data = ("\n".join(map(self._json_dumps, bulks)) + "\n").encode()

        retries = self._retries
        while True:
            try:
                self._session.post(self._url + "/_bulk", data=data, timeout=self._url_timeout)
                break
            except requests.exceptions.RequestException:
                if retries == 0:
                    _logger.exception("ElasticHandler could not send %d log records after %d retries",
                        len(messages), self._retries)
                    break
                retries -= 1
                time.sleep(self._retry_interval)

    def _json_dumps(self, obj):
        return json.dumps(obj, cls=_DatetimeEncoder, time_format=self._time_format)


class _DatetimeEncoder(json.JSONEncoder):
    def __init__(self, time_format, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)
        self._time_format = time_format

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            return format(obj, self._time_format)
        return repr(obj)  # Convert non-encodable objects to string


##### Private methods #####
def _exc_stderr(msg):
    print(msg, file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
