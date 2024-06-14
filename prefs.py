import os

PROJECT_NAME_PREFIX = "Debrief "

PKG = __package__
# Recording directories
TAGFILE_LINES_TO_SCAN_FROM_END_TO_FIND_STOPTIME = 200
EMPTY_SECONDS_BEFORE_NEW_TIMELINE = 60

TIMELINE_FPS = 25

EVENT_MARKER_TRACK = (11, "Event Marker")
RMCAM_TRACK = (10, "RM Cam")
DOCCAM_TRACK = (9, "Doc Cam")
SOFECAM_TRACK = (8, "SO FE Cam")
TAIL_TRACK = (7, "Tail")
MCC_TRACK = (6, "MCC")
OPLS_TRACK = (5, "OPLS")
HOISTCAM_TRACK = (4, "Hoist")
EO_ACT_TRACK = (3, "EO Active")
EO_OPP_TRACK = (2, "EO Opposite")
QUAD_TRACK = (1, "Quad")

PILOT_TRACK = (1, "Pilot")
COPILOT_TRACK = (2, "CoPilot")
SO_TRACK = (3, "SO")
FE_TRACK = (4, "FE")
SOFECAM_AUDIO_TRACK = (5, "SO FE Cam")
DOCCAM_AUDIO_TRACK = (6, "Doc Cam")
RMCAM_AUDIO_TRACK = (7, "RM Cam")

class TrackType():
    #Alias to different types of tracks in the timeline
	VIDEO = "video"
	AUDIO = "audio"

class MarkerColor():
	BLUE     = "Blue"
	CYAN     = "Cyan"
	GREEN    = "Green"
	YELLOW   = "Yellow"   # 240, 157, 0   #0.94117647059, 0.61568627451, 0.00000000000
	RED      = "Red"
	PINK     = "Pink"
	PURPLE   = "Purple"
	FUCHSIA  = "Fuchsia"
	ROSE     = "Rose"
	LAVENDER = "Lavender"
	SKY      = "Sky"
	MINT     = "Mint"
	LEMON    = "Lemon"
	SAND     = "Sand"
	COCOA    = "Cocoa"
	CREAM    = "Cream"


RECORDING_DIRECTORIES = [
    'D:\\vrd_database' ,
]
# Match filenames of the following format EO_ACT_0000_000.mkv (The $ ensures that the filename ends with .mkv)

#*********************
#   Video file names
#*********************
EO_ACT_MKV_FILENAME_REGEX     = 'EO_ACT_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
EO_ACT_TAG_FILENAME_REGEX     = 'EO_ACT_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

EO_OPP_MKV_FILENAME_REGEX     = 'EO_OPP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
EO_OPP_TAG_FILENAME_REGEX     = 'EO_OPP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

MCC_MKV_FILENAME_REGEX     = 'MCC_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
MCC_TAG_FILENAME_REGEX     = 'MCC_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

OPLS_XCS_QUAD_MKV_FILENAME_REGEX     = 'OPLS_XCS_QUAD_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
OPLS_XCS_QUAD_TAG_FILENAME_REGEX     = 'OPLS_XCS_QUAD_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

#*********************
#   Audio file names
#*********************
PILOT_MKV_FILENAME_REGEX     = 'Pilot_CAP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
PILOT_TAG_FILENAME_REGEX     = 'Pilot_CAP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

COPILOT_MKV_FILENAME_REGEX     = 'CoPilot_CAP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
COPILOT_TAG_FILENAME_REGEX     = 'CoPilot_CAP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

SO_MKV_FILENAME_REGEX     = 'SO_CAP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
SO_TAG_FILENAME_REGEX     = 'SO_CAP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

FE_MKV_FILENAME_REGEX     = 'FE_CAP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
FE_TAG_FILENAME_REGEX     = 'FE_CAP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

#*********************
#   Event file names
#*********************
# Match the following filenames:
# EO_ACT_0000.evt
# EO_OPP_0000.evt
# MCC_0000.evt
# OPLS_XCS_QUAD_0000.evt
# Pilot_CAP_0000.evt
# CoPilot_CAP_0000.evt
# SO_CAP_0000.evt
# FE_CAP_0000.evt
 
#EVT_FILENAME_REGEX     = '(EO_ACT|EO_OPP|MCC|OPLS_XCS_QUAD|Pilot_CAP|CoPilot_CAP|SO_CAP|FE_CAP)_[0-9]{4}.[E,e][V,v][T,t]$'
EVT_FILENAME_REGEX     = '(EO_ACT|EO_OPP|MCC|OPLS_XCS_QUAD|Pilot_CAP|CoPilot_CAP|SO_CAP|FE_CAP)_[0-9]{4}.[E,e][V,v][T,t]$'

#*********************
#   USB identifiers
#*********************
USB_VRD_VENDOR_ID = 0x0525
USB_VRD_PRODUCT_ID = 0x3110

#Texas Instruments, Inc. TUSB9261 USB3.0 to SATA Bridge
USB_VRD_DOCK_VENDOR_ID = 0x0451
USB_VRD_DOCK_PRODUCT_ID = 0x9261

USB_EXTERNAL_DRIVE_VENDOR_ID = 0x0bc2
USB_EXTERNAL_DRIVE_PRODUCT_ID = 0x0200c


EXCEPTION_MSG_DURATION_ERROR = "The video file does not have it's duration in position 0x160. This suggests that this is not a video file or that the format has been changed."
EXCEPTION_MSG_MISSING_TAG_FILE = "The .tag file is missing, and handling of this has not been implemented yet."
