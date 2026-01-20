import os
import sys
import configparser

project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources import dispatch_context as context
from resources import logger_context as logger

# -------------------------------------------------------------------------
# set different alias for dfferent components in the imported module

# dispatch ouput context
out_ctx = context

# dispatch input context
in_ctx = context

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# debug logger methods

def set_logger_on():
    logger.dubug_mode = True
    print(f"[LOGGER MODE]=TRUE", file=sys.stderr)

def set_logger_off():
    logger.debug_mode = False
    print(f"[LOGGER MODE]=FALSE", file=sys.stderr)

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# env scope

def set_scope(value):
    global broadcast 
    out_ctx.broadcast = context.Signal.SET_SCOPE
    config_path = f"{project_root}/resources/ng_config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)
    files_read = config.read(config_path)

    #check file location is valid
    if len(files_read) == 0:
        logger.log(f"config_file loction was not found")

    if "scope" not in config:
        config["scope"] = {}

    config["scope"]["tag_scope"] = value

    with open(config_path, "w") as configfile:
        config.write(configfile)

    return f"successfull[set]: --scope = {value}"

def cur_scope():
    config_path = f"{project_root}/resources/ng_config.ini"
    config = configparser.ConfigParser()
    config.read(config_path)
    files_read = config.read(config_path)
    scope= config["scope"]["tag_scope"]
    print(scope) 

# set_scope("*")
# cur_scope()
# -------------------------------------------------------------------------

