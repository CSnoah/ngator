import os
import sys

project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources import dispatch_context as context
from resources import logger_context as logger

# -------------------------------------------------------------------------
# cmd_flag is the input context to the dispatcher

# dispatch input context
in_ctx = context

# -------------------------------------------------------------------------

def set_logger_on():
    logger.dubug_mode = True
    print(f"[LOGGER MODE]=TRUE", file=sys.stderr)

def set_logger_off():
    logger.debug_mode = False
    print(f"[LOGGER MODE]=FALSE", file=sys.stderr)
