print("[G4PPYY] : Geant4 Python wrapper for CPPYY")
print("[G4PPYY] : Author: P. Stowell (p.stowell@sheffield.ac.uk)")
print("[G4PPYY] :         R. Foster")

import sys as _sys

from . import _lazy_loader
from ._lazy_loader import lazy_include as include
from ._lazy_loader import lazy_load as load
from ._lazy_loader import cppyy

_lazy_loader.set_top_level(__name__)

# Module level lazy loader, intercepts attr calls
# for the module allowing for access of G4 variables through this
# e.g. g4ppyy.G4VisAttributes,
def __getattr__(name):
    
    try:
        return globals()[name]
    except:
        pass   

    try:
        globals()[name] =  _lazy_loader.__getattr__(name)
        current_module = _sys.modules[__name__]
        setattr(current_module, name, globals()[name])
        return _lazy_loader.__getattr__(name)
    except:
        pass  

    # If the attribute is not found, raise AttributeError as usual
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


from . import SI 

# from ._bindings import *

from . import register 

from . import run 

from . import vis

from . import builder

class _macro_callback_handler:
    def __init__(self, base=""):
        self.rdir = base

    def __getattr__(self, key):
        return _macro_callback_handler(self.rdir.replace("_","-") + "/" + key)

    def __dir__(self):
        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        UImanager.ListCommands(self.rdir)
    
    def __call__(self, *args):
        callstr = self.rdir + " "
        for obj in args:
            callstr += str(obj) + " "

        UImanager = _lazy_loader.G4UImanager.GetUIpointer()
        
        with open("./.G4temp.cmd", "w") as f:
            f.write(callstr + "\n")
        f.close()
        
        UImanager.ExecuteMacroFile("./.G4temp.cmd")

mc = _macro_callback_handler()

from . destructor import *

from . import magic as _magic

print("[G4PPYY] : Imported all definitions.")



