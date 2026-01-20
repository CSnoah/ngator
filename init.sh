#!/usr/bin/env bash

# ----------------------------------------------------------
# ngator utility parent shell access/startup

# program environment variables
config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ngator"
config_file="$config_dir/ng.config"
source "$config_file"

# cli interface command
ngator() {
  cwd="$PWD"
  source $PROGM_DIR/shell_execution.sh "$cwd" "$@"
}
alias ng='ngator'

# mitigate autocomplete
autoc() {
  local db_aliases="$($PROGM_DIR/src/autocomplete.py)"
  local cur="${COMP_WORDS[COMP_CWORD]}"
  COMPREPLY=( $(compgen -W "${db_aliases}" -- "$cur") )
}
complete -F autoc ng
complete -F autoc ngator

# ----------------------------------------------------------

