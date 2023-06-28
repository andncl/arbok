def initMixed(
    delta,
    tramp,
    tInitLoadMixed,
    vInitPreLoadMixed1,
    tInitPreLoad,
    tInitPreLoadRamp,
    tControl,
    tInitLoadRamp,
    vInitMixed2,
    tPreControl,
    vHome0,
    vLoadMixed1
):
 
    align()
    play('unit_ramp_20ns'*amp(vInitPreLoadMixed1[0] - Home0[0]),
         'P1',duration=tInitLoadRamp)
    play('unit_ramp_20ns'*amp(vInitPreLoadMixed1[2] - vHome0[2]),
         'P2',duration=tInitLoadRamp)
    align()
    play('unit_ramp_20ns'*amp(vInitPreLoadMixed1[1] -vHome0[1]),
         'J1',duration=tInitLoadRamp)
    align()
    wait(tInitLoadMixed)
    
    align()
    play('unit_ramp_20ns'*amp(-vInitPreLoadMixed1[1] + vLoadMixed1[1]),
         'J1', duration=tInitLoadRamp)

    align()
    play('unit_ramp_20ns'*amp(-vInitPreLoadMixed1[0] + vLoadMixed1[0]),
         'P1', duration=tramp)
    play('unit_ramp_20ns'*amp(-vInitPreLoadMixed1[2] + vLoadMixed1[2]),
         'P2', duration=tramp)

    align()  
    play('unit_ramp_20ns'*amp(vHome0[0]- vLoadMixed1[0]),
         'P1',duration=tInitLoadRamp)
    play('unit_ramp_20ns'*amp(vHome0[1]- vLoadMixed1[1]),
         'J1',duration=tInitLoadRamp)
    play('unit_ramp_20ns'*amp(vHome0[2]- vLoadMixed1[2]),
         'P2',duration=tInitLoadRamp)
    align()