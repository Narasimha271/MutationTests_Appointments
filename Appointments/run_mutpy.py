import sys
from mutpy import commandline

# Simulate actual CLI arguments
sys.argv = [
    'run_mutpy.py',  # placeholder for script name
    '--target', 'Services.main',
    '--unit-test', 'Test.appointments_test',
    '--runner', 'unittest'
]

# ✅ Define args before using them
args = [
    '--target', 'services.main',
    '--unit-test', 'Test.appointments_test',
    '--runner', 'unittest'
]

# ✅ Pass the args to the main function
commandline.main(argv=args)

