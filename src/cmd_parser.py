import argparse
import os
import io
import sys
from enum import Enum
from contextlib import redirect_stderr

project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from resources import dispatch_context as context
from resources import logger_context as logger

# -------------------------------------------------------------------------
# capturing error logging to send to an error logger

buf = io.StringIO()
argparse_error_log = ""
parsed_argp = None 

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# cmd_flag is the input context to the dispatcher

# dispatch input context
in_ctx = context

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# pre argparse procesing resources

subcommand_set = {
    # subcommands: cd (change director to specified alias)
    "goto", "go", "g",
    # subcommands: add an alias
    "add", "a",
    # subcommans: remove an alias
    "delete", "del",
    # subcommands: ls (list commmand data)
    "list", "ls",
    # subcommand: set a database field
    "set",
    # subcommand: enable/disable logging
    "dlog"
}

# c-style enum for index readability
# class Argp_Index(Enum):
#     COMMAND = 0
#     ARG1 = 1
#     ARG2 = 2
#     ARG4 = 3

argv_subcommand_index = 2
argp_subcommand_index = 0
# the command name and cwd argument is not used in parsing
# argp[0] = subcommand, argp[1:] = subcommand/flag arguments
argp = []

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# pre argparse processing

# documenting craw arguments
# sys.argv[0] is= command(default)
# sys.argv[1] is= cwd(default)
# ------------------------------------
# sys.argv[2] is= subcommand(if present)
# sys.argv[3] is= subcommand argi(if present)

# first two args are always provided despite user input, third on are not
# so checking if the user inputed atlease one argument past ng
if len(sys.argv) >= (argv_subcommand_index+1):
    argp = sys.argv[argv_subcommand_index:]
else:
    print("cmd_parser.py(62):: -m invalid index, defalut args unprovided", file=sys.stderr)

# handle outlier command: ng <path> (has no subcommand)
if argp:
    # check if the first possition after ng command is an alias or a subcommand
    if argp[argp_subcommand_index] not in subcommand_set:
        argp = ["goto"] + argp

# logging...
# print(f"PARSE ARGS::{argp}", file=sys.stderr)

# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# argparse subparser parsing

parser = argparse.ArgumentParser(description="ngator cli parser")
subparser = parser.add_subparsers(dest="command")

# INFO: changes the parent shells current directory
# CMD: ng goto <alias>
goto_parser = subparser.add_parser(
    "goto",
    aliases=["go","g"],
    help="change current directory to an alias path"
)
goto_parser.add_argument(
    "cd_alias", help="ng goto <alias>"
)

# INFO: adding an alias w/ specifying path
# CMD: ng add <path> <alias>
add_parser = subparser.add_parser(
    "add",
    aliases=["a"],
    help="Add an alias"
)
add_parser.add_argument(
    "-c",
    "--current",
    action="store_true",
    help="add current directory"
)
add_parser.add_argument("add_args", nargs="+", help="<path> <alias> OR -c <alias>")

# INFO: delete an alias
# CMD: ng delete <alias>
del_parser = subparser.add_parser(
    "delete",
    aliases=["del"],
    help="delete an alias"
)
del_parser.add_argument("del_alias", nargs=1, help="ng del <alias>")

# INFO: list stored data
# CMD: ng ls
list_parser = subparser.add_parser(
    "list",
    aliases=["ls"],
    help="list stored data"
)
list_parser.add_argument(
    "-l",
    "-long",
    action="store_true",
    help="long listing of stored data"
)

# INFO: changes the parent shells current directory
# CMD: ng set --field <alias> <entry>
set_parser = subparser.add_parser(
    "set",
    help="set a database field or environment scope"
)

# enforeces only one tag specifier is used
mode = set_parser.add_mutually_exclusive_group(required=True)

mode.add_argument(
    "--tag",
    # action="store_true",
    dest="tag_field",
    nargs=2,
    metavar=("alias", "tag"),
    help="set the tag field: ng set --tag <alias> <tag-name>"
)
mode.add_argument(
    "--alias",
    dest="alias_field",
    nargs=2,
    metavar=("old-alias", "new-alias"),
    help="rename a path's alias: ng set --alias <alias> <new-alias-name>"
)
mode.add_argument(
    "--scope",
    dest="scope",
    metavar="tag",
    help="set the environment tag scope: ng set --scope <tag>"
)
# mode.add_argument(
#     "--tag",
#     # action="store_true",
#     dest="field",
#     action="store_const",
#     const="tag",
#     help="set the tag field: ng set --tag <alias> <tag-name>"
# )
# mode.add_argument(
#     "--alias",
#     dest="field",
#     action="store_const",
#     const="alias",
#     help="rename a path's alias: ng set --alias <alias> <new-alias-name>"
# )
# mode.add_argument(
#     "--scope",
#     dest="tag",
#     help="set the environment tag scope: ng set --scope <alias> <tag>"
# )
# mode.add_argument(
#     "--scope",
#     # action="store_true",
#     dest="field",
#     action="store_const",
#     const="scope",
#     help="set the environment tag scope: ng set --scope <alias> <tag>"
# )
# set_parser.add_argument("set_args", nargs=2, help="ng set --field(or scope) <alias> <entry>")

# INFO: activate debugger logging
# CMD: ng dlog -t, ng dlog -f
log_parser = subparser.add_parser(
    "dlog",
    help="enable/disagle debugging logs"
)
log_parser.add_argument(
    '-f',
    "--false",
    action="store_true",
    help="turn debugging log off"
)
log_parser.add_argument(
    "-t",
    "--true",
    action="store_true",
    help="turn debugging log on"
)

parsed_argp = parser.parse_args(argp)



# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# post argparse parsing

match parsed_argp.command:
    case "add" | "a":
        if parsed_argp.current:
            in_ctx.cmd_flag = context.Flags.ADD_CURRENT
            in_ctx.cmd_args = [parsed_argp.add_args[0]]
        else:
            in_ctx.cmd_flag = context.Flags.ADD
            in_ctx.cmd_args.append(parsed_argp.add_args[0])
            in_ctx.cmd_args.append(parsed_argp.add_args[1])
    case "delete" | "del":
        in_ctx.cmd_flag = context.Flags.DELETE
        in_ctx.cmd_args = [parsed_argp.del_alias[0]]
    case "list" | "ls":
        in_ctx.cmd_flag = context.Flags.LIST
    case "goto" | "g":
        in_ctx.cmd_flag = context.Flags.GOTO
        in_ctx.cmd_args = [parsed_argp.cd_alias]
    case "set":
        if parsed_argp.scope:
            in_ctx.cmd_flag = context.Flags.SET_SCOPE
            # the scope associated with a specific tag name
            in_ctx.cmd_args.append(parsed_argp.scope)
        else:
            in_ctx.cmd_flag = context.Flags.SET_FIELD
            if parsed_argp.tag_field:
                # flag = database query field
                in_ctx.cmd_args.append("tag")
                # alais
                in_ctx.cmd_args.append(parsed_argp.tag_field[0])
                # entry
                in_ctx.cmd_args.append(parsed_argp.tag_field[1])
            elif parsed_argp.alias_field:
                # flag = database query field
                in_ctx.cmd_args.append("alias")
                # alais
                in_ctx.cmd_args.append(parsed_argp.alias_field[0])
                # entry
                in_ctx.cmd_args.append(parsed_argp.alias_field[1])
    case "dlog":
        if parsed_argp.true:
            in_ctx.cmd_flag = context.Flags.DLOG_ON
        elif parsed_argp.false:
            in_ctx.cmd_flag = context.Flags.DLOG_OFF
    case _:
        in_ctx.cmd_flag = context.Flags.NO_FLAG

# logging...
# print(in_ctx.cmd_flag, file=sys.stderr)

# -------------------------------------------------------------------------
