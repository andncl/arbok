#########################################
# Quantum Machine Configuration
#########################################
from qm.qua import *
import numpy as np
import time


tESRchirp=int(50e3/4) #50e3/4
tLoadRamp = int(1e3/4) # int(1e3/4) # 
unit_amp = 0.499
tUnitRamp = 48//4 # 16 ns

GA_label = 'P1'
GB_label = 'P2'
GC_label = 'J1'
GD_label = 'J2'
GE_label = 'P3'

GFB_label = 'P3'

GA = GA_label
GB = GB_label
GC = GC_label
Gread_label = 'SDC2'

G1_label = 'P1'
G2_label = 'J1'
G3_label = 'P2'
G4_label = 'J2'
G5_label = 'P3'
G6_label = 'P5'
G7_label = 'J5'
G8_label = 'P6'

# Coupling factors from GC to GA and GB. Used for virtual gates.
mGA = 0
mGB = 0
      
# vHome = [0.0, -0.0/unit_amp, 0.0, 0.0, 0.0,0.0,0.0,0.0]
# #vDelta = [-0.0/unit_amp, -0.0/unit_amp, 0.0/unit_amp,-0.0/unit_amp, -0.0/unit_amp,-0.0/unit_amp, -0.0/unit_amp, 0.0/unit_amp]

vHome = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

initTminus = 0

vInitPreLoadMixed = [-0.15/unit_amp, (0.0)/unit_amp, 0.15/unit_amp, 0.0,0.0,-0.2/unit_amp, (0.0)/unit_amp, 0.2/unit_amp] #d130013
vInitPreLoadTminus = [-0.15/unit_amp, (0.0)/unit_amp, 0.15/unit_amp, 0.0,0.0,-0.2/unit_amp, (0.0)/unit_amp, 0.2/unit_amp]#d130013
vInitLoadMixed = [-0.1/unit_amp, (0.0)/unit_amp, 0.1/unit_amp, 0.0,0.0,-0.125/unit_amp, (0.19)/unit_amp, 0.125/unit_amp] #d130013
# vInitLoadMixed = [-0.1/unit_amp, (0.0)/unit_amp, 0.1/unit_amp, 0.0,0.0,-0.125/unit_amp, (0.0)/unit_amp, 0.125/unit_amp] #d130013
vInitLoadTminus = [-0.1/unit_amp, (0.0)/unit_amp, 0.1/unit_amp, 0.0,0.0,-0.125/unit_amp, (0.0)/unit_amp, 0.125/unit_amp] #d130013
vDeltaMixed = [0.05/unit_amp, -0.0/unit_amp, -0.05/unit_amp,-0.0/unit_amp, -0.0/unit_amp,0.06/unit_amp, -0.0/unit_amp, -0.06/unit_amp]#130013
vDeltaTminus = [0.05/unit_amp, -0.0/unit_amp, -0.05/unit_amp,-0.0/unit_amp, -0.0/unit_amp,0.06/unit_amp, -0.0/unit_amp, -0.06/unit_amp] #130013
vControl = [(-0.0)/unit_amp,-0.0/unit_amp, (0.0)/unit_amp, -0.0/unit_amp,(-0.0)/unit_amp,0.0/unit_amp, (-0.4)/unit_amp, -0.0/unit_amp]
vPreRead = [(-0.045)/unit_amp,(-0.1)/unit_amp,(0.045)/unit_amp,0.0,
            0.0,(-0.06)/unit_amp,(0.0)/unit_amp,(0.06)/unit_amp] #130013
vRead=[(-0.085)/unit_amp,-0.1/unit_amp,(0.085)/unit_amp,0.0,
       0.0,(-0.1)/unit_amp,(0.0)/unit_amp,(0.1)/unit_amp]#130013

tInitPreLoadRampMixed = int(1e4/4)
tInitPreLoadMixed  = int(200e3/4)

tInitPreLoadRampTminus = int(1e4/4)
tInitPreLoadTminus = int(200e3/4)

tInitPreLoad4level = int(1000e3/4)
tInitPreLoad4levelHome = int(1000e3/4)

# After the preload pulses above
tInitLoadRampMixed = int(0.1e3/4) 
tInitLoadMixed = int(0.1e3/4) 

tInitLoadRampTminus = int(0.1e3/4) 
tInitLoadTminus = int(0.1e3/4) 

tDeltaLoadRampMixed = int(1.6e3/4)
tDeltaLoadMixed = int(1e3/4)

tDeltaLoadRampTminus = int(5000e3/4) 
tDeltaLoadTminus = int(1e3/4) 

tControlRamp = int(6)
tControl = int(1*1e2/4)
tControlPre = int(1e3/4)  
tControlPost = int(80e3/4)  

tHomeWait = int(100e3/4)

tPreRead = int(10e3/4) # will be not used if measure pulsign
tPreReadRamp = int(0.1e3/4)

tReadPre = int(30e3/4)#int(0.5e3/4) # 0.05e3/4   500e3/4 
tReadRamp = int(4e3/4) 
tReadInt = int(100e3/4)  # <================ HERE!
tReadPost = int(0.1e3/4) 

tReadReferenceRamp = int(17) #
tReadRefPre = int(10e3/4) 
tReadRef = int(100e3/4)  # 0.3 us
tReadRefPost = int(0.03e3/4)  # 0.3 us
tPostReadRef2 = int(0.1e3/4) 
# vReadReference = [(-0.045)/unit_amp,(-0.1)/unit_amp,(0.045)/unit_amp,0.0,0.0,(-0.06)/unit_amp,(0.0)/unit_amp,(0.06)/unit_amp] 
vReadReference = vPreRead 


tShotPost = int(4e3/4)

tArriveHome = int(0.1e3/4)

tReadInt_nominal = int(180e3/4)
tReadInt_nominal = int(180e3/4)

tSliceInt = int(1e5/4)

tRI = int(1e3/4)
min_tunnel_rate = 1e5
chop_wait = int(250e6/min_tunnel_rate/2 - tReadInt)
if chop_wait > tPreRead:
    tPreRead = chop_wait
nChops = 4
tChop = 2 * (tReadRamp + tPreRead + tReadInt + tReadPost)
tChopRead = nChops * tChop * 4e-9
tRead = tReadInt + tPreRead + tReadPost + tReadRamp

SETFB_RFsetpt = float(0)
# tInitTriplet = 2.2 * (tInitLoadTMinus + tInitMixed + tRead / 2)
# tLoadTriplet = tPreControlRampTminus

# tShotMixed = 4e-9*(tInitMixed + tLoadMixed + 3*tRead)
# tShotTriplet = 4e-9*(tInitTriplet + tLoadTriplet+ 4*tRead)
# tShot = tShotTriplet
   
tReadFB = 4e-9 * (tReadRamp + tPreRead + tReadInt + tReadPost + tReadRamp)

tInterSequence = int(100e3/4) # 100 us


fLO = int(23.17e9)
IfOffRes=int(-10e6)
# IfQ1 = int(0.16e6)
# IfQ2 = int(0.934e6)
IfQ1 = int(34.349e6)
IfQ2 = int(71.119e6)
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

# in MHz
frabi1 = 0.2658
frabi2 = 0.1826


# tX2Q2 = 4*int(0.25*1006/2)
tX2Q1 = int(1/frabi1*1e3/4/4)*4
tXQ1 = int(1/frabi1*1e3/4/4)*4*2
tX2Q2 = int(1/frabi2*1e3/4/4)*4
tXQ2 = int(1/frabi2*1e3/4/4)*4*2
tX2Q1s = int(1/frabi1*1e3/4/4)*4
tX2Q2s = int(1/frabi2*1e3/4/4)*4

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
tDCZ = int(176/4) #dCZ

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


SETFB_DCalpha = 3e-0
SETFB_DCbeta = 0.0e-4
SDC_threshold = 0.004
# SDC1_threshold = -0.003
# SDC2_threshold = 0.0025
SDC1_threshold = -0.00
SDC2_threshold = -0.004

SDC_I_weight = -0.1
SDC_Q_weight = 0.5

# vJ_RLFB = readJ/unit_amp
vJ_RLFB = -0.22/unit_amp
vPreFeedback = [(0.0)/unit_amp,vJ_RLFB,(-0.0)/unit_amp,0.0,0.0,0.0,0.0,0.0]
vFeedback = [(0.0)/unit_amp,vJ_RLFB,(-0.0)/unit_amp,0.0,0.0,0.0,0.0,0.0]
# vPreFeedback = [(0.105)/unit_amp,vJ_RLFB,(-0.105)/unit_amp]
# vFeedback = [(0.07)/unit_amp,vJ_RLFB,(-0.07)/unit_amp]

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

# Unit ramp definition. Used to normalise pulse generation
base_sample_num = tUnitRamp*4
unit_ramp_arb = np.linspace(0,unit_amp,base_sample_num).tolist()
base_sample_num_J = tUnitRampJ*4
# base_sample_num_J = tUnitRampJ*16
unit_ramp_J_arb = np.linspace(0,unit_amp,base_sample_num_J).tolist()

unit_ramp_arb_20ns = np.linspace(0,unit_amp,20).tolist()
# unit_ramp_arb_1us = np.linspace(0,unit_amp,base_sample_num*10).tolist()
# unit_ramp_arb_100us = np.linspace(0,unit_amp,base_sample_num*1000).tolist()

measurement_length = int(tReadInt*4) # Single point
# mslice_length = int(1e2) # in ns

measurement_length_slice = int(tSliceInt*4) # tSliceInt = int(1e5/4)
mslice_length = measurement_length_slice
# mslice_length = measurement_length

def IQ_imbalance_correction(g, phi):
    c = np.cos(phi)
    s = np.sin(phi)
    N = 1 / ((1 - g ** 2) * (2 * c ** 2 - 1))
    return [float(N * x) for x in [(1 - g) * c, (1 + g) * s, (1 - g) * s, (1 + g) * c]]

# Amplitude, mean, stddev, detuning, length
def gauss(amplitude, mu, sigma, delf, length):
    t = np.linspace(-length / 2, length / 2, length)
    gauss_wave = amplitude * np.exp(-((t - mu) ** 2) / (2 * sigma ** 2))
    # Detuning correction Eqn. (4) in Chen et al. PRL, 116, 020501 (2016)
    gauss_wave = gauss_wave * np.exp(2 * np.pi * delf * t)
    return [float(x) for x in gauss_wave]

min_length = 16

gauss_len = tX2Q1
gauss_sigma = gauss_len / 2
gauss_pulse = gauss(IQamp, 0, gauss_sigma, 0, gauss_len)
ngauss_pulse = (-np.array(gauss_pulse)).tolist()
gauss_pulse_q1 = gauss(IQampQ1, 0, gauss_sigma, 0, tX2Q1s)
ngauss_pulse_q1 = gauss(IQampQ1, 0, gauss_sigma, 0, tX2Q1s)
gauss_pulse_q2 = gauss(IQampQ2, 0, gauss_sigma, 0, tX2Q2s)
ngauss_pulse_q2 = gauss(IQampQ2, 0, gauss_sigma, 0, tX2Q2s)


short_gauss_len = 40 # 40ns 
short_gauss_sigma = short_gauss_len / 6
short_gauss_pulse = gauss(IQamp, 0, short_gauss_sigma, 0, short_gauss_len)

# Cosine modulation for smart (mw)
def cosine_mod(Tmod):
    # t0=np.arange(1,Nt*Tmod+1,1) 
    t0 = np.linspace(-Nt*Tmod / 2, Nt*Tmod / 2, Nt*Tmod)
    # return IQamp_max*np.cos(2*np.pi*(1/Tmod)*t0) # GLOBAL DRIVE MODULATION/I
    return 1.45*IQamp_max*np.cos(2*np.pi*(1/Tmod)*t0) # GLOBAL DRIVE MODULATION/I

def cosine3_mod(Tmod):
    # t0=np.arange(1,Nt*Tmod+1,1) 
    t0 = np.linspace(-Nt*Tmod / 2, Nt*Tmod / 2, Nt*Tmod)
    return IQamp_max*np.cos(6*np.pi*(1/Tmod)*t0) # GLOBAL DRIVE MODULATION/I


def cosine3rd_mod(Tmod):
    t0 = np.linspace(-Nt*Tmod / 2, Nt*Tmod / 2, Nt*Tmod)
    return IQamp_max*(np.cos(2.50045)*np.cos(2*np.pi*(1/Tmod)*t0)+np.sin(2.50045)*np.cos(6*np.pi*(1/Tmod)*t0)) # GLOBAL DRIVE MODULATION/I

# sine modulation for smart (top gate)
def sine_mod(Tmod):
    t0 = np.linspace(-Nt*Tmod / 2, Nt*Tmod / 2, Nt*Tmod)
    return 0.49*np.sin(2*np.pi*(1/Tmod)*t0)            # Y GATE

def cosine_2mod(Tmod):
    t0 = np.linspace(-Nt*Tmod / 2, Nt*Tmod / 2, Nt*Tmod)
    return 0.49*np.cos(2*2*np.pi*(1/Tmod)*t0)    # X GATE

kk=0.4 #0.4
t0=np.linspace(0,1,int(kk*100))
smooth = (-np.cos(np.pi*t0)+np.cos(2*np.pi*t0))*0.5*IQamp_max
smoothR=np.flipud(smooth)

Tmod = int(1.8e3) # 7 us

# Tmod = int(2.5e3) # 7 us
Nt = 1

cos_NT=cosine_mod(Tmod)
cos3_NT=cosine3_mod(Tmod)
sin_NT=sine_mod(Tmod)
cos2_NT=cosine_2mod(Tmod)
cos3rd_NT=cosine3rd_mod(Tmod)

# Integrated rectangular constant pulse
t_pulse = tCZ*4 #64
# t_pulse = 20
t_ramp_arb = 10
ramp_arb = np.linspace(0,unit_amp,t_ramp_arb).tolist()
nramp_arb = (-np.array(ramp_arb) + ramp_arb[-1]).tolist()
sine_ramp_arb = (np.array(1-np.cos(np.linspace(0,np.pi,t_ramp_arb)))*unit_amp/2).tolist()
nsine_ramp_arb = (np.array(1+np.cos(np.linspace(0,np.pi,t_ramp_arb)))*unit_amp/2).tolist()
# rect_pulse_arb = ramp_arb + [unit_amp]*(t_rect_pulse-2*t_ramp_arb) + nramp_arb
rect_pulse_arb = sine_ramp_arb + [unit_amp]*(t_pulse-2*t_ramp_arb) + nsine_ramp_arb
rect_pulse_arb[0] = 0
rect_pulse_arb[-1] = 0

feedback_length=int(tRLFB*4)

aurora_qua_config = {
    'version': 1,

    'controllers': {
        'con1': {
            'type': 'opx1',
            'analog_outputs': {
                1: {'offset': 0},  # P1
                2: {'offset': 0},  # J1
                3: {'offset': 0},  # P2
                4: {'offset': 0},  # J2
                5: {'offset': 0},  # P3
                6: {'offset': 0},  # P5
                8: {'offset': 0},  # J5
                7: {'offset': 0},  # P6
                9: {'offset': I0},  # I
                10: {'offset': Q0}, # Q
            },
            'digital_outputs': {
                1: {},  # MW Trigger: {}, MW Pulse Mod
                2: {},  # MW Trigger: {},
                3: {},  # MW Trigger: {},
                4: {},  # MW Trigger: {}, SDC Read Marker
                8: {},  # MW Trigger: {},
            },
            'analog_inputs': {
                1: {'offset': 0},  # DC SET1 READ
                2: {'offset': 0},  # DC SET2 READ

            },
        }
    },

    'elements': {

        'P1': {
            'singleInput': {
                'port': ('con1', 1)},
            'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'd'
        },

        'J1': {
            'singleInput': {
                'port': ('con1', 2)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'e'
        },
        
        'P2': {
            'singleInput': {
                'port': ('con1', 3)},
            'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'a'
        },

        'J2': {
            'singleInput': {
                'port': ('con1', 4)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'b'
        },

        'P3': {
            'singleInput': {
                'port': ('con1', 5)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'c'
        },
        'P5': {
            'singleInput': {
                'port': ('con1', 6)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'c'
        },
        'J5': {
            'singleInput': {
                'port': ('con1', 7)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'c'
        },
        'P6': {
            'singleInput': {
                'port': ('con1', 8)},
            # 'intermediate_frequency': 0,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'c'
        },
        
        
        # 'RB': {
        #     'singleInput': {
        #         'port': ('con1', 6)},
        #     # 'intermediate_frequency': 0,
        #     'hold_offset': {'duration': 400},
        #     'operations': {
        #         'const': 'const_pulse',
        #         'unit_ramp': 'unit_ramp_pulse',
        # 'step':'stepPulse',
        #         #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
        #         #'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
        #         #'unit_ramp_1us': 'unit_ramp_pulse_1us'
        #     },
        #     # 'thread': 'c'
        # },
        
        'Dref': {
            'digitalInputs':{
                'digital_input1':{
                          'port': ('con1', 8),
                          'delay': 24,
                          'buffer': 0
                          }
                },
            'operations': {
                'dmarker': 'dig_pulse',
            }
        },
        
        
        'SDC1': {
            'singleInput': {
                'port': ('con1', 10)},
            'hold_offset': {'duration': 400},# 400
            'outputs': {
                'output1': ('con1', 1)
            },
            'digitalInputs':{
                'digital_input1':{
                         'port': ('con1', 4),
                         'delay': 24,
                         'buffer': 0
                         }
               },
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                'measure': 'measure_pulse',
                'mslice': 'mslice_pulse'
            },
            'time_of_flight': 180,
            'smearing': 0,
            'intermediate_frequency': 0,
            # 'thread': 'a'

        },

        'SDC2': {
            'singleInput': {
                'port': ('con1', 10)},
            'hold_offset': {'duration': 400},# 400
            'outputs': {
                'output1': ('con1', 2)
            },
            'digitalInputs':{
                'digital_input1':{
                         'port': ('con1', 4),
                         'delay': 24,
                         'buffer': 0
                         }
               },
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'step':'stepPulse',
                'measure': 'measure_pulse',
                'mslice': 'mslice_pulse'
            },
            'time_of_flight': 180,
            'smearing': 0,
            'intermediate_frequency': 0,
            # 'thread': 'a'

        },
        #     'singleInput': {
        #         'port': ('con1', 9)},
        #     'hold_offset': {'duration': 400},
        #     'outputs': {
        #         'output1': ('con1', 1)
        #     },
        #     'digitalInputs':{
        #         'digital_input1':{
        #                  'port': ('con1', 4),
        #                  'delay': 24,
        #                  'buffer': 0
        #                  }
        #        },
        #     'operations': {
        #         'const': 'const_pulse',
        #         'unit_ramp': 'unit_ramp_pulse',
        #         'step':'stepPulse',
        #         #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
        #         #'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
        #         #'unit_ramp_1us': 'unit_ramp_pulse_1us',
        #         'measure': 'measure_pulse',
        #         # 'measure_sliced':'measure_sliced_pulse'
        #     },
        #     'time_of_flight': 180,
        #     'smearing': 0,
        #     'intermediate_frequency': 0,
        #     # 'thread': 'a'

        # },
        
        # 'SRF': {
        #     'singleInput':{
        #         'port': ('con1', 10),
        #     },            
        #     'hold_offset': {'duration': 400},
        #     'outputs': {
        #         'output1': ('con1', 1)
        #     },
        #     'digitalInputs':{
        #         'digital_input1':{
        #                   'port': ('con1', 3),
        #                   'delay': 24,
        #                   'buffer': 0
        #                   }
        #     },
        #     'intermediate_frequency': 0,
        #     'time_of_flight': 180,
        #     'smearing': 0,
        #     'operations': {
        #         'unit_ramp': 'unit_ramp_pulse',
        #         'measure': 'measure_pulse',
        #         'mslice': 'mslice_pulse'
        #     },
        #     # 'thread': 'e'
        # },
    
        'trigger':{
          'digitalInputs': {
                "switch1": {
                    "port": ("con1", 3),
                    "delay": 0,
                    "buffer": 0,
                },
            },
            'operations':{
                'trig':'trigger_pulse'
            }
        },
        
        # 'ESR': {
        #     'mixInputs': {
        #         'I': ('con1', 1),
        #         'Q': ('con1', 2),
        #         'lo_frequency': fLO,
        #         # 'intermediate_frequency': IfQ1,
        #         'mixer': 'mixer_q1'
        #     },
        #     'digitalInputs': {
        #         "switch1": {
        #             "port": ("con1", 1),
        #             "delay": 100,
        #             "buffer": 20,
        #         },
        #     },
        #     'intermediate_frequency': IfQ1,
        #     'time_of_flight': 180,
        #     'smearing': 0,
        #     'operations': {
        #         'control': 'ESR_const_pulse',
        #         'chirp': 'ESR_chirp_pulse',
        #         'shaped': 'ESR_gauss_pulse'
        #     },
        #     'thread': 'a'
        # },

        'Q1': {
            'mixInputs': {
                # 'I': ('con1', 9),
                # 'Q': ('con1', 10),
                'I': ('con1', 9),
                'Q': ('con1', 10),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_q1'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 4,
                },
            },
            'intermediate_frequency': IfQ1,
            #'time_of_flight': 180,
            #'smearing': 0,
            'operations': {
                'control': 'ESR_const_pulse',
                'chirp': 'ESR_chirp_pulse',
                'shaped': 'ESR_gauss_pulse',
                'short_shaped': 'ESR_short_gauss_pulse',
                'X/2': "X/2PulseQ1",
                'X': "XPulseQ1",
                '-X/2': "-X/2PulseQ1",
                'nop2': "nop2Pulse",
                'nop': "nopPulse",
            },
            # 'thread': 'e'
        },
        'Y1': {
            'mixInputs': {
                # 'I': ('con1', 9),
                # 'Q': ('con1', 10),
                'I': ('con1', 10),
                'Q': ('con1', 9),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_y1'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 4,
                },
            },
            'intermediate_frequency': IfQ1,
            #'time_of_flight': 180,
            #'smearing': 0,
            'operations': {
                'control': 'ESR_const_pulse',
                'max_amp': 'ESR_max_amp',
                # 'X/2': "X/2Pulse",
                # 'X': "XPulse",
                # '-X/2': "-X/2Pulse",
                'Y/2': "Y/2PulseQ1",
                'Y': "YPulseQ1",
                '-Y/2': "-Y/2PulseQ1",
                'nop2': "nop2Pulse",
                'nop': "nopPulse",
            },
            # 'thread': 'b'
        },

        'Q2': {
            'mixInputs': {
                # 'I': ('con1', 9),
                # 'Q': ('con1', 10),
                'I': ('con1', 9),
                'Q': ('con1', 10),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_q2'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 4,
                },
            },
            'intermediate_frequency': IfQ2,
            #'time_of_flight': 180,
            #'smearing': 0,
            'operations': {
                'control': 'ESR_const_pulse',
                'chirp': 'ESR_chirp_pulse',
                'shaped': 'ESR_gauss_pulse',
                'X/2': "X/2PulseQ2",
                'X': "XPulseQ2",
                '-X/2': "-X/2PulseQ2",
                'nop2': "nop2Pulse",
                'nop': "nopPulse",
            },
        },
        
        'Y2': {
            'mixInputs': {
                # 'I': ('con1', 7),
                # 'Q': ('con1', 8),
                'I': ('con1', 10),
                'Q': ('con1', 9),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_q2'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 4,
                },
            },
            'intermediate_frequency': IfQ2,
            #'time_of_flight': 180,
            #'smearing': 0,
            'operations': {
                'control': 'ESR_const_pulse',
                'chirp': 'ESR_chirp_pulse',
                'shaped': 'ESR_gauss_pulse',
                'Y/2': "Y/2PulseQ2",
                'Y': "YPulseQ2",
                '-Y/2': "-Y/2PulseQ2",
                'nop2': "nop2Pulse",
                'nop': "nopPulse",
            },
        },
        
        # 'OffRes': {
        #     'mixInputs': {
        #         'I': ('con1', 1),
        #         'Q': ('con1', 2),
        #         'lo_frequency': fLO,
        #         # 'intermediate_frequency': IfQ1,
        #         'mixer': 'mixer_offres'
        #     },
        #     'digitalInputs': {
        #         "switch1": {
        #             "port": ("con1", 1),
        #             # "delay": 160,
        #             # "buffer": 100,
        #             "delay": 00,
        #             "buffer": 0,
        #         },
        #     },
        #     # 'singleInput':{
        #     #     'port': ('con1', 4)},
        #     # },
        #     'intermediate_frequency': IfOffRes,
        #     'time_of_flight': 180,
        #     'smearing': 0,
        #     'operations': {
        #         'control': 'ESR_const_pulse',
        #         # 'I': "X/2Pulse"
        #     },
        #     'thread': 'd'
        # },
    },

    'pulses': {
        'trigger_pulse':{
            'operation': 'measure',
            'length':1000,
            'digital_marker': 'ON',
        },
        
        'measure_pulse': {
            'operation': 'measure',
            'length': measurement_length,
            'waveforms': {
                    'single': 'zero_wf'
                },
            'digital_marker': 'ON',
            'integration_weights': {
                'x': 'cos',
                'y': 'sin',
                'x_test': 'cos_test',
                'y_test': 'sin_test'}

        },
        'unit_ramp_pulse_20ns': {
            'operation': 'control',
            'length': 20,
            'waveforms': {
                'single': 'unit_ramp_wf_20ns',
            }
        },
        'mslice_pulse': {
            'operation': 'measure',
            'length': mslice_length,
            'waveforms': {
                'single': 'srf_wf'
            },
            'digital_marker': 'ON',
            'integration_weights': {
                'x': 'sliced_cos',
                'y': 'sliced_sin'
                }
        },

        'dig_pulse': {
            'operation': 'dmarker',
            'length': int(250e6/Dfreq/2)*4,
            'digital_marker': 'ON',
        },
        "stepPulse": {
            "operation": "control",
            "length": 1000,  # in ns
            "waveforms": {"single": "step_wf"},
        },
        
        # },
        # 'measure_sliced_pulse': {
        #     'operation': 'measure',
        #     'length': slice_length_ns,
        #     'waveforms': {
        #         'single': 'zero_wf'
        #     },
        #     'digital_marker': 'ON',
        #     'integration_weights': {
        #         'sliced': 'sliced',
        #         }

        # },
        'const_pulse': {
            'operation': 'control',
            'length': 1000,
            'waveforms': {
                'single': 'const_wf',
            }
        },
         'unit_ramp_pulse': {
            'operation': 'control',
            'length': base_sample_num,
            'waveforms': {
                'single': 'unit_ramp_wf',
            }
        },
         'unit_ramp_J_pulse': {
            'operation': 'control',
            'length': base_sample_num_J,
            'waveforms': {
                'single': 'unit_ramp_J_wf',
            }
        },
        'ESR_const_pulse': {
            'operation': 'control',
            'length': min_length,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'max_amp_wf',
                'Q': 'max_amp_wf'
            }
        },
        'ESR_max_amp': {
            'operation': 'max_amp',
            'length': tX2Q1,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'max_amp_wf',
                'Q': 'max_amp_wf'
            }
        },
        'ESR_gauss_pulse': {
            'operation': 'control',
            'length': tX2Q1s,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q1_gauss_wf',
                'Q': 'q1_gauss_wf'
            }
        },
        'ESR_short_gauss_pulse': {
            'operation': 'control',
            'length': short_gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q1_short_gauss_wf',
                'Q': 'q1_short_gauss_wf'
            }
        },
        'ESR_chirp_pulse': {
            'operation': 'control',
            'length': tESRchirp*4,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q1_ctrl_wf',
                'Q': 'q1_ctrl_wf'
            }
        },
        'XPulseQ1': {
            'operation': 'control',
            'length': tXQ1,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q1_ctrl_wf',
                'Q': 'q1_ctrl_wf'
            }
        },
        'XPulseQ2': {
            'operation': 'control',
            'length': tXQ2,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q2_ctrl_wf',
                'Q': 'q2_ctrl_wf'
            }
        },
        'X/2PulseQ1': {
            'operation': 'control',
            'length': tX2Q1,# gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q1_gauss_wf',
                # 'Q': 'q1_gauss_wf'
                'I': 'q1_ctrl_wf',
                'Q': 'q1_ctrl_wf'
            }
        },
        '-X/2PulseQ1': {
            'operation': 'control',
            'length': tX2Q1,# gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q1_ngauss_wf',
                # 'Q': 'q1_ngauss_wf'
                'I': 'q1_nctrl_wf',
                'Q': 'q1_nctrl_wf'
            }
        },
        'X/2PulseQ2': {
            'operation': 'control',
            'length': tX2Q2,# gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q2_gauss_wf',
                # 'Q': 'q2_gauss_wf'
                'I': 'q2_ctrl_wf',
                'Q': 'q2_ctrl_wf'
            }
        },
        '-X/2PulseQ2': {
            'operation': 'control',
            'length': tX2Q2,# gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q2_ngauss_wf',
                # 'Q': 'q2_ngauss_wf'
                'I': 'q2_nctrl_wf',
                'Q': 'q2_nctrl_wf'
            }
        },
        'YPulseQ1': {
            'operation': 'control',
            'length': tXQ1,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q1_ctrl_wf',
                'Q': 'q1_ctrl_wf'
            }
        },
        'Y/2PulseQ1': {
            'operation': 'control',
            'length': tX2Q1,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q1_gauss_wf',
                # 'Q': 'q1_gauss_wf'
                'I': 'q1_ctrl_wf',
                'Q': 'q1_ctrl_wf'
            }
        },
        '-Y/2PulseQ1': {
            'operation': 'control',
            'length': tX2Q1,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q1_ngauss_wf',
                # 'Q': 'q1_ngauss_wf'
                'I': 'q1_nctrl_wf',
                'Q': 'q1_nctrl_wf'
            }
        },   
        'YPulseQ2': {
            'operation': 'control',
            'length': tXQ2,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'q2_ctrl_wf',
                'Q': 'q2_ctrl_wf'
            }
        },
        'Y/2PulseQ2': {
            'operation': 'control',
            'length': tX2Q2,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q2_gauss_wf',
                # 'Q': 'q2_gauss_wf'
                'I': 'q2_ctrl_wf',
                'Q': 'q2_ctrl_wf'
            }
        },
        '-Y/2PulseQ2': {
            'operation': 'control',
            'length': tX2Q2,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q2_ngauss_wf',
                # 'Q': 'q2_ngauss_wf'
                'I': 'q2_nctrl_wf',
                'Q': 'q2_nctrl_wf'
            }
        },
        'nop2Pulse': {
            'operation': 'control',
            'length': gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'zero_wf',
                'Q': 'zero_wf'
            }
        },
        'nopPulse': {
            'operation': 'control',
            'length': tXQ1,
            'digital_marker': 'ON',
            'waveforms': {
                'I': 'zero_wf',
                'Q': 'zero_wf'
            }
        },
        # 'X2test_pulse': {
        #     'operation': 'control',
        #     'length': 980,
        #     'waveforms': {
        #         'I': 'x2test_ctrl_wf',
        #         'Q': 'x2test_ctrl_wf'
        #     }
        # },
        # 'ESR_sweep_pulse': {
        #     'operation': 'control',
        #     'length': sweep_samples,
        #     'waveforms': {
        #         'I': 'I_sweep_wf',
        #         'Q': 'Q_sweep_wf'
        #     }
        # },
        # 'ESR_adb_pulse': {
        #     'operation': 'control',
        #     'length': tQ1*4,
        #     'waveforms': {
        #         'I': 'ESR_adb_wf',
        #         'Q': 'ESR_adb_wf'
        #     }
        # },
        # 'Q2_const_pulse': {
        #     'operation': 'control',
        #     'length': tQ1*4,
        #     'waveforms': {
        #         'I': 'q2_ctrl_wf',
        #         'Q': 'q2_ctrl_wf'
        #     }
        # },
    },

    'waveforms': {
        'zero_wf': {
            'type': 'constant',
            'sample': 0.0
        },
        'const_wf': {
            'type': 'constant',
            'sample': 0.49
        },
        'unit_ramp_wf':{
            'type':'arbitrary',
            'samples':unit_ramp_arb
            },
        'unit_ramp_J_wf':{
            'type':'arbitrary',
            'samples':unit_ramp_J_arb
            },
        "step_wf": {
            'type': 'constant',
            'sample': step_amp
            },
        # 'unit_ramp_wf_1us':{
        #     'type':'arbitrary',
        #     'samples':unit_ramp_arb_1us
        #     },
        'unit_ramp_wf_20ns':{
            'type':'arbitrary',
            'samples':unit_ramp_arb_20ns
            },
        'srf_wf': {
            'type': 'constant',
            'sample': 0.001
        },
        'q1_ctrl_wf': {
            'type': 'constant',
            # 'sample': 0.352 # Should be max amplitude without overflow
            'sample': IQampQ1 # Some margin added to allow for adjustment
        },
        'q1_nctrl_wf': {
            'type': 'constant',
            # 'sample': -0.352 # Should be max amplitude without overflow
            'sample': -IQampQ1 # Some margin added to allow for adjustment
        },
        'q2_ctrl_wf': {
            'type': 'constant',
            # 'sample': 0.352 # Should be max amplitude without overflow
            'sample': IQampQ2 # Some margin added to allow for adjustment
        },
        'q2_nctrl_wf': {
            'type': 'constant',
            # 'sample': -0.352 # Should be max amplitude without overflow
            'sample': -IQampQ2 # Some margin added to allow for adjustment
        },
        'max_amp_wf': {
            'type': 'constant',
            # 'sample': 0.352 # Should be max amplitude without overflow
            'sample': IQamp_max # Some margin added to allow for adjustment
        },
        'q1_gauss_wf': {
            'type':'arbitrary',
            'samples':gauss_pulse_q1
        },
        'q1_ngauss_wf': {
            'type':'arbitrary',
            'samples':ngauss_pulse_q1
        },
        'q2_gauss_wf': {
            'type':'arbitrary',
            'samples':gauss_pulse_q2
        },
        'q2_ngauss_wf': {
            'type':'arbitrary',
            'samples':ngauss_pulse_q2
        },
        'q1_short_gauss_wf': {
            'type':'arbitrary',
            'samples':short_gauss_pulse
        },
        # 'q1_short_ngauss_wf': {
        #     'type':'arbitrary',
        #     'samples':short_ngauss_pulse
        # },
        # 'q2_ctrl_wf': {
        #     'type': 'constant',
        #     'sample': 0.352 # Should be max amplitude without overflow 0.5/sqrt(2)
        # },
    },

    'digital_waveforms': {
        'ON': {
            'samples': [(1, 0)]
        },
    },

    'integration_weights': {
        'sliced_cos': {
            'cosine': [SDC_I_weight]*(mslice_length//4),
            'sine': [0.0]*(mslice_length//4)
        },
        'sliced_sin': {
            'cosine': [0.0]*(mslice_length//4),
            'sine': [SDC_Q_weight]*(mslice_length//4)
        },
        # 'cos': {
        #     # 'cosine': [-1.0]*(measurement_length//4),
        #     # 'sine': [0.0]*(measurement_length//4)
        #     'cosine': [0.4]*(measurement_length//4),
        #     'sine': [0.0]*(measurement_length//4)
        # },
        # 'sin': {
        #     'cosine': [0.0]*(measurement_length//4),
        #     'sine': [0.4]*(measurement_length//4) 
        # },
        'cos': {
            # 'cosine': [-1.0]*(measurement_length//4),
            # 'sine': [0.0]*(measurement_length//4)
            'cosine': [SDC_I_weight]*(measurement_length//4),
            'sine': [0.0]*(measurement_length//4)
        },
        'sin': {
            'cosine': [0.0]*(measurement_length//4),
            'sine': [SDC_Q_weight]*(measurement_length//4) 
        },
        'cos_test': {
            # 'cosine': [-1.0]*(measurement_length//4),
            # 'sine': [0.0]*(measurement_length//4)
            'cosine': [0.4]*(measurement_length//4),
            'sine': [0.0]*(measurement_length//4)
        },
        'sin_test': {
            'cosine': [0.0]*(measurement_length//4),
            'sine': [0.4]*(measurement_length//4) 
        },
    },
    'mixers': {
        'mixer_q1': [
            {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
            # {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [1.0, 0.0, 0.0, 1.0]}
        ],
        'mixer_y1': [
            # {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [0.0, -1.0, 1.0, 0.0]},
            {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
        ],
        # 'mixer_nx1': [
        #     {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [-1.0, 0.0, 0.0, -1.0]},
        #     # {'intermediate_frequency': IfQ2_cnot, 'lo_frequency': fLO_cnot, 'correction': [1.0, 0.0, 0.0, 1.0]}
        # ],
        # 'mixer_ny1': [
        #     {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [0.0, 1.0, -1.0, 0.0]},
        #     # {'intermediate_frequency': IfQ2_cnot, 'lo_frequency': fLO_cnot, 'correction': [1.0, 0.0, 0.0, 1.0]}
        # ],
        'mixer_q2': [
            {'intermediate_frequency': IfQ2, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
            # {'intermediate_frequency': IfQ2_cnot, 'lo_frequency': fLO_cnot, 'correction': [1.0, 0.0, 0.0, 1.0]}
        ],
        'mixer_offres': [
            {'intermediate_frequency': IfOffRes, 'lo_frequency': fLO, 'correction': [1.0, 0.0, 0.0, 1.0]},
        ],
        # 'mixer_det': [
        #     {'intermediate_frequency': 0, 'lo_frequency': 0, 'correction': [1.0, 0.0, -1.0, 0.0]},
               
        # ],
        # 'mixer_Sref': [
        #     {'intermediate_frequency': Sfreq, 'lo_frequency': 0, 'correction': [1.0, 0.0, 0.0, 1.0]},
        #     # {'intermediate_frequency': IfQ2_cnot, 'lo_frequency': fLO_cnot, 'correction': [1.0, 0.0, 0.0, 1.0]}
        # ],

    }
}

# Adds Entropy support
def get_config():
    return {'config': config}

#%%
import winsound
def finishSound():
    duration = 200  # milliseconds
    freq = 2000  # Hz
    for ii in range(0,2,1):
        winsound.Beep(freq//2, duration)
        time.sleep(0.05)
        winsound.Beep(freq, duration)
