#!/bin/bash

# Change the algorithm name to the desired algorithm
ALG=AES_256

echo "from $ALG import *" > Alg.py

# Avalance Tests

echo "Running Avalanche Tests"
python3 aval_mk_rc.py & 
python3 aval_mk_rk.py & 
python3 aval_p_rc.py &

# Correlation Tests

echo "Running Correlation Tests"
python3 corr_mk_rk.py 

# Move the drawings to the Results folder
#mv -t ../Results/ aval_* corr_*