mkdir run-64_late_uniform_1

export RADICAL_PILOT_BENCHMARK=
export RADICAL_PILOT_VERBOSE=debug
export RADICAL_UTILS_VERBOSE=debug
export SAGA_VERBOSE=debug

export RADICAL_PILOT_LOG_TARGETS=run-64_late_uniform_1/debug.txt_rp
export RADICAL_UTILS_LOG_TARGETS=run-64_late_uniform_1/debug.txt_ru
export SAGA_LOG_TARGETS=run-64_late_uniform_1/debug.txt_saga

python ./andre_test.py

