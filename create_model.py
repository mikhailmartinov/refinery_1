import pyomo.environ as pyo
import pulp as pl


def create_model(distillation, reforming, cracking, lubeOilProduction, octane, octanePetrol, vapourPressure,
                 fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax, crackingOilMax,
                 lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit):
    """
    Постановка задачи переработки сырой нефти на НПЗ
    :return: model - Модель типа pyomo
    """
    model = pyo.ConcreteModel("Base model")

    Q = q
    Dmax = distillationMax
    RFmax = reformingNaphtaMax
    CRmax = crackingOilMax
    profit = profit

    PRmin = premiumPetrolByRegularMin

    q_max = distillationMax
    JFvapour = jetFuleVapour

    distillation = distillation
    S = list(distillation.keys())
    D = list(distillation[S[0]].keys())

    octanePetrol = octanePetrol
    P = list(octanePetrol.keys())

    octane = octane
    OC = list(octane.keys())

    VP = list(vapourPressure.keys())

    # FO = list(fuelOilBlending.keys())

    reforming = reforming
    R = list(reforming.keys())

    cracking = cracking
    CR = list(cracking.keys())

    COU = crackedOilUsing

    LO = list(lubeOilProduction.keys())

    LOmin, LOmax = lubeOilMin, lubeOilMax

    # Объемы нефти на входе в НПЗ обоих типов
    # Прямая перегонка - Distillation
    model.q = pyo.Var(S, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qd = pyo.Var(S, D, bounds=(0, q_max), within=pyo.NonNegativeIntegers)

    def conQD_rule(model, s, d):
        return model.q[s] * distillation[s][d] == model.qd[s, d]
    model.conQD = pyo.Constraint(S, D, rule=conQD_rule)

    # Риформинг - Reforming
    model.qReformedGasolineByPetrol = pyo.Var(S, R, P, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qReformedGasoline = pyo.Var(P, bounds=(0, q_max), within=pyo.NonNegativeReals)

    def conReformedPetrol_rule(model, p):
        return model.qReformedGasoline[p] == sum([model.qReformedGasolineByPetrol[s, r, p] * reforming[r]
                                                  for s in S for r in R])
    model.conReformedPetrol = pyo.Constraint(P, rule=conReformedPetrol_rule)

    # def exprReformedPetrol(model, p):
    #     return sum([model.qReformedGasolineByPetrol[s, r, p] * reforming[r] for s in S for r in R])
    # model.qReformedGasoline = pyo.Expression(P, rule=exprReformedPetrol)

    # Крекинг - Cracking
    model.qCrackingBySource = pyo.Var(S, CR, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qCrackedOil = pyo.Expression(expr=sum([model.qCrackingBySource[s, cr] * cracking[cr]["Cracked oil"]
                                                 for s in S for cr in CR]))
    model.qCrackedGasoline = pyo.Expression(expr=sum([model.qCrackingBySource[s, cr] * cracking[cr]["Cracked gasoline"]
                                                      for s in S for cr in CR]))
    model.qCrackedGasolineByPetrol = pyo.Var(P, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.conCrackedGasolineByPetrol = pyo.Constraint(
        expr=sum([model.qCrackedGasolineByPetrol[p] for p in P]) == model.qCrackedGasoline)

    model.qCrackedOilByProduct = pyo.Var(COU, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.conCrackedOilVolume = pyo.Constraint(
        expr=sum([model.qCrackedOilByProduct[cou] for cou in COU]) == model.qCrackedOil)

    # Блендинг бензина
    OCC = [oc for oc in OC if oc not in ["Reformed gasoline", "Cracked gasoline"]]
    model.qPetrolBySource = pyo.Var(S, OCC, P, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qPetrol = pyo.Var(P, bounds=(0, q_max), within=pyo.NonNegativeReals)

    def conQPetrol_rule(model, p):
        return (model.qPetrol[p] == sum([model.qPetrolBySource[s, occ, p] for occ in OCC for s in S]) +
                model.qReformedGasoline[p] + model.qCrackedGasolineByPetrol[p])
    model.conQPetrol = pyo.Constraint(P, rule=conQPetrol_rule)

    # def exprQPetrol_rule(model, p):
    #     return sum([model.qPetrolBySource[s, occ, p] for occ in OCC for s in S]) + model.qReformedGasoline[p] + model.qCrackedGasolineByPetrol[p]
    # model.qPetrol = pyo.Expression(P, rule=exprQPetrol_rule)

    # octaneMin, octaneMax = min(octane.values()), max(octane.values())
    # model.octanePetrol = pyo.Var(P, bounds=(octaneMin, octaneMax), within=pyo.NonNegativeReals)
    #
    # def conOctanePetrol_rule(model, p):
    #     return (sum([model.qPetrolBySource[s, occ, p] * octane[occ] for occ in OCC for s in S]) +
    #             model.qReformedGasoline[p] * octane["Reformed gasoline"] +
    #             model.qCrackedGasolineByPetrol[p] * octane["Cracked gasoline"] == model.qPetrol[p] * model.octanePetrol[p])
    # model.conOctanePetrol = pyo.Constraint(P, rule=conOctanePetrol_rule)
    #
    # model.conOctanePetrolByProduct = pyo.Constraint(P,
    #                                                 rule=lambda model, p: model.octanePetrol[p] >= octanePetrol[p])

    def conOctanePetrol_rule(model, p):
        return (sum([model.qPetrolBySource[s, occ, p] * (octanePetrol[p] - octane[occ]) for occ in OCC for s in S]) +
                model.qReformedGasoline[p] * (octanePetrol[p] - octane["Reformed gasoline"]) +
                model.qCrackedGasolineByPetrol[p] * (octanePetrol[p] - octane["Cracked gasoline"]) <= 0)
    model.conOctanePetrol = pyo.Constraint(P, rule=conOctanePetrol_rule)

    # Объемы компаундирования для производства реактивного топлива "Jet fuel"
    VPC = [vp for vp in VP if vp != "Cracked oil"]
    model.qJetFuelBySource = pyo.Var(S, VPC, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qJetFuel = pyo.Expression(expr=sum([model.qJetFuelBySource[s, vpc] for vpc in VPC for s in S]) +
                                         model.qCrackedOilByProduct["Jet fuel"])

    # vapourMin, vapourMax = min(vapourPressure.values()), max(vapourPressure.values())
    # model.vapourJetFuel = pyo.Var(bounds=(vapourMin, vapourMax), within=pyo.NonNegativeReals)
    # def conVapourJetFuel_rule(model):
    #     return (sum([model.qJetFuelBySource[s, vpc] * vapourPressure[vpc] for vpc in VPC for s in S]) +
    #             model.qCrackedOilByProduct["Jet fuel"] * vapourPressure[
    #                 "Cracked oil"] == model.qJetFuel * model.vapourJetFuel)
    # model.conVapourJetFuel = pyo.Constraint(rule=conVapourJetFuel_rule)
    #
    # model.conVapourJetFuelRef = pyo.Constraint(expr=model.vapourJetFuel <= JFvapour)

    def conVapourJetFuel_rule(model):
        return (sum([model.qJetFuelBySource[s, vpc] * (vapourPressure[vpc] - JFvapour) for vpc in VPC for s in S]) +
                model.qCrackedOilByProduct["Jet fuel"] * (vapourPressure["Cracked oil"] - JFvapour) <= 0)
    model.conVapourJetFuel = pyo.Constraint(rule=conVapourJetFuel_rule)

    # Объемы компаундирования для производства мазута "Fuel oil"
    fuelOilBlendingSum = sum(fuelOilBlending.values())

    # FOC = [fo for fo in FO if fo != "Cracked oil"]
    # model.qFuelOilBySource = pyo.Var(S, FOC, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    # model.qFuelOil = pyo.Expression(expr=(sum([model.qFuelOilBySource[s, foc] for foc in FOC for s in S])
    #                                       + model.qCrackedOilByProduct["Fuel oil"]))
    #
    # def conFuelOil_rule(model, fo):
    #     if not fo == "Cracked oil":
    #         return (model.qFuelOil * fuelOilBlending[fo] ==
    #                 sum([model.qFuelOilBySource[s, fo] for s in S]) * fuelOilBlendingSum)
    #     else:
    #         return (model.qFuelOil * fuelOilBlending["Cracked oil"] ==
    #                 model.qCrackedOilByProduct["Fuel oil"] * fuelOilBlendingSum)
    # model.conFuelOil = pyo.Constraint(FO, rule=conFuelOil_rule)

    model.qFuelOil = pyo.Var(bounds=(0, q_max), within=pyo.NonNegativeReals)
    model.conCrackedOilFuelOil = pyo.Constraint(expr=model.qCrackedOilByProduct["Fuel oil"] * fuelOilBlendingSum ==
                                                     model.qFuelOil * fuelOilBlending["Cracked oil"])
    # FOC = [fo for fo in FO if fo not in ["Cracked oil"]]
    # fuelOilCrackedOilShare = 1 - sum([round(fuelOilBlending[foc] / fuelOilBlendingSum, 2) for foc in FOC])
    # model.conCrackedOilFuelOil = pyo.Constraint(expr=model.qCrackedOilByProduct["Fuel oil"] ==
    #                                                  model.qFuelOil * fuelOilCrackedOilShare)

    # Производство битума
    model.qLubeOilBySource = pyo.Var(S, LO, bounds=(0, q_max), within=pyo.NonNegativeIntegers)
    model.qLubeOil = pyo.Var(bounds=(0, q_max), within=pyo.NonNegativeIntegers)

    def conLubeOil_rule(model, lo):
        return sum([model.qLubeOilBySource[s, lo] for s in S]) * lubeOilProduction[lo] == model.qLubeOil
    model.conLubeOil = pyo.Constraint(LO, rule=conLubeOil_rule)

    # Доступность сырья
    model.conCrudeAvailable = pyo.Constraint(S, rule=lambda model, s: model.q[s] <= Q[s])

    # Доступность для прямой перегонки
    model.conDistillationAvailable = pyo.Constraint(expr=sum([model.q[s] for s in S]) <= Dmax)

    # Доступность для риформинга
    def conReformedAvailable_rule(model):
        return sum([model.qReformedGasolineByPetrol[s, r, p] for s in S for r in R for p in P]) <= RFmax
    model.conReformedAvailable = pyo.Constraint(rule=conReformedAvailable_rule)

    # Доступность для крекинга
    def conCrackingAvailable_rule(model):
        return sum([model.qCrackingBySource[s, cr] for s in S for cr in CR]) <= CRmax
    model.conCrackingAvailable = pyo.Constraint(rule=conCrackingAvailable_rule)

    # Выход битума
    model.conLubeOildomain = pyo.Constraint(expr=(LOmin, model.qLubeOil, LOmax))

    # Выход Премиум бензина относительно Регуляр
    model.conPremiumRegularPetrol = pyo.Constraint(expr=model.qPetrol["Premium motor fuel"] >=
                                                        PRmin * model.qPetrol["Regular motor fuel"])

    # Выходы после прямой перегонки
    model.conD = pyo.ConstraintList()
    for d in D:
        if d in ["Light naphta", "Medium naphta", "Heavy naphta"]:
            model.conD.add(expr=sum(model.qPetrolBySource[s, d, p] for s in S for p in P) +
                                sum(model.qReformedGasolineByPetrol[s, d, p] for s in S for p in P) ==
                                sum(model.qd[s, d] for s in S)
                           )
        elif d in ["Light oil", "Heavy oil"]:
            model.conD.add(expr=sum(model.qCrackingBySource[s, d] for s in S) +
                                sum(model.qJetFuelBySource[s, d] for s in S) +
                                # model.qFuelOil * round(fuelOilBlending[d] / fuelOilBlendingSum, 2) ==
                                model.qFuelOil * fuelOilBlending[d] / fuelOilBlendingSum ==
                                # sum(model.qFuelOilBySource[s, d] for s in S) ==
                                sum(model.qd[s, d] for s in S)
                           )
        elif d == "Residuum":
            model.conD.add(expr=sum(model.qJetFuelBySource[s, d] for s in S) +
                                # model.qFuelOil * round(fuelOilBlending[d] / fuelOilBlendingSum, 2) +
                                model.qFuelOil * fuelOilBlending[d] / fuelOilBlendingSum +
                                # sum(model.qFuelOilBySource[s, d] for s in S) +
                                sum(model.qLubeOilBySource[s, d] for s in S) ==
                                sum(model.qd[s, d] for s in S)
                           )

    # Целевая - выручка
    model.objProfit = pyo.Objective(expr=model.qPetrol["Premium motor fuel"] * profit["Premium motor fuel"] +
                                         model.qPetrol["Regular motor fuel"] * profit["Regular motor fuel"] +
                                         model.qJetFuel * profit["Jet fuel"] +
                                         model.qFuelOil * profit["Fuel oil"] +
                                         model.qLubeOil * profit["Lube oil"],
                                    sense=pyo.maximize
                                    )

    return model


def create_modelPuLP(distillation, reforming, cracking, lubeOilProduction, octane, octanePetrol, vapourPressure,
                     fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax, crackingOilMax,
                     lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit, tradeData):
    """
    Постановка задачи переработки сырой нефти на НПЗ
    :return: model - Модель типа pulp
    """
    model = pl.LpProblem("Base model PuLP", pl.LpMaximize)

    Q = q
    Dmax = distillationMax
    RFmax = reformingNaphtaMax
    CRmax = crackingOilMax
    profit = profit

    PRmin = premiumPetrolByRegularMin

    q_max = distillationMax
    JFvapour = jetFuleVapour

    distillation = distillation
    S = list(distillation.keys())
    D = list(distillation[S[0]].keys())

    octanePetrol = octanePetrol
    P = list(octanePetrol.keys())

    octane = octane
    OC = list(octane.keys())

    VP = list(vapourPressure.keys())

    # FO = list(fuelOilBlending.keys())

    reforming = reforming
    R = list(reforming.keys())

    cracking = cracking
    CR = list(cracking.keys())

    COU = crackedOilUsing

    LO = list(lubeOilProduction.keys())

    LOmin, LOmax = lubeOilMin, lubeOilMax

    q, qd = dict(), dict()
    qReformedGasoline, qReformedGasolineByPetrol = dict(), dict()
    qCrackingBySource, qCrackedGasolineByPetrol, qCrackedOilByProduct = dict(), dict(), dict()
    qPetrol, qPetrolBySource = dict(), dict()
    qJetFuelBySource = dict()
    qLubeOilBySource = dict()

    # Объемы нефти на входе в НПЗ обоих типов
    # Прямая перегонка - Distillation
    for s in S:
        q[s] = pl.LpVariable(f"q_{s}", lowBound=0, upBound=q_max, cat=pl.LpInteger)
        for d in D:
            qd[s, d] = pl.LpVariable(f"q_{s}_{d}", lowBound=0, upBound=q_max, cat=pl.LpInteger)
            model += q[s] * distillation[s][d] == qd[s, d], f"conQD_{s},{d}"

    # Риформинг - Reforming
    for p in P:
        qReformedGasoline[p] = pl.LpVariable(f"qReformedGasoline_{p}", lowBound=0, upBound=q_max, cat=pl.LpContinuous)
        for s in S:
            for r in R:
                qReformedGasolineByPetrol[s, r, p] = pl.LpVariable(f"qReformedGasolineByPetrol_{s}_{r}_{p}",
                                                                   lowBound=0, upBound=q_max, cat=pl.LpInteger)

    for p in P:
        model += (qReformedGasoline[p] == sum([qReformedGasolineByPetrol[s, r, p] * reforming[r] for s in S for r in R]),
                  f"conReformedPetrol_{s},{r}_{p}")

    # Крекинг - Cracking
    for s in S:
        for cr in CR:
            qCrackingBySource[s, cr] = pl.LpVariable(f"qCrackingBySource_{s}_{cr}",
                                                               lowBound=0, upBound=q_max, cat=pl.LpInteger)
    qCrackedOil = pl.lpSum([qCrackingBySource[s, cr] * cracking[cr]["Cracked oil"]
                            for s in S for cr in CR])
    qCrackedGasoline = pl.lpSum([qCrackingBySource[s, cr] * cracking[cr]["Cracked gasoline"]
                                 for s in S for cr in CR])
    for p in P:
        qCrackedGasolineByPetrol[p] = pl.LpVariable(f"qCrackedGasolineByPetrol_{p}",
                                                    lowBound=0, upBound=q_max, cat=pl.LpInteger)
    model += qCrackedGasoline == sum([qCrackedGasolineByPetrol[p] for p in P]), f"conCrackedGasolineByPetrol"

    for cou in COU:
        qCrackedOilByProduct[cou] = pl.LpVariable(f"qCrackedOilByProduct_{cou}",
                                                  lowBound=0, upBound=q_max, cat=pl.LpInteger)
    model += qCrackedOil == sum([qCrackedOilByProduct[cou] for cou in COU]), f"conCrackedOilVolume"

    # Блендинг бензина
    OCC = [oc for oc in OC if oc not in ["Reformed gasoline", "Cracked gasoline"]]

    for p in P:
        qPetrol[p] = pl.LpVariable(f"qPetrol_{p}",
                                   lowBound=0, upBound=q_max, cat=pl.LpContinuous)
        for s in S:
            for occ in OCC:
                qPetrolBySource[s, occ, p] = pl.LpVariable(f"qPetrolBySource_{s}_{occ}_{p}",
                                                           lowBound=0, upBound=q_max, cat=pl.LpInteger)

    for p in P:
        model += (qPetrol[p] == sum([qPetrolBySource[s, occ, p] for occ in OCC for s in S]) + qReformedGasoline[p] +
                  qCrackedGasolineByPetrol[p],
                  f"conQPetrol_{p}")
        model += (sum([qPetrolBySource[s, occ, p] * (octanePetrol[p] - octane[occ]) for occ in OCC for s in S]) +
                  qReformedGasoline[p] * (octanePetrol[p] - octane["Reformed gasoline"]) +
                  qCrackedGasolineByPetrol[p] * (octanePetrol[p] - octane["Cracked gasoline"]) <= 0,
                  f"conOctanePetrol_{p}")

    # Объемы компаундирования для производства реактивного топлива "Jet fuel"
    VPC = [vp for vp in VP if vp != "Cracked oil"]
    for s in S:
        for vpc in VPC:
            qJetFuelBySource[s, vpc] = pl.LpVariable(f"qJetFuelBySource_{s}_{vpc}",
                                                     lowBound=0, upBound=q_max, cat=pl.LpInteger)
    qJetFuel = pl.lpSum([qJetFuelBySource[s, vpc] for vpc in VPC for s in S]) + qCrackedOilByProduct["Jet fuel"]

    model += (sum([qJetFuelBySource[s, vpc] * (vapourPressure[vpc] - JFvapour) for vpc in VPC for s in S]) +
              qCrackedOilByProduct["Jet fuel"] * (vapourPressure["Cracked oil"] - JFvapour) <= 0, f"conVapourJetFuel")

    # Объемы компаундирования для производства мазута "Fuel oil"
    fuelOilBlendingSum = sum(fuelOilBlending.values())

    qFuelOil = pl.LpVariable(f"qFuelOil", lowBound=0, upBound=q_max, cat=pl.LpContinuous)

    model += (qCrackedOilByProduct["Fuel oil"] * fuelOilBlendingSum == qFuelOil * fuelOilBlending["Cracked oil"],
              f"conCrackedOilFuelOil")

    # Производство битума
    for s in S:
        for lo in LO:
            qLubeOilBySource[s, lo] = pl.LpVariable(f"qLubeOilBySource_{s}_{lo}",
                                                    lowBound=0, upBound=q_max, cat=pl.LpInteger)
    qLubeOil = pl.LpVariable(f"qLubeOil", lowBound=0, upBound=q_max, cat=pl.LpInteger)

    for lo in LO:
        model += sum([qLubeOilBySource[s, lo] for s in S]) * lubeOilProduction[lo] == qLubeOil, f"conLubeOil_{lo}"

    # Доступность сырья
    for s in S:
        model += q[s] <= Q[s], f"conCrudeAvailable_{s}"

    # Доступность для прямой перегонки
    model += sum([q[s] for s in S]) <= Dmax, f"conDistillationAvailable"

    # Доступность для риформинга
    model += (sum([qReformedGasolineByPetrol[s, r, p] for s in S for r in R for p in P]) <= RFmax,
              f"conReformedAvailable")

    # Доступность для крекинга
    model += sum([qCrackingBySource[s, cr] for s in S for cr in CR]) <= CRmax, f"conCrackingAvailable"

    # Выход битума
    model += qLubeOil <= LOmax, f"conLubeOilDomainMax"
    model += qLubeOil >= LOmin, f"conLubeOilDomainMin"

    # Выход Премиум бензина относительно Регуляр
    model += qPetrol["Premium motor fuel"] >= PRmin * qPetrol["Regular motor fuel"], f"conPremiumRegularPetrol"

    # Выходы после прямой перегонки
    for d in D:
        if d in ["Light naphta", "Medium naphta", "Heavy naphta"]:
            model += (sum(qPetrolBySource[s, d, p] for s in S for p in P) +
                      sum(qReformedGasolineByPetrol[s, d, p] for s in S for p in P) ==
                      sum(qd[s, d] for s in S),
                      f"conD_{d}")
        elif d in ["Light oil", "Heavy oil"]:
            model += (sum(qCrackingBySource[s, d] for s in S) +
                      sum(qJetFuelBySource[s, d] for s in S) +
                      qFuelOil * fuelOilBlending[d] / fuelOilBlendingSum ==
                      sum(qd[s, d] for s in S),
                      f"conD_{d}")
        elif d == "Residuum":
            model += (sum(qJetFuelBySource[s, d] for s in S) +
                      qFuelOil * fuelOilBlending[d] / fuelOilBlendingSum +
                      sum(qLubeOilBySource[s, d] for s in S) ==
                      sum(qd[s, d] for s in S),
                      f"conD_{d}")

    qPetrolTrade, qPetrolRetail, qPetrolB = dict(), dict(), dict()
    for p in P:
        qPetrolTrade[p] = pl.LpVariable(f"qPetrolTrade_{p}", lowBound=0, upBound=q_max,
                                        cat=pl.LpContinuous)
        qPetrolRetail[p] = pl.LpVariable(f"qPetrolRetail_{p}", lowBound=0, upBound=q_max,
                                         cat=pl.LpContinuous)
        qPetrolB[p] = pl.LpVariable(f"qPetrolB_{p}", cat=pl.LpBinary)

        model += qPetrolRetail[p] + qPetrolTrade[p] == qPetrol[p], f"conPetrolRetailTrade_{p}"

        model += qPetrolRetail[p] >= qPetrolB[p] * tradeData[p]["tradeVol"], f"conPetrolRetailVolMin_{p}"
        model += qPetrolRetail[p] <= tradeData[p]["tradeVol"], f"conPetrolRetailVolMax_{p}"

        model += qPetrolTrade[p] >= qPetrolB[p] * tradeData[p]["tradeVol"], f"conPetrolTradeVolMin_{p}"
        model += qPetrolTrade[p] <= qPetrolB[p] * q_max, f"conPetrolTradeVolMax_{p}"

    # Целевая - выручка
    # model += (qPetrol["Premium motor fuel"] * profit["Premium motor fuel"] +
    #           qPetrol["Regular motor fuel"] * profit["Regular motor fuel"] +
    #           qJetFuel * profit["Jet fuel"] +
    #           qFuelOil * profit["Fuel oil"] +
    #           qLubeOil * profit["Lube oil"])
    model += (qPetrolRetail["Premium motor fuel"] * profit["Premium motor fuel"] +
              qPetrolTrade["Premium motor fuel"] * tradeData["Premium motor fuel"]["tradePrice"] +
              qPetrolRetail["Regular motor fuel"] * profit["Regular motor fuel"] +
              qPetrolTrade["Regular motor fuel"] * tradeData["Regular motor fuel"]["tradePrice"] +
              qJetFuel * profit["Jet fuel"] +
              qFuelOil * profit["Fuel oil"] +
              qLubeOil * profit["Lube oil"])

    return (model, q, qd ,qReformedGasoline, qReformedGasolineByPetrol, qCrackingBySource, qCrackedGasolineByPetrol,
            qCrackedOilByProduct, qPetrol, qPetrolBySource, qJetFuelBySource, qLubeOilBySource,
            qJetFuel, qFuelOil, qLubeOil, qCrackedOil, qCrackedGasoline)
