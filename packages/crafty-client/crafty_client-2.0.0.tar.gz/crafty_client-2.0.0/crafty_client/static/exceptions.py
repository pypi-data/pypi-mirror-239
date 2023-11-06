class ServerNotFound(Exception):
    pass


class ServerNotRunning(Exception):
    pass


class ServerAlreadyRunning(Exception):
    pass


class MissingParameters(Exception):
    pass


class AccessDenied(Exception):
    pass


class NotAllowed(Exception):
    pass


class ServerStopping(Exception):
    pass


class InvalidJson(Exception):
    pass
