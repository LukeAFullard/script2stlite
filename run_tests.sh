#!/bin/bash
# This script runs pytest and saves a datetime-stamped log of the test results.

# Get the current datetime
now=$(date +'%Y-%m-%d_%H-%M-%S')
logfile="test_run_${now}.log"

echo "Running tests and logging to ${logfile}..."

# Run pytest and save the output to the logfile
poetry run pytest -v --log-file="${logfile}"

# Check the exit code of pytest
if [ $? -eq 0 ]; then
    echo "All tests passed." >> "${logfile}"
    echo "Tests complete. Log saved to ${logfile}"
else
    echo "Some tests failed. Check the log for details." >> "${logfile}"
    echo "Tests complete with failures. Log saved to ${logfile}"
fi
