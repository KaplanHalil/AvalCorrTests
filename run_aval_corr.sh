#!/bin/bash

# Change Test algorihms before running tests

# Avalance Tests

python3 aval_mk_rc.py & python3 aval_mk_rk.py & python3 aval_p_rc.py

# Correlation Tests