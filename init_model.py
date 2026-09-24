import json
import pandas as pd


calcMode = "real"  # "real" "int"

distillation = {
    "Crude 1": {
        "Light naphta": 0.1,
        "Medium naphta": 0.2,
        "Heavy naphta": 0.2,
        "Light oil": 0.12,
        "Heavy oil": 0.2,
        "Residuum": 0.13
    },
    "Crude 2": {
        "Light naphta": 0.15,
        "Medium naphta": 0.25,
        "Heavy naphta": 0.18,
        "Light oil": 0.08,
        "Heavy oil": 0.19,
        "Residuum": 0.12
    }
}

octane = {
    "Light naphta": 90,
    "Medium naphta": 80,
    "Heavy naphta": 70,
    "Reformed gasoline": 115,
    "Cracked gasoline": 105
}

reforming = {
    "Light naphta": 0.6,
    "Medium naphta": 0.52,
    "Heavy naphta": 0.45
}

cracking = {
    "Light oil": {"Cracked oil": 0.68, "Cracked gasoline": 0.28},
    "Heavy oil": {"Cracked oil": 0.75, "Cracked gasoline": 0.2}
}

residuum_by_lube_oil = {"Residuum": {"Lube oil": 0.5}}
octanePetrol = {"Regular": 84, "Premium": 94}

vapour_pressure = {"Light oil": 1.0, "Heavy oil": 0.6, "Cracked oil": 1.5, "Residuum": 0.05}

fuel_oil_blending = {"Light oil": 10, "Cracked oil": 4, "Heavy oil": 3, "Residuum": 1}

lube_oil_production = {"Residuum": 0.5}

q = {"Crude 1": 20_000, "Crude 2": 30_000}

crackedOilUsing = ["Jet fuel", "Fuel oil"]

jet_fule_vapour = 1.0
premium_regular_petrol = 0.4
distillation_max = 45_000
reforming_oil_max = 10_000
cracking_oil_max = 8_000
lube_oil_min, lube_oil_max = 500, 1000

# Premium motor fuel production must be at least 40% of regular motor fuel production

profit = {"Premium": 700, "Regular": 600, "Jet fuel": 400, "Fuel oil": 350, "Lube oil": 150}
profit = {k: int(v/100) for k, v in profit.items()}


def initModel(fnm):
    """
    Функция инициализации исходных данных задачи
    :param fnm: Имя файла с исходными данными
    :return:
    """
    with open(fnm, "r", encoding="utf-8") as f:
        initDataJson = json.load(f)

    raws = initDataJson["products"]["raws"]
    intermediateProducts = initDataJson["products"]["intermediateProducts"]
    finalProducts = initDataJson["products"]["finalProducts"]
    products = {**raws, **intermediateProducts, **finalProducts}

    distillationJson = initDataJson["processes"]["distillation"]
    distillation = dict()
    for dsJ in distillationJson:
        rawName = products[dsJ["rawId"]]
        outputFractionByProductsName = {products[k]: v for k, v in dsJ["outputFraction"].items()}
        distillation[rawName] = outputFractionByProductsName

    reformingYieldFraction = initDataJson["processes"]["reforming"]["yieldFraction"]
    reforming = {products[k]: v for k, v in reformingYieldFraction.items()}

    crackingJson = initDataJson["processes"]["cracking"]
    cracking = dict()
    for crJ in crackingJson:
        rawName = products[crJ["rawId"]]
        yieldFractionByProductsName = {products[k]: v for k, v in crJ["yieldFraction"].items()}
        cracking[rawName] = yieldFractionByProductsName

    lubeOilJson = initDataJson["processes"]["lubeOilProduction"]
    lubeOilProduction = {products[lubeOilJson["intermediateProductId"]]: lubeOilJson["yieldFraction"]}

    blendingPetrolsJson = initDataJson["processes"]["blending"]["petrols"]
    octane = {products[k]: v for k, v in blendingPetrolsJson["octaneNumberIngredients"].items()}
    octanePetrol = {products[k]: v for k, v in blendingPetrolsJson["finalProductsOctaneNumber"].items()}

    blendingJetFuelJson = initDataJson["processes"]["blending"]["jetFuel"]
    vapourPressure = {products[k]: v for k, v in blendingJetFuelJson["vapourPressureIngredients"].items()}

    blendingFuelOilJson = initDataJson["processes"]["blending"]["fuelOil"]
    fuelOilBlending = {products[k]: v for k, v in blendingFuelOilJson["shareIngredients"].items()}

    crackedOilUsing = []
    crackedOilName = "Cracked oil"
    if crackedOilName in vapourPressure.keys():
        crackedOilUsing.append("Jet fuel")
    if crackedOilName in fuelOilBlending.keys():
        crackedOilUsing.append("Fuel oil")

    paramsJson = initDataJson["params"]
    q = {products[k]: v for k, v in paramsJson["rawsAvailable"].items()}
    distillationMax = paramsJson["distillationMax"]
    reformingNaphtaMax = paramsJson["reformingNaphtaMax"]
    crackingOilMax = paramsJson["crackingOilMax"]
    lubeOilMin, lubeOilMax = paramsJson["lubeOil"]["min"], paramsJson["lubeOil"]["max"]
    jetFuleVapour = paramsJson["jetFuelVapour"]
    premiumPetrolByRegularMin = paramsJson["premiumPetrolByRegularMin"]
    profit = {products[k]: v for k, v in paramsJson["profit"].items()}
    profit = {k: int(v/100) for k, v in profit.items()}

    distillationD2 = {"Сырье": []}
    for k, v in distillation.items():
        distillationD2["Сырье"].append(k)
        for k2, v2 in v.items():
            if not k2 in distillationD2.keys():
                distillationD2[k2] = [v2]
            else:
                distillationD2[k2].append(v2)
    distillationDf = pd.DataFrame.from_dict(distillationD2)

    reformingD2 = {"Сырье": [], "Выход Reformed gasoline": []}
    for k, v in reforming.items():
        reformingD2["Сырье"].append(k)
        reformingD2["Выход Reformed gasoline"].append(v)
    reformingDf = pd.DataFrame.from_dict(reformingD2)

    crackingD2 = {"Сырье": [], "Выход Cracked gasoline": [], "Выход Cracked oil": []}
    for k, v in cracking.items():
        crackingD2["Сырье"].append(k)
        crackingD2["Выход Cracked gasoline"].append(v["Cracked gasoline"])
        crackingD2["Выход Cracked oil"].append(v["Cracked oil"])
    crackingDf = pd.DataFrame.from_dict(crackingD2)

    octaneD2 = {"Продукт": list(octane.keys()), "Октановое число": list(octane.values())}
    octanePetrolD2 = {"Продукт": list(octanePetrol.keys()), "Октановое число": list(octanePetrol.values())}
    octaneDf = pd.DataFrame.from_dict(octaneD2)
    octanePetrolDf = pd.DataFrame.from_dict(octanePetrolD2)

    vapourPressureD2 = {"Продукт": list(vapourPressure.keys()),
                        "Давление насыщенных паров": list(vapourPressure.values())}
    vapourPressureDf = pd.DataFrame.from_dict(vapourPressureD2)

    fuelOilBlendingD2 = {"Продукт": list(fuelOilBlending.keys()),
                         "Доля": list(fuelOilBlending.values())}
    fuelOilBlendingDf = pd.DataFrame.from_dict(fuelOilBlendingD2)

    return (raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking, lubeOilProduction,
            octane, octanePetrol, vapourPressure,
            fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax, crackingOilMax,
            lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
            distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf, vapourPressureDf, fuelOilBlendingDf)
