"""Load the game's Python files again when they change under a running app.

Why: the host can copy new files into the app without restarting it. Python then still has
the OLD modules in memory, while the 3D page is built from the NEW files on disk, and the
two stop matching (specs/fresh-code-after-deploy.md).

How: remember a fingerprint of the files. When it changes, reload the modules, in order.
"""

import hashlib
import importlib
import sys

# The fingerprint of the files as Python last loaded them. None until the first check.
LOADED = {"version": None}


def version(files) -> str:
    """A short fingerprint of the files' contents. It changes when any of them changes."""
    digest = hashlib.sha1()
    for path in files:
        digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def refresh(files, module_names, state=LOADED) -> bool:
    """Reload the modules if the files changed since the last check. True when it reloaded.

    The first call only remembers the fingerprint: a process that just started has fresh code.
    A module that imports from another one must come after it in `module_names`.
    """
    current = version(files)
    if state["version"] is None:
        state["version"] = current
        return False
    if current == state["version"]:
        return False
    importlib.invalidate_caches()
    for name in module_names:
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    state["version"] = current
    return True
