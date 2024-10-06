#!/usr/bin/env bash
<<EOF

   Python Tool Template \ Shared \ Functions

   A collection of shared and reusable functions for performing operations

EOF
CURRENT_SCRIPT_DIRECTORY=${CURRENT_SCRIPT_DIRECTORY:-$(dirname $(realpath $0))}
export CURRENT_SCRIPT_FILENAME=${CURRENT_SCRIPT_FILENAME:-$(basename $0)}
export CURRENT_SCRIPT_FILENAME_BASE=${CURRENT_SCRIPT_FILENAME%.*}
#. "$SHARED_SCRIPTS_PATH/shared-variables.sh"

unset -f write_header
unset -f write_header_sub
unset -f write_info
unset -f write_warning
unset -f write_error
unset -f write_debug
unset -f write_response
unset -f write_success
unset -f is_command_available

is_command_available() {
   if [[ "$(command -v $1)" != "" ]] && [[ "$(type -t $1)" != "" ]]; then
      return 0
   fi

   return 1
}

write_header_sub() {
   if [ ! -z "$CURRENT_SCRIPT_FILENAME" ]; then
      echo ""
      write_info "*** SCRIPT: $(echo \"${CURRENT_SCRIPT_FILENAME%.*}\" | awk '{print toupper($0)}')"
      echo ""
   fi

   return 0
}

write_header() {
   if [[ "$OPTIONS_LOG_SHOW_HEADER" == "1" ]] && [ -z "$HEADER_OUTPUT" ] && [ -e "$SHARED_SCRIPTS_PATH_ENV/script-header" ]; then
      if [ ! -z "$HEADER_OUTPUT_LOLCAT" ]; then
         cat $SHARED_SCRIPTS_PATH_ENV/script-header | lolcat
      else
         echo -e "\033[1;37m$(cat $SHARED_SCRIPTS_PATH_ENV/script-header)\033[0m"
      fi
   fi

   export HEADER_OUTPUT=1

   write_header_sub

   return 0
}

write_info() {
   MSG=$2
   echo -e "\033[1;36m $1\033[0m \033[0;37m${MSG}\033[0m" 1>&2
}

write_success() {
   MSG=$2
   echo -e "\033[1;32m $1\033[0m \033[0;37m${MSG}\033[0m" 1>&2
}

write_error() {
   MSG=$2
   echo -e "\033[1;31m $1\033[0m \033[0;37m${MSG}\033[0m" 1>&2
}

write_warning() {
   MSG=$2
   echo -e "\033[1;33m $1\033[0m \033[0;37m${MSG}\033[0m" 1>&2
}

write_debug() {
   if [ -z "$OPTIONS_LOG_ENABLE_DEBUG" ]; then
      return 1
   fi
   MSG=$2
   echo -e "\e[1;33m$1\e[0m \e[0;37m${MSG}\e[0m" 1>&2
   return 0
}

write_response() {
   if [ $? -ne 0 ]; then
      write_error "error" "$2"
      return 1
   fi

   write_success "success" "$2"
   return 0
}

export -f write_header
export -f write_header_sub
export -f write_info
export -f write_warning
export -f write_error
export -f write_debug
export -f write_response
export -f write_success
export -f is_command_available
