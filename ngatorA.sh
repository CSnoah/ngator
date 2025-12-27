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
# stdout path

# stream=$(/mnt/c/Users/noahm/documents/dev_sandbox/ngator/ngatorB "$cwd" "$@")
stream=$($PROGM_DIR/ngatorB "$cwd" "$@")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# exitcode, shellcode request

request_channel=$?
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# parse request

case "$request_channel" in
  0)
    echo "do nothing"
    echo"$stream"
    ;;
  1|2|3)
    # add, delte, or list message
    echo "$stream"
    ;;
  4)
    # echo "goto"
    cd "$stream"
    ;;
  *)
    echo "NA"
  esac
# ---------------------------------------------------------------------------------

