"""The main module for communicating with the Crafty Web API"""
from urllib.parse import urljoin
import requests
import sys

from crafty_client.static.routes import CraftyAPIRoutes
from crafty_client.static.exceptions import (
    MissingParameters,
    ServerAlreadyRunning,
    ServerNotFound,
    ServerNotRunning,
    AccessDenied,
    NotAllowed,
    ServerStopping,
    InvalidJson,
)


# allow room for commander :)
class Crafty4:
    """The main class for communicating with the Crafty Web API"""

    def __init__(self, url, api_token, verify_ssl=False, debug=False):
        self.url = url
        self.verify_ssl = verify_ssl
        self.token = api_token
        self.debug = debug

    def _unpack_response(self, response_dict):
        if response_dict["status"] == "error":
            return (
                response_dict["status"],
                response_dict["error"],
            )
        if self.debug:
            sys.stderr.write(f"Crafty4 DEBUG: RES:{response_dict}\n")
        return (
            response_dict["status"],
            response_dict.get("data", {}),
        )

    def _check_errors(self, error):
        if error == "ACCESS_DENIED" or error == "NOT_AUTHORIZED":
            raise AccessDenied()
        elif error == "SER_NOT_RUNNING":
            raise ServerNotRunning()
        elif error == "SER_STOP_CALLED" or error == "SER_RESTART_CALLED":
            raise ServerStopping()
        elif error == "NO_COMMAND" or error == "MISSING_PARAMS":
            raise MissingParameters(
                "Your request is missing essential parameters or they are invalid"
            )
        elif error == "INVALID_JSON" or error == "INVALID_JSON_SCHEMA":
            raise InvalidJson()
        elif error == "TRAVERSAL DETECTED":
            raise ValueError("Path traversal detected")
        elif error == "SER_RUNNING":
            raise ServerAlreadyRunning()
        elif error == "NOT_ALLOWED":
            raise NotAllowed()
        elif error == "NOT_FOUND":
            raise ServerNotFound()
        else:
            pass

    def _make_get_request(self, api_route, extra_params=None, body=None):
        api_location = urljoin(self.url, api_route)

        params = {"token": self.token}
        if extra_params:
            params.update(extra_params)
        with requests.get(
            api_location, verify=self.verify_ssl, params=params, data=body
        ) as route:
            if self.debug:
                sys.stderr.write(f"Crafty4 DEBUG: REQ:GET:{api_route}::{extra_params}::{body}\n")
            data = route.json()
            return self._unpack_response(data)

    def _make_post_request(self, api_route, extra_params=None, body=None):
        api_location = urljoin(self.url, api_route)

        params = {"token": self.token}
        if extra_params:
            params.update(extra_params)
        with requests.post(
            api_location, verify=self.verify_ssl, params=params, data=body
        ) as route:
            if self.debug:
                sys.stderr.write(f"Crafty4 DEBUG: REQ:POST:{api_route}::{extra_params}::{body}\n")
            data = route.json()
            return self._unpack_response(data)

    def list_mc_servers(self, by_name=False, all_data=False):
        """Asks Crafty for a list of servers"""
        status, data = self._make_get_request(CraftyAPIRoutes.LIST)
        if status == "ok":
            if by_name:
                server_count = 0
                return_data = dict()
                for items in data:
                    return_data[server_count] = items.get("server_id", 0)
                    server_count += 1
                    return_data[server_count] = items.get("server_name", 0)
                return return_data
            if all_data:
                server_count = 0
                return_data = dict()
                for items in data:
                    return_data[server_count] = items.get("server_id", 0)
                    server_count += 1
                    return_data[server_count] = items.get("server_name", 0)
                    server_count += 1
                    return_data[server_count] = items.get("running", 0)
                    server_count += 1
                    return_data[server_count] = items.get("auto_start", 0)
                return return_data
            else:
                return data
        else:
            self._check_errors(data)

    def start_server(self, server_id):
        """Tells crafty to start the specified server, raises
        ServerNotFound if crafty cannot find the server"""
        status, data = self._make_post_request(
            CraftyAPIRoutes.SEND_CMD.format(id=server_id, action="start_server"),
        )

        if status == "ok":
            return True
        else:
            self._check_errors(data)

    def stop_server(self, server_id):
        """Tells crafty to stop the specified server, raises
        ServerNotFound if crafty cannot find the server"""
        status, data = self._make_post_request(
            CraftyAPIRoutes.SEND_CMD.format(id=server_id, action="stop_server"),
        )

        if status == "ok":
            return True
        else:
            self._check_errors(data)

    def backup_server(self, server_id):
        """Tells crafty to backup the specified server, raises
        ServerNotFound if crafty cannot find the server"""
        status, data = self._make_post_request(
            CraftyAPIRoutes.SEND_CMD.format(id=server_id, action="backup_server"),
        )
        if status == "ok":
            return True
        else:
            self._check_errors(data)

    def restart_server(self, server_id):
        """Tells crafty to restart the specified server,
        raises ServerNotFound if crafty cannot find the server"""
        status, data = self._make_post_request(
            CraftyAPIRoutes.SEND_CMD.format(id=server_id, action="restart_server"),
        )

        if status == "ok":
            return True
        else:
            self._check_errors(data)

    def get_server_logs(self, server_id):
        """Grabs the whole server log, raises ServerNotFound
        if crafty cannot find the server. Returned as list of dict."""
        status, data = self._make_get_request(
            CraftyAPIRoutes.GET_LOGS.format(id=server_id)
        )

        if status == "ok":
            return data
        else:
            self._check_errors(data)

    def run_command(self, server_id, cmd):
        """Runs a command on the specified server, raises ServerNotFound
        if crafty cannot find the server. Returned as list of dict."""
        status, data = self._make_post_request(
            CraftyAPIRoutes.SEND_STDIN.format(id=server_id),
            body=cmd,
        )

        if status == "ok":
            return data
        else:
            self._check_errors(data)

    def get_host_stats(self):
        """Grabs host node stats from crafty"""
        status, data = self._make_get_request(CraftyAPIRoutes.HOST_STATS)

        if status == "ok":
            return data
        else:
            self._check_errors(data)

    def get_server_stats(self, server_id):
        """Grabs (mc) server stats from crafty"""
        status, data = self._make_get_request(
            CraftyAPIRoutes.SERVER_STATS.format(id=server_id)
        )

        if status == "ok":
            return data
        else:
            self._check_errors(data)
