import os, sys


RESOLVE_SUPPORT_DIR = os.path.join(*[
    os.environ["PROGRAMDATA"],
    "Blackmagic Design",
    "DaVinci Resolve",
    "Support",
])

RESOLVE_LUT_DIR = os.path.join(*[
    RESOLVE_SUPPORT_DIR,
    "LUT",
])

RESOLVE_SCRIPT_API = os.path.join(*[
    RESOLVE_SUPPORT_DIR,
    "Developer",
    "Scripting",
])

RESOLVE_SCRIPT_LIB = os.path.join(*[
    os.environ["ProgramFiles"],
    "Blackmagic Design",
    "DaVinci Resolve",
    "fusionscript.dll",
])

def initConnection():
    # define environment variables

    os.environ["RESOLVE_SCRIPT_API"] = RESOLVE_SCRIPT_API
    os.environ["RESOLVE_SCRIPT_LIB"] = RESOLVE_SCRIPT_LIB

    # setup python path

    sys.path.append(os.path.join(RESOLVE_SCRIPT_API, 'Modules'))

    # now it's ready to import module
    import DaVinciResolveScript as dvrs

    # major objects
    resolve = dvrs.scriptapp("Resolve")
    if not resolve:
        print("Please launch DaVinci Resolve first.")
        sys.exit()

    projectManager = resolve.GetProjectManager()
    currentProject = projectManager.GetCurrentProject()
    mediaStorage = resolve.GetMediaStorage()
    fusion = resolve.Fusion()

    return resolve, projectManager, currentProject, mediaStorage, fusion