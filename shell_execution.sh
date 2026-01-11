# ngator access to parent process

# ---------------------------------------------------------------------------------
# get program root directory from config

config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ngator"
config_file="$config_dir/ng.config"

if [[ ! -f "$config_file" ]]; then
  echo "@ngatorA - Error Msg"
  echo "Cannot find program filepath"
  echo "run startup.sh to set the programs path"
  return
fi

source "$config_file"
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# save and shift parameters

cwd="$1"
shift
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------

# create temporary file
stdout=$(mktemp)
stderr=$(mktemp)

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# direct file descriptor ouput to temp files

# stream=$(/mnt/c/Users/noahm/documents/dev_sandbox/ngator/ngatorB "$cwd" "$@")
# stream=$($PROGM_DIR/ngatorB "$cwd" "$@")

export PROGM_DIR

"$PROGM_DIR/cmd_dispatch.py" "$cwd" "$@" 1>"$stdout" 2>"$stderr"

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# exitcode, shellcode request

# extract the exit code of the most recently executed command
request_channel=$?

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# capture out and err data

path=$(<"$stdout")
out_s=$(<"$stderr")
out_a=($out_s)

rm "$stdout" "$stderr"
# echo $path

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# report any debugging or errors to the command line
echo -n "$out_s"

# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# parse request

case "$request_channel" in
  0)
    # echo "do nothing"

    # argparse prints to stdout for command mismatch
    echo "$path"
    ;;
  1|2|3)
    # subcommand feedback message
    echo "$path"
    ;;
  4)
    # echo "goto"
    cd "$path"
    ;;
  *)
    echo "shell_execution.sh(~89):: -m command not recognized"
  esac
# ---------------------------------------------------------------------------------

