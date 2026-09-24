import json
import os
import sys
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components
import pyomo.environ as pyo

from millifyNumber import millify
import init_model
import create_model
import draw_flow

curDir = os.getcwd()
solverPathExeChoice = {
    # "scip": "C:\\scip\\SCIPOptSuite 9.2.3\\bin\\scip.exe",
                       "cbc": os.path.join(curDir, "solvers/cbc/cbc_2.10.12/bin/cbc.exe"),
    #                    "highs": "C:\\highs-1.15.1\\bin\\highs.exe",
    #                    "cplex": "D:\\Projects\\demetra\\bin\\x64_win64\\cplex.exe",
    #                    "glpk": "C:\\glpk\\glpk-4.65\\w64\\glpsol.exe",
    #                    "ipopt": 'C:\\ipopt\\bin\\ipopt.exe'
}
sys.path.append(solverPathExeChoice["cbc"])
solverNames = list(solverPathExeChoice.keys())
# solverName = "cplex"

curDir = os.getcwd()
dirData = os.path.join(curDir, "data/")
dirResults = os.path.join(curDir, "results/")
dirModel = os.path.join(curDir, "model/")
dirStatic = os.path.join(curDir, "./static")
icoFileName = os.path.join(dirStatic, "./icons/1.png")

dataFileName = os.path.join(dirData, "init_data.json")
summaryFileName = os.path.join(dirResults, "summary_data.json")
graphFlowFileName = os.path.join(dirModel, "flow_data.html")


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

    (raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking, lubeOilProduction, octane,
     octanePetrol, vapourPressure, fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax,
     crackingOilMax, lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
     distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf,
     vapourPressureDf, fuelOilBlendingDf) = init_model.initModel(dataFileName)

    return (summaryData, raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking,
            lubeOilProduction, octane, octanePetrol, vapourPressure,
            fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax, crackingOilMax,
            lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
            distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf, vapourPressureDf, fuelOilBlendingDf)


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

(summaryData, raws, intermediateProducts, finalProducts, products, distillation, reforming, cracking, lubeOilProduction,
 octane, octanePetrol, vapourPressure,
 fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax, crackingOilMax,
 lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit,
 distillationDf, reformingDf, crackingDf, octaneDf, octanePetrolDf, vapourPressureDf, fuelOilBlendingDf) = loadData()


with sidebar:
    selectedSolver = st.selectbox("Решатель", solverNames)

with (st.sidebar.form(key="form1")):
    submitted = st.form_submit_button("Рассчитать оптимальный план производства")
    if submitted:
        print()
        print(f"=== Новый расчет плана производства === {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # print(f"products = {products}")

        model = create_model.create_model(distillation, reforming, cracking, lubeOilProduction, octane, octanePetrol,
                                          vapourPressure,
                                          fuelOilBlending, crackedOilUsing, q, distillationMax, reformingNaphtaMax,
                                          crackingOilMax,
                                          lubeOilMin, lubeOilMax, jetFuleVapour, premiumPetrolByRegularMin, profit)

        solverName = selectedSolver
        if solverName == "highs":
            solver = pyo.SolverFactory("appsi_highs")
        else:
            solver = pyo.SolverFactory(solverName)  # , executable=solverPathExeChoice[solverName])
            solver.set_executable(solverPathExeChoice[solverName], validate=False)
        if solverName == "cplex":
            solver.options = {"mip tolerances mipgap": 0.000001}
        elif solverName == "cbc":
            solver.options = {"ratio": 0.000001}
        elif solverName == "glpk":
            solver.options["mipgap"] = 0.000001
        elif solverName == "highs":
            solver.options["mip_rel_gap"] = 0.000001
        elif solverName == "scip":
            solver.options = {"limits/gap": 0.000001}
        status = solver.solve(model, tee=True)

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
            elif pyo.name(v) == "qFuelOil":
                qFuelOil = pyo.value(v)
            elif pyo.name(v) == "qLubeOil":
                qLubeOil = pyo.value(v)

        for v in model.component_objects(ctype=pyo.Expression):
            if pyo.name(v) == "qReformedGasoline":
                for index in v:
                    qReformedGasoline[index] = pyo.value(v[index])
            elif pyo.name(v) == "qCrackedOil":
                qCrackedOil = pyo.value(v)
            elif pyo.name(v) == "qCrackedGasoline":
                qCrackedGasoline = pyo.value(v)
            elif pyo.name(v) == "qJetFuel":
                qJetFuel = pyo.value(v)
            elif pyo.name(v) == "qPetrol":
                for index in v:
                    qPetrol[index] = pyo.value(v[index])

        fuelOilBlendingSum = sum(fuelOilBlending.values())
        qFuelOilBlending = {k: (qFuelOil * v / fuelOilBlendingSum) for k, v in fuelOilBlending.items()}

        # print(f"q = {q}")
        # print(f"qd = {qd}")
        # print(f"qCrackingBySource = {qCrackingBySource}")
        # print(f"qReformed = {qReformed}")
        # print(f"qPetrolBySource = {qPetrolBySource}")
        # print(f"qReformedGasoline = {qReformedGasoline}")
        # print(f"qCrackedOil = {qCrackedOil}")
        # print(f"qCrackedGasoline = {qCrackedGasoline}")
        # print(f"qCrackedGasolineByPetrol = {qCrackedGasolineByPetrol}")
        # print(f"qCrackedOilByProduct = {qCrackedOilByProduct}")

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
    col1.metric(label="Выручка", value=millify(summaryData["profit"], precision=3) + " $")
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
            st.markdown("<h5 style='text-align': left;> Давление насыщенных паров продуктов компаундирования для керосина </h5>",
                        unsafe_allow_html=True)
            st.dataframe(vapourPressureDf, hide_index=True)

        with tab16:
            st.markdown("<h5 style='text-align': left;> Пропорции продуктов компаундирования для керосина </h5>",
                        unsafe_allow_html=True)
            st.dataframe(fuelOilBlendingDf, hide_index=True)

    with tab2:
        with open(graphFlowFileName) as gHtml:
            components.html(gHtml.read(), height=600, scrolling=True)
