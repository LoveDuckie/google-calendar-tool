#!/usr/bin/env bash
<<EOF

   Tool \ Shell Scripts \ Run \ Tool

   Run the tool from this repository.

EOF
CURRENT_SCRIPT_DIRECTORY=${CURRENT_SCRIPT_DIRECTORY:-$(dirname $(realpath ${BASH_SOURCE[0]:-${(%):-%x}}))}
export SHARED_EXT_SCRIPTS_PATH=${SHARED_EXT_SCRIPTS_PATH:-$(realpath $CURRENT_SCRIPT_DIRECTORY)}
export CURRENT_SCRIPT_FILENAME=${CURRENT_SCRIPT_FILENAME:-$(basename ${BASH_SOURCE[0]:-${(%):-%x}})}
export CURRENT_SCRIPT_FILENAME_BASE=${CURRENT_SCRIPT_FILENAME%.*}
. "$SHARED_EXT_SCRIPTS_PATH/shared_functions.sh"
write_header

if ! is_command_available python; then
    write_error "run" "Failed: Unable to find \"python\" installed on this system. Unable to continue."
    exit 1
fi

CURRENT_PYTHON_VERSION=$(python --version | cut -d ' ' -f2)
PROJECT_PYTHON_VERSION=<(.python-version)

if [[ ! "$PROJECT_PYTHON_VERSION" ~= $CURRENT_PYTHON_VERSION ]]; then
    write_error "run" "Python $PROJECT_PYTHON_VERSION is not present from the command-line. Check your configuration and try again."
    exit 1
fi

if is_command_available pipx; then
    write_info "run" "\"pipx\" was found on this system. Continuing."

    # pipx install .

    exit 0
else
    write_warning "run" "Unable to find \"pipx\" on this system."
fi

if is_command_available virtualenv; then
    write_info "run" "\"virtualenv\" was found on this system."
fi
