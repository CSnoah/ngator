#!/usr/bin/env python3

import sys
import sqlite3
import os
from enum import Enum

from src import db_requests as qy
from resources import dispatch_context as context
from resources import logger_context as logger
from src import cmd_parser as parser
from src import env_requests as env_req

# -------------------------------------------------------------------------
# set different alias for dfferent components in the imported module

# dispatch ouput context
out_ctx = context

# dispatch input context
in_ctx = context

# -------------------------------------------------------------------------

# print(in_ctx.cmd_flag)

# ROOT_DIR = os.environ.get("PROGM_DIR")
# print(f"prg_dir: {ROOT_DIR}")

# cmd_flag = "0"
# cmd_args = []
# prg_root = os.path.dirname(os.path.abspath(__file__))
# database_name = os.path.join(prg_root, "database", "ngator.db")
# broadcast = Signal.NONE

# --------------------------------------------------------------------------

# send the path to stdout
def to_stdout(path):
    print(path)

# # parse cli arguments
# def parse_args():
#     global cmd_flag, cmd_args
#     noflag_cmd = False
#     if len(sys.argv) > 1:
#         for f in in_ctx.Flags:
#             if f.value == sys.argv[2]:
#                 noflag_cmd = True
#                 in_ctx.cmd_flag = f
#                 in_ctx.cmd_args = sys.argv[3:]
#                 break;
#     if len(sys.argv) == 3 and not noflag_cmd:
#         in_ctx.cmd_flag = in_ctx.Flags.NOFLAG
#         in_ctx.cmd_args = sys.argv[2:]

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# # dictionary of actions to dispatch input context to
# actions = {
#     in_ctx.Flags.ADD: qy.add_path,
#     in_ctx.Flags.ADD_CURRENT: qy.add_cwd_path,
#     in_ctx.Flags.DELETE: qy.delete_path,
#     in_ctx.Flags.LIST: qy.list_paths,
#     in_ctx.Flags.NOFLAG: qy.goto_path
# }

# dictionary of actions to dispatch input context to
actions = {
    in_ctx.Flags.ADD: qy.add_path,
    in_ctx.Flags.ADD_CURRENT: qy.add_cwd_path,
    in_ctx.Flags.DELETE: qy.delete_path,
    in_ctx.Flags.LIST: qy.list_paths,
    in_ctx.Flags.GOTO: qy.goto_path,
    in_ctx.Flags.DLOG_ON: env_req.set_logger_on,
    in_ctx.Flags.DLOG_OFF: env_req.set_logger_off
}

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# send the command arguments to the correct database query function 

def dispatch(flag: in_ctx.Flags):
    global cmd_flag, cmd_args
    if flag in actions:
        func = actions[flag]
        if len(in_ctx.cmd_args) != func.__code__.co_argcount:
            error_log = f"=> Dispatch Error: ({func.__name__}) w/ ({flag}) " \
                f"expects ({func.__code__.co_argcount}) arguments " \
                f"recieved ({len(in_ctx.cmd_args)}) arguments"
            logger.log(error_log)
        else:
            # print(f"ARGS::{in_ctx.cmd_args}", file=sys.stderr)
            return actions[flag](*in_ctx.cmd_args)

# --------------------------------------------------------------------------

# set input context flag based on raw command argument flag
# parse_args()
# perform action based on flag
result_set = dispatch(in_ctx.cmd_flag)
# send message through stdout to parent shell code
to_stdout(result_set)
# no request identified
# if out_ctx.broadcast == in_ctx.Signal.NONE:
    # print("=> cmd_dispatch.py argv: ", end="", file=sys.stderr)
    # print(sys.argv, file=sys.stderr)

# # sent alias through err
# get_all_alias()

# send request through exit code to parent processes for shell code execution
sys.exit(out_ctx.broadcast.value)
