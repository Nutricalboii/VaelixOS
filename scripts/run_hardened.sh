#!/bin/bash
# run_hardened.sh - Wrapper for Vaelix OS build steps with safety guards
# Usage: ./scripts/run_hardened.sh "description" "command" "timeout_duration"

DESC="$1"
CMD="$2"
TIMEOUT_DUR="${3:-20m}"
LOG_FILE="build/phase2_optimization.log"

mkdir -p build
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[${TIMESTAMP}] ✦ STARTING: ${DESC}" | tee -a "${LOG_FILE}"
echo "[${TIMESTAMP}] ✦ COMMAND: ${CMD}" | tee -a "${LOG_FILE}"

# Execute with timeout
if timeout "${TIMEOUT_DUR}" bash -c "${CMD}"; then
    TIMESTAMP_DONE=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[${TIMESTAMP_DONE}] ✅ SUCCESS: ${DESC}" | tee -a "${LOG_FILE}"
else
    EXIT_CODE=$?
    TIMESTAMP_FAIL=$(date "+%Y-%m-%d %H:%M:%S")
    if [ $EXIT_CODE -eq 124 ]; then
        echo "[${TIMESTAMP_FAIL}] ❌ TIMEOUT: ${DESC} exceeded ${TIMEOUT_DUR}" | tee -a "${LOG_FILE}"
    else
        echo "[${TIMESTAMP_FAIL}] ❌ FAILED: ${DESC} exited with code ${EXIT_CODE}" | tee -a "${LOG_FILE}"
    fi
    exit $EXIT_CODE
fi
