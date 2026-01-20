from enum import Enum

# -------------------------------------------------
# dispatch context

# ouput context
class Signal(Enum):
    NONE = 0
    ADD = 1
    DELETE = 2
    LIST = 3
    GOTO = 4
    SET_FIELD = 5
    SET_SCOPE = 6
broadcast = Signal.NONE

# # input context (old API interface)
# class Flags(Enum):
#     ADD = "-a"
#     ADD_CURRENT = '-ac'
#     DELETE = "-d"
#     LIST = "ls"
#     NOFLAG = "0"
# cmd_flag = "0"
# cmd_args = []

# input context (new API interface)
class Flags(Enum):
    GOTO = 1
    ADD = 2
    ADD_CURRENT = 3
    DELETE = 4
    LIST = 5
    DLOG_ON = 6
    DLOG_OFF = 7
    SET_FIELD = 8
    SET_SCOPE = 9
    NO_FLAG = 10
cmd_flag = Flags.NO_FLAG 
cmd_args = []

# -------------------------------------------------
