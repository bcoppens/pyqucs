<Qucs Schematic 0.0.19>
<Properties>
  <View=0,-20,1213,852,1,0,0>
  <Grid=10,10,1>
  <DataSet=FMHighPass.dat>
  <DataDisplay=FMHighPass.dpl>
  <OpenDisplay=1>
  <Script=FMHighPass.m>
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
  <Pac P1 1 170 420 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 170 450 0 0 0 0>
  <L L1 1 280 420 17 -26 0 1 "40.56 nH" 1 "" 0>
  <GND * 1 280 450 0 0 0 0>
  <L L2 1 420 420 17 -26 0 1 "25.31 nH" 1 "" 0>
  <GND * 1 420 450 0 0 0 0>
  <L L3 1 560 420 17 -26 0 1 "24.58 nH" 1 "" 0>
  <GND * 1 560 450 0 0 0 0>
  <L L4 1 700 420 17 -26 0 1 "24.58 nH" 1 "" 0>
  <GND * 1 700 450 0 0 0 0>
  <L L5 1 840 420 17 -26 0 1 "25.31 nH" 1 "" 0>
  <GND * 1 840 450 0 0 0 0>
  <L L6 1 980 420 17 -26 0 1 "40.56 nH" 1 "" 0>
  <GND * 1 980 450 0 0 0 0>
  <Pac P2 1 1090 420 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 1 1090 450 0 0 0 0>
  <.SP SP1 1 180 520 0 77 0 0 "log" 1 "50MHz" 1 "170MHz" 1 "201" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Eqn Eqn1 1 400 530 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
  <C C1 1 350 340 -27 10 0 0 "18.37 pF" 1 "" 0 "neutral" 0>
  <C C2 1 490 340 -27 10 0 0 "16.82 pF" 1 "" 0 "neutral" 0>
  <C C3 1 630 340 -27 10 0 0 "16.65 pF" 1 "" 0 "neutral" 0>
  <C C4 1 770 340 -27 10 0 0 "16.82 pF" 1 "" 0 "neutral" 0>
  <C C5 1 910 340 -27 10 0 0 "18.37 pF" 1 "" 0 "neutral" 0>
</Components>
<Wires>
  <170 340 170 390 "" 0 0 0 "">
  <170 340 280 340 "" 0 0 0 "">
  <280 340 280 390 "" 0 0 0 "">
  <420 340 420 390 "" 0 0 0 "">
  <560 340 560 390 "" 0 0 0 "">
  <700 340 700 390 "" 0 0 0 "">
  <840 340 840 390 "" 0 0 0 "">
  <980 340 980 390 "" 0 0 0 "">
  <280 340 320 340 "" 0 0 0 "">
  <380 340 420 340 "" 0 0 0 "">
  <420 340 460 340 "" 0 0 0 "">
  <520 340 560 340 "" 0 0 0 "">
  <560 340 600 340 "" 0 0 0 "">
  <660 340 700 340 "" 0 0 0 "">
  <700 340 740 340 "" 0 0 0 "">
  <800 340 840 340 "" 0 0 0 "">
  <840 340 880 340 "" 0 0 0 "">
  <940 340 980 340 "" 0 0 0 "">
  <1090 340 1090 390 "" 0 0 0 "">
  <980 340 1090 340 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
  <Text 510 520 12 #000000 0 "Chebyshev high-pass filter \n 130MHz cutoff, pi-type, \n impedance matching 50 Ohm">
</Paintings>
