<Qucs Schematic 0.0.19>
<Properties>
  <View=0,180,1195,1172,1,0,0>
  <Grid=10,10,1>
  <DataSet=VoltageDivider.dat>
  <DataDisplay=VoltageDivider.dpl>
  <OpenDisplay=1>
  <Script=VoltageDivider.m>
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
  <Vdc V1 1 380 350 -69 -26 0 1 "10 V" 1>
  <GND * 1 380 380 0 0 0 0>
  <GND * 1 540 380 0 0 0 0>
  <R R1 1 460 320 -34 -67 0 0 "35 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <R R2 1 540 350 15 -26 0 1 "35 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <.DC DC1 1 470 550 0 46 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <Eqn Rin 1 490 880 -31 19 0 0 "Rin=-10/V1.I" 1 "yes" 0>
</Components>
<Wires>
  <380 320 430 320 "" 0 0 0 "">
  <490 320 540 320 "" 0 0 0 "">
  <540 320 640 320 "" 0 0 0 "">
  <640 320 640 320 "Vout" 670 290 0 "">
</Wires>
<Diagrams>
  <Tab 460 830 300 200 3 #c0c0c0 1 00 1 0 1 1 1 0 1 1 1 0 1 1 315 0 225 "" "" "">
	<"Vout.V" #0000ff 0 3 1 0 0>
	<"Rin" #0000ff 0 3 1 0 0>
  </Tab>
</Diagrams>
<Paintings>
</Paintings>
