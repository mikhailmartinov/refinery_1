import os
from pyvis.network import Network


def formatFloatNumber(num, sep=" "):
    return f"{int(round(num, 0)):_d}".replace("_", " ")


def createTitle(p1, p2, v):
    return f"{p1} --> {p2}\nОбъем {v} т."


def createTitle2(p11, p12, p2, v1, v2):
    return (f"{p11} --> {p2}: Объем {v1} т.\n"
            f"{p12} --> {p2}: Объем {v2} т.")


def drawFlow(raws, intermediateProducts, finalProducts, products,
             q, qd, qCrackingBySource, qReformed, qPetrolBySource, qReformedGasoline,
             qCrackedOil, qCrackedGasoline, qCrackedGasolineByPetrol, qCrackedOilByProduct,
             qJetFuelBySource, qFuelOil, qFuelOilBlending, qJetFuel, qPetrol, qLubeOil):
    g = Network(bgcolor="#fefefe", font_color="black", height="950px", width="100%", directed=True)

    rawColor, distillationColor, reformingColor, finalProdColor = "#FFFFFF", "#F5DEB3", "#008080", "#B0E0E6"
    blendingPetrolColor, distillationEdgeColor, crackingColor = "#808000", "#000000", "#006400"
    blendingJetFuelColor, blendingFuelOilColor = "#20B2AA", "#4682B4"
    rawSize, distillationSize, reformingSize = 25, 20, 10
    rawShape, distillationShape, reformingShape = "square", "square", "circle"
    edgesWidth = 1
    edgeColor = "#808080"  # "#A9A9A9" "#C0C0C0"
    processColor = "#F0FFFF"  # "#F0FFF0"  #  "#FFFAFA" "#DCDCDC"
    xStep = 200
    yStep = 85
    xStart, yStart = 0, 175

    productsName = list(products.values())
    points = dict()
    rawsIdx = 0
    distillationIdx = 0

    g.add_node("distillation", x=xStart + xStep, y=yStart + yStep / 2,
               label="\n\n\n\n\nDistillation\n\n\n\n\n",
               color=processColor, size=50, shape="box")
    g.add_node("reforming", x=xStart + 2.75 * xStep, y=- 1.5 * yStep,
               label="\n\nReforming\n\n",
               color=processColor, size=40, shape="box")
    g.add_node("reformed gasoline", x=xStart + 3.55 * xStep, y=- 1.5 * yStep,
               label="Reformed\ngasoline",
               color=processColor, size=40, shape="box")
    g.add_node("blending premium regular", x=xStart + 4.5 * xStep, y=- 1.5 * yStep,
               label="Blending\nPremium / Regular",
               color=processColor, size=50, shape="box")

    g.add_node("cracking", x=xStart + 3.5 * xStep, y=yStart + yStep * 0.65,
               label="\n\nCracking\n\n",
               color=processColor, size=40, shape="box")
    g.add_node("cracked gasoline", x=xStart + 4.25 * xStep, y=yStart + yStep * 0.3,
               label="Cracked\ngasoline",
               color=processColor, size=40, shape="box")
    g.add_node("cracked oil", x=xStart + 4.25 * xStep, y=yStart + yStep * 1.05,
               label="Cracked\noil",
               color=processColor, size=40, shape="box")

    g.add_node("blending jet fuel", x=xStart + 3.25 * xStep, y=yStart + yStep * 2.65,
               label="\nBlending\nJet fuel\n",
               color=processColor, size=40, shape="box")
    g.add_node("blending fuel oil", x=xStart + 3.25 * xStep, y=yStart + yStep * 4.25,
               label="\nBlending\nFuel oil\n",
               color=processColor, size=40, shape="box")

    g.add_node("jet fuel", x=xStart + 6 * xStep, y=yStart + yStep * 2.65,
               label="Jet fuel", color=finalProdColor, size=40, shape="circle")
    g.add_node("fuel oil", x=xStart + 6 * xStep, y=yStart + yStep * 4.25,
               label="Fuel oil", color=finalProdColor, size=40, shape="circle")

    g.add_node("lube oil", x=xStart + 6 * xStep, y=yStart + yStep * 5.6,
               label="Lube oil", color=finalProdColor, size=40, shape="circle")

    rawsName = list(raws.values())
    distillationProducts = []
    for d in qd.keys():
        if d[1] not in distillationProducts:
            distillationProducts.append(d[1])

    for pn in productsName:
        if pn in rawsName:
            points[pn] = {"x": xStart, "y": yStart + rawsIdx * yStep, "label": pn,
                          "color": rawColor, "size": rawSize, "shape": rawShape}
            g.add_node(pn, x=points[pn]["x"], y=points[pn]["y"], label=points[pn]["label"],
                       color=points[pn]["color"], size=points[pn]["size"], shape=points[pn]["shape"])
            v = formatFloatNumber(q[pn])
            g.add_edge(pn, "distillation", width=edgesWidth, label=v, color=edgeColor,
                       title=createTitle(pn, "Distillation", v))
            rawsIdx += 1
        elif pn in distillationProducts:
            points[pn] = {"x": xStart + 2 * xStep, "y": distillationIdx * yStep, "label": pn,
                          "color": distillationColor, "size": distillationSize, "shape": distillationShape}
            g.add_node(pn, x=points[pn]["x"], y=points[pn]["y"], label=points[pn]["label"],
                       color=points[pn]["color"], size=points[pn]["size"], shape=points[pn]["shape"])
            distillationIdx += 1
            v1, v2 = formatFloatNumber(qd[rawsName[0], pn]), formatFloatNumber(qd[rawsName[1], pn])
            if pn in ["Light naphta", "Medium naphta", "Heavy oil", "Residuum"]:
                pName = "dist-" + pn
                points[pName] = {"x": xStart + xStep, "y": points[pn]["y"],
                                 "shape": "dot", "size": 0.5, "color": edgeColor}
                g.add_node(pName, x=points[pName]["x"], y=points[pName]["y"], label=" ",
                           size=points[pName]["size"], shape=points[pName]["shape"], color=points[pName]["color"])
                g.add_edge("distillation", pName, width=edgesWidth, color=distillationEdgeColor)
                g.add_edge(pName, pn, width=edgesWidth, color=distillationEdgeColor,
                           label=f"{v1}\n{v2}\n\n\n", title=createTitle2(rawsName[0], rawsName[1], pn, v1, v2))
            elif pn in ["Heavy naphta", "Light oil"]:
                g.add_edge("distillation", pn, width=edgesWidth, color=distillationEdgeColor,
                           label=f"{v1}\n{v2}\n\n\n", title=createTitle2(rawsName[0], rawsName[1], pn, v1, v2))

    for pn in ["Light oil", "Heavy oil"]:
        g.add_edge(pn, "cracking", width=edgesWidth, color=crackingColor,
                   label=f"{formatFloatNumber(sum(qCrackingBySource[rawsName[i], pn] for i in range(2)))}")

    motorFuels = ["Premium motor fuel", "Regular motor fuel"]
    for pn in ["Light naphta", "Medium naphta", "Heavy naphta"]:
        if pn == "Light naphta":
            pName = pn + "-reforming"
            g.add_node(pName, x=xStart + 2 * xStep, y=- 1.5 * yStep, label=" ", size=0.5, shape="dot", color=edgeColor)
            g.add_edge(pn, pName, width=edgesWidth, color=reformingColor,
                       label=f"{formatFloatNumber(sum(qReformed[rawsName[i], pn, mF] for i in range(2) for mF in motorFuels))}")
            g.add_edge(pName, "reforming", width=edgesWidth, color=reformingColor)
        else:
            g.add_edge(pn, "reforming", width=edgesWidth, color=reformingColor,
                       label=f"{formatFloatNumber(sum(qReformed[rawsName[i], pn, mF] for i in range(2) for mF in motorFuels))}")

        pName = pn + "-" + motorFuels[0] + "-" + motorFuels[1]
        g.add_node(pName, x=xStart + 4.5 * xStep, y=points[pn]["y"], label=" ", size=0.5, shape="dot", color=edgeColor)
        g.add_edge(pn, pName, width=edgesWidth, color=blendingPetrolColor,
                   label=f"{formatFloatNumber(sum(qPetrolBySource[rawsName[i], pn, motorFuels[0]] for i in range(2)))} / "
                         f"{formatFloatNumber(sum(qPetrolBySource[rawsName[i], pn, motorFuels[1]] for i in range(2)))}\n\n")
        g.add_edge(pName, "blending premium regular", width=edgesWidth, color=blendingPetrolColor)

    g.add_edge("reforming", "reformed gasoline", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(sum(qReformedGasoline[motorFuels[i]] for i in range(2)))}\n\n")
    g.add_edge("reformed gasoline", "blending premium regular", width=edgesWidth, color=blendingPetrolColor,
               label=f"{formatFloatNumber(qReformedGasoline[motorFuels[0]])} / "
                     f"{formatFloatNumber(qReformedGasoline[motorFuels[1]])}         \n\n")
    g.add_edge("cracking", "cracked oil", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qCrackedOil)}")
    g.add_edge("cracking", "cracked gasoline", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qCrackedGasoline)}")

    pn = "cracked gasoline"
    pName = pn + "-" + motorFuels[0] + "-" + motorFuels[1]
    pName1, pName2 = pName + "_1", pName + "_2"
    g.add_node(pName1, x=xStart + 5.1 * xStep, y=yStart + yStep * 0.3, label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 5.1 * xStep, y=- 1.5 * yStep, label=" ", size=0.5, shape="dot",
               color=edgeColor)
    g.add_edge(pn, pName1, width=edgesWidth, color=blendingPetrolColor,
               label=f"{formatFloatNumber(qCrackedGasolineByPetrol[motorFuels[0]])} / "
                     f"{formatFloatNumber(qCrackedGasolineByPetrol[motorFuels[1]])}\n\n")
    g.add_edge(pName1, pName2, width=edgesWidth, color=blendingPetrolColor)
    g.add_edge(pName2, "blending premium regular", width=edgesWidth, color=blendingPetrolColor)

    for pn in ["Light oil", "Heavy oil", "Residuum"]:
        g.add_edge(pn, "blending jet fuel", width=edgesWidth, color=blendingJetFuelColor,
                   label=f"{formatFloatNumber(sum(qJetFuelBySource[rawsName[i], pn] for i in range(2)))}")
    g.add_edge("cracked oil", "blending jet fuel", width=edgesWidth, color=blendingJetFuelColor,
               label=f"{formatFloatNumber(qCrackedOilByProduct['Jet fuel'])}")

    pn = "Residuum"
    pName = pn + "-blending fuel oil"
    pName1, pName2 = pName + "_1", pName + "_2"
    g.add_node(pName1, x=xStart + 2 * xStep, y=yStart + yStep * 5.1, label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 3.25 * xStep, y=yStart + yStep * 5.1, label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_edge(pn, pName1, width=edgesWidth, color=blendingFuelOilColor)
    g.add_edge(pName1, pName2, width=edgesWidth, color=blendingFuelOilColor,
               label=f"{formatFloatNumber(qFuelOilBlending[pn])}")
    g.add_edge(pName2, "blending fuel oil", width=edgesWidth, color=blendingFuelOilColor)

    pn = "Heavy oil"
    pName = pn + "-blending fuel oil"
    pName1, pName2 = pName + "_1", pName + "_2"
    g.add_node(pName1, x=xStart + 2.25 * xStep, y=4 * yStep, label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 2.25 * xStep, y=yStart + yStep * 4.25, label=" ", size=0.5, shape="dot",
               color=edgeColor)
    g.add_edge(pn, pName1, width=edgesWidth, color=blendingFuelOilColor)
    g.add_edge(pName1, pName2, width=edgesWidth, color=blendingFuelOilColor)
    g.add_edge(pName2, "blending fuel oil", width=edgesWidth, color=blendingFuelOilColor,
               label=f"{formatFloatNumber(qFuelOilBlending[pn])}")

    pn = "Light oil"
    pName = pn + "-blending fuel oil"
    pName1, pName2 = pName + "_1", pName + "_2"
    g.add_node(pName1, x=xStart + 2.35 * xStep, y=3 * yStep, label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 2.35 * xStep, y=yStart + yStep * 3.5, label=" ", size=0.5, shape="dot",
               color=edgeColor)
    g.add_edge(pn, pName1, width=edgesWidth, color=blendingFuelOilColor)
    g.add_edge(pName1, pName2, width=edgesWidth, color=blendingFuelOilColor)
    g.add_edge(pName2, "blending fuel oil", width=edgesWidth, color=blendingFuelOilColor,
               label=f"{formatFloatNumber(qFuelOilBlending[pn])}")

    g.add_edge("blending jet fuel", "jet fuel", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qJetFuel)}")
    g.add_edge("blending fuel oil", "fuel oil", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qFuelOil)}")

    pn = motorFuels[0]
    pName1, pName2 = "premium_1", "premium_2"
    g.add_node(pName1, x=xStart + 4.5 * xStep, y=- 2.1 * yStep,
               label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 5.5 * xStep, y=- 2.1 * yStep,
               label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pn, x=xStart + 5.5 * xStep, y=2 * yStep,
               label=f"Premium\n motor fuel", color=finalProdColor, size=50, shape="circle")
    g.add_edge("blending premium regular", pName1, width=edgesWidth, color=edgeColor)
    g.add_edge(pName1, pName2, width=edgesWidth, color=edgeColor)
    g.add_edge(pName2, pn, width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qPetrol[pn])}")

    pn = motorFuels[1]
    pName1, pName2 = "regular_1", "regular_2"
    g.add_node(pName1, x=xStart + 4.5 * xStep, y=- 2.6 * yStep,
               label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pName2, x=xStart + 6 * xStep, y=- 2.6 * yStep,
               label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_node(pn, x=xStart + 6 * xStep, y=2 * yStep,
               label=f"Regular\n motor fuel", color=finalProdColor, size=50, shape="circle")
    g.add_edge("blending premium regular", pName1, width=edgesWidth, color=edgeColor)
    g.add_edge(pName1, pName2, width=edgesWidth, color=edgeColor)
    g.add_edge(pName2, pn, width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qPetrol[pn])}")

    pName1 = "Residuum-lube oil_1"
    g.add_node(pName1, x=xStart + 2 * xStep, y=yStart + yStep * 5.6,
               label=" ", size=0.5, shape="dot", color=edgeColor)
    g.add_edge("Residuum", pName1, width=edgesWidth, color=edgeColor)
    g.add_edge(pName1, "lube oil", width=edgesWidth, color=edgeColor,
               label=f"{formatFloatNumber(qLubeOil)}")

    print(f"points = {points}")
    g.toggle_physics(False)

    return g
