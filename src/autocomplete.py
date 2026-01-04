#!/usr/bin/env python3

import sys
import sqlite3
import os

prg_root = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(prg_root, "..", "database", "ngator.db")

# get all the aliases stored in the database
with sqlite3.connect(database_path) as conn:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT alias FROM paths"
    )
    aliases = cursor.fetchall()
    # remove tuples
    flattened = []
    for row in aliases:
        flattened.append(row[0])

    # prep data as a string
    s_aliases = ' '.join(flattened)

    # send data to stdout channel
    print(s_aliases)

