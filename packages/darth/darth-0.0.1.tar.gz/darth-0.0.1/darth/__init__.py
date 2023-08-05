"""
Helpers for adding dependencies to the import path.

Darth Vendor is so named because of the evil, evil things we've done
for all the right reasons. Forgive us.

           _.-'~~~~~~`-._
          /      ||      \
         /       ||       \
        |        ||        |
        | _______||_______ |
        |/ ----- \/ ----- \|
       /  (     )  (     )  \
      / \  ----- () -----  / \
     /   \      /||\      /   \
    /     \    /||||\    /     \
   /       \  /||||||\  /       \
  /_        \o========o/        _\
    `--...__|`-._  _.-'|__...--'
            |    `'    |             
"""
 
import site
import os.path
import sys
 

def vendor(folder, position=1):
  """
  Adds the given folder to the python path. Supports namespaced packages.
  By default, packages in the given folder take precedence over site-packages
  and any previous path manipulations.
 
  Args:
    folder: Path to the folder containing packages, relative to ``os.getcwd()``
    position: Where in ``sys.path`` to insert the vendor packages. By default
      this is set to 1. It is inadvisable to set it to 0 as it will override
      any modules in the current working directory.
  """
  # Use site.addsitedir() because it appropriately reads .pth
  # files for namespaced packages. Unfortunately, there's not an
  # option to choose where addsitedir() puts its paths in sys.path
  # so we have to do a little bit of magic to make it play along.

  # We're going to grab the current sys.path and split it up into
  # the first entry and then the rest. Essentially turning
  #   ['.', '/site-packages/x', 'site-packages/y']
  # into
  #   ['.'] and ['/site-packages/x', 'site-packages/y']
  # The reason for this is we want '.' to remain at the top of the
  # list but we want our vendor files to override everything else.
  sys.path, remainder = sys.path[:1], sys.path[1:]

  # Now we call addsitedir which will append our vendor directories
  # to sys.path (which was truncated by the last step.)
  site.addsitedir(os.path.join(os.path.dirname(__file__), folder))

  # Finally, we'll add the paths we removed back.
  sys.path.extend(remainder)



def virtualenv(path, position=1):
  """
  Adds the given virtualenv's site-packages to the python path.
 
  Args:
    path: Path to a root of the virtualenv, relative to ``os.getcwd()``
    position: passed through to :func:`vendor`.
  """
  site_dir = os.path.join(path, 'lib', 'python' + sys.version[:3], 'site-packages')
  vendor(site_dir, position=position)
