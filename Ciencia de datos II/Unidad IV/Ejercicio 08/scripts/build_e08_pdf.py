"""Genera U04_E08_Roque_Ventura.pdf y U04_E08_Evidencias_Roque_Ventura.pdf a partir de los artefactos del repositorio.
Uso: uv run --with reportlab --with pillow python scripts/build_e08_pdf.py
Mismo formato que el informe de E07."""
import csv
import json
import re
import textwrap
from pathlib import Path

import numpy as np
import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, Image, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table)

PROJECT = Path(__file__).resolve().parents[1]
EVIDENCE = PROJECT / "reports/e08/evidencias"
OUT_MAIN, OUT_EVID = PROJECT / "U04_E08_Roque_Ventura.pdf", PROJECT / "U04_E08_Evidencias_Roque_Ventura.pdf"

FONTS = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Arial", FONTS / "arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", FONTS / "arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Italic", FONTS / "ariali.ttf"))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", FONTS / "arialbi.ttf"))
pdfmetrics.registerFont(TTFont("Consolas", FONTS / "consola.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-BoldItalic")

BLUE = colors.HexColor("#1F4E79")
NAVY = colors.HexColor("#1F3E66")
GRAY = colors.HexColor("#595959")
RULE = colors.HexColor("#B4C3D6")
LABEL_BG = colors.HexColor("#EEF2F7")
HIGHLIGHT = colors.HexColor("#FFF4D6")
REPO = "https://github.com/RoqueVentura/UASD-Maestria-Ciencia-De-Datos"
FOLDER = "Ciencia%20de%20datos%20II/Unidad%20IV/Ejercicio%2008"
REPO_URL = f"{REPO}/tree/main/{FOLDER}"
EVID_URL = f"{REPO}/blob/main/{FOLDER}/U04_E08_Evidencias_Roque_Ventura.pdf"

body = ParagraphStyle("body", fontName="Arial", fontSize=9.5, leading=12.6, alignment=4, spaceAfter=5)
small = ParagraphStyle("small", parent=body, fontSize=8.3, leading=10.4, alignment=0, spaceAfter=0)
cell = ParagraphStyle("cell", parent=small)
tiny = ParagraphStyle("tiny", parent=small, fontSize=7.8, leading=9.6)
head = ParagraphStyle("head", parent=small, fontName="Arial-Bold", textColor=colors.white)
title = ParagraphStyle("title", fontName="Arial-Bold", fontSize=19, leading=23, textColor=BLUE, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Arial", fontSize=10.5, leading=13, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)
h1 = ParagraphStyle("h1", fontName="Arial-Bold", fontSize=13.5, leading=17, textColor=BLUE, spaceBefore=10, spaceAfter=2, keepWithNext=1)
ev_title = ParagraphStyle("ev_title", parent=small, fontName="Arial-Bold", fontSize=9.2, leading=11.5, spaceAfter=3)
ev_text = ParagraphStyle("ev_text", parent=small, fontSize=8.6, leading=11)
code = ParagraphStyle("code", fontName="Consolas", fontSize=7.0, leading=8.8, backColor=colors.HexColor("#F3F3F3"),
                      borderPadding=5, spaceBefore=4, spaceAfter=8)
hanging = ParagraphStyle("ref", parent=body, leftIndent=18, firstLineIndent=-18, alignment=0)
WIDTH = letter[0] - 1.5 * inch


def p(text, style=body):
    return Paragraph(text, style)


def link(url, text):
    return f'<link href="{url}"><u><font color="#1F4E79">{text}</font></u></link>'


def section(text):
    rule = HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=0, spaceAfter=5)
    rule.keepWithNext = 1
    return [p(text, h1), rule]


def table(rows, widths, highlight_rows=(), style_cell=cell):
    data = [[p(str(c), head) for c in rows[0]]] + [[p(str(c), style_cell) for c in row] for row in rows[1:]]
    style = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), 0.4, RULE),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 5)]
    style += [("BACKGROUND", (0, r), (-1, r), HIGHLIGHT) for r in highlight_rows]
    return Table(data, colWidths=[w * WIDTH for w in widths], style=style, repeatRows=1, spaceBefore=3, spaceAfter=7)


def label_table(rows, label_width=0.2):
    data = [[p(f"{a}", cell), p(b, cell)] for a, b in rows]
    style = [("BACKGROUND", (0, 0), (0, -1), LABEL_BG), ("GRID", (0, 0), (-1, -1), 0.4, RULE),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    return Table(data, colWidths=[label_width * WIDTH, (1 - label_width) * WIDTH], style=style, spaceAfter=8)


def footer_for(code_name):
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Arial", 7.5)
        canvas.setFillColor(GRAY)
        canvas.drawString(0.75 * inch, 0.5 * inch, f"INF-8239, {code_name}. Roque Alexis Ventura Vallejo, 100805873")
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, f"Página {doc.page}")
        canvas.restoreState()
    return footer


def read_csv(path):
    with open(PROJECT / path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(path):
    return json.loads((PROJECT / path).read_text(encoding="utf-8"))


f3 = lambda v: "—" if v in ("", None) else f"{np.round(float(v), 3):.3f}"

# ---------------------------------------------------------------- datos (todo se lee de los artefactos)
gates = yaml.safe_load((PROJECT / "configs/governance.yml").read_text(encoding="utf-8"))["gates"]
mon = yaml.safe_load((PROJECT / "configs/monitoring.yml").read_text(encoding="utf-8"))
retention = read_csv("student_inputs/retention_policy.csv")
raci, handoffs = read_csv("student_inputs/raci.csv"), read_csv("student_inputs/handoffs.csv")
decision = read_json("reports/lab13/deployment_decision.json")
month = {r["month"]: r for r in read_csv("reports/e08/monitoring_by_month.csv")}
month_eg = {r["month"]: r for r in read_csv("reports/e08/monitoring_by_month_expgrad.csv")}
drill = read_json("reports/e08/incident_drill/timeline.json")
d_base, d_inc = read_json("reports/e08/incident_drill/decision_baseline.json"), read_json("reports/e08/incident_drill/decision_incident.json")
d_rec = read_json("reports/e08/incident_drill/decision_recovered.json")
manifest = read_json("reports/e08/incident_drill/manifest.json")
profile = {r["zone"]: r for r in read_csv("reports/e08/incident_drill/batch_profile.csv")}
fair_inc = {r["protected_group"]: r for r in read_csv("reports/e08/incident_drill/fairness_incident.csv")}
fair_lab13 = {r["protected_group"]: r for r in read_csv("reports/lab13/fairness_by_group.csv")}
rec = decision["recommendation"]
# Test count comes from the real console output, so the PDF cannot claim more than what ran.
run_log = (PROJECT / "reports/e08/run_log.txt").read_text(encoding="utf-8")
n_tests = int(re.search(r"(\d+) passed", run_log).group(1))
assert "failed" not in run_log.split("$ uv run python")[0]
assert decision["decision"]["status"] == "GO" and d_inc["decision"]["status"] == "REVIEW" and d_rec["decision"]["status"] == "GO"
assert month["2026-11"]["support_ok"] == "True"

story = []
# ---------------------------------------------------------------- portada
story += [p("Ejercicio 08: Expediente de gobernanza y simulacro", title),
          p("INF-8239 Ciencia de Datos II, Unidad 04 (U04.E08)", subtitle),
          label_table([
              ("Estudiante", "Roque Alexis Ventura Vallejo"),
              ("Matrícula", "100805873"),
              ("Repositorio", f'{link(REPO_URL, "github.com/RoqueVentura/UASD-Maestria-Ciencia-De-Datos")}, Ciencia de datos II/Unidad IV/Ejercicio 08'),
              ("Evidencia", f'{link(EVID_URL, "U04_E08_Evidencias_Roque_Ventura.pdf")} (abrir en GitHub)'),
              ("Base", "LAB13, proyecto INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv"),
              ("Decisión final", "<b>Modificar y limitar</b> (sección 6)"),
          ])]
story.append(p("<b>Caso.</b> El Territorial Review DSS prioriza casos territoriales sintéticos para revisión humana. Solo recomienda "
               "un orden y presenta evidencia; la decisión es humana. Las cifras de este informe se leen de los archivos editables del "
               "repositorio (CSV, YAML y JSON)."))

# ---------------------------------------------------------------- 1. normativa
story += section("1. Obligación legal, marco voluntario y recomendación ética")
story.append(table([
    ["Tipo", "Instrumento", "Aplicación en este caso"],
    ["Obligación legal", "Ley 172-13 de Protección de Datos Personales y Constitución de la República Dominicana",
     "Con datos reales, <i>protected_group</i>, <i>age_band</i> y <i>zone</i> serían datos personales: exigirían base legal, minimización, "
     "conservación limitada y derechos de acceso y rectificación. Con datos sintéticos la obligación no se activa"],
    ["Marco voluntario", "NIST AI RMF 1.0; Model Cards; Datasheets",
     "Estructuran la RACI y los traspasos (GOVERN), el inventario (MAP), el monitoreo (MEASURE), el runbook y el simulacro (MANAGE), "
     "y la documentación del modelo y de los datos"],
    ["Recomendación ética", "Criterio propio",
     f"Revisión humana de todos los casos; evidencia de incidentes sin filas de casos; brechas solo con {mon['min_support']} o más "
     "casos por grupo"],
], [0.17, 0.27, 0.56]))

# ---------------------------------------------------------------- 2. inventario
story += section("2. Inventario, minimización y retención")
story.append(table([
    ["Campos", "Uso", "Minimización"],
    ["name, document_number, email, phone", "Ninguno", "No se recolectan; el contrato rechaza el lote antes de predecir"],
    ["case_id, received_date", "Trazabilidad y corte temporal", "Fuera del modelo; la fecha se agrega a mes en el monitoreo"],
    ["protected_group", "Solo auditoría de equidad", "Fuera del modelo; acceso restringido al equipo de auditoría"],
    ["age_band", "Modelo y auditoría", "Tramos de edad, no fecha de nacimiento"],
    ["zone, previous_incidents, infrastructure_score, exposure", "Modelo", "4 zonas amplias; conteos e índices agregados; zone se vigila como proxy"],
    ["target", "Entrenamiento y evaluación", "Resultado de la revisión humana"],
], [0.36, 0.22, 0.42]))
story.append(table([["Artefacto", "Retención", "Responsable"]] +
                   [[r["artifact"], r["retention"], r["owner"]] for r in retention], [0.38, 0.4, 0.22], style_cell=tiny))
story.append(p("Detalle por campo en <i>student_inputs/data_inventory.csv</i> y por artefacto en <i>student_inputs/retention_policy.csv</i>. "
               "Una prueba verifica que el inventario coincida con el contrato de datos y con las variables del modelo."))

# ---------------------------------------------------------------- 3. datasheet y model card
story += section("3. Datasheet y Model Card trazables")
story.append(p(f"<i>docs/DATASET_CARD.md</i> describe motivación, composición (640 casos, 0 faltantes), preprocesamiento, usos y "
               f"retención. <i>docs/MODEL_CARD.md</i> registra la versión <b>{rec['model_version']}</b>, las puertas, los grupos, el "
               "monitoreo y el simulacro. Cada cifra apunta a su archivo de origen."))
story.append(table([
    ["Puerta", "Valor", "Umbral", "Resultado"],
    ["Recall global", f3(decision["metrics"]["recall"]), f"≥ {gates['min_recall']}", "Pasa"],
    ["Brecha de recall", f3(decision["gaps"]["recall_gap"]), f"≤ {gates['max_recall_gap']}", "Pasa"],
    ["Brecha de FPR", f3(decision["gaps"]["fpr_gap"]), f"≤ {gates['max_fpr_gap']}", "Pasa"],
    ["Latencia y tamaño", f"{decision['resources']['latency_ms']:.2f} ms; {decision['resources']['model_kb']:.1f} KB",
     f"≤ {gates['max_latency_ms']} ms; ≤ {gates['max_model_kb']} KB", "Pasa"],
    ["Recall G1 (vigilancia)", f3(fair_lab13["G1"]["recall"]), "0.68", "<b>Bajo</b>"],
], [0.3, 0.25, 0.27, 0.18], highlight_rows=(5,)))

# ---------------------------------------------------------------- 4. RACI y traspasos
story += section("4. RACI y traspaso entre roles")
story.append(p("Cada actividad tiene un solo Accountable (<i>student_inputs/raci.csv</i>). Los traspasos "
               "(<i>student_inputs/handoffs.csv</i>) definen entregable, criterio de aceptación y firma; una prueba exige que firme "
               "el Accountable de la actividad y que la evidencia exista."))
story.append(table([["Traspaso", "De → a", "Firma (Accountable)"]] +
                   [[h["stage"], f"{h['from_role']} → {h['to_role']}", h["sign_off"]] for h in handoffs],
                   [0.24, 0.48, 0.28], style_cell=tiny))

# ---------------------------------------------------------------- 5. monitoreo, runbook y simulacro
story += section("5. Monitoreo, runbook y simulacro")
story.append(p("<i>configs/monitoring.yml</i> define señales, frecuencia, responsable y acción. Resultado mensual del periodo de prueba "
               "con el modelo base y con el modelo mitigado de E07 (EG):"))
rows = [["Mes", "n (G1/G2)", "Recall", "Brecha recall", "Brecha FPR", "Brecha recall EG", "Brecha FPR EG"]]
for m in ("2026-10", "2026-11", "2026-12"):
    a, b = month[m], month_eg[m]
    gap = (lambda v: f3(v)) if a["support_ok"] == "True" else (lambda v: f"<i>{f3(v)}</i>*")
    rows.append([m, f"{a['n']} ({a['n_G1']}/{a['n_G2']})", f3(a["recall"]), gap(a["recall_gap"]), gap(a["fpr_gap"]),
                 gap(b["recall_gap"]), gap(b["fpr_gap"])])
story.append(table(rows, [0.1, 0.14, 0.1, 0.15, 0.14, 0.19, 0.18], highlight_rows=(2,)))
story.append(p(f"* Menos de {mon['min_support']} casos en un grupo: no se interpreta. Octubre tiene recall {f3(month['2026-10']['recall'])} "
               f"(&lt; {gates['min_recall']}) y noviembre una brecha de recall de {f3(month['2026-11']['recall_gap'])} (&gt; {gates['max_recall_gap']}). "
               f"El modelo mitigado la reduce a {f3(month_eg['2026-11']['recall_gap'])}, pero la brecha de FPR sube a {f3(month_eg['2026-11']['fpr_gap'])}.", tiny))
story.append(p(f"<b>Simulacro</b> (<i>scripts/e08_incident_drill.py</i>): {drill['scenario']}."))
story.append(table([
    ["Métrica", "Lote correcto", "Lote con fallo", "Lote corregido"],
    ["Recall global", f3(d_base["metrics"]["recall"]), f3(d_inc["metrics"]["recall"]), f3(d_rec["metrics"]["recall"])],
    ["Brecha de recall", f3(d_base["gaps"]["recall_gap"]), f3(d_inc["gaps"]["recall_gap"]), f3(d_rec["gaps"]["recall_gap"])],
    ["Recall G1 / G2", f"{f3(fair_lab13['G1']['recall'])} / {f3(fair_lab13['G2']['recall'])}",
     f"{f3(fair_inc['G1']['recall'])} / {f3(fair_inc['G2']['recall'])}", f"{f3(fair_lab13['G1']['recall'])} / {f3(fair_lab13['G2']['recall'])}"],
    ["Decisión", d_base["decision"]["status"], f"<b>{d_inc['decision']['status']}</b> ({', '.join(d_inc['decision']['failed'])})", d_rec["decision"]["status"]],
], [0.25, 0.22, 0.31, 0.22], highlight_rows=(4,)))
story.append(table([
    ["Fase", "Resultado"],
    ["Detección", f"Contrato: un lote con <i>email</i> fue rechazado. PSI global {f3(drill['psi_previous_incidents'])} (no alcanza 0.25); "
     f"ceros en Oeste: {100 * float(profile['Oeste']['share_zero_reference']):.0f} % en la referencia frente a "
     f"{100 * float(profile['Oeste']['share_zero_batch']):.0f} % en el lote. Las puertas pasan a REVIEW"],
    ["Contención y rollback", "REVIEW, cola en FIFO y lote en cuarentena (runbook). Con el lote corregido vuelve a GO; la reactivación requiere firma de la Dirección"],
    ["Evidencia", f"{len(manifest['files'])} archivos con SHA-256, versión y hash del modelo, sin filas de casos (<i>reports/e08/incident_drill/</i>)"],
    ["Comunicación", "Interna y a representantes de personas afectadas, según el runbook (<i>docs/RUNBOOK.md</i>)"],
    ["Postmortem", "Causa, impacto y acciones con responsable y fecha (<i>reports/e08/POSTMORTEM.md</i>)"],
], [0.22, 0.78], style_cell=tiny))

# ---------------------------------------------------------------- 6. decisión
story += section("6. Decisión final")
story.append(table([
    ["Opción", "Decisión", "Razón"],
    ["Desplegar", "No", "El GO agregado oculta fallas por mes, y un fallo de ingesta baja el recall a "
     f"{f3(d_inc['metrics']['recall'])}. Los datos son sintéticos"],
    ["Modificar", "<b>Sí</b>", "Modelo mitigado de E07, regla de calidad de datos por zona y monitoreo mensual de recall y FPR"],
    ["Limitar", "<b>Sí</b>", "Solo piloto, con revisión humana de todos los casos y FIFO como respaldo"],
    ["No utilizar", "No, por ahora", "Se aplica si se cumple la condición de retiro de LAB11"],
], [0.15, 0.14, 0.71], highlight_rows=(2, 3)))
story.append(p("La Dirección de Gestión de Riesgo Territorial (Accountable) firma el despliegue, la suspensión y la reactivación."))

# ---------------------------------------------------------------- 7. pruebas y git
story += section("7. Pruebas y Git")
story.append(p(f"{n_tests} pruebas aprobadas: contrato de datos, privacidad, equidad, gobernanza, app, inventario, retención, traspasos, "
               "monitoreo y simulacro. El historial de commits y las etiquetas <i>u04-lab13</i> y <i>u04-e08</i> están en el "
               "repositorio. La salida de consola está en <i>reports/e08/run_log.txt</i> y en el anexo."))
story.append(Preformatted("uv sync --frozen\nuv run pytest -q\nuv run python scripts/e08_monitoring.py\nuv run python scripts/e08_incident_drill.py", code))

# ---------------------------------------------------------------- 8. IA
story += section("8. Uso de inteligencia artificial")
story.append(label_table([
    ("Herramienta", "Claude Code (Claude Opus 5.5, de Anthropic) en Visual Studio Code, octubre de 2026."),
    ("Mi trabajo", "Ejecuté LAB13 en mi equipo y preparé las capturas de evidencia (anexo, E1–E7). Dirigí el trabajo con la IA: "
     "indiqué qué verificar contra el manual, el mandato y la rúbrica, definí el alcance, elegí el repositorio y la carpeta de "
     "entrega y pedí reutilizar el formato de E07. Revisé cada propuesta antes de aceptarla y pedí cambios: resumir el informe, "
     "limitar las referencias a tres con DOI, dejar solo lo que pide el mandato y reflejar mi participación. Revisé e implementé "
     "los artefactos y sus valores (retención, traspasos, umbrales y decisión final). Ejecuté las pruebas y los scripts, hice los "
     "commits y las etiquetas, detecté los errores al integrar el proyecto en el repositorio del curso, los resolví con la IA e "
     "hice el push."),
    ("Prompts relevantes", "Verificar LAB13 contra el manual y corregir lo faltante. Completar E08 según el mandato y la rúbrica. "
     "Adaptar el formato del PDF de E07 e incluir mis capturas. Diagnosticar los errores al integrar el repositorio."),
    ("Apoyo recibido", "Propuestas de código (monitoreo, simulacro, pruebas y generador del PDF) y de redacción, que revisé y ajusté; "
     "diagnóstico de errores de Git."),
    ("Verificaciones", f"Las {n_tests} pruebas pasan. Las cifras del informe se leen de los CSV y JSON; las comparé con "
     "<i>run_log.txt</i>."),
    ("Correcciones", "(1) La alerta mensual omitía el recall cuando un grupo tenía poco soporte. (2) El PSI global no detectó el fallo "
     "del simulacro; se documentó y se añadió el perfil por zona. (3) Se recortó de las capturas una cuenta corporativa. (4) Al "
     "revisar la primera versión del informe, pedí resumirla y retirar contenido y referencias que el mandato no pedía."),
    ("Responsabilidad", "Los valores y las conclusiones son míos. Puedo explicar cada parte y asumo la responsabilidad de lo entregado."),
], label_width=0.2))

# ---------------------------------------------------------------- 9. referencias
story += section("9. Referencias")
story += [
    p("Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., &amp; Crawford, K. (2021). Datasheets for "
      "datasets. <i>Communications of the ACM, 64</i>(12), 86–92. https://doi.org/10.1145/3458723", hanging),
    p("Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., &amp; Gebru, T. (2019). "
      "Model cards for model reporting. En <i>Proceedings of the Conference on Fairness, Accountability, and Transparency</i> (pp. 220–229). "
      "https://doi.org/10.1145/3287560.3287596", hanging),
    p("National Institute of Standards and Technology. (2023). <i>Artificial Intelligence Risk Management Framework (AI RMF 1.0)</i> "
      "(NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1", hanging),
]

doc = SimpleDocTemplate(str(OUT_MAIN), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.8 * inch, title="U04.E08 · Expediente de gobernanza y simulacro",
                        author="Roque Alexis Ventura Vallejo")
doc.build(story, onFirstPage=footer_for("U04.E08"), onLaterPages=footer_for("U04.E08"))
print("PDF:", OUT_MAIN)


# ================================================================ anexo de evidencias
def evidence(name, heading, text):
    image = Image(str(EVIDENCE / name))
    scale = WIDTH / image.imageWidth
    image.drawWidth, image.drawHeight = image.imageWidth * scale, image.imageHeight * scale
    box = Table([[p(heading, ev_title)], [p(text, ev_text)]], colWidths=[WIDTH],
                style=[("BACKGROUND", (0, 0), (-1, -1), LABEL_BG), ("BOX", (0, 0), (-1, -1), 0.4, RULE),
                       ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 7)])
    return KeepTogether([image, Spacer(1, 4), box, Spacer(1, 14)])


ev = [p("Anexo de evidencias · Ejercicio 08", title),
      p("INF-8239 Ciencia de Datos II, Unidad 04 (U04.E08)", subtitle),
      label_table([
          ("Estudiante", "Roque Alexis Ventura Vallejo (100805873)"),
          ("Informe", f'{link(f"{REPO}/blob/main/{FOLDER}/U04_E08_Roque_Ventura.pdf", "U04_E08_Roque_Ventura.pdf")}'),
          ("Qué contiene", "Capturas de la ejecución de LAB13 en mi equipo (E1–E7) y la salida de consola de E08 (E8)."),
      ])]
ev += section("Capturas de LAB13 · Gobernanza y DSS responsable")
ev.append(p("Ejecuté LAB13 en VS Code el 31 de octubre de 2026. Solo recorté la barra de estado inferior de E1, E2, E3 y E7, que "
            "mostraba datos de una cuenta corporativa; el terminal no se modificó."))
ev.append(evidence("E1.png", "E1. Pruebas y comprobación del entorno al iniciar LAB13",
    "<b>Qué se realiza:</b> <i>uv run pytest -q</i> da 12 pruebas aprobadas. <i>check_environment.py</i> confirma "
    "<i>dataset_status: valid</i>, con 640 filas y 9 columnas. En el explorador está abierta <i>raci.csv</i>, el primer paso de LAB13."))
ev.append(evidence("E2.png", "E2. Pipeline de gobernanza (lab13_governance.py)",
    "<b>Qué se realiza:</b> el pipeline valida la RACI, entrena, audita y evalúa las cinco puertas. Resultado: <i>GO</i> con "
    "<i>failed: []</i>. Es la fuente de la sección 3 del informe."))
ev.append(evidence("E3.png", "E3. Simulacro de LAB13 (simulate_incident.py)",
    "<b>Qué se realiza:</b> el script del curso genera <i>reports/lab13/INCIDENT_POSTMORTEM.md</i> como plantilla con campos REPLACE, "
    "completada después. En E08 se complementa con un simulacro reproducible (sección 5 del informe y E8)."))
ev.append(evidence("E4.png", "E4. Inicio del tablero (streamlit run app.py)",
    "<b>Qué se realiza:</b> Streamlit levanta el servidor en el puerto 8501 y avisa que <i>use_container_width</i> está obsoleto; se "
    "corrigió en <i>app.py</i>."))
ev.append(evidence("E5.png", "E5. Tablero del DSS en el navegador",
    "<b>Qué se realiza:</b> la app muestra el aviso de caso sintético, el propósito, los usos prohibidos, accuracy 0.719, recall 0.717, "
    "decisión GO, métricas por grupo y puertas. Después se añadió la recomendación con versión, política, evidencia y acción humana."))
ev.append(evidence("E6.png", "E6. Pruebas al cerrar LAB13",
    f"<b>Qué se realiza:</b> 19 pruebas aprobadas. Con las correcciones posteriores y E08 pasan a {n_tests} (E8)."))
ev.append(evidence("E7.png", "E7. Preparación de la publicación (uv export)",
    "<b>Qué se realiza:</b> el primer intento falla por un comando incompleto; el segundo resuelve 55 paquetes y genera "
    "<i>requirements.txt</i> sin dependencias de desarrollo ni secretos."))
ev += section("E8. Salida de consola de E08")
ev.append(p("<b>Qué se realiza:</b> pruebas, comprobación del entorno, pipeline de gobernanza, monitoreo mensual y simulacro. Texto "
            "copiado sin cambios de <i>reports/e08/run_log.txt</i>."))
# Long console lines are wrapped (not cut) so no output is lost at the page margin.
wrapped = "\n".join("\n    ".join(textwrap.wrap(line, 128, drop_whitespace=False)) or line
                    for line in run_log.replace("\r", "").strip().splitlines())
ev.append(Preformatted(wrapped, code))
ev.append(p("<b>Manifiesto de evidencia del simulacro</b> (<i>reports/e08/incident_drill/manifest.json</i>):", ev_title))
ev.append(Preformatted(json.dumps(manifest, indent=2), code))

doc = SimpleDocTemplate(str(OUT_EVID), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.8 * inch, title="U04.E08 · Anexo de evidencias", author="Roque Alexis Ventura Vallejo")
doc.build(ev, onFirstPage=footer_for("U04.E08 · Anexo de evidencias"), onLaterPages=footer_for("U04.E08 · Anexo de evidencias"))
print("PDF:", OUT_EVID)
