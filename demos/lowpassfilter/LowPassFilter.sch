<Qucs Schematic 0.0.19>
<Properties>
  <View=11,49,1304,1369,1,40,240>
  <Grid=10,10,1>
  <DataSet=LowPassFilter.dat>
  <DataDisplay=LowPassFilter.dpl>
  <OpenDisplay=1>
  <Script=LowPassFilter.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <L LS2 1 680 330 10 -26 0 1 "Ls" 1 "" 0>
  <L LS3 1 1000 330 10 -26 0 1 "Ls" 1 "" 0>
  <L LS1 1 320 330 10 -26 0 1 "Ls" 1 "" 0>
  <GND * 1 320 420 0 0 0 0>
  <GND * 1 680 420 0 0 0 0>
  <GND * 1 1000 420 0 0 0 0>
  <L L2 1 490 80 -26 10 0 0 "20 nH" 1 "" 0>
  <L L4 1 790 80 -26 10 0 0 "20 nH" 1 "" 0>
  <R RSC1 1 320 390 15 -26 0 1 "Rsc" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RSC2 1 680 390 15 -26 0 1 "Rsc" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RSC3 1 1000 390 15 -26 0 1 "Rsc" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RP1 1 380 270 15 -26 0 1 "Rp" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RP2 1 740 270 15 -26 0 1 "Rp" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RP3 1 1060 270 15 -26 0 1 "Rp" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <C CP1 1 530 140 -26 17 0 0 "Cp" 1 "" 0 "neutral" 0>
  <C CP2 1 830 140 -26 17 0 0 "Cp" 1 "" 0 "neutral" 0>
  <R RSL1 1 570 80 -26 15 0 0 "Rsl" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R RSL2 1 870 80 -26 15 0 0 "Rsl" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <GND * 1 120 420 0 0 0 0>
  <GND * 1 1180 420 0 0 0 0>
  <C C1 1 260 270 17 -26 0 1 "9.1pF" 1 "" 0 "neutral" 0>
  <C C5 1 940 270 17 -26 0 1 "9.1pF" 1 "" 0 "neutral" 0>
  <C C3 1 620 270 17 -26 0 1 "13 pF" 1 "" 0 "neutral" 0>
  <Eqn DefaultValues 1 120 690 -31 19 0 0 "Rsl=0" 1 "Rp=10000M" 1 "Rsc=0" 1 "Ls=0" 1 "Cp=0" 1 "yes" 0>
  <Pac P1 1 120 290 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P2 1 1180 290 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn dB 1 120 570 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
  <.SP SP1 1 430 610 0 77 0 0 "lin" 1 "0 MHz" 1 "600 MHz" 1 "101" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
</Components>
<Wires>
  <260 300 320 300 "" 0 0 0 "">
  <320 300 380 300 "" 0 0 0 "">
  <620 300 680 300 "" 0 0 0 "">
  <680 300 740 300 "" 0 0 0 "">
  <940 300 1000 300 "" 0 0 0 "">
  <1000 300 1060 300 "" 0 0 0 "">
  <520 80 540 80 "" 0 0 0 "">
  <820 80 840 80 "" 0 0 0 "">
  <460 80 460 110 "" 0 0 0 "">
  <460 140 500 140 "" 0 0 0 "">
  <560 140 600 140 "" 0 0 0 "">
  <600 80 600 110 "" 0 0 0 "">
  <760 80 760 110 "" 0 0 0 "">
  <760 140 800 140 "" 0 0 0 "">
  <860 140 900 140 "" 0 0 0 "">
  <900 80 900 110 "" 0 0 0 "">
  <260 240 320 240 "" 0 0 0 "">
  <620 240 680 240 "" 0 0 0 "">
  <940 240 1000 240 "" 0 0 0 "">
  <320 240 380 240 "" 0 0 0 "">
  <320 110 320 240 "" 0 0 0 "">
  <460 110 460 140 "" 0 0 0 "">
  <320 110 460 110 "" 0 0 0 "">
  <600 110 600 140 "" 0 0 0 "">
  <760 110 760 140 "" 0 0 0 "">
  <600 110 680 110 "" 0 0 0 "">
  <680 110 760 110 "" 0 0 0 "">
  <680 240 740 240 "" 0 0 0 "">
  <680 110 680 240 "" 0 0 0 "">
  <1000 240 1060 240 "" 0 0 0 "">
  <1000 110 1000 240 "" 0 0 0 "">
  <900 110 900 140 "" 0 0 0 "">
  <900 110 1000 110 "" 0 0 0 "">
  <120 320 120 420 "" 0 0 0 "">
  <120 110 120 260 "" 0 0 0 "">
  <120 110 320 110 "" 0 0 0 "">
  <1180 320 1180 420 "" 0 0 0 "">
  <1000 110 1180 110 "" 0 0 0 "">
  <1180 110 1180 260 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 710 1285 543 415 3 #c0c0c0 1 00 1 0 5e+07 6e+08 0 -2 0.25 0 1 -1 0.2 1 315 0 225 "" "" "">
	<"dBS21" #0000ff 0 3 0 0 0>
  </Rect>
  <Rect 90 1285 543 415 3 #c0c0c0 1 00 1 0 5e+07 6e+08 0 0 0.2 1 1 -1 0.2 1 315 0 225 "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>