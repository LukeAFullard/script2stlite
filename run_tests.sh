#!/bin/bash
# This script runs pytest and saves a datetime-stamped log of the test results.

# Create the test_logs directory if it doesn't exist
mkdir -p test_logs

# Get the current datetime
now=$(date +'%Y-%m-%d_%H-%M-%S')
logfile="test_logs/test_run_${now}.log"

echo "Running tests and logging to ${logfile}..."

# Run pytest and save the output to the logfile
pytest > "${logfile}" 2>&1

# Check the exit code of pytest
if [ $? -eq 0 ]; then
    echo "All tests passed." >> "${logfile}"
    echo "Tests complete. Log saved to ${logfile}"
else
    echo "Some tests failed. Check the log for details." >> "${logfile}"
    echo "Tests complete with failures. Log saved to ${logfile}"
fi
