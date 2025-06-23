from enum import Enum, auto

class ClientState(Enum):
    CLOSED = 0
    SYNSENT = auto()
    ESTABLISHED = auto()
    FINWAIT1 = auto()
    FINWAIT2 = auto()
    TIMEWAIT = auto()


class ServerState(Enum):
    CLOSED = 0
    LISTEN = auto()
    SYNRECEIVED = auto()
    ESTABLISHED = auto()
    CLOSEWAIT = auto()
    LASTACK = auto()
