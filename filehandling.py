import os
import prefs
import win32gui
from win32com.shell import shell, shellcon


class DaVinciHandle:
    def __init__(self) -> None:
        self.windowText = prefs.DAVINCI_WINDOWTEXT
        self.windowText = 'Project Manager'
        self.hWindows = []
        self.foundHandle = False
        self.numberOfHandles = 0
        self.hWnd = self.get_hWnd()

    def EnumWindows_callback(self, hwnd, lParam):
        windowText = win32gui.GetWindowText(hwnd)
        if self.windowText in windowText:
            self.hWindows.append(hwnd)
            self.foundHandle = True
            self.numberOfHandles = self.numberOfHandles + 1

    def get_hWnd(self):
        # Iterate through all windows looking for the correct title (daVinciWindows.windowText)
        win32gui.EnumWindows(self.EnumWindows_callback, None)

        return self.hWindows[0] #If multiple daVinci windows, use the first. TODO - Handle this better.



def selectImportFolder():
    # Get DaVinci Resolve window handle

    hWnd = DaVinciHandle().hWnd
    win32gui.SetForegroundWindow(hWnd)


    drives_pidl = shell.SHGetFolderLocation (hWnd, shellcon.CSIDL_DRIVES, 0, 0)

    pidl, display_name, image_list = shell.SHBrowseForFolder (
    win32gui.GetDesktopWindow (),
        drives_pidl,
        "Select a folder with video or audio from your flight, typically named vrd_database",
        0,    #Bit flags e.g. shellcon.BIF_BROWSEINCLUDEFILES
        None, #Callback function
        None  #Data passed back to the callback function.
        )

    if pidl is not None:
        return shell.SHGetPathFromIDList (pidl)
    else:
        return None
    

    

def findVRD() -> str:
    # These are the possible drive letters to check for the presence of a VRD with data.
    drives = 'DEFGHIJKLMNOPQRSTUVWXYZ'

    foundVRD = False
    result = [] # An empty list to hold possible correct drive letters

    # Loop through every drive letter 
    for drive in range(0, len(drives)):
        driveletter = drives[drive]
        path = driveletter + ":\\vrd_database\\"
        
        # Check if the root folder exists on the drive beeing checked
        if os.path.exists(path):

            # The presence of one of these subfolders is a indication that we might have the correct drive.
            if os.path.exists(path):
                if os.path.exists(os.path.join(path, r'EO_ACT')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'EO_OPP')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'MCC')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'OPLS_XCS_QUAD')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'Pilot_CAP')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'CoPilot_CAP')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'SO_CAP')):
                    foundVRD = True
                elif os.path.exists(os.path.join(path, r'FE_CAP')):
                    foundVRD = True
                
                if foundVRD:
                    result.append(path) #Add candidate to list
                    foundVRD = False #Reset to test next drive letter

    if len(result) == 0:
        # No VRD detected. Let the user select manually
        return selectImportFolder()
    elif len(result) == 1:
        return result[0]
    elif len(result) > 1:
        # More than two possible locations exist. Let the user select manually
        return selectImportFolder()



if __name__ == "__main__":
    selectImportFolder()
