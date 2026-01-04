#!/usr/bin/env python3

import sys
import sqlite3
import os
from enum import Enum

from src import db_requests as qy
from resources import dispatch_context as context

# -------------------------------------------------------------------------
# set different alias for dfferent components in the imported module

# dispatch ouput context
out_ctx = context

# dispatch input context
in_ctx = context

# -------------------------------------------------------------------------

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

# parse cli arguments
def parse_args():
    global cmd_flag, cmd_args
    noflag_cmd = False
    if len(sys.argv) > 1:
        for f in in_ctx.Flags:
            if f.value == sys.argv[2]:
                noflag_cmd = True
                in_ctx.cmd_flag = f
                in_ctx.cmd_args = sys.argv[3:]
                break;
    if len(sys.argv) == 3 and not noflag_cmd:
        in_ctx.cmd_flag = in_ctx.Flags.NOFLAG
        in_ctx.cmd_args = sys.argv[2:]

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# dictionary of actions to dispatch input context to
actions = {
    in_ctx.Flags.ADD: qy.add_path,
    in_ctx.Flags.ADD_CURRENT: qy.add_cwd_path,
    in_ctx.Flags.DELETE: qy.delete_path,
    in_ctx.Flags.LIST: qy.list_paths,
    in_ctx.Flags.NOFLAG: qy.goto_path
}

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# send the command arguments to the correct database query function 

def dispatch(flag: in_ctx.Flags):
    global cmd_flag, cmd_args
    # print(f"FLAG: {arg_flag}")
    # print(f":: {arg_params}")
    if flag in actions:
        func = actions[flag]
        if len(in_ctx.cmd_args) != func.__code__.co_argcount:
            return print(f"Error: {flag} expects {func.__code__.co_argcount} arguments")
        else:
            return actions[flag](*in_ctx.cmd_args)

# --------------------------------------------------------------------------

# set input context flag based on raw command argument flag
parse_args()
# perform action based on flag
result_set = dispatch(in_ctx.cmd_flag)
# send message through stdout to parent shell code
to_stdout(result_set)
# no request identified
if out_ctx.broadcast == in_ctx.Signal.NONE:
    print(sys.argv)

# # sent alias through err
# get_all_alias()

# send request through exit code to parent processes for shell code execution
sys.exit(out_ctx.broadcast.value)
