import os
import sys

command = 'for x in {1..newnumber}; do (python3 ./main.py "$x") & done'
try:
    num = sys.argv[1]
    command.replace('newnumber', num)
    os.system(command)
except:
    command.replace('newnumber', '1')
    os.system(command)
