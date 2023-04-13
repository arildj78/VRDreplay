import os

PROJECT_NAME_PREFIX = "Debrief-"

PKG = __package__
# Recording directories
TAGFILE_LINES_TO_SCAN_FROM_END_TO_FIND_STOPTIME = 200
EMPTY_SECONDS_BEFORE_NEW_TIMELINE = 60

MCC_TRACK = (4, "MCC")
EO_ACT_TRACK = (3, "EO Active")
EO_OPP_TRACK = (2, "EO Opposite")
QUAD_TRACK = (1, "Quad")

class TrackType():
    #Alias to different types of tracks in the timeline
	VIDEO = "video"
	AUDIO = "audio"


RECORDING_DIRECTORIES = [
    'F:\\AW101\\Disk1\\vrd_database' ,
]
#                                         0         1         2         3         4
#                                         012345678901234567890123456789012345678901234
# Match filenames of the following format EO_ACT_0000_000.mkv (The $ ensures that the filename ends with .mkv)
EO_ACT_MKV_FILENAME_REGEX     = 'EO_ACT_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
EO_ACT_TAG_FILENAME_REGEX     = 'EO_ACT_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

EO_OPP_MKV_FILENAME_REGEX     = 'EO_OPP_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
EO_OPP_TAG_FILENAME_REGEX     = 'EO_OPP_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

MCC_MKV_FILENAME_REGEX     = 'MCC_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
MCC_TAG_FILENAME_REGEX     = 'MCC_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

OPLS_XCS_QUAD_MKV_FILENAME_REGEX     = 'OPLS_XCS_QUAD_[0-9]{4}_[0-9]{3}.[M,m][K,k][V,v]$'
OPLS_XCS_QUAD_TAG_FILENAME_REGEX     = 'OPLS_XCS_QUAD_[0-9]{4}_[0-9]{3}.[T,t][A,a][G,g]$'

