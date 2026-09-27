\* Source Pyomo model name=Base model *\

max 
objProfit:
+700 qPetrol(Premium_motor_fuel)
+600 qPetrol(Regular_motor_fuel)
+400 qJetFuelBySource(Crude_1_Light_oil)
+400 qJetFuelBySource(Crude_1_Heavy_oil)
+400 qJetFuelBySource(Crude_1_Residuum)
+400 qJetFuelBySource(Crude_2_Light_oil)
+400 qJetFuelBySource(Crude_2_Heavy_oil)
+400 qJetFuelBySource(Crude_2_Residuum)
+400 qCrackedOilByProduct(Jet_fuel)
+350 qFuelOil
+150 qLubeOil

s.t.

c_e_conQD(Crude_1_Light_naphta)_:
+0.1 q(Crude_1)
-1 qd(Crude_1_Light_naphta)
= 0

c_e_conQD(Crude_1_Medium_naphta)_:
+0.2 q(Crude_1)
-1 qd(Crude_1_Medium_naphta)
= 0

c_e_conQD(Crude_1_Heavy_naphta)_:
+0.2 q(Crude_1)
-1 qd(Crude_1_Heavy_naphta)
= 0

c_e_conQD(Crude_1_Light_oil)_:
+0.12 q(Crude_1)
-1 qd(Crude_1_Light_oil)
= 0

c_e_conQD(Crude_1_Heavy_oil)_:
+0.2 q(Crude_1)
-1 qd(Crude_1_Heavy_oil)
= 0

c_e_conQD(Crude_1_Residuum)_:
+0.13 q(Crude_1)
-1 qd(Crude_1_Residuum)
= 0

c_e_conQD(Crude_2_Light_naphta)_:
+0.15 q(Crude_2)
-1 qd(Crude_2_Light_naphta)
= 0

c_e_conQD(Crude_2_Medium_naphta)_:
+0.25 q(Crude_2)
-1 qd(Crude_2_Medium_naphta)
= 0

c_e_conQD(Crude_2_Heavy_naphta)_:
+0.18 q(Crude_2)
-1 qd(Crude_2_Heavy_naphta)
= 0

c_e_conQD(Crude_2_Light_oil)_:
+0.08 q(Crude_2)
-1 qd(Crude_2_Light_oil)
= 0

c_e_conQD(Crude_2_Heavy_oil)_:
+0.19 q(Crude_2)
-1 qd(Crude_2_Heavy_oil)
= 0

c_e_conQD(Crude_2_Residuum)_:
+0.12 q(Crude_2)
-1 qd(Crude_2_Residuum)
= 0

c_e_conReformedPetrol(Premium_motor_fuel)_:
+1 qReformedGasoline(Premium_motor_fuel)
-0.6 qReformedGasolineByPetrol(Crude_1_Light_naphta_Premium_motor_fuel)
-0.52 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Premium_motor_fuel)
-0.45 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Premium_motor_fuel)
-0.6 qReformedGasolineByPetrol(Crude_2_Light_naphta_Premium_motor_fuel)
-0.52 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Premium_motor_fuel)
-0.45 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Premium_motor_fuel)
= 0

c_e_conReformedPetrol(Regular_motor_fuel)_:
+1 qReformedGasoline(Regular_motor_fuel)
-0.6 qReformedGasolineByPetrol(Crude_1_Light_naphta_Regular_motor_fuel)
-0.52 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Regular_motor_fuel)
-0.45 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Regular_motor_fuel)
-0.6 qReformedGasolineByPetrol(Crude_2_Light_naphta_Regular_motor_fuel)
-0.52 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Regular_motor_fuel)
-0.45 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Regular_motor_fuel)
= 0

c_e_conCrackedGasolineByPetrol_:
+1 qCrackedGasolineByPetrol(Premium_motor_fuel)
+1 qCrackedGasolineByPetrol(Regular_motor_fuel)
-0.28 qCrackingBySource(Crude_1_Light_oil)
-0.2 qCrackingBySource(Crude_1_Heavy_oil)
-0.28 qCrackingBySource(Crude_2_Light_oil)
-0.2 qCrackingBySource(Crude_2_Heavy_oil)
= 0

c_e_conCrackedOilVolume_:
+1 qCrackedOilByProduct(Jet_fuel)
+1 qCrackedOilByProduct(Fuel_oil)
-0.68 qCrackingBySource(Crude_1_Light_oil)
-0.75 qCrackingBySource(Crude_1_Heavy_oil)
-0.68 qCrackingBySource(Crude_2_Light_oil)
-0.75 qCrackingBySource(Crude_2_Heavy_oil)
= 0

c_e_conQPetrol(Premium_motor_fuel)_:
+1 qPetrol(Premium_motor_fuel)
-1 qReformedGasoline(Premium_motor_fuel)
-1 qCrackedGasolineByPetrol(Premium_motor_fuel)
-1 qPetrolBySource(Crude_1_Light_naphta_Premium_motor_fuel)
-1 qPetrolBySource(Crude_1_Medium_naphta_Premium_motor_fuel)
-1 qPetrolBySource(Crude_1_Heavy_naphta_Premium_motor_fuel)
-1 qPetrolBySource(Crude_2_Light_naphta_Premium_motor_fuel)
-1 qPetrolBySource(Crude_2_Medium_naphta_Premium_motor_fuel)
-1 qPetrolBySource(Crude_2_Heavy_naphta_Premium_motor_fuel)
= 0

c_e_conQPetrol(Regular_motor_fuel)_:
+1 qPetrol(Regular_motor_fuel)
-1 qReformedGasoline(Regular_motor_fuel)
-1 qCrackedGasolineByPetrol(Regular_motor_fuel)
-1 qPetrolBySource(Crude_1_Light_naphta_Regular_motor_fuel)
-1 qPetrolBySource(Crude_1_Medium_naphta_Regular_motor_fuel)
-1 qPetrolBySource(Crude_1_Heavy_naphta_Regular_motor_fuel)
-1 qPetrolBySource(Crude_2_Light_naphta_Regular_motor_fuel)
-1 qPetrolBySource(Crude_2_Medium_naphta_Regular_motor_fuel)
-1 qPetrolBySource(Crude_2_Heavy_naphta_Regular_motor_fuel)
= 0

c_u_conOctanePetrol(Premium_motor_fuel)_:
-21 qReformedGasoline(Premium_motor_fuel)
-11 qCrackedGasolineByPetrol(Premium_motor_fuel)
+4 qPetrolBySource(Crude_1_Light_naphta_Premium_motor_fuel)
+14 qPetrolBySource(Crude_1_Medium_naphta_Premium_motor_fuel)
+24 qPetrolBySource(Crude_1_Heavy_naphta_Premium_motor_fuel)
+4 qPetrolBySource(Crude_2_Light_naphta_Premium_motor_fuel)
+14 qPetrolBySource(Crude_2_Medium_naphta_Premium_motor_fuel)
+24 qPetrolBySource(Crude_2_Heavy_naphta_Premium_motor_fuel)
<= 0

c_u_conOctanePetrol(Regular_motor_fuel)_:
-31 qReformedGasoline(Regular_motor_fuel)
-21 qCrackedGasolineByPetrol(Regular_motor_fuel)
-6 qPetrolBySource(Crude_1_Light_naphta_Regular_motor_fuel)
+4 qPetrolBySource(Crude_1_Medium_naphta_Regular_motor_fuel)
+14 qPetrolBySource(Crude_1_Heavy_naphta_Regular_motor_fuel)
-6 qPetrolBySource(Crude_2_Light_naphta_Regular_motor_fuel)
+4 qPetrolBySource(Crude_2_Medium_naphta_Regular_motor_fuel)
+14 qPetrolBySource(Crude_2_Heavy_naphta_Regular_motor_fuel)
<= 0

c_u_conVapourJetFuel_:
-0.4 qJetFuelBySource(Crude_1_Heavy_oil)
-0.95 qJetFuelBySource(Crude_1_Residuum)
-0.4 qJetFuelBySource(Crude_2_Heavy_oil)
-0.95 qJetFuelBySource(Crude_2_Residuum)
+0.5 qCrackedOilByProduct(Jet_fuel)
<= 0

c_e_conCrackedOilFuelOil_:
+18 qCrackedOilByProduct(Fuel_oil)
-4 qFuelOil
= 0

c_e_conLubeOil(Residuum)_:
-1 qLubeOil
+0.5 qLubeOilBySource(Crude_1_Residuum)
+0.5 qLubeOilBySource(Crude_2_Residuum)
= 0

c_u_conCrudeAvailable(Crude_1)_:
+1 q(Crude_1)
<= 20000

c_u_conCrudeAvailable(Crude_2)_:
+1 q(Crude_2)
<= 30000

c_u_conDistillationAvailable_:
+1 q(Crude_1)
+1 q(Crude_2)
<= 45000

c_u_conReformedAvailable_:
+1 qReformedGasolineByPetrol(Crude_1_Light_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Light_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Light_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Light_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Regular_motor_fuel)
<= 10000

c_u_conCrackingAvailable_:
+1 qCrackingBySource(Crude_1_Light_oil)
+1 qCrackingBySource(Crude_1_Heavy_oil)
+1 qCrackingBySource(Crude_2_Light_oil)
+1 qCrackingBySource(Crude_2_Heavy_oil)
<= 8000

r_l_conLubeOildomain_:
+1 qLubeOil
>= 500

r_u_conLubeOildomain_:
+1 qLubeOil
<= 1000

c_u_conPremiumRegularPetrol_:
-1 qPetrol(Premium_motor_fuel)
+0.4 qPetrol(Regular_motor_fuel)
<= 0

c_e_conD(1)_:
-1 qd(Crude_1_Light_naphta)
-1 qd(Crude_2_Light_naphta)
+1 qReformedGasolineByPetrol(Crude_1_Light_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Light_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Light_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Light_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_1_Light_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_1_Light_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_2_Light_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_2_Light_naphta_Regular_motor_fuel)
= 0

c_e_conD(2)_:
-1 qd(Crude_1_Medium_naphta)
-1 qd(Crude_2_Medium_naphta)
+1 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Medium_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Medium_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_1_Medium_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_1_Medium_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_2_Medium_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_2_Medium_naphta_Regular_motor_fuel)
= 0

c_e_conD(3)_:
-1 qd(Crude_1_Heavy_naphta)
-1 qd(Crude_2_Heavy_naphta)
+1 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Regular_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Premium_motor_fuel)
+1 qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_1_Heavy_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_1_Heavy_naphta_Regular_motor_fuel)
+1 qPetrolBySource(Crude_2_Heavy_naphta_Premium_motor_fuel)
+1 qPetrolBySource(Crude_2_Heavy_naphta_Regular_motor_fuel)
= 0

c_e_conD(4)_:
+1 qJetFuelBySource(Crude_1_Light_oil)
+1 qJetFuelBySource(Crude_2_Light_oil)
+0.5555555555555556 qFuelOil
-1 qd(Crude_1_Light_oil)
-1 qd(Crude_2_Light_oil)
+1 qCrackingBySource(Crude_1_Light_oil)
+1 qCrackingBySource(Crude_2_Light_oil)
= 0

c_e_conD(5)_:
+1 qJetFuelBySource(Crude_1_Heavy_oil)
+1 qJetFuelBySource(Crude_2_Heavy_oil)
+0.16666666666666666 qFuelOil
-1 qd(Crude_1_Heavy_oil)
-1 qd(Crude_2_Heavy_oil)
+1 qCrackingBySource(Crude_1_Heavy_oil)
+1 qCrackingBySource(Crude_2_Heavy_oil)
= 0

c_e_conD(6)_:
+1 qJetFuelBySource(Crude_1_Residuum)
+1 qJetFuelBySource(Crude_2_Residuum)
+0.05555555555555555 qFuelOil
-1 qd(Crude_1_Residuum)
-1 qd(Crude_2_Residuum)
+1 qLubeOilBySource(Crude_1_Residuum)
+1 qLubeOilBySource(Crude_2_Residuum)
= 0

bounds
   0 <= qPetrol(Premium_motor_fuel) <= 45000
   0 <= qPetrol(Regular_motor_fuel) <= 45000
   0 <= qJetFuelBySource(Crude_1_Light_oil) <= 45000
   0 <= qJetFuelBySource(Crude_1_Heavy_oil) <= 45000
   0 <= qJetFuelBySource(Crude_1_Residuum) <= 45000
   0 <= qJetFuelBySource(Crude_2_Light_oil) <= 45000
   0 <= qJetFuelBySource(Crude_2_Heavy_oil) <= 45000
   0 <= qJetFuelBySource(Crude_2_Residuum) <= 45000
   0 <= qCrackedOilByProduct(Jet_fuel) <= 45000
   0 <= qCrackedOilByProduct(Fuel_oil) <= 45000
   0 <= qFuelOil <= 45000
   0 <= qLubeOil <= 45000
   0 <= q(Crude_1) <= 45000
   0 <= q(Crude_2) <= 45000
   0 <= qd(Crude_1_Light_naphta) <= 45000
   0 <= qd(Crude_1_Medium_naphta) <= 45000
   0 <= qd(Crude_1_Heavy_naphta) <= 45000
   0 <= qd(Crude_1_Light_oil) <= 45000
   0 <= qd(Crude_1_Heavy_oil) <= 45000
   0 <= qd(Crude_1_Residuum) <= 45000
   0 <= qd(Crude_2_Light_naphta) <= 45000
   0 <= qd(Crude_2_Medium_naphta) <= 45000
   0 <= qd(Crude_2_Heavy_naphta) <= 45000
   0 <= qd(Crude_2_Light_oil) <= 45000
   0 <= qd(Crude_2_Heavy_oil) <= 45000
   0 <= qd(Crude_2_Residuum) <= 45000
   0 <= qReformedGasoline(Premium_motor_fuel) <= 45000
   0 <= qReformedGasoline(Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Light_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Light_naphta_Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Medium_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Medium_naphta_Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Light_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Light_naphta_Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Medium_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Medium_naphta_Regular_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Premium_motor_fuel) <= 45000
   0 <= qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Regular_motor_fuel) <= 45000
   0 <= qCrackedGasolineByPetrol(Premium_motor_fuel) <= 45000
   0 <= qCrackedGasolineByPetrol(Regular_motor_fuel) <= 45000
   0 <= qCrackingBySource(Crude_1_Light_oil) <= 45000
   0 <= qCrackingBySource(Crude_1_Heavy_oil) <= 45000
   0 <= qCrackingBySource(Crude_2_Light_oil) <= 45000
   0 <= qCrackingBySource(Crude_2_Heavy_oil) <= 45000
   0 <= qPetrolBySource(Crude_1_Light_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_1_Light_naphta_Regular_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_1_Medium_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_1_Medium_naphta_Regular_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_1_Heavy_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_1_Heavy_naphta_Regular_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Light_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Light_naphta_Regular_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Medium_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Medium_naphta_Regular_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Heavy_naphta_Premium_motor_fuel) <= 45000
   0 <= qPetrolBySource(Crude_2_Heavy_naphta_Regular_motor_fuel) <= 45000
   0 <= qLubeOilBySource(Crude_1_Residuum) <= 45000
   0 <= qLubeOilBySource(Crude_2_Residuum) <= 45000
general
  qJetFuelBySource(Crude_1_Light_oil)
  qJetFuelBySource(Crude_1_Heavy_oil)
  qJetFuelBySource(Crude_1_Residuum)
  qJetFuelBySource(Crude_2_Light_oil)
  qJetFuelBySource(Crude_2_Heavy_oil)
  qJetFuelBySource(Crude_2_Residuum)
  qCrackedOilByProduct(Jet_fuel)
  qCrackedOilByProduct(Fuel_oil)
  qLubeOil
  q(Crude_1)
  q(Crude_2)
  qd(Crude_1_Light_naphta)
  qd(Crude_1_Medium_naphta)
  qd(Crude_1_Heavy_naphta)
  qd(Crude_1_Light_oil)
  qd(Crude_1_Heavy_oil)
  qd(Crude_1_Residuum)
  qd(Crude_2_Light_naphta)
  qd(Crude_2_Medium_naphta)
  qd(Crude_2_Heavy_naphta)
  qd(Crude_2_Light_oil)
  qd(Crude_2_Heavy_oil)
  qd(Crude_2_Residuum)
  qReformedGasolineByPetrol(Crude_1_Light_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_1_Light_naphta_Regular_motor_fuel)
  qReformedGasolineByPetrol(Crude_1_Medium_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_1_Medium_naphta_Regular_motor_fuel)
  qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_1_Heavy_naphta_Regular_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Light_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Light_naphta_Regular_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Medium_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Medium_naphta_Regular_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Premium_motor_fuel)
  qReformedGasolineByPetrol(Crude_2_Heavy_naphta_Regular_motor_fuel)
  qCrackedGasolineByPetrol(Premium_motor_fuel)
  qCrackedGasolineByPetrol(Regular_motor_fuel)
  qCrackingBySource(Crude_1_Light_oil)
  qCrackingBySource(Crude_1_Heavy_oil)
  qCrackingBySource(Crude_2_Light_oil)
  qCrackingBySource(Crude_2_Heavy_oil)
  qPetrolBySource(Crude_1_Light_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_1_Light_naphta_Regular_motor_fuel)
  qPetrolBySource(Crude_1_Medium_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_1_Medium_naphta_Regular_motor_fuel)
  qPetrolBySource(Crude_1_Heavy_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_1_Heavy_naphta_Regular_motor_fuel)
  qPetrolBySource(Crude_2_Light_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_2_Light_naphta_Regular_motor_fuel)
  qPetrolBySource(Crude_2_Medium_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_2_Medium_naphta_Regular_motor_fuel)
  qPetrolBySource(Crude_2_Heavy_naphta_Premium_motor_fuel)
  qPetrolBySource(Crude_2_Heavy_naphta_Regular_motor_fuel)
  qLubeOilBySource(Crude_1_Residuum)
  qLubeOilBySource(Crude_2_Residuum)
end
