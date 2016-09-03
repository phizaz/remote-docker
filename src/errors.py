class RemoteDockerError(Exception): pass

class ArgumentError(RemoteDockerError): pass

class LatestTagNotFound(RemoteDockerError): pass

class TagNotFound(RemoteDockerError): pass

class HostNotFound(RemoteDockerError): pass

class LatestHostNotFound(RemoteDockerError): pass

class JobDuplicate(RemoteDockerError): pass

class JobNotStarted(RemoteDockerError): pass

class WrongDockerExitcode(RemoteDockerError): pass

class WrongExitCode(RemoteDockerError): pass