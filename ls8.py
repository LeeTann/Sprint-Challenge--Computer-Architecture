import sys
from cpu import *

if len(sys.argv) == 2:
    cpu = CPU()
    cpu.load(sys.argv[1]) # pass the filename to load
    cpu.run()
else:
    print("error: please provide filename to execute function")
    