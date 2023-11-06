"""All Routes Enabled For Crafty API"""


class CraftyAPIRoutes(object):
    """All Routes Enabled For Crafty API"""

    ADD_USER = "/api/v2/users/"
    DEL_USER = "/api/v2/users/user/{id}/"
    GET_LOGS = "/api/v2/crafty/logs/"
    SEND_CMD = "/api/v2/servers/{id}/action/{action}"
    SEND_STDIN = "/api/v2/servers/{id}/stdin"
    GET_LOGS = "/api/v2/servers/{id}/logs/"
    SERVER_STATS = "/api/v2/servers/{id}/stats"
    LIST = "/api/v2/servers/"
    HOST_STATS = "/api/v2/crafty/stats/"
