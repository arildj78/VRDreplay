# Reversing the Event file
The file contains an array of a binary data structure. The structure is 0x90 (144) bytes long.

## Data structure
The event files seems to contain an array of the following C datastructure. The byte order is LITTLE Endian.
| Offset | Size (bytes) | Data type | Description         | Assesment                                                   |
|--------|--------------|-----------|---------------------|-------------------------------------------------------------|
| 0x00   | 0x08         | time64    | Event timestamp     | OK                                                          |
| 0x08   | 0x08         | int64     | Unknown 1           | unique data in each record                                  |
| 0x10   | 0x20         | string    | Event description   | Fixed width data, null terminated                           |
| 0x30   | 0x08         | int64     | Unknown 2           |                                                             |
| 0x38   | 0x08         | int64     | Unknown 3           |                                                             |
| 0x40   | 0x08         | int64     | Unknown 4           |                                                             |
| 0x48   | 0x08         | int64     | Unknown 5           |                                                             |
| 0x50   | 0x08         | int64     | Unknown 6           |                                                             |
| 0x58   | 0x08         | int64     | Unknown 7           |                                                             |
| 0x60   | 0x08         | int64     | Unknown 8           |                                                             |
| 0x68   | 0x08         | int64     | Unknown 9           | <> 0 on START_ and STOP_ event                              |
| 0x70   | 0x08         | int64     | Unknown 10          | <> 0 on START_ and STOP_ event                              |
| 0x78   | 0x08         | int64     | Unknown 11          |                                                             |
| 0x80   | 0x08         | int64     | Unknown 12          |                                                             |
| 0x88   | 0x08         | int64     | Unknown 13          |                                                             |


## Example data
### Timestamp
Seconds since 1 JAN 1970 stored as a signed 64 bit integer.

### Unknown 1

### Event description
START_EOS_ACT_230603155406_001
START_EOS_ACT_230603155406_001
event2
event3
event4
event5
event6
START_EOS_ACT_230303133429_001
START_EOS_ACT_230304084542_001
START_EOS_ACT_230307121355_001


### Unknown 2

### Unknown 3

### Unknown 4

### Unknown 5

### Unknown 6

### Unknown 7

### Unknown 8
### Unknown 9
Value seems to be == 0 for event marker. This will be used to identify the events to show during debrief.

### Unknown 10
Value seems to be == 0 for event marker.

### Unknown 11
### Unknown 12
### Unknown 13
