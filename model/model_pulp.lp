\* Base_model_PuLP *\
Maximize
OBJ: 400 qCrackedOilByProduct_Jet_fuel + 350 qFuelOil
 + 400 qJetFuelBySource_Crude_1_Heavy_oil
 + 400 qJetFuelBySource_Crude_1_Light_oil
 + 400 qJetFuelBySource_Crude_1_Residuum
 + 400 qJetFuelBySource_Crude_2_Heavy_oil
 + 400 qJetFuelBySource_Crude_2_Light_oil
 + 400 qJetFuelBySource_Crude_2_Residuum + 150 qLubeOil
 + 700 qPetrol_Premium_motor_fuel + 600 qPetrol_Regular_motor_fuel
Subject To
conCrackedGasolineByPetrol: - qCrackedGasolineByPetrol_Premium_motor_fuel
 - qCrackedGasolineByPetrol_Regular_motor_fuel
 + 0.2 qCrackingBySource_Crude_1_Heavy_oil
 + 0.28 qCrackingBySource_Crude_1_Light_oil
 + 0.2 qCrackingBySource_Crude_2_Heavy_oil
 + 0.28 qCrackingBySource_Crude_2_Light_oil = 0
conCrackedOilFuelOil: 18 qCrackedOilByProduct_Fuel_oil - 4 qFuelOil = 0
conCrackedOilVolume: - qCrackedOilByProduct_Fuel_oil
 - qCrackedOilByProduct_Jet_fuel + 0.75 qCrackingBySource_Crude_1_Heavy_oil
 + 0.68 qCrackingBySource_Crude_1_Light_oil
 + 0.75 qCrackingBySource_Crude_2_Heavy_oil
 + 0.68 qCrackingBySource_Crude_2_Light_oil = 0
conCrackingAvailable: qCrackingBySource_Crude_1_Heavy_oil
 + qCrackingBySource_Crude_1_Light_oil + qCrackingBySource_Crude_2_Heavy_oil
 + qCrackingBySource_Crude_2_Light_oil <= 8000
conCrudeAvailable_Crude_1: q_Crude_1 <= 20000
conCrudeAvailable_Crude_2: q_Crude_2 <= 30000
conD_Heavy_naphta: qPetrolBySource_Crude_1_Heavy_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_1_Heavy_naphta_Regular_motor_fuel
 + qPetrolBySource_Crude_2_Heavy_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_2_Heavy_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Regular_motor_fuel
 - q_Crude_1_Heavy_naphta - q_Crude_2_Heavy_naphta = 0
conD_Heavy_oil: qCrackingBySource_Crude_1_Heavy_oil
 + qCrackingBySource_Crude_2_Heavy_oil + 0.166666666667 qFuelOil
 + qJetFuelBySource_Crude_1_Heavy_oil + qJetFuelBySource_Crude_2_Heavy_oil
 - q_Crude_1_Heavy_oil - q_Crude_2_Heavy_oil = 0
conD_Light_naphta: qPetrolBySource_Crude_1_Light_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_1_Light_naphta_Regular_motor_fuel
 + qPetrolBySource_Crude_2_Light_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_2_Light_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Light_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Light_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Light_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Light_naphta_Regular_motor_fuel
 - q_Crude_1_Light_naphta - q_Crude_2_Light_naphta = 0
conD_Light_oil: qCrackingBySource_Crude_1_Light_oil
 + qCrackingBySource_Crude_2_Light_oil + 0.555555555556 qFuelOil
 + qJetFuelBySource_Crude_1_Light_oil + qJetFuelBySource_Crude_2_Light_oil
 - q_Crude_1_Light_oil - q_Crude_2_Light_oil = 0
conD_Medium_naphta: qPetrolBySource_Crude_1_Medium_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_1_Medium_naphta_Regular_motor_fuel
 + qPetrolBySource_Crude_2_Medium_naphta_Premium_motor_fuel
 + qPetrolBySource_Crude_2_Medium_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Medium_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Medium_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Medium_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Medium_naphta_Regular_motor_fuel
 - q_Crude_1_Medium_naphta - q_Crude_2_Medium_naphta = 0
conD_Residuum: 0.0555555555556 qFuelOil + qJetFuelBySource_Crude_1_Residuum
 + qJetFuelBySource_Crude_2_Residuum + qLubeOilBySource_Crude_1_Residuum
 + qLubeOilBySource_Crude_2_Residuum - q_Crude_1_Residuum - q_Crude_2_Residuum
 = 0
conDistillationAvailable: q_Crude_1 + q_Crude_2 <= 45000
conLubeOilDomainMax: qLubeOil <= 1000
conLubeOilDomainMin: qLubeOil >= 500
conLubeOil_Residuum: - qLubeOil + 0.5 qLubeOilBySource_Crude_1_Residuum
 + 0.5 qLubeOilBySource_Crude_2_Residuum = 0
conOctanePetrol_Premium_motor_fuel:
 - 11 qCrackedGasolineByPetrol_Premium_motor_fuel
 + 24 qPetrolBySource_Crude_1_Heavy_naphta_Premium_motor_fuel
 + 4 qPetrolBySource_Crude_1_Light_naphta_Premium_motor_fuel
 + 14 qPetrolBySource_Crude_1_Medium_naphta_Premium_motor_fuel
 + 24 qPetrolBySource_Crude_2_Heavy_naphta_Premium_motor_fuel
 + 4 qPetrolBySource_Crude_2_Light_naphta_Premium_motor_fuel
 + 14 qPetrolBySource_Crude_2_Medium_naphta_Premium_motor_fuel
 - 21 qReformedGasoline_Premium_motor_fuel <= 0
conOctanePetrol_Regular_motor_fuel:
 - 21 qCrackedGasolineByPetrol_Regular_motor_fuel
 + 14 qPetrolBySource_Crude_1_Heavy_naphta_Regular_motor_fuel
 - 6 qPetrolBySource_Crude_1_Light_naphta_Regular_motor_fuel
 + 4 qPetrolBySource_Crude_1_Medium_naphta_Regular_motor_fuel
 + 14 qPetrolBySource_Crude_2_Heavy_naphta_Regular_motor_fuel
 - 6 qPetrolBySource_Crude_2_Light_naphta_Regular_motor_fuel
 + 4 qPetrolBySource_Crude_2_Medium_naphta_Regular_motor_fuel
 - 31 qReformedGasoline_Regular_motor_fuel <= 0
conPremiumRegularPetrol: qPetrol_Premium_motor_fuel
 - 0.4 qPetrol_Regular_motor_fuel >= 0
conQD_Crude_1,Heavy_naphta: 0.2 q_Crude_1 - q_Crude_1_Heavy_naphta = 0
conQD_Crude_1,Heavy_oil: 0.2 q_Crude_1 - q_Crude_1_Heavy_oil = 0
conQD_Crude_1,Light_naphta: 0.1 q_Crude_1 - q_Crude_1_Light_naphta = 0
conQD_Crude_1,Light_oil: 0.12 q_Crude_1 - q_Crude_1_Light_oil = 0
conQD_Crude_1,Medium_naphta: 0.2 q_Crude_1 - q_Crude_1_Medium_naphta = 0
conQD_Crude_1,Residuum: 0.13 q_Crude_1 - q_Crude_1_Residuum = 0
conQD_Crude_2,Heavy_naphta: 0.18 q_Crude_2 - q_Crude_2_Heavy_naphta = 0
conQD_Crude_2,Heavy_oil: 0.19 q_Crude_2 - q_Crude_2_Heavy_oil = 0
conQD_Crude_2,Light_naphta: 0.15 q_Crude_2 - q_Crude_2_Light_naphta = 0
conQD_Crude_2,Light_oil: 0.08 q_Crude_2 - q_Crude_2_Light_oil = 0
conQD_Crude_2,Medium_naphta: 0.25 q_Crude_2 - q_Crude_2_Medium_naphta = 0
conQD_Crude_2,Residuum: 0.12 q_Crude_2 - q_Crude_2_Residuum = 0
conQPetrol_Premium_motor_fuel: - qCrackedGasolineByPetrol_Premium_motor_fuel
 - qPetrolBySource_Crude_1_Heavy_naphta_Premium_motor_fuel
 - qPetrolBySource_Crude_1_Light_naphta_Premium_motor_fuel
 - qPetrolBySource_Crude_1_Medium_naphta_Premium_motor_fuel
 - qPetrolBySource_Crude_2_Heavy_naphta_Premium_motor_fuel
 - qPetrolBySource_Crude_2_Light_naphta_Premium_motor_fuel
 - qPetrolBySource_Crude_2_Medium_naphta_Premium_motor_fuel
 + qPetrol_Premium_motor_fuel - qReformedGasoline_Premium_motor_fuel = 0
conQPetrol_Regular_motor_fuel: - qCrackedGasolineByPetrol_Regular_motor_fuel
 - qPetrolBySource_Crude_1_Heavy_naphta_Regular_motor_fuel
 - qPetrolBySource_Crude_1_Light_naphta_Regular_motor_fuel
 - qPetrolBySource_Crude_1_Medium_naphta_Regular_motor_fuel
 - qPetrolBySource_Crude_2_Heavy_naphta_Regular_motor_fuel
 - qPetrolBySource_Crude_2_Light_naphta_Regular_motor_fuel
 - qPetrolBySource_Crude_2_Medium_naphta_Regular_motor_fuel
 + qPetrol_Regular_motor_fuel - qReformedGasoline_Regular_motor_fuel = 0
conReformedAvailable:
 qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Light_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Light_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Medium_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_1_Medium_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Light_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Light_naphta_Regular_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Medium_naphta_Premium_motor_fuel
 + qReformedGasolineByPetrol_Crude_2_Medium_naphta_Regular_motor_fuel <= 10000
conReformedPetrol_Crude_2,Heavy_naphta_Premium_motor_fuel:
 - 0.45 qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Premium_motor_fuel
 - 0.6 qReformedGasolineByPetrol_Crude_1_Light_naphta_Premium_motor_fuel
 - 0.52 qReformedGasolineByPetrol_Crude_1_Medium_naphta_Premium_motor_fuel
 - 0.45 qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Premium_motor_fuel
 - 0.6 qReformedGasolineByPetrol_Crude_2_Light_naphta_Premium_motor_fuel
 - 0.52 qReformedGasolineByPetrol_Crude_2_Medium_naphta_Premium_motor_fuel
 + qReformedGasoline_Premium_motor_fuel = 0
conReformedPetrol_Crude_2,Heavy_naphta_Regular_motor_fuel:
 - 0.45 qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Regular_motor_fuel
 - 0.6 qReformedGasolineByPetrol_Crude_1_Light_naphta_Regular_motor_fuel
 - 0.52 qReformedGasolineByPetrol_Crude_1_Medium_naphta_Regular_motor_fuel
 - 0.45 qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Regular_motor_fuel
 - 0.6 qReformedGasolineByPetrol_Crude_2_Light_naphta_Regular_motor_fuel
 - 0.52 qReformedGasolineByPetrol_Crude_2_Medium_naphta_Regular_motor_fuel
 + qReformedGasoline_Regular_motor_fuel = 0
conVapourJetFuel: 0.5 qCrackedOilByProduct_Jet_fuel
 - 0.4 qJetFuelBySource_Crude_1_Heavy_oil
 - 0.95 qJetFuelBySource_Crude_1_Residuum
 - 0.4 qJetFuelBySource_Crude_2_Heavy_oil
 - 0.95 qJetFuelBySource_Crude_2_Residuum <= 0
Bounds
 0 <= qCrackedGasolineByPetrol_Premium_motor_fuel <= 45000
 0 <= qCrackedGasolineByPetrol_Regular_motor_fuel <= 45000
 0 <= qCrackedOilByProduct_Fuel_oil <= 45000
 0 <= qCrackedOilByProduct_Jet_fuel <= 45000
 0 <= qCrackingBySource_Crude_1_Heavy_oil <= 45000
 0 <= qCrackingBySource_Crude_1_Light_oil <= 45000
 0 <= qCrackingBySource_Crude_2_Heavy_oil <= 45000
 0 <= qCrackingBySource_Crude_2_Light_oil <= 45000
 qFuelOil <= 45000
 0 <= qJetFuelBySource_Crude_1_Heavy_oil <= 45000
 0 <= qJetFuelBySource_Crude_1_Light_oil <= 45000
 0 <= qJetFuelBySource_Crude_1_Residuum <= 45000
 0 <= qJetFuelBySource_Crude_2_Heavy_oil <= 45000
 0 <= qJetFuelBySource_Crude_2_Light_oil <= 45000
 0 <= qJetFuelBySource_Crude_2_Residuum <= 45000
 0 <= qLubeOil <= 45000
 0 <= qLubeOilBySource_Crude_1_Residuum <= 45000
 0 <= qLubeOilBySource_Crude_2_Residuum <= 45000
 0 <= qPetrolBySource_Crude_1_Heavy_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_1_Heavy_naphta_Regular_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_1_Light_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_1_Light_naphta_Regular_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_1_Medium_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_1_Medium_naphta_Regular_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Heavy_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Heavy_naphta_Regular_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Light_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Light_naphta_Regular_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Medium_naphta_Premium_motor_fuel <= 45000
 0 <= qPetrolBySource_Crude_2_Medium_naphta_Regular_motor_fuel <= 45000
 qPetrol_Premium_motor_fuel <= 45000
 qPetrol_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Light_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Light_naphta_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Medium_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_1_Medium_naphta_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Light_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Light_naphta_Regular_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Medium_naphta_Premium_motor_fuel <= 45000
 0 <= qReformedGasolineByPetrol_Crude_2_Medium_naphta_Regular_motor_fuel <= 45000
 qReformedGasoline_Premium_motor_fuel <= 45000
 qReformedGasoline_Regular_motor_fuel <= 45000
 0 <= q_Crude_1 <= 45000
 0 <= q_Crude_1_Heavy_naphta <= 45000
 0 <= q_Crude_1_Heavy_oil <= 45000
 0 <= q_Crude_1_Light_naphta <= 45000
 0 <= q_Crude_1_Light_oil <= 45000
 0 <= q_Crude_1_Medium_naphta <= 45000
 0 <= q_Crude_1_Residuum <= 45000
 0 <= q_Crude_2 <= 45000
 0 <= q_Crude_2_Heavy_naphta <= 45000
 0 <= q_Crude_2_Heavy_oil <= 45000
 0 <= q_Crude_2_Light_naphta <= 45000
 0 <= q_Crude_2_Light_oil <= 45000
 0 <= q_Crude_2_Medium_naphta <= 45000
 0 <= q_Crude_2_Residuum <= 45000
Generals
qCrackedGasolineByPetrol_Premium_motor_fuel
qCrackedGasolineByPetrol_Regular_motor_fuel
qCrackedOilByProduct_Fuel_oil
qCrackedOilByProduct_Jet_fuel
qCrackingBySource_Crude_1_Heavy_oil
qCrackingBySource_Crude_1_Light_oil
qCrackingBySource_Crude_2_Heavy_oil
qCrackingBySource_Crude_2_Light_oil
qJetFuelBySource_Crude_1_Heavy_oil
qJetFuelBySource_Crude_1_Light_oil
qJetFuelBySource_Crude_1_Residuum
qJetFuelBySource_Crude_2_Heavy_oil
qJetFuelBySource_Crude_2_Light_oil
qJetFuelBySource_Crude_2_Residuum
qLubeOil
qLubeOilBySource_Crude_1_Residuum
qLubeOilBySource_Crude_2_Residuum
qPetrolBySource_Crude_1_Heavy_naphta_Premium_motor_fuel
qPetrolBySource_Crude_1_Heavy_naphta_Regular_motor_fuel
qPetrolBySource_Crude_1_Light_naphta_Premium_motor_fuel
qPetrolBySource_Crude_1_Light_naphta_Regular_motor_fuel
qPetrolBySource_Crude_1_Medium_naphta_Premium_motor_fuel
qPetrolBySource_Crude_1_Medium_naphta_Regular_motor_fuel
qPetrolBySource_Crude_2_Heavy_naphta_Premium_motor_fuel
qPetrolBySource_Crude_2_Heavy_naphta_Regular_motor_fuel
qPetrolBySource_Crude_2_Light_naphta_Premium_motor_fuel
qPetrolBySource_Crude_2_Light_naphta_Regular_motor_fuel
qPetrolBySource_Crude_2_Medium_naphta_Premium_motor_fuel
qPetrolBySource_Crude_2_Medium_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_1_Heavy_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_1_Light_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_1_Light_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_1_Medium_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_1_Medium_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_2_Heavy_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_2_Light_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_2_Light_naphta_Regular_motor_fuel
qReformedGasolineByPetrol_Crude_2_Medium_naphta_Premium_motor_fuel
qReformedGasolineByPetrol_Crude_2_Medium_naphta_Regular_motor_fuel
q_Crude_1
q_Crude_1_Heavy_naphta
q_Crude_1_Heavy_oil
q_Crude_1_Light_naphta
q_Crude_1_Light_oil
q_Crude_1_Medium_naphta
q_Crude_1_Residuum
q_Crude_2
q_Crude_2_Heavy_naphta
q_Crude_2_Heavy_oil
q_Crude_2_Light_naphta
q_Crude_2_Light_oil
q_Crude_2_Medium_naphta
q_Crude_2_Residuum
End
