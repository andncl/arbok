from qm.qua import *
from Configuration import *
from PulseSequence import PulseSequence

class GeneralMeasurement_1Q(PulseSequence):

    def __init__(self,parent):
        super().__init__(parent)
        
        self.dummy = int(0)
        self.vPreRead_P1 = float(vPreRead[0])
        self.vPreRead_J1 = float(vPreRead[1])
        self.vPreRead_P2 = float(vPreRead[2])
        self.vRead_P1 = float(vRead[0])
        self.vRead_J1 = float(vRead[1])
        self.vRead_P2 = float(vRead[2])
        
        self.vHome1 = float(vHome[0])
        self.vHome2 = float(vHome[1])
        self.vHome3 = float(vHome[2])
        self.vHome4 = float(vHome[3])
        # self.vHome5 = float(vHome[4])
        
        self.vLoadMixed11 = float(vLoadMixed1[0])
        self.vLoadMixed12 = float(vLoadMixed1[1])
        self.vLoadMixed13 = float(vLoadMixed1[2])

        self.tReadRamp = int(tReadRamp)
        self.tPreRead = int(tPreRead)
        self.tPostRead = int(tPostRead)
        self.tPreReadRef = int(tPreReadRef)
        self.tPostReadRef = int(tPostReadRef)
        self.tPreReadRef2 = int(tPreReadRef2)
        self.tPostReadRef2 = int(tPostReadRef2)
        self.tPreReadPoint = int(tPreReadPoint)
        self.tPreReadRamp = int(tPreReadRamp)
        self.tReadReferenceRamp = int(tReadReferenceRamp)
        
        self.vPreFeedback1 = float(vPreFeedback[0])
        self.vPreFeedback2 = float(vPreFeedback[1])
        self.vPreFeedback3 = float(vPreFeedback[2])

        self.vFeedback1 = float(vFeedback[0])
        self.vFeedback2 = float(vFeedback[1])
        self.vFeedback3 = float(vFeedback[2])        
        
        self.vReference1 = float(vReadReference[0])
        self.vReference2 = float(vReadReference[1])
        self.vReference3 = float(vReadReference[2])
        self.tReadReferenceRamp = int(tReadReferenceRamp)
        
        self.vDeltaM1 = float(vDeltaM[0])
        self.vDeltaM2 = float(vDeltaM[1])
        self.vDeltaM3 = float(vDeltaM[2])

        self.tPreControlRampMixed = int(tPreControlRampMixed)
        self.tInitLoadMixed = int(tInitLoadMixed)
        self.vInitPreLoadMixed11 = float(vInitPreLoadMixed1[0])
        self.vInitPreLoadMixed12 = float(vInitPreLoadMixed1[1])
        self.vInitPreLoadMixed13 = float(vInitPreLoadMixed1[2])
        self.tInitPreLoad = int(tInitPreLoad)
        self.tControl = int(tControl)
        self.tInitLoadRamp = int(tInitLoadRamp)
        self.vInitMixed21 = float(vInitMixed2[0])
        self.vInitMixed22 = float(vInitMixed2[1])
        self.vInitMixed23 = float(vInitMixed2[2])
        self.tPreControl = int(tPreControl)
        self.tInitPreLoadRamp = int(tInitPreLoadRamp)
        
        self.tWait = self.control.tWait
        self.tESRchirp = int(tESRchirp)
        
        self.vInitPreLoadTminus1 = float(vInitPreLoadTminus[0])
        self.vInitPreLoadTminus2 = float(vInitPreLoadTminus[1])
        self.vInitPreLoadTminus3 = float(vInitPreLoadTminus[2])
        self.vDelta1 = float(vDelta[0])
        self.vDelta2 = float(vDelta[1])
        self.vDelta3 = float(vDelta[2])
        self.tPreControlRampTminus = int(tPreControlRampTminus)
        self.tInitLoadTMinus = int(tInitLoadTMinus)
        self.tInitPreLoad = int(tInitPreLoad)
        self.tInitPreLoadRamp = int(tInitPreLoadRamp)
        self.vInitMixed1 = float(vInitMixed[0])
        self.vInitMixed2 = float(vInitMixed[1])
        self.vInitMixed3 = float(vInitMixed[2])
        
        self.fESR = int(IfQ1)
        self.vControl_P1 = float(vControl[0])
        self.vControl_J1 = float(vControl[1])
        self.vControl_P2 = float(vControl[2])
        self.vControl_J2 = float(vControl[3])
        # self.vControl_P3 = float(vControl[4])
        
        self.vControl2_P1 = float(vControl2[0])
        # self.vControl2_J1 = float(self.control.vControl2_J1) #float(vControl2[1])
        self.vControl2_J1 = float(vControl2[1])
        self.vControl2_P2 = float(vControl2[2])
        self.vControl2_J2 = float(vControl2[3])
        # self.vControl2_P3 = float(vControl2[4])
        
        self.vControl3_P1 = float(vControl3[0])
        self.vControl3_J1 = float(vControl3[1])
        self.vControl3_P2 = float(vControl3[2])
        self.vControl3_J2 = float(vControl3[3])
        # self.vControl3_P3 = float(vControl3[4])
        
        self.tPreControl = int(tPreControl)
        self.tPostControl = int(tPostControl)
        self.tControlRamp = int(tControlRamp)
        self.theta= self.control.theta

        self.piBefore = self.control.piBefore
        self.piAfter = self.control.piAfter        
        self.rep = self.control.rep

        self.starkAmp = self.control.starkAmp
        self.starkAmp1 = self.control.starkAmp1
        self.starkAmp2 = self.control.starkAmp2
        self.beta=self.control.beta
        self.alpha=self.control.alpha

        self.fESR = self.control.fESR
        self.fESRcos = self.control.fESRcos
        self.tRabi = self.control.tRabi
        self.tpiontwo = self.control.tpiontwo
        self.tpi = self.control.tpi
        self.modAmp = self.control.modAmp
        self.reps = self.control.reps
        self.rabiAmp = self.control.rabiAmp
        self.rabiAmp1 = self.control.rabiAmp1
        self.rabiAmp2 = self.control.rabiAmp2

        self.amp = self.control.amp
        self.chirp_rate = self.control.chirp_rate  # MHz/sec

        self.frameRot = self.control.frameRot
        self.timeScalar = self.control.timeScalar
        self.tPulseMod = self.control.tPulseMod
        self.tJ = self.control.tJ
        self.Tmod = self.control.Tmod
        # self.warmAmp = float(warmAmp)
        # self.warmT = int(warmT)
        self.preWait = self.control.preWait
        self.RamseyPhase = self.control.RamseyPhase
        self.TM = self.control.TM
        
        self.vControlSWAP = self.control.vControlSWAP
        self.vControlsqrtSWAP = self.control.vControlsqrtSWAP
        self.tSWAP = self.control.tSWAP
        self.tSWAP23 = self.control.tSWAP23

        self.tsqrtSWAP = self.control.tsqrtSWAP


    def run_seq(self):    
        reset_phase('Q1')
        reset_frame('Q1')
        reset_phase('Q1pm')
        reset_frame('Q1pm')
        # reset_phase('Q1add')
        # reset_frame('Q1add')
           
        align()
        update_frequency('Q1',self.fESR)
        update_frequency('Q1pm',self.fESR)
        align()
        goHome([self.vHome1,self.vHome2,self.vHome3,self.vHome4])
        align()
        
        ## Init ----------------------------------------------------------------------------------------------------------------------------   
        with if_(self.TM==0):
            initMixed(
                delta = [self.vDeltaM1,self.vDeltaM2,self.vDeltaM3],
                tramp = self.tPreControlRampMixed,
                tInitLoadMixed=self.tInitLoadMixed,
                vInitPreLoadMixed1 = [
                    self.vInitPreLoadMixed11,
                    self.vInitPreLoadMixed12,
                    self.vInitPreLoadMixed13
                    ],
                tInitPreLoad=tInitPreLoad,
                tInitPreLoadRamp=self.tInitPreLoadRamp,
                tControl=self.tControl,
                tInitLoadRamp=self.tInitLoadRamp,
                vInitMixed2=[
                    self.vInitMixed21,
                    self.vInitMixed22,
                    self.vInitMixed23
                    ],
                tPreControl=self.tPreControl,
                vHome0=[self.vHome1,self.vHome2,self.vHome3,self.vHome4],
                vLoadMixed1=[
                    self.vLoadMixed11,
                    self.vLoadMixed12,
                    self.vLoadMixed13
                    ]
            )
            
        with else_():
            initTMinus(
                vInitPreLoadTminus=[
                    self.vInitPreLoadTminus1,
                    self.vInitPreLoadTminus2,
                    self.vInitPreLoadTminus3
                    ],
                delta = [self.vDelta1,self.vDelta2,self.vDelta3],
                tramp=self.tPreControlRampTminus,
                tInitLoadTMinus=self.tInitLoadTMinus,
                tInitPreLoad=self.tInitPreLoad,
                tInitPreLoadRamp=self.tInitPreLoadRamp,
                tControl=self.tControl,
                tInitLoadRamp=self.tInitLoadRamp,
                tPreControl=self.tPreControl,
                vInitMixed=[
                    self.vInitMixed1,
                    self.vInitMixed2,
                    self.vInitMixed3
                    ],
                vHome0=[
                    self.vHome1,
                    self.vHome2,
                    self.vHome3
                    ])
            
            # nn = declare(int)
            # with for_(nn, 0, nn < 0.4*1e5, nn+1):
            #     play('control'*amp(0),'Q1',duration=int(10e3/4))                                    
        # ## Control -------------------------------------------------------------------
        align()

        toControlPoint(
            [
                self.vControl2_P1,
                 self.vControl2_J1,
                 self.vControl2_P2,
                 self.vControl2_J2
             ],
            tControlRamp=self.tControlRamp,
            fast = False,
            vHome0=[self.vHome1,self.vHome2,self.vHome3,self.vHome4]
            )
        align()
        
        
        play('control'*amp(0), 'Q1pm',duration=self.tPulseMod)

        wait(self.tPreControl)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        self.control.runControl(self)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPostControl)
  
    
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        fromControlPoint(
            [
                self.vControl2_P1,self.vControl2_J1,
                self.vControl2_P2,self.vControl2_J2
            ],
            tControlRamp=self.tControlRamp,
            fast = False,
            vHome0=[self.vHome1,self.vHome2,self.vHome3,self.vHome4]
            )
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')

        wait(self.tPostControl)


        # # ## Read reference ---------------------------------------------------------------------         
   
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        play('unit_ramp_20ns'*amp(self.vReference1 - self.vHome1),GA,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(self.vReference2 - self.vHome2),GC,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(self.vReference3 - self.vHome3),GB,duration=self.tReadReferenceRamp)
           
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPreRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        ref2.measureAndSave()
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
         
        play('unit_ramp_20ns'*amp(-self.vReference1 + self.vHome1),GA,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-self.vReference2 + self.vHome2),GC,duration=self.tReadReferenceRamp)
        play('unit_ramp_20ns'*amp(-self.vReference3 + self.vHome3),GB,duration=self.tReadReferenceRamp)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
            
        ## ---------------------------------  ONLY FOR RLFB TESTER --------------------------
        # play('unit_ramp'*amp(self.vPreFeedback1 - self.vHome1),'P1',duration = self.tPreReadRamp)
        # play('unit_ramp'*amp(self.vPreFeedback2 - self.vHome2),'J1',duration = self.tPreReadRamp)
        # play('unit_ramp'*amp(self.vPreFeedback3 - self.vHome3),'P2',duration = self.tPreReadRamp)
        # align('Q1','P1','P2','J1','P3','P2')
        # wait(int(100e3/4))
        # align('Q1','P1','P2','J1','P3','P2')
        
        ## Read-out ---------------------------------------------------------------------------
        
        # play('unit_ramp'*amp(self.vPreRead_P1 - self.vPreFeedback1),'P1',duration = self.tPreReadRamp)
        # play('unit_ramp'*amp(self.vPreRead_J1 - self.vPreFeedback2),'J1',duration = self.tPreReadRamp)
        # play('unit_ramp'*amp(self.vPreRead_P2 - self.vPreFeedback3),'P2',duration = self.tPreReadRamp)
         
        play('unit_ramp_20ns'*amp(self.vPreRead_P1 - self.vHome1),'P1',duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vPreRead_J1 - self.vHome2),'J1',duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vPreRead_P2 - self.vHome3),'P2',duration = self.tPreReadRamp)
           
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPreReadPoint)
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
           
        play('unit_ramp_20ns'*amp(self.vRead_P1 - self.vPreRead_P1),'P1',duration = self.tReadRamp)
        play('unit_ramp_20ns'*amp(self.vRead_J1 - self.vPreRead_J1),'J1',duration = self.tReadRamp)
        play('unit_ramp_20ns'*amp(self.vRead_P2 - self.vPreRead_P2),'P2',duration = self.tReadRamp)
                  
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPreRead,'SDC')       
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        read.measureAndSave() 
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
        wait(self.tPostRead,'SDC')
        align('Q1','J1','Q1add','P1','P2','J2','P1_not_sticky','P2_not_sticky','Qoff','J1_not_sticky')
         
        play('unit_ramp_20ns'*amp(self.vHome1-self.vRead_P1),'P1')#,duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vHome2-self.vRead_J1),'J1')#,duration = self.tPreReadRamp)
        play('unit_ramp_20ns'*amp(self.vHome3-self.vRead_P2),'P2')#,duration = self.tPreReadRamp)

        align()
                     
        setVars.feedback_SSR(ref2.read,set_pt=SETFB_DCsetpt, fb_gate='SDC', gain = SETFB_DCalpha)

        resetChannels()
        diff.takeDiff(read, ref2)