# Builds all index.py files
# in the serve directory automatically,
# also making adihtml available
# using a mod to the Python path
import os
import pathlib
import sys
import subprocess
import time
import multiprocessing

adiHTMLDir = ( pathlib.Path() / "adihtml" ).resolve().absolute()

# Find all index.py files in serve
indexes = subprocess.check_output( """find serve/ -name "index.py" """, shell=True).decode().split()

print ( indexes )

# For each one, spawn up a different subprocess,
# each one polling every 300ms to check if their
# file has been updated. If so, re-run it
WATCH_TIME_MS = 300

def builder( fName, loop ):
  parentDir = str(pathlib.Path(fName).parent.absolute())
  fNameTail = pathlib.Path(fName).name

  env = os.environ.copy()
  env["PYTHONPATH"] = adiHTMLDir
  command = f"cd {parentDir}; python3 {fNameTail}"
  build = lambda : subprocess.run( command, shell=True, capture_output=True, env=env )

  # First, build. Then, store
  # the last mtime
  mtime = os.path.getmtime(fName)

  buildOut = build()
  print( buildOut.returncode )
  error = buildOut.returncode != 0
  if error or True:
    print ( buildOut.stderr.decode() )

  while True and loop:
    time.sleep(WATCH_TIME_MS / 1000)

    if os.path.getmtime(fName) > mtime:
      build()
      mtime = os.path.getmtime(fName)

# First, build all the index.py files once
for index in indexes:
  builder( index, False )

# Now, spawn up multirocesses
# to run the builder
mps = []
for index in indexes:
  newProc = multiprocessing.Process ( target = builder, args = (index, True) )
  newProc.start()
  mps.append(newProc)

# Use a try to run a loop
# forever, if we get a keyboard
# interrupt kill all the mps
# and exit
try:
  while True:
    time.sleep(1)
except:
  print("\n\nExiting gracefully")
  for mp in mps:
    mp.terminate()
  sys.exit(0)
