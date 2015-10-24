<Qucs Schematic 0.0.19>
<Properties>
  <View=11,20,1304,1765,1,40,0>
  <Grid=10,10,1>
  <DataSet=LowPassFilterOriginal.dat>
  <DataDisplay=LowPassFilterOriginal.dpl>
  <OpenDisplay=1>
  <Script=LowPassFilterOriginal.m>
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
  <GND * 1 320 420 0 0 0 0>
  <GND * 1 680 420 0 0 0 0>
  <GND * 1 1000 420 0 0 0 0>
  <GND * 1 120 420 0 0 0 0>
  <GND * 1 1180 420 0 0 0 0>
  <Pac P1 1 120 290 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Pac P2 1 1180 290 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn dB 1 120 570 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
  <.SP SP1 1 430 610 0 77 0 0 "lin" 1 "0 MHz" 1 "2GHz" 1 "201" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <L L2 1 490 110 -26 10 0 0 "21 nH" 1 "" 0>
  <C C3 1 680 270 17 -26 0 1 "14.3 pF" 1 "" 0 "neutral" 0>
  <L L4 1 790 110 -26 10 0 0 "21 nH" 1 "" 0>
  <C C5 1 1000 270 17 -26 0 1 "9 pF" 1 "" 0 "neutral" 0>
  <C C1 1 320 270 17 -26 0 1 "9 pF" 1 "" 0 "neutral" 0>
</Components>
<Wires>
  <120 320 120 420 "" 0 0 0 "">
  <120 110 120 260 "" 0 0 0 "">
  <120 110 320 110 "" 0 0 0 "">
  <1180 320 1180 420 "" 0 0 0 "">
  <1000 110 1180 110 "" 0 0 0 "">
  <1180 110 1180 260 "" 0 0 0 "">
  <320 110 320 240 "" 0 0 0 "">
  <320 300 320 420 "" 0 0 0 "">
  <520 110 680 110 "" 0 0 0 "">
  <320 110 460 110 "" 0 0 0 "">
  <680 110 680 240 "" 0 0 0 "">
  <680 300 680 420 "" 0 0 0 "">
  <820 110 1000 110 "" 0 0 0 "">
  <680 110 760 110 "" 0 0 0 "">
  <1000 110 1000 240 "" 0 0 0 "">
  <1000 300 1000 420 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 710 1285 543 415 3 #c0c0c0 1 00 1 0 5e+07 6e+08 0 -2 0.25 0 1 -1 0.2 1 315 0 225 "" "" "">
	<"dBS21" #0000ff 0 3 0 0 0>
  </Rect>
  <Rect 90 1285 543 415 3 #c0c0c0 1 00 1 0 5e+07 6e+08 0 0 0.2 1 1 -1 0.2 1 315 0 225 "" "" "">
	<"S[1,1]" #0000ff 0 3 0 0 0>
  </Rect>
  <Rect 710 1745 543 415 3 #c0c0c0 1 00 1 0 2e+08 2e+09 0 -60 10 0 1 -1 0.2 1 315 0 225 "" "" "">
	<"dBS21" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
