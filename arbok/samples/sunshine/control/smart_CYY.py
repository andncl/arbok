        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        play('control'*amp(1), 'Q1',duration=seq.tRabi)        
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        

        nn = declare(int)

        amp1=(seq.alpha)*(seq.starkAmp)-(seq.beta)*(seq.starkAmp)
        amp2=(seq.alpha)*(seq.starkAmp)+(seq.beta)*(seq.starkAmp)
        #amp1=(seq.alpha)*(seq.starkAmp1)-(seq.beta)*(seq.starkAmp2)
        #amp2=(seq.alpha)*(seq.starkAmp1)+(seq.beta)*(seq.starkAmp2)
        
        play('smooth'*amp(0), 'P2_not_sticky')
        play('smooth'*amp(1.45), 'Q1')
        # SMART 1/2 SWAP
        with strict_timing_():                
            align('Q1','J1')
            wait(seq.tWait,'J1')
            play('cos', 'Q1')
            play('unit_ramp_20ns'*amp(-seq.vControl2_J1+seq.vControlsqrtSWAP),
                  'J1', duration=tControlRamp)
            wait(seq.tsqrtSWAP, 'J1')
            play('unit_ramp_20ns'*amp(+seq.vControl2_J1-seq.vControlsqrtSWAP),
                  'J1', duration=tControlRamp)
                       
            
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')

        # SMART Y-gate
        with for_(nn, 0, nn < seq.rep, nn+1):
            play('sine'*amp(amp1), 'P2_not_sticky')
            play('cos', 'Q1')
                
        # SMART SWAP
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        with strict_timing_():                
            align('Q1','J1')
            wait(seq.tWait,'J1')
            play('cos', 'Q1')
            play('unit_ramp_20ns'*amp(-seq.vControl2_J1+seq.vControlSWAP),
                  'J1', duration=tControlRamp)
            wait(seq.tSWAP, 'J1')
            play('unit_ramp_20ns'*amp(+seq.vControl2_J1-seq.vControlSWAP),
                  'J1', duration=tControlRamp)
            
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        
        
        # SMART +Y-gate
        nn = declare(int)
        with for_(nn, 0, nn < seq.rep, nn+1):
            play('sine'*amp(amp2), 'P2_not_sticky')
            play('cos', 'Q1')

        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')
        
        
        # SMART 3/2 SWAP
        with strict_timing_():
            align('Q1','J1')
            wait(seq.tWait,'J1')
            play('cos', 'Q1')
            play('unit_ramp_20ns'*amp(-seq.vControl2_J1+seq.vControlSWAP),
                  'J1', duration=tControlRamp)
            wait(seq.tSWAP23, 'J1')
            play('unit_ramp_20ns'*amp(+seq.vControl2_J1-seq.vControlSWAP),
                  'J1', duration=tControlRamp)
            

           
        play('smoothR'*amp(0), 'P2_not_sticky')
        play('smoothR'*amp(1.45), 'Q1')
        
        align('Q1','P1','P2','J1','P2_not_sticky','P1_not_sticky','J1_not_sticky')