import json
import os
import sys
import re
from datetime import datetime
import subprocess
import streamlit as st
import streamlit.components.v1 as components
import pyomo.environ as pyo
import pulp as pl

from millifyNumber import millify
import init_model
import create_model
import draw_flow

curDir = os.getcwd()
solverPathExeChoice = {
    "cbc": os.path.join(curDir, "solvers/cbc/cbc_2.10.12/bin/cbc.exe"),
    "glpk": os.path.join(curDir, "solvers/glpk/glpk-4.65/w64/glpsol.exe"),
}
sys.path.append(solverPathExeChoice["cbc"])
solverNames = list(solverPathExeChoice.keys())

curDir = os.getcwd()
dirData = os.path.join(curDir, "data/")
dirResults = os.path.join(curDir, "results/")
dirModel = os.path.join(curDir, "model/")
dirStatic = os.path.join(curDir, "./static")
icoFileName = os.path.join(dirStatic, "./icons/1.png")

dataFileName = os.path.join(dirData, "init_data.json")
settingParamsFileName = os.path.join(dirData, "setting_params.json")
modelFileNameLP = os.path.join(dirModel, "model.lp")
modelFileNameLPPuLP = os.path.join(dirModel, "model_pulp.lp")
summaryFileName = os.path.join(dirResults, "summary_data.json")
solutionFileName = os.path.join(dirResults, "sol.soln")
graphFlowFileName = os.path.join(dirModel, "flow_data.html")

replaceDict = {"Crude_1": "Crude 1", "Crude_2": "Crude 2",
               "Light_naphta": "Light naphta", "Medium_naphta": "Medium naphta", "Heavy_naphta": "Heavy naphta",
               "Light_oil": "Light oil", "Heavy_oil": "Heavy oil", "Residuum": "Residuum",
               "Reformed_gasoline": "Reformed gasoline", "Cracked_gasoline": "Cracked gasoline",
               "Cracked_oil": "Cracked oil", "Premium_motor_fuel": "Premium motor fuel",
               "Regular_motor_fuel": "Regular motor fuel", "Jet_fuel": "Jet fuel", "Fuel_oil": "Fuel oil",
               "Lube_oil": "Lube oil"}


def style_metric_cards(
        color: str = "#232323",
        background_color: str = "#FFF",
        border_size_px: int = 1,
        border_color: str = "#CCC",
        border_radius_px: int = 5,
        border_left_color: str = "#9AD8E1",
        box_shadow: bool = True):
    box_shadow_str = (
        "box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;"
        if box_shadow
        else "box-shadow: none !important;"
    )
    st.markdown(
        f"""
        <style>
            div[data-tested="metric-container"] {{
                background-color: {background_color};
                border: {border_size_px}px solid {border_color};
                padding: 5% 5% 5% 10%;
                border-radius: {border_radius_px}px;
                border-left: 0.5rem solid {border_left_color} !important;
                color: {color};
                {box_shadow_str}
            }}
             div[data-tested="metric-container"] p {{
              color: {color};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def loadData():
    with open(summaryFileName, "r", encoding="utf-8") as sf:
        summaryData = json.load(sf)
    with open(settingParamsFileName, "r", encoding="utf-8") as sp:
        settingParams = json.load(sp)

    (raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking, lubeOilProduction, octane,
     octanePetrol, vapourPressure, fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax,
     crackingOilMax, lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
     distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf,
     vapourPressureDf, fuelOilBlendingDf) = init_model.initModel(dataFileName)

    return (summaryData, settingParams, raws, intermediateProducts, finalProducts, products, distillation, reforming,
            cracking, lubeOilProduction, octane, octanePetrol, vapourPressure, fuelOilBlending, crackedOilUsing,
            q, distillationMax, reformingNaphtaMax, crackingOilMax, lubeOilMin, lubeOilMax, jetFuleVapour,
            premiumPetrolByRegularMin, profit, distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf,
            vapourPressureDf, fuelOilBlendingDf)


st.set_page_config(page_title="Планирование нефтепереработки", page_icon=icoFileName, layout="wide",
                   initial_sidebar_state='collapsed')

st.markdown(f"""
        <style>
               .block-container {{
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                }}
        </style>
        """,
            unsafe_allow_html=True
            )

sidebar = st.sidebar
dash1 = st.container()
dash2 = st.container()
dash3 = st.container()

(summaryData, settingParams, raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking,
 lubeOilProduction, octane, octanePetrol, vapourPressure, fuelOilBlending, crackedOilUsing, q, distillationMax,
 reformingNaphtaMax, crackingOilMax, lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
 distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf, vapourPressureDf, fuelOilBlendingDf) = loadData()


with sidebar:
    selectedWrapper = st.selectbox("Библиотека", ["pyomo", "pulp"])
    if selectedWrapper == "pyomo":
        selectedSolver = st.selectbox("Решатель", solverNames)
    elif selectedWrapper == "pulp":
        selectedSolver = st.selectbox("Решатель", ["highs", "cbc", "scip"])
    useCLI = st.checkbox("Командная строка", value=True)
    gapTol = st.number_input("Погрешность (%)", value=0.001, format="%0.4f")
    premiumMotorFuelPrice = st.number_input("Цена Premium",
                                            value=settingParams["params"]["profit"]["Premium motor fuel"],
                                            min_value=690, max_value=710)
    regularMotorFuelPrice = st.number_input("Цена Regular",
                                            value=settingParams["params"]["profit"]["Regular motor fuel"],
                                            min_value=590, max_value=610)
    jetFuelPrice = st.number_input("Цена Керосина",
                                            value=settingParams["params"]["profit"]["Jet fuel"],
                                            min_value=390, max_value=410)
    fuelOilPrice = st.number_input("Цена Мазута",
                                            value=settingParams["params"]["profit"]["Fuel oil"],
                                            min_value=340, max_value=360)
    lubeOilPrice = st.number_input("Цена Масел",
                                            value=settingParams["params"]["profit"]["Lube oil"],
                                            min_value=140, max_value=160)

with (st.sidebar.form(key="form1")):
    submitted = st.form_submit_button("Рассчитать оптимальный план производства")
    if submitted:
        print()
        print(f"=== Новый расчет плана производства === {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # print(f"products = {products}")

        solverName = selectedSolver

        profit = settingParams["params"]["profit"]
        profit["Premium motor fuel"] = premiumMotorFuelPrice
        profit["Regular motor fuel"] = regularMotorFuelPrice
        profit["Jet fuel"] = jetFuelPrice
        profit["Fuel oil"] = fuelOilPrice
        profit["Lube oil"] = lubeOilPrice

        if selectedWrapper == "pyomo":
            print(f"=== Pyomo START ===")
            model = create_model.create_model(distillation, reforming, cracking, lubeOilProduction, octane, octanePetrol,
                                              vapourPressure,
                                              fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax,
                                              crackingOilMax,
                                              lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin,
                                              profit)
            model.write(modelFileNameLP, io_options={"symbolic_solver_labels": True})

            if useCLI:
                print("== Запуск решателя из командной строки ! ==")
                subprocess.run([solverPathExeChoice[solverName],
                                '-ratio', str(gapTol / 100), '-printingOptions', 'all',
                                '-import', modelFileNameLP,
                                '-stat=1', '-solve',
                                '-solu', solutionFileName])

                # solDataDict = dict()
                with open(solutionFileName, "r") as sf:
                    solData = sf.readlines()
                solData = [re.sub(r'\s+', " ", sd.strip()).split(" ") for sd in solData]
                # print(f"solData = {solData}")

                statusSol = solData[0][0]
                print(f"status is {statusSol}")

                # Целевая функция
                objProfit = float(solData[0][-1])
                print('Objective = %f' % objProfit)

                solData = list(filter(lambda z: z[1][0] == "q", solData[1:]))
                solData = [[sd[1], float(sd[2])] for sd in solData]
                # print(f"solData = {solData}")

                for i, sd in enumerate(solData):
                    sdk = sd[0]
                    for k, v in replaceDict.items():
                        sdk = sdk.replace(k, v)
                    solData[i][0] = sdk
                # print(f"solData = {solData}")

                q, qd, qCrackingBySource, qReformed = dict(), dict(), dict(), dict()
                qPetrolBySource, qReformedGasoline, qCrackedGasolineByPetrol = dict(), dict(), dict()
                qCrackedOilByProduct, qJetFuelBySource, qPetrol = dict(), dict(), dict()

                for sd in solData:
                    if "q(" in sd[0]:
                        l = len("q(")
                        k = sd[0][l:][:-1].split("_")
                        if len(k) == 1:
                            q[k[0]] = sd[1]
                        else:
                            q[tuple(k)] = sd[1]
                    elif "qd(" in sd[0]:
                        l = len("qd(")
                        k = tuple(sd[0][l:][:-1].split("_"))
                        qd[k] = sd[1]
                    elif "qCrackingBySource(" in sd[0]:
                        l = len("qCrackingBySource(")
                        k = tuple(sd[0][l:][:-1].split("_"))
                        qCrackingBySource[k] = sd[1]
                    elif "qReformedGasolineByPetrol(" in sd[0]:
                        l = len("qReformedGasolineByPetrol(")
                        k = tuple(sd[0][l:][:-1].split("_"))
                        qReformed[k] = sd[1]
                    elif "qPetrolBySource(" in sd[0]:
                        l = len("qPetrolBySource(")
                        k = tuple(sd[0][l:][:-1].split("_"))
                        qPetrolBySource[k] = sd[1]
                    elif "qCrackedGasolineByPetrol(" in sd[0]:
                        l = len("qCrackedGasolineByPetrol(")
                        k = sd[0][l:][:-1].split("_")
                        if len(k) == 1:
                            qCrackedGasolineByPetrol[k[0]] = sd[1]
                        else:
                            qCrackedGasolineByPetrol[tuple(k)] = sd[1]
                    elif "qCrackedOilByProduct(" in sd[0]:
                        l = len("qCrackedOilByProduct(")
                        k = sd[0][l:][:-1].split("_")
                        if len(k) == 1:
                            qCrackedOilByProduct[k[0]] = sd[1]
                        else:
                            qCrackedOilByProduct[tuple(k)] = sd[1]
                    elif "qJetFuelBySource(" in sd[0]:
                        l = len("qJetFuelBySource(")
                        k = tuple(sd[0][l:][:-1].split("_"))
                        qJetFuelBySource[k] = sd[1]
                    elif "qReformedGasoline(" in sd[0]:
                        l = len("qReformedGasoline(")
                        k = sd[0][l:][:-1].split("_")
                        if len(k) == 1:
                            qReformedGasoline[k[0]] = sd[1]
                        else:
                            qReformedGasoline[tuple(k)] = sd[1]
                    elif "qPetrol(" in sd[0]:
                        l = len("qPetrol(")
                        k = sd[0][l:][:-1].split("_")
                        if len(k) == 1:
                            qPetrol[k[0]] = sd[1]
                        else:
                            qPetrol[tuple(k)] = sd[1]
                    elif sd[0] == "qFuelOil":
                        qFuelOil = sd[1]
                    elif sd[0] == "qLubeOil":
                        qLubeOil = sd[1]

                qCrackedOil = sum(qCrackedOilByProduct.values())
                qCrackedGasoline = sum(qCrackedGasolineByPetrol.values())
                qJetFuel = sum(qJetFuelBySource.values()) + qCrackedOilByProduct["Jet fuel"]
            else:
                print("== Запуск решателя стредствами pyomo ! ==")
                if solverName == "highs":
                    solver = pyo.SolverFactory("appsi_highs")
                else:
                    solver = pyo.SolverFactory(solverName)  # , executable=solverPathExeChoice[solverName])
                    solver.set_executable(solverPathExeChoice[solverName], validate=False)
                if solverName == "cplex":
                    solver.options = {"mip tolerances mipgap": 0.000001}
                elif solverName == "cbc":
                    solver.options["ratio"] = gapTol / 100
                    # solver.options["solu"] = os.path.join(dirResults, "sol_1.soln")
                    # solver.options["printingOptions"] = "all"
                    # solver.options["import"] = os.path.join(curDir, "model/model.lp")
                elif solverName == "glpk":
                    solver.options["mipgap"] = 0.00001
                elif solverName == "highs":
                    solver.options["mip_rel_gap"] = 0.000001
                elif solverName == "scip":
                    solver.options = {"limits/gap": 0.000001}
                status = solver.solve(model, tee=True, keepfiles=True, logfile=os.path.join(curDir, "model/logf.log"),
                                      symbolic_solver_labels=True)

                print('iStatus = %s' % status.solver.termination_condition)
                print(f"status is {status}")
                # Целевая функция
                objProfit = model.objProfit()
                print('Objective = %f' % objProfit)

                print("\n=== Variables ===")
                for v in model.component_data_objects(ctype=pyo.Var):
                    print('{0} = {1}'.format(v, pyo.value(v)))

                print("\n=== Expressions ===")
                for v in model.component_data_objects(ctype=pyo.Expression):
                    print('{0} = {1}'.format(v, pyo.value(v)))

                q, qd, qCrackingBySource, qReformed = dict(), dict(), dict(), dict()
                qPetrolBySource, qReformedGasoline, qCrackedGasolineByPetrol = dict(), dict(), dict()
                qCrackedOilByProduct, qJetFuelBySource, qPetrol = dict(), dict(), dict()
                for v in model.component_objects(ctype=pyo.Var):
                    if pyo.name(v) == "q":
                        for index in v:
                            q[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qd":
                        for index in v:
                            qd[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qCrackingBySource":
                        for index in v:
                            qCrackingBySource[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qReformedGasolineByPetrol":
                        for index in v:
                            qReformed[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qPetrolBySource":
                        for index in v:
                            qPetrolBySource[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qCrackedGasolineByPetrol":
                        for index in v:
                            qCrackedGasolineByPetrol[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qCrackedOilByProduct":
                        for index in v:
                            qCrackedOilByProduct[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qJetFuelBySource":
                        for index in v:
                            qJetFuelBySource[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qReformedGasoline":
                        for index in v:
                            qReformedGasoline[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qPetrol":
                        for index in v:
                            qPetrol[index] = pyo.value(v[index])
                    elif pyo.name(v) == "qFuelOil":
                        qFuelOil = pyo.value(v)
                    elif pyo.name(v) == "qLubeOil":
                        qLubeOil = pyo.value(v)

                for v in model.component_objects(ctype=pyo.Expression):
                    if pyo.name(v) == "qCrackedOil":
                        qCrackedOil = pyo.value(v)
                    elif pyo.name(v) == "qCrackedGasoline":
                        qCrackedGasoline = pyo.value(v)
                    elif pyo.name(v) == "qJetFuel":
                        qJetFuel = pyo.value(v)
        elif selectedWrapper == "pulp":
            print(f"=== PuLP START ===")
            (model, q, qd, qReformedGasoline, qReformedGasolineByPetrol, qCrackingBySource, qCrackedGasolineByPetrol,
             qCrackedOilByProduct, qPetrol, qPetrolBySource, qJetFuelBySource,
             qLubeOilBySource, qJetFuel, qFuelOil, qLubeOil, qCrackedOil,
             qCrackedGasoline) = create_model.create_modelPuLP(
                distillation, reforming, cracking, lubeOilProduction,
                octane, octanePetrol,
                vapourPressure,
                fuelOilBlending, crackedOilUsing, q, distillationMax,
                reformingNaphtaMax,
                crackingOilMax,
                lubeOilMin, lubeOilMax, jetFuleVapour,
                premiumPetrolByRegularMin,
                profit)
            print(f"available solvers is {pl.listSolvers(onlyAvailable=True)}")
            model.writeLP(modelFileNameLPPuLP)

            if solverName == "cbc":
                solver = pl.PULP_CBC_CMD(gapRel=gapTol / 100)
            elif solverName == "highs":
                solver = pl.HiGHS(gapRel=gapTol / 100)
            elif solverName == "scip":
                solver = pl.SCIP_CMD(gapRel=gapTol / 100)
            # solver = pl.HiGHS(mip_rel_gap=gapTol / 100)

            status = model.solve(solver)

            print(f"status is {status}")
            print(f"optimal = {status == 1}")
            print(f"infeasible = {status == -1}")

            if status == 1:
                objProfit = model.objective.value()
                solveTime = model.solutionTime
                q = {k: v.value() for k, v in q.items()}
                qd = {k: v.value() for k, v in qd.items()}

                qCrackingBySource = {k: v.value() for k, v in qCrackingBySource.items()}
                qReformed = {k: v.value() for k, v in qReformedGasolineByPetrol.items()}
                qPetrolBySource = {k: v.value() for k, v in qPetrolBySource.items()}
                qReformedGasoline = {k: v.value() for k, v in qReformedGasoline.items()}
                qPetrol = {k: v.value() for k, v in qPetrol.items()}
                qCrackedGasolineByPetrol = {k: v.value() for k, v in qCrackedGasolineByPetrol.items()}
                qCrackedOilByProduct = {k: v.value() for k, v in qCrackedOilByProduct.items()}
                qJetFuelBySource = {k: v.value() for k, v in qJetFuelBySource.items()}
                qJetFuel = qJetFuel.value()
                qFuelOil = qFuelOil.value()
                qLubeOil = qLubeOil.value()
                qCrackedOil = qCrackedOil.value()
                qCrackedGasoline = qCrackedGasoline.value()

        fuelOilBlendingSum = sum(fuelOilBlending.values())
        qFuelOilBlending = {k: (qFuelOil * v / fuelOilBlendingSum) for k, v in fuelOilBlending.items()}

        print(f"q = {q}")
        print(f"qd = {qd}")
        print(f"qCrackingBySource = {qCrackingBySource}")
        print(f"qReformed = {qReformed}")
        print(f"qPetrolBySource = {qPetrolBySource}")
        print(f"qReformedGasoline = {qReformedGasoline}")
        print(f"qPetrol = {qPetrol}")
        print(f"qCrackedGasolineByPetrol = {qCrackedGasolineByPetrol}")
        print(f"qCrackedOilByProduct = {qCrackedOilByProduct}")
        print(f"qJetFuelBySource = {qJetFuelBySource}")

        print(f"qCrackedOil = {qCrackedOil}")
        print(f"qCrackedGasoline = {qCrackedGasoline}")
        print(f"qJetFuel = {qJetFuel}")
        print(f"qFuelOil = {qFuelOil}")
        print(f"qLubeOil = {qLubeOil}")

        optimResult = dict()
        optimResult["profit"] = objProfit
        optimResult["Crude 1"], optimResult["Crude 2"] = q["Crude 1"], q["Crude 2"]
        optimResult["Total Inflow"] = q["Crude 1"] + q["Crude 2"]
        optimResult["Premium motor fuel"] = qPetrol["Premium motor fuel"]
        optimResult["Regular motor fuel"] = qPetrol["Regular motor fuel"]
        optimResult["Jet Fuel"] = qJetFuel
        optimResult["Fuel Oil"] = qFuelOil
        optimResult["Lube Oil"] = qLubeOil
        optimResult["Total Outflow"] = (qPetrol["Premium motor fuel"] + qPetrol["Regular motor fuel"] +
                                        qJetFuel + qFuelOil + qLubeOil)

        with open(summaryFileName, "w") as sf:
            json.dump(optimResult, sf)

        g = draw_flow.drawFlow(raws, intermediateProducts, finalProducts, products,
                               q, qd, qCrackingBySource, qReformed, qPetrolBySource, qReformedGasoline,
                               qCrackedOil, qCrackedGasoline, qCrackedGasolineByPetrol, qCrackedOilByProduct,
                               qJetFuelBySource, qFuelOil, qFuelOilBlending, qJetFuel, qPetrol, qLubeOil)
        g.save_graph(graphFlowFileName)

        st.rerun()


with dash1:
    st.markdown("<h2 style='text-align': center;> Аналитика планирования </h2>",
                unsafe_allow_html=True)

with dash2:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    col1.metric(label="Выручка", value=millify(summaryData["profit"] / 100, precision=3) + " $")
    col2.metric(label="Вход, итого", value=millify(summaryData["Total Inflow"], precision=3) + " т")
    col3.metric(label="Выход, итого", value=millify(summaryData["Total Outflow"], precision=3) + " т")
    col4.metric(label="Выход бензина Premium", value=millify(summaryData["Premium motor fuel"], precision=3) + " т")
    col5.metric(label="Выход бензина Regular", value=millify(summaryData["Regular motor fuel"], precision=3) + " т")
    col6.metric(label="Выход керосина", value=millify(summaryData["Jet Fuel"], precision=3) + " т")
    col7.metric(label="Выход мазута", value=millify(summaryData["Fuel Oil"], precision=3) + " т")
    col8.metric(label="Выход масел", value=millify(summaryData["Lube Oil"], precision=3) + " т")

    style_metric_cards(border_left_color="#DBF227")

with dash3:
    tab1, tab2 = st.tabs(["Исходные данные", "Схема потоков"])

    with tab1:
        tab11, tab12, tab13, tab14, tab15, tab16 = st.tabs(["Перегонка", "Риформинг", "Крекинг", "Октановое число",
                                                            "Давление насыщенных паров", "Компаундирование для мазута"])

        with tab11:
            st.markdown("<h5 style='text-align': left;> Выходы после атмосферной перегонки </h5>",
                        unsafe_allow_html=True)
            st.dataframe(distillationDf, hide_index=True)

        with tab12:
            st.markdown("<h5 style='text-align': left;> Выходы после Риформинга </h5>",
                        unsafe_allow_html=True)
            st.dataframe(reformingDf, hide_index=True)

        with tab13:
            st.markdown("<h5 style='text-align': left;> Выходы после Крекинга </h5>",
                        unsafe_allow_html=True)
            st.dataframe(crackingDf, hide_index=True)

        with tab14:
            st.markdown("<h5 style='text-align': left;> Октановое число промежуточных и конечных продуктов </h5>",
                        unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 2, 5])
            with col1:
                st.write("Промежуточные продукты")
                st.dataframe(octaneDf, hide_index=True)

            with col2:
                st.write("Конечные продукты")
                st.dataframe(octanePetrolDf, hide_index=True)

            with col3:
                st.write("   ")

        with tab15:
            st.markdown("<h5 style='text-align': left;> Давление насыщенных паров продуктов "
                        "компаундирования для керосина </h5>",
                        unsafe_allow_html=True)
            st.dataframe(vapourPressureDf, hide_index=True)

        with tab16:
            st.markdown("<h5 style='text-align': left;> Пропорции продуктов компаундирования для керосина </h5>",
                        unsafe_allow_html=True)
            st.dataframe(fuelOilBlendingDf, hide_index=True)

    with tab2:
        with open(graphFlowFileName) as gHtml:
            components.html(gHtml.read(), height=600, scrolling=True)
