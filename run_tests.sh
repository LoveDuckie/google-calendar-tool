#!/usr/bin/env bash
<<EOF

   Tool \ Shell Scripts \ Run \ Tests

   Run the unit tests discovered in the codebase.

EOF
CURRENT_SCRIPT_DIRECTORY=${CURRENT_SCRIPT_DIRECTORY:-$(dirname $(realpath ${BASH_SOURCE[0]:-${(%):-%x}}))}
export SHARED_EXT_SCRIPTS_PATH=${SHARED_EXT_SCRIPTS_PATH:-$(realpath $CURRENT_SCRIPT_DIRECTORY)}
export CURRENT_SCRIPT_FILENAME=${CURRENT_SCRIPT_FILENAME:-$(basename ${BASH_SOURCE[0]:-${(%):-%x}})}
export CURRENT_SCRIPT_FILENAME_BASE=${CURRENT_SCRIPT_FILENAME%.*}
. "$SHARED_EXT_SCRIPTS_PATH/shared_functions.sh"
write_header

# Run the tests with coverage
write_info "Running unit tests with coverage"
coverage run -m unittest discover -s google_calendar_tool_tests -p "*.py" || { echo "Tests failed"; exit 1; }

# Generate the coverage report
write_info "Generating coverage report"
coverage report -m

# Optional: Generate HTML report for detailed analysis
coverage html
write_success "run_tests" "Unit tests completed with coverage reporting"
write_info "Check the coverage report in the 'htmlcov' directory for details."

write_success "run_tests" "Done"
exit 0