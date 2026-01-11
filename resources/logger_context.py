import inspect
import os
import sys

log_number = 0
debug_mode = True 

def get_linenum():
    return inspect.currentframe().f_back.f_lineno

def get_filename():
    return '/'.join(map(str,__file__.split('/')[-2:]))
    
def log(message):
    global log_number
    if debug_mode:
        caller_frame = inspect.stack()[1]
        filename = os.path.basename(caller_frame.filename)
        shortened_filepath = caller_frame.filename.split('/')[-2:]
        short_filepath = "/".join(shortened_filepath)
        linenum = caller_frame.lineno
        print(f"[LOG {log_number}]:{short_filepath}({linenum}):: -m {message}", file=sys.stderr)
    log_number+=1
