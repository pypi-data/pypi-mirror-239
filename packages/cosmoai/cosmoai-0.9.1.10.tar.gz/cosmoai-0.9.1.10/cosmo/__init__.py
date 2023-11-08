import sys

from .core.core import Cosmo

# This is done so when users `import cosmo`,
# they get an instance of cosmo:

sys.modules["cosmo"] = Cosmo()

# **This is a controversial thing to do,**
# because perhaps modules ought to behave like modules.

# But I think it saves a step, removes friction, and looks good.

