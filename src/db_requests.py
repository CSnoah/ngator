#!/usr/bin/env python3

# ngator interface with SQLite database

import sys
import sqlite3
import os
from enum import Enum

project_root = os.path.dirname(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# from resources import actions
from resources import dispatch_context as context

# -------------------------------------------------------------------------
# set different alias for dfferent components in the imported module

# dispatch ouput context
out_ctx = context

# -------------------------------------------------------------------------

prg_root = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(prg_root, "..", "database", "ngator.db")
# broadcast = context.Signal.NONE

def add_path(path, alias):
    global broadcast 
    out_ctx.broadcast = context.Signal.ADD
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paths (path, alias) VALUES (?, ?)",
                (path, alias)
        )
        conn.commit()
    return f"successfull[add]: [ {alias} ] = {path}"

def add_cwd_path(alias):
    global broadcast 
    out_ctx.broadcast = context.Signal.ADD
    # arg containing cwd path
    path = sys.argv[1]
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paths (path, alias) VALUES (?, ?)",
                (path, alias)
        )
        conn.commit()
    return f"successfull[add]: [ {alias} ] = {path}"

def delete_path(alias):
    global broadcast 
    out_ctx.broadcast = context.Signal.DELETE
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM paths WHERE alias = ?",
            (alias,)
        )
        conn.commit()
    return f"successfull[remove]: [ {alias} ]"

def list_paths():
    query_collector = ""
    global broadcast
    out_ctx.broadcast = context.Signal.LIST
    # print("lsing")
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM paths"
        )
        for row in cursor.fetchall():
            alias = row[1]
            path = row[3]
            query_collector+=f"[ {alias} ] = {path}\n"
        return query_collector

def goto_path(alias):
    global broadcast
    out_ctx.broadcast = context.Signal.GOTO
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT path FROM paths WHERE alias = ?", (alias,)
        )
        query_out = cursor.fetchone()
        if query_out:
            # a match was found
            snached_path = query_out[0]
            return snached_path
        else:
            print(f"No path found for alias:: {alias}")



# try:
#     sqlite3.connect(database_name)
#     print("Connection successful!")
# except sqlite3.Error:
#     print("Connection failed!")
#
# print(list_paths())
