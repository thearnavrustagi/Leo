OCCUPIED = 1.0
FREE = 0.0

P_FREE = 0.1
P_OCC = 0.8
P_INIT = 0.5
DEC_BOUNDARY = 0.5

STATES = [(0,1),(1,0),(0,-1),(-1,0)]
FWD = 0
RGT = 1
BWD = 2
LFT = 3
INITIAL_STATE = STATES[FWD]

FIG_SIZE = (6,8)
INITIAL_POSN = (0,0)
MAP_SIZE = (5,5) # size of the
L2R = lambda x,y,s : y*s[1] + x # Left to right
T2B = lambda x,y,s : x*s[0] + y # Top to bottom
