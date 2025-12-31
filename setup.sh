#!/usr/bin/env bash

# ---------------------------------------------------------------------------------
# config: setup program directory 

config_dir="${XDG_CONFIG_HOME:-$HOME/.config}/ngator"
config_file="$config_dir/ng.config"

mkdir -p "$config_dir"

if [[ ! -f "$config_file" ]]; then
  touch "$config_file"
  echo "PROGM_DIR=\"$PWD\"" >> "$config_file"
  # source "$config_file"
  echo "[NOTE]: ngator path: $PWD"
  echo "[NOTE]: If utility path changes update ng.config: PROGM_DIR=new-path"
  echo "[NOTE]: Config location: ~/.config/ngator/ng.config"
fi

# if run setup butconfig file exists,
# and remove init from .bashrc still grabs PROGM_DIR
source "$config_file"
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# determine users shell

shell_name=$(basename "$SHELL")

# ~ = $HOME
case "$shell_name" in
  bash) 
    rc="$HOME/.bashrc"
    ;;
  zsh)
    rc="$HOME/.zshrc"
    ;;
  ksh)
    rc="$HOME/.kshrc"
    ;;
  fish)
    rc="$HOME/.config/fish/config.fish"
    ;;
  *)
    rc="NA"
    echo "Cannot find appropriate shell"
    ;;
  esac

if [ "$rc" != "NA" ]; then
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# heredoc program entry point goes to .<shell-type>rc

echo "SHELL CODE WRAPPER >> .$shell_name.rc"
cat << EOF >> "$rc"
# ----------------------------------------------------------
# ngator utility parent shell access/startup

source "$PROGM_DIR/ngator.init.sh"
# ----------------------------------------------------------
EOF

fi

# re-run rc file in current shell context
echo "[ACTION]: source $rc"
source "$rc"


# BELOW - older approaches
# ########################->
#
# ########################->
# BELOW - older approaches

# read from the config file to get the PROGM_DIR
# cat << EOF >> "$rc"
# # ----------------------------------------------------------
# # ngator utility parent shell access/startup
#
# ngator() {
#   cwd="\$PWD"
#   source $PROGM_DIR/ngatorA.sh "\$cwd" "\$@"
# }
# alias ng='ngator'
#
# autoc() {
#   local db_aliases="$($PROGM_DIR/cmd_autocomplete.py)"
#   local cur="\${COMP_WORDS[COMP_CWORD]}"
#   # out_a => variable sourced from ngatorA.sh
#   COMPREPLY=( \$(compgen -W "\${db_aliases}" -- "\$cur") )
# }
# complete -F autoc -o default ng
# complete -F autoc ngator
# # ----------------------------------------------------------
# EOF
#
# fi

# # re-run rc file in current shell context
# echo "[ACTION]: source $rc"
# source "$rc"
# ---------------------------------------------------------------------------------



# if [ "$rc" != "NA" ]; then
#
# echo "SHELL CODE WRAPPER >> .$shell_name.rc"
# cat << 'EOF' >> "$rc"
# ngator() {
#   cwd="$PWD"
#   source /mnt/c/Users/noahm/documents/dev_sandbox/ngator/ngatorA "$cwd" "$@"
# }
# alias ng='ngator'
# EOF
#
# fi
