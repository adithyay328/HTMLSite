# Builds all index.py files
# in the serve directory automatically,
# also making adihtml available
# using a mod to the Python path
import os
import pathlib
import re
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

# A #DEPS line declares an extra file (e.g. a .tex) that the
# generator depends on; changing it re-runs the builder.
# Paths are resolved relative to the generator's directory.
_DEPS_RE = re.compile( r"^\s*#DEPS\s+(\S+)\s*$", re.MULTILINE )

def parse_deps( fName ):
  """Return absolute paths of every #DEPS-declared file in fName."""
  parent = pathlib.Path(fName).parent
  try:
    src = pathlib.Path(fName).read_text( encoding="utf-8" )
  except OSError:
    return []
  return [ str( (parent / m).resolve() ) for m in _DEPS_RE.findall( src ) ]

def builder( fName, loop ):
  parentDir = str(pathlib.Path(fName).parent.absolute())
  fNameTail = pathlib.Path(fName).name

  env = os.environ.copy()
  env["PYTHONPATH"] = adiHTMLDir
  command = f"cd {parentDir}; python3 {fNameTail}"
  build = lambda : subprocess.run( command, shell=True, env=env )

  # First, build. Then, store
  # the last mtime for the .py and every #DEPS file
  watch_paths = [ fName ] + parse_deps( fName )
  mtimes = {}
  def refresh():
    for p in watch_paths:
      try:
        mtimes[p] = os.path.getmtime(p)
      except OSError:
        mtimes[p] = 0.0
  refresh()

  buildOut = build()
  print( buildOut.returncode )

  while True and loop:
    time.sleep(WATCH_TIME_MS / 1000)

    changed = False
    for p in watch_paths:
      try:
        cur = os.path.getmtime(p)
      except OSError:
        cur = 0.0
      if cur != mtimes.get(p):
        changed = True
        mtimes[p] = cur
    if changed:
      build()
      # A rebuild may have introduced new #DEPS lines; refresh the watch set
      new_paths = [ fName ] + parse_deps( fName )
      if new_paths != watch_paths:
        watch_paths = new_paths
      refresh()

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
