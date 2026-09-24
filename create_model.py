import pyomo.environ as pyo
import init_model


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

    def exprReformedPetrol(model, p):
        return sum([model.qReformedGasolineByPetrol[s, r, p] * reforming[r] for s in S for r in R])
    model.qReformedGasoline = pyo.Expression(P, rule=exprReformedPetrol)

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

    def exprQPetrol_rule(model, p):
        return sum([model.qPetrolBySource[s, occ, p] for occ in OCC for s in S]) + model.qReformedGasoline[p] + model.qCrackedGasolineByPetrol[p]
    model.qPetrol = pyo.Expression(P, rule=exprQPetrol_rule)

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
