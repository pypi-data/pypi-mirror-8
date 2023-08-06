import json
import time
import requests
import logging
from datetime import datetime
from urllib.parse import urljoin

from .exceptions import AuthenticationError, ResourceNotFoundError, InternalServerError, ConnectionError

JSON_HTTP_HEADERS = {'content-type': 'application/json'}

class RequestsMixin:
    def __init__(self):
        self.entity_id = ""
        self.api_key = ""
        self.session = requests.Session()
        self.connected = False

        self.set_hpit_root_url('https://www.hpit-project.org')
        self.set_requests_log_level('debug')

        self._add_hooks('pre_connect', 'post_connect', 'pre_disconnect', 'post_disconnect')


    def set_hpit_root_url(self, root_url):
        self._hpit_root_url = root_url


    def set_requests_log_level(self, log_level):
        requests_log = logging.getLogger("requests")

        if log_level == 'warning':
            requests_log.setLevel(logging.WARNING)
        elif log_level == 'debug':
            requests_log.setLevel(logging.DEBUG)
        elif log_level == 'info':
            requests_log.setLevel(logging.INFO)

        self._requests_log_level = log_level


    def connect(self, retry=True):
        """
        Register a connection with the HPIT Server.

        This essentially sets up a session and logs that you are actively using
        the system. This is mostly used to track plugin use with the site.
        """
        self._try_hook('pre_connect')
        self._post_data('connect', {
                'entity_id': self.entity_id, 
                'api_key': self.api_key
            }, retry=retry
        )

        self.connected = True
        self._try_hook('post_connect')
       
        return self.connected


    def disconnect(self, retry=True):
        """
        Tells the HPIT Server that you are not currently going to poll
        the server for messages or responses. This also destroys the current session
        with the HPIT server.
        """
        self._try_hook('pre_disconnect')
        
        self._post_data('disconnect', {
                'entity_id': self.entity_id,
                'api_key': self.api_key
            }, retry=retry
        )

        self.connected = False
        self._try_hook('post_disconnect')

        return self.connected


    def _post_data(self, url, data=None, retry=True):
        """
        Sends arbitrary data to the HPIT server. This is mainly a thin
        wrapper ontop of requests that ensures we are using sessions properly.

        Returns: requests.Response : class - The response from HPIT. Normally a 200:OK.
        """
        url = urljoin(self._hpit_root_url, url)

        failure_count = 0
        while failure_count < 3:
            try:
                if data:
                    response = self.session.post(url, data=json.dumps(data), headers=JSON_HTTP_HEADERS)
                else:
                    response = self.session.post(url)

                if response is None:
                    raise ConnectionError("Connection was reset by a peer or the server rebooted.")
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    raise AuthenticationError("Request could not be authenticated")
                elif response.status_code == 404:
                    raise ResourceNotFoundError("Requested resource not found")
                elif response.status_code == 500:
                    raise InternalServerError("Internal server error")

                return response

            except requests.exceptions.ConnectionError:
                if failure_count == 3:
                    raise ConnectionError("Could not connect to server. Tried 3 times.")

                failure_count += 1
                continue

        #It looks like the server went down. Wait 5 minutes and try again
        if retry:
            return self._attempt_reconnection(lambda: self._post_data(url, data))

        raise ConnectionError("Connection was reset by a peer or the server stopped responding.")


    def _get_data(self, url, retry=True):
        """
        Gets arbitrary data from the HPIT server. This is mainly a thin
        wrapper on top of requests that ensures we are using session properly.

        Returns: dict() - A Python dictionary representing the JSON recieved in the request.
        """
        url = urljoin(self._hpit_root_url, url)

        failure_count = 0
        while failure_count < 3:
            try:
                response = self.session.get(url)

                if response is None:
                    raise ConnectionError("Connection was reset by a peer or the server rebooted.")

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    raise AuthenticationError("Request could not be authenticated")
                elif response.status_code == 404:
                    raise ResourceNotFoundError("Requested resource not found")
                elif response.status_code == 500:
                    raise InternalServerError("Internal server error")

                return response

            except requests.exceptions.ConnectionError as e:
                if failure_count == 3:
                    raise e

                failure_count += 1
                continue

        #It looks like the server went down. Wait 5 minutes and try again
        if retry:
            return self._attempt_reconnection(lambda: self._get_data(url))

        raise ConnectionError("Connection was reset by a peer or the server stopped responding.")


    def _attempt_reconnection(self, callback):
        self.connected = False
        print("Looks like the server went down. Waiting 5 minutes...")

        failure_count = 0
        while failure_count < 3:
            time.sleep(300)

            #Just hit the front page
            response = self.session.get(self._hpit_root_url)

            if response and response.status_code == 200:
                print("Server looks like it finished rebooting... attempting reconnect.")

                try:
                    self.connect(retry=False)
                except: #Still having problems
                    failure_count += 1
                    continue

                print("Successfully reconnected... continuing as normal")
                return callback()
            else:
                failure_count += 1


        raise ConnectionError("Could not reconnect to the server. Shutting down.")


    def send_log_entry(self, text):
        """
        Send a log entry to the HPIT server.
        """
        self._post_data("log", data={'log_entry':text})

        #Log to file if a logger variable is set on this class instance
        logger = getattr(self, 'logger', None)
        if logger:
            logger.debug(text)


    def _add_hooks(self, *hooks):
        """
        Adds hooks to this class. If the function is already defined, this leaves that definition. If 
        it doesn't exists the hook is created and set to None
        """
        for hook in hooks:
            if not hasattr(self, hook):
                setattr(self, hook, None)


    def _try_hook(self, hook_name):
        """
        Try's to call a signal hook. Hooks take in no parameters and return a boolean result.
        True will cause the plugin to continue execution.
        False will cause the plugon to stop execution.
        """
        hook = getattr(self, hook_name, None)

        if hook:
            return hook()
        else:
            return True

