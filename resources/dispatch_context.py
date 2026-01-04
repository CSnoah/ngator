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
broadcast = Signal.NONE

# input context
class Flags(Enum):
    ADD = "-a"
    ADD_CURRENT = '-ac'
    DELETE = "-d"
    LIST = "ls"
    NOFLAG = "0"
cmd_flag = "0"
cmd_args = []

# -------------------------------------------------
