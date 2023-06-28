#########################################
# Quantum Machine Configuration
#########################################

import numpy as np

from Configuration import *

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


rf2v_config = {
    'version': 1,

    'controllers': {
        'con1': {
            'type': 'opx1',
            'analog_outputs': {
                1: {'offset': 0},  # P1
                2: {'offset': 0},  # J1
                3: {'offset': 0},  # P2
                4: {'offset': 0},  # J2
                5: {'offset': 0.0},  # P3
                6: {'offset': 0},  # RB
                7: {'offset': I0},  # I 
                8: {'offset': Q0},  # Q
                9: {'offset': 0},  # ST
                10: {'offset': 0}, # SDC/ST
            },
            'digital_outputs': {
                1: {},  # MW Trigger: {}, MW Pulse Mod
                2: {},  # MW Trigger: {},
                3: {},  # MW Trigger: {},
                4: {},  # MW Trigger: {}, SDC Read Marker
                # 8: {},  # MW Trigger: {},
                7: {},  # MW Trigger: {},
            },
            'analog_inputs': {
                1: {'offset': 0},  # DC SET READ
                2: {'offset': 0},  # DC SET READ

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
        'P1_not_sticky': {
            'singleInput': {
                'port': ('con1', 1)},
            # 'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                'sine':"sineP",
                'cosine2':"cosine2P",
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                'smooth': "smooth0p",
                'smoothR': "smoothR0p",
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'd'
        },
        'P2_not_sticky': {
            'singleInput': {
                'port': ('con1', 3)},
            # 'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                'sine':"sineP",
                'cosine2':"cosine2P",
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                'smooth': "smooth0p",
                'smoothR': "smoothR0p",
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'd'
        },
        
        'J1_not_sticky': {
            'singleInput': {
                'port': ('con1', 2)},
            # 'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                'sine':"sineP",
                'cosine2':"cosine2P",
                'smooth': "smooth0p",
                'smoothR': "smoothR0p",
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'd'
        },
        
        'J2_not_sticky': {
            'singleInput': {
                'port': ('con1', 4)},
            # 'hold_offset': {'duration': 100},
            'operations': {
                'const': 'const_pulse',
                'unit_ramp': 'unit_ramp_pulse',
                'unit_ramp_J': 'unit_ramp_J_pulse',
                'step':'stepPulse',
                'sine':'sineP',
                'cosine2':'cosine2P',
                'smooth': 'smooth0p',
                'smoothR': 'smoothR0p',
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
                'rect_pulse_arb': 'rect_pulse_arb',
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us'
            },
            # 'thread': 'e'
        },
        
        'J1Noise': {
            'singleInput': {
                'port': ('con1', 2)},
            'intermediate_frequency': 2e6,
            'hold_offset': {'duration': 400},
            'operations': {
                'const': 'const_pulse',
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
        
        # 'P3': {
        #     'singleInput': {
        #         'port': ('con1', 5)},
        #     'hold_offset': {'duration': 100},
        #     'operations': {
        #         'const': 'const_pulse',
        #         'unit_ramp': 'unit_ramp_pulse',
        #         'unit_ramp_J': 'unit_ramp_J_pulse',
        #         'step':'stepPulse',
        #         #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
        #         'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
        #         #'unit_ramp_1us': 'unit_ramp_pulse_1us'
        #     },
        #     # 'thread': 'a'
        # },

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

        
        'Dref': {
            'digitalInputs':{
                'digital_input1':{
                          # 'port': ('con1', 8),
                          'port': ('con1', 7),
                          'delay': 24,
                          'buffer': 0
                          }
                },
            'operations': {
                'dmarker': 'dig_pulse',
            }
        },
        
        'SDC': {
            'singleInput': {
                'port': ('con1', 10)},
            'hold_offset': {'duration': 400},
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
                #'unit_ramp_100ns': 'unit_ramp_pulse_100ns',
                'unit_ramp_20ns': 'unit_ramp_pulse_20ns',
                #'unit_ramp_1us': 'unit_ramp_pulse_1us',
                'measure': 'measure_pulse',
                'mslice': 'mslice_pulse',
                'measure_tRLFB': 'measure_RLFB_pulse'
                # 'measure_sliced':'measure_sliced_pulse'
            },
            'time_of_flight': 180,
            'smearing': 0,
            'intermediate_frequency': 0,
            # 'thread': 'a'

        },
        
    
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
        

        'Q1': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                'lo_frequency': fLO,
                'mixer': 'mixer_q1'   
            },
            # 'digitalInputs': {
            #     "switch1": {
            #         "port": ("con1", 1),
            #         "delay": 0, #76
            #         "buffer":0,
            #     },
            # },
            'intermediate_frequency': IfQ1,
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
                'cos': "cosine",
                'cos3': "cosine3",
                'cos3rd': "cosine3rd",
                'smooth': "smooth0",
                'smoothR': "smoothR0",
                '-smooth': "-smooth0",
                '-smoothR': "-smoothR0",

            },
        },

        'Q1add': {
            'mixInputs': {

                'I': ('con1', 7),
                'Q': ('con1', 8),
                'lo_frequency': fLO,
                'mixer': 'mixer_q1add'
            },
            'intermediate_frequency': IfQ1,

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
                'cos': "cosine",
                'cos3': "cosine3",
                'cos3rd': "cosine3rd",
            },
        },        
        'Q1pm': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                'lo_frequency': fLO,
                'mixer': 'mixer_q1'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 0,#76,
                    "buffer":0#76
                },
            },
            'intermediate_frequency': IfQ1,
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
                'cos': "cosine",
            },
        },

        'Y1': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                # 'I': ('con1', 8),
                # 'Q': ('con1', 7),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_y1'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 76,
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
                'I': ('con1', 7),
                'Q': ('con1', 8),
                # 'I': ('con1', 8),
                # 'Q': ('con1', 7),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_q2'
            },
            # 'digitalInputs': {
            #     "switch1": {
            #         "port": ("con1", 1),
            #         "delay": 76,
            #         "buffer": 76,
            #     },
            # },
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
        'Q2pm': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                'lo_frequency': fLO,
                'mixer': 'mixer_q2'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 0,#76,
                    "buffer":0#76
                },
            },
            'intermediate_frequency': IfQ2,
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
                'cos': "cosine",
            },
        },
        'Y2': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                # 'I': ('con1', 8),
                # 'Q': ('con1', 7),
                'lo_frequency': fLO,
                # 'intermediate_frequency': IfQ1,
                'mixer': 'mixer_q2'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 76,
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
        'Qoff': {
            'mixInputs': {
                'I': ('con1', 7),
                'Q': ('con1', 8),
                # 'I': ('con1', 8),
                # 'Q': ('con1', 7),
                'lo_frequency': fLO,
                'mixer': 'mixer_offres'
            },
            'digitalInputs': {
                "switch1": {
                    "port": ("con1", 1),
                    "delay": 76,
                    "buffer": 4,
                },
            },
            'intermediate_frequency': IfQoff,
            'operations': {
                'control': 'ESR_const_pulse'
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
        
        'mslice_pulse': {
            'operation': 'measure',
            'length': measurement_length_slice,
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
        'unit_ramp_pulse_20ns': {
        'operation': 'control',
        'length': 20,
        'waveforms': {
            'single': 'unit_ramp_wf_20ns',
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
                'I': 'q1_ctrl_wfx2',
                'Q': 'q1_ctrl_wfx2'
            }
        },
        '-X/2PulseQ1': {
            'operation': 'control',
            'length': tX2Q1,# gauss_len,
            'digital_marker': 'ON',
            'waveforms': {
                # 'I': 'q1_ngauss_wf',
                # 'Q': 'q1_ngauss_wf'
                'I': 'q1_nctrl_wfx2',
                'Q': 'q1_nctrl_wfx2'
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
        'rect_pulse_arb': {
            'operation': 'control',
            'length': len(rect_pulse_arb),
            'waveforms': {
                'single': 'rect_pulse_wf',
            }
        },
        'cosine': {
            'operation': 'control',
            'length': Nt*Tmod,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': 'cosine_mod',
                'Q': 'cosine_mod'
                }
        },
        'cosine3': {
            'operation': 'control',
            'length': Nt*Tmod,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': 'cosine3_mod',
                'Q': 'cosine3_mod'
                }
        },
        'cosine3rd': {
            'operation': 'control',
            'length': Nt*Tmod,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': 'cosine3rd_mod',
                'Q': 'cosine3rd_mod'
                }
        },
        'sineP': {
            'operation': 'control',
            'length': Nt*Tmod,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'single': 'sine_modP',
                }
              },
        
        'cosine2P': {
            'operation': 'control',
            'length': Nt*Tmod,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'single': 'cosine_2modP',
                }
        },
        'smooth0': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': 'smoothwf',
                'Q': 'smoothwf'
                }
        },
        'smoothR0': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': 'smoothRwf',
                'Q': 'smoothRwf'
                }
        },
        '-smooth0': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': '-smoothwf',
                'Q': '-smoothwf'
                }
        },
        '-smoothR0': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'I': '-smoothRwf',
                'Q': '-smoothRwf'
                }
        },
        'smooth0p': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'single': 'smoothwf',
                }
        },
        'smoothR0p': {
            'operation': 'control',
            'length': kk*0.1e3,       #?
            'digital_marker': 'ON', #?
            'waveforms': {
                'single': 'smoothRwf',
                }
        },

        'measure_RLFB_pulse': {
            'operation': 'measure',
            'length': feedback_length,
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
        'q1_ctrl_wfx2': {
            'type': 'constant',
            # 'sample': 0.352 # Should be max amplitude without overflow
            'sample': IQamp_max*IQscalarQ1 # Some margin added to allow for adjustment
        },
        'q1_nctrl_wfx2': {
            'type': 'constant',
            # 'sample': -0.352 # Should be max amplitude without overflow
            'sample': -IQamp_max*IQscalarQ1 # Some margin added to allow for adjustment
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
        
        'rect_pulse_wf':{
            'type':'arbitrary',
            'samples':rect_pulse_arb
            },
        'cosine_mod':{
            'type':'arbitrary',
            'samples':cos_NT,
            # 'maxAllowedError':1e-2
        },  
        'cosine3_mod':{
            'type':'arbitrary',
            'samples':cos3_NT,
            # 'maxAllowedError':1e-2
        },
        'cosine3rd_mod':{
            'type':'arbitrary',
            'samples':cos3rd_NT,
            # 'maxAllowedError':1e-2
        },
        'sine_modP':{
            'type':'arbitrary',
            'samples':sin_NT,
            # 'maxAllowedError':1e-2
        },
        'cosine_2modP':{
            'type':'arbitrary',
            'samples':cos2_NT,
            # 'maxAllowedError':1e-2
        },
        'smoothwf':{
            'type':'arbitrary',
            'samples':smooth,
            # 'maxAllowedError':1e-2
        },
        'smoothRwf':{
            'type':'arbitrary',
            'samples':smoothR,
            # 'maxAllowedError':1e-2
        },
        '-smoothwf':{
            'type':'arbitrary',
            'samples':[-x for x in smooth],
            # 'maxAllowedError':1e-2
        },
        '-smoothRwf':{
            'type':'arbitrary',
            'samples':[-x for x in smoothR],
            # 'maxAllowedError':1e-2
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
        # 'cos_test': {
            # 'cosine': [-1.0]*(measurement_length//4),
            # 'sine': [0.0]*(measurement_length//4)
            # 'cosine': [0.4]*(measurement_length//4),
            # 'sine': [0.0]*(measurement_length//4)
        # },
        # 'sin_test': {
        #     'cosine': [0.0]*(measurement_length//4),
        #     'sine': [0.4]*(measurement_length//4) 
        # },
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
        'mixer_q1add': [
            # {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [0.0, -1.0, 1.0, 0.0]},
            {'intermediate_frequency': IfQ1add, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
        ],
        'mixer_q1pm': [
            # {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [0.0, -1.0, 1.0, 0.0]},
            {'intermediate_frequency': IfQ1add, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
        ],
        'mixer_q1addpm': [
            # {'intermediate_frequency': IfQ1, 'lo_frequency': fLO, 'correction': [0.0, -1.0, 1.0, 0.0]},
            {'intermediate_frequency': IfQ1add, 'lo_frequency': fLO, 'correction': \
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
            {'intermediate_frequency': IfQoff, 'lo_frequency': fLO, 'correction': \
              IQ_imbalance_correction(g, phi)},
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


        
