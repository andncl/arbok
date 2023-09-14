import numpy as np

tESRchirp=int(50e3/4) #50e3/4
tLoadRamp = int(1e3/4) # int(1e3/4) # 
unit_amp = 0.499
tUnitRamp = 48//4 # 16 ns

GA_label = 'P1'
GB_label = 'P2'
GC_label = 'J1'
GD_label = 'J2'
GE_label = 'P3'

GA = GA_label
GB = GB_label
GC = GC_label
Gread_label = 'SDC'

# Coupling factors from GC to GA and GB. Used for virtual gates.
mGA = 0
mGB = 0
                
vHome = [0.0, -0.49/unit_amp, 0.0, 0.0, 0.0]

vDelta = [0.045/unit_amp, -0.0/unit_amp, -0.045/unit_amp]
vDeltaM = [-5*0.035/unit_amp, -0.0/unit_amp, 5*0.035/unit_amp]

vInitPreLoadTminus = [(-0.095)/unit_amp, (0.2)/unit_amp, (0.095)/unit_amp]
vInitMixed = [-0.12/unit_amp, (0.075)/unit_amp, 0.12/unit_amp, 0.0]


vInitMixed2 = [0.11/unit_amp, (-0.0)/unit_amp, -0.11/unit_amp, 0.0]
vInitPreLoadMixed1 = [(0.2)/unit_amp, (-0.0)/unit_amp, (-0.2)/unit_amp] 
vLoadMixed1 = [(0.00)/unit_amp, (-0.0)/unit_amp, (-0.00)/unit_amp] 

vControl = [(-0.0)/unit_amp,0.4/unit_amp, (0.0)/unit_amp, -0.0/unit_amp]
vControl2 = [(-0.02)/unit_amp,-0.49/unit_amp, (0.0168)/unit_amp, -0.0/unit_amp] # 1Q
#vControl2 = [(-0.02)/unit_amp,-0.3/unit_amp, (0.0168)/unit_amp, -0.0/unit_amp] # 1Q
vControl3 = [(-0.0168)/unit_amp,0.25/unit_amp, (0.0168)/unit_amp, -0.0/unit_amp] # swap

readJ=(-0.0)/unit_amp
vPreRead = [(0.065)/unit_amp,(readJ),(-0.065)/unit_amp] 
vRead=[(0.0925)/unit_amp,(readJ),(-0.0925)/unit_amp]

vReadReference = [ (0.00)/unit_amp ,0.0/unit_amp,(-0.00)/unit_amp]
# vReadReference = [ (0.00)/unit_amp ,-0.1/unit_amp,(-0.00)/unit_amp]

tArriveHome = int(1e2/4)
tInitLoadRamp = int(1*0.1e3/4) 

tInitLoadMixed =  int(6000e3/4) 
tInitLoadTMinus = int(3e3/4)

tInitPreLoadRamp = int(1e4/4)
tInitPreLoad = int(0.1e3/4)

tPreControlRampMixed = int(9e3/4)#int(4e3/4)
tPreControlRampTminus = int(8000e3/4) 

tControlRamp = int(6)#int(0.1e3/4) # 1e2/4
tControl = int(1*1e2/4)

tPreControl = int(0.1e3/4)  
tPostControl = int(1e3/4)     

tPreReadPoint = int(50)
tPreReadRamp = int(0.1e3/4)

tPreRead = int(0.05e3/4) # 0.05e3/4   500e3/4 
tReadRamp = int(0.05e3/4) 
tPostRead = int(0.1e3/4)  

tPreReadRef = int(0.03e3/4)  # 0.3 us
tPreReadRef2 = int(0.03e3/4)  # 0.3 us
tReadReferenceRamp = int(17) #
tPostReadRef = int(0.1e3/4) 
tPostReadRef2 = int(0.1e3/4) 

tReadInt = int(1e2/4) # <================ HERE!
tReadInt_nominal = int(180e3/4)

tSliceInt = int(1e5/4)
# tPulseMod = int(70e3/4)#70


# warmT=int(80e3/4)
# warmAmp=float(0.8)




tRI = int(1e3/4)
min_tunnel_rate = 1e5
chop_wait = int(250e6/min_tunnel_rate/2 - tReadInt)
if chop_wait > tPreRead:
    tPreRead = chop_wait
nChops = 4
tChop = 2 * (tReadRamp + tPreRead + tReadInt + tPostRead)
tChopRead = nChops * tChop * 4e-9
tRead = tReadInt + tPreRead + tPostRead + tReadRamp

tInitMixed = tInitLoadMixed
tLoadMixed = tPreControlRampMixed

tInitTriplet = 2.2 * (tInitLoadTMinus + tInitMixed + tRead / 2)
tLoadTriplet = tPreControlRampTminus

tShotMixed = 4e-9*(tInitMixed + tLoadMixed + 3*tRead)
tShotTriplet = 4e-9*(tInitTriplet + tLoadTriplet+ 4*tRead)
tShot = tShotTriplet
   
tReadFB = 4e-9 * (tReadRamp + tPreRead + tReadInt + tPostRead + tReadRamp)

tInterSequence = int(100e3/4) # 100 us


fLO = int(23.17e9)
IfOffRes=int(-10e6)
IfQ1 = int(11e6)
IfQ1add=IfQ1
IfQ2 = int(11.5e6)
IfQoff = int(40e6)
fQh = int(-175e6)
fQ1=IfQ1
fQ2=IfQ2
fOffRes=IfOffRes
ampQoff = 1.99*0.5

# manual rotation correction
Q1rotCorr = 0.999



tX2Q1 = 4*int(0.25*(1/1)*1e3/4) #int(420) #int(624) # nanoseconds , J = -0.0, 
IQscalarQ1 = 1.4



tX2Q2 = 4*int(0.25*1006/2)
tX2Q1s = int(800) # nanoseconds , J = -0.0
tXQ1 = int(1440) # nanoseconds
tX2Q2s = int(1040) # Shaped pulse
tXQ2 = int(1072) # nanoseconds
tQoff = int(3000/4) #nanoseconds


# Initialisation mode
S_init = False

# Readout mode
readout_on_other_side = True

# dCZ, d6CZ, d7CZ
CZ_mode = 'dCZ'
tPredCZ = int(20/4)

Pulse_J_Mode = 'Constant'
Ramp_Mode = 'Linear' 

t_mw_delay = int(96/4) #int(24/4)
tUnitRampJ = tUnitRamp#int(16/4)

vCZ = [0.00/unit_amp, 0.362/unit_amp, -0.00/unit_amp]
tCZ = int(176/4) #dCZ

tCZwait = int(64)
phaseCZQ2 = 0.93#0.25#0.58 #0.35#0.72# 0.598 #-0.09599 # This one hopefully correct
phaseCZQ1 = 0.58#0.91#0.24 #0.0 #0.0 #0.300 #-0.52466
RCZ = 0.25


# tCZ = int(264/4)
tCZgate = int(tCZ + 2*16/4)
tCZRampSettle = int(40/4)
# RCZ = 0.25
# phase = 7.838

B0=370
B0str=str(B0)+"mT"
Pstr="12.5dBm"
T=25
Tstr=str(T)+"mK"
Jstr = str(vControl[1]*unit_amp)

# Mixer calibration factors
I0 = -0.00873*0 # DC offsets
Q0 = -0.01251*0   
 
g = 0.00493
phi = 0.00579

IQamp_max = 0.5 /2.5 #  # Tuomo & Nard


IQamp = IQamp_max / 1 # Tuomo & Nard


Q1amp_factor = 0.98*0.994*0.998*0.994*1.0075*0.98*1.02*0.97*1.03*0.96*1.01*1.01* 1.01*0.98*1.01*1.02*1.04*0.955*1.01*1.03*1.0075*  0.985* 0.75 * 1.02 * 0.98 * 1.02 * 1.01 * 0.993 * 1.025 * 0.96 * 1.02 * 1.02 * 0.98 * 1.02 * 1.02 * 1.02 * 1.02 * 0.98*1.01*1.01*0.99 * 0.98 *0.97*1.01 * 1.03
Q2amp_factor = 1.04*1.015*0.99*0.99*0.99*1.01*0.985*1.015*0.97*1.01*0.98*1.02*1.01*1.01* 1.01*0.98*1.01*1.04*1.075*1.03*0.99*0.75 * 0.98 * 1.03 * 1.03 * 0.96 * 1.02 * 1.02 * 0.98 * 1.02 * 1.02 * 1.02 * 1.02 * 1.02 * 0.96 * 0.96 * 0.96 * 1.10*1.01*1.01*0.985*0.97 * 1.01*1.02*0.96*1.03
IQampQ1 = IQamp_max * Q1amp_factor
IQampQ2 = IQamp_max * Q2amp_factor
IQscaling = 1.0

SDCfreq = 0

Dfreq = 543
a_chop = 1/nChops
vChop = 0.025/unit_amp
vChop = int(vChop*2**15)/(2**15) + 2**-28 # Correct fixed pt error
step_amp = unit_amp

# SET Feedback params
tWait_stfb = int(10e3/4)

SETFB_DCsetpt = 0.115 * tReadInt / tReadInt_nominal # Lower set point for charge maps


SETFB_DCalpha = 3e-0#10e-4
SETFB_DCbeta = 0.0e-4
SDC_threshold = 0.004#0.008#-0.0035#-0.0025* tReadInt / tReadInt_nominal #-0.016


SDC_I_weight = -0.1#0.1315
SDC_Q_weight = 0.5#-0.4073s




# vJ_RLFB = readJ/unit_amp
vJ_RLFB = -0.22/unit_amp
vPreFeedback = [(0.105)/unit_amp,vJ_RLFB,(-0.105)/unit_amp]
vFeedback = [(0.07)/unit_amp,vJ_RLFB,(-0.07)/unit_amp]

RLFB_S1 =  -0.2 
RLFB_S2 = 0.29
RLFB_delta = ( RLFB_S2 - RLFB_S1 ) * tReadInt/tReadInt_nominal
RLFB_setpt = ( RLFB_S2 + RLFB_S1 )/2 * tReadInt/tReadInt_nominal
RLFB_alpha = 0*0.4e-2 / abs(RLFB_delta)
# RLFB_setpt = -0.035
# RLFB_alpha = 1e-4
RLFB_beta = 0#0.5e-7
# RLFB_

tRLFB=int(tReadInt*1)#int(25e3/4)



# Rabi feedback params
RabiFB_alpha = 0*1e-4
RabiFB_alpha_baked = 1e-4
# RabiFB_alpha = 0
# RabiFB_nx2 = [5,7,9,11] # Flanks of the 3pi and 5pi peaks
RabiFB_nx2 = [3,5] # Flanks of the 5pi peak
RabiFB_nx21 = RabiFB_nx2[0]
RabiFB_nx22 = RabiFB_nx2[1] #for upgraded feedback

RabiCFB_nx2 = [11,13]

RabiFB_npts = len(RabiFB_nx2)
RabiFB_prop = 0.4 # Proportion of shots that will be used for frequency feedback

# Frequency feedback params
FreqFB_det = int(0.5e6)
# FreqFB_det = int(1/(4*tX2Q1*1e-9))
FreqFB_offset = int(0e3) # Offset to correct for frequency shift
FreqFB_alpha_baked = int(-500) # Hz/shot
FreqFB_alpha = int(1500) # Hz/shot
FreqFB_alpha_for_all = int(-1000)#int(1500) # Hz/shot

# FreqFB_nx2 = 10 # 5pi
# FreqFB_tESR = int(3.736e3/4) # Equivalent to 5pi using long pulse. Assumes that
# the calibrated X/2 time is 416ns.
# FreqFB_t_scalef = 4 * FreqFB_tESR / (10 * tX2Q1)
FreqFB_t_scalef = 0.98 # Rough guess
# FreqFB_tESR = int(10 * FreqFB_t_scalef * tX2Q1 / 4)
FreqFB_tESR = int(6 * FreqFB_t_scalef * tX2Q1 / 4)
FreqFB_tWait = int(0.1e3/4) # Initial test value
FreqFB_npts = 2
FreqFB_prop = 0.4 # Proportion of shots that will be used for frequency feedback

# Init feedback params
IFB_MaxAttempts = 20
IFB_MaxReadAttempts = 3

# CZ feedback params
# CZFB_npts = 6
CZFB_Ncz = 3
CZFB_prop = 0.75
# CZFB_Jalpha = 0e-5# CZ
CZFB_Jalpha = 0.2e-4# dCZ
# CZFB_Jalpha = 0
CZFB_Phalpha = 10e-4#5e-5
CZFB_NczBalancedPhase = 2
CZFB_NczBalanced = 2
CZFB_wait = int(100/4)
# CZFB_n_CZ_L = [CZFB_Ncz]
# CZFB_n_CZ_R = [CZFB_Ncz]
CZFB_n_CZ_L = [3]
CZFB_n_CZ_R = [5]
CZFB_npts = len(CZFB_n_CZ_R)
CZFB_playto = CZFB_n_CZ_R[-1]#40#
J_offset = 0

# GST corrections, format: targetGate_corrGate
X1_Z2 = -0.02
X2_Z2 = -0.03
Z1_Z2 = 0.01
CZ_Z1 = 0.13


# new feedback sequences
Q1Freqfbseq1 = [ 2,1,1,1,0,2]
Q1Freqfbseq2 = [ 2,1,0,2]
Q2Freqfbseq1 = [ 4,3,3,3,0,4]
Q2Freqfbseq2 = [ 4,3,0,4]
Q1Rabifbseq1 = [ 2,0]*RabiFB_nx21
Q1Rabifbseq2 = [ 2,0]*RabiFB_nx22
Q2Rabifbseq1 = [ 4,0]*RabiFB_nx21
Q2Rabifbseq2 = [ 4,0]*RabiFB_nx22
# CZ feedback sequences
tempPh1 = [5,2,2,7,2,2]*CZFB_NczBalancedPhase
tempPh2 = [5,4,4,7,4,4]*CZFB_NczBalancedPhase
# tempJ1   = [5,4,2,2,4,5]*CZFB_NczBalanced
# tempJ2   = [5,2,4,4,2,5]*CZFB_NczBalanced
tempJ1   = [5,10,5]*CZFB_NczBalanced
tempJ2   = [5,10,5]*CZFB_NczBalanced
PH1fbseq1    = [2]+tempPh1+[1,1,1,2]
PH1fbseq2    = [2]+tempPh1+[1,2]
PH2fbseq1    = [4]+tempPh2+[3,3,3,4]
PH2fbseq2    = [4]+tempPh2+[3,4]
Jfbseq1 = [2]+tempJ1+[1,1,1,2]
# Jfbseq2 = [2]+tempJ2+[1,2]
Jfbseq2 = [2]+tempJ1+[1,2]

    


FBseqs = [Q1Freqfbseq1,Q1Freqfbseq2,Q2Freqfbseq1,Q2Freqfbseq2,Q1Rabifbseq1, \
          Q1Rabifbseq2,Q2Rabifbseq1,Q2Rabifbseq2,PH1fbseq1,PH1fbseq2,PH2fbseq1,PH2fbseq2,Jfbseq1,Jfbseq2]


FBseqInd = [len(x) for x in FBseqs]
FBseqsLong = []

for i in range(len(FBseqs)):
    FBseqsLong = FBseqsLong+FBseqs[i]

for i in range(1,len(FBseqInd)):
    FBseqInd[i] = FBseqInd[i] + FBseqInd[i-1]

FBseqInd = [0] + FBseqInd



