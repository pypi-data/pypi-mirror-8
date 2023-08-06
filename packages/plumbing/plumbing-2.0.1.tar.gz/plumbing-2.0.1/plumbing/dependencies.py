# Built-in modules #
import subprocess, sys

# Constants #
module_names = {
    "biopython": "Bio",
    "ipython": "IPython",
    "scikit-learn": "sklearn",
    "scikit-bio": "skbio",
}

################################################################################
def check_setup(mod_name):
    """Parses the required modules from a setup.py file and check they are
    available in the PYTHONPATH"""
    pass

################################################################################
def check_executable(tool_name):
    """Raises an warning if the executable *tool_name* is not found."""
    result = subprocess.call(['which', tool_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result != 0:
        message = "The executable '%s' cannot be found in your $PATH" % tool_name
        raise Exception(message)

################################################################################
def check_module(mod_name):
    """Calls sys.exit() if the module *mod_name* is not found."""
    # Special cases #
    if mod_name == "biopython": mod_name = "Bio"
    if mod_name == "ipython": mod_name = "IPython"
    if mod_name == "scikit-learn": mod_name = "sklearn"
    # Use a try except block
    try:
        __import__(mod_name)
    except ImportError as e:
        if str(e) != 'No module named %s' % mod_name: raise e
        print 'You do not seem to have the "%s" package properly installed.' \
              ' Either you never installed it or your $PYTHONPATH is not set up correctly.' \
              ' For more instructions see the README file. (%s)' % (mod_name, e)
        sys.exit()