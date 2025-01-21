#!/bin/bash

# Change the algorithm name to the desired algorithm
ALG=AES_256

echo "from $ALG import *" > Alg.py

# Avalance Tests

python3 aval_mk_rc.py & 
python3 aval_mk_rk.py & 
python3 aval_p_rc.py

# Move the drawings to the Results folder
mv -t ../Results/ aval_mk_rc.png aval_mk_rk.png aval_p_rc.png

# Correlation Tests