#!/usr/bin/env bash
<<EOF

   Tool \ Shell Scripts \ Run \ Lint

   Run the linting tool (pylint) on the codebase.

EOF
CURRENT_SCRIPT_DIRECTORY=${CURRENT_SCRIPT_DIRECTORY:-$(dirname $(realpath ${BASH_SOURCE[0]:-${(%):-%x}}))}
export SHARED_EXT_SCRIPTS_PATH=${SHARED_EXT_SCRIPTS_PATH:-$(realpath $CURRENT_SCRIPT_DIRECTORY)}
export CURRENT_SCRIPT_FILENAME=${CURRENT_SCRIPT_FILENAME:-$(basename ${BASH_SOURCE[0]:-${(%):-%x}})}
export CURRENT_SCRIPT_FILENAME_BASE=${CURRENT_SCRIPT_FILENAME%.*}
. "$SHARED_EXT_SCRIPTS_PATH/shared_functions.sh"
write_header

# Check if pylint is installed; if not, prompt installation
if ! command -v pylint &> /dev/null; then
    echo "pylint is not installed. Installing it now..."
    pip install pylint || { echo "Failed to install pylint"; exit 1; }
fi

# Run pylint on the google_calendar_tool directory
write_info "Running pylint on google_calendar_tool"
pylint google_calendar_tool || { echo "Linting failed"; exit 1; }
if ! write_response "run_lint" "Run Pylint"; then
   write_error "run_lint" "Failed: Unable to run Pylint, exit code was not zero."
   exit 1
fi

write_success "run_lint" "Pylint completed successfully"
exit 0
