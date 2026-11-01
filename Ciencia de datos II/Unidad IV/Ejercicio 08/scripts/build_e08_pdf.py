"""Genera U04_E08_Roque_Ventura.pdf y U04_E08_Evidencias_Roque_Ventura.pdf a partir de los artefactos del repositorio.
Uso: uv run --with reportlab --with pillow python scripts/build_e08_pdf.py
Mismo formato que el informe de E07."""
import csv
import json
import re
import subprocess
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
tiny = ParagraphStyle("tiny", parent=small, fontSize=7.6, leading=9.4)
head = ParagraphStyle("head", parent=small, fontName="Arial-Bold", textColor=colors.white)
title = ParagraphStyle("title", fontName="Arial-Bold", fontSize=19, leading=23, textColor=BLUE, alignment=TA_CENTER)
subtitle = ParagraphStyle("subtitle", fontName="Arial", fontSize=10.5, leading=13, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)
h1 = ParagraphStyle("h1", fontName="Arial-Bold", fontSize=13.5, leading=17, textColor=BLUE, spaceBefore=10, spaceAfter=2, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Arial-Bold", fontSize=10.5, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=2, keepWithNext=1)
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


def table(rows, widths, bold_rows=(), highlight_rows=(), style_cell=cell):
    data = [[p(str(c), head) for c in rows[0]]] + [[p(str(c), style_cell) for c in row] for row in rows[1:]]
    for r in bold_rows:
        data[r] = [p(f"<b>{c}</b>", style_cell) for c in rows[r]]
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


def read_yaml(path):
    return yaml.safe_load((PROJECT / path).read_text(encoding="utf-8"))


f3 = lambda v: "—" if v in ("", None) else f"{np.round(float(v), 3):.3f}"
code_path = lambda s: f"<i>{s}</i>"

# ---------------------------------------------------------------- datos
gov, mon = read_yaml("configs/governance.yml"), read_yaml("configs/monitoring.yml")
gates = gov["gates"]
inventory, retention = read_csv("student_inputs/data_inventory.csv"), read_csv("student_inputs/retention_policy.csv")
raci, handoffs = read_csv("student_inputs/raci.csv"), read_csv("student_inputs/handoffs.csv")
decision = read_json("reports/lab13/deployment_decision.json")
monthly, monthly_eg = read_csv("reports/e08/monitoring_by_month.csv"), read_csv("reports/e08/monitoring_by_month_expgrad.csv")
drift = {r["feature"]: r["psi"] for r in read_csv("reports/e08/drift_psi.csv")}
drill = read_json("reports/e08/incident_drill/timeline.json")
d_base, d_inc = read_json("reports/e08/incident_drill/decision_baseline.json"), read_json("reports/e08/incident_drill/decision_incident.json")
d_rec = read_json("reports/e08/incident_drill/decision_recovered.json")
manifest = read_json("reports/e08/incident_drill/manifest.json")
profile = {r["zone"]: r for r in read_csv("reports/e08/incident_drill/batch_profile.csv")}
fair_inc = {r["protected_group"]: r for r in read_csv("reports/e08/incident_drill/fairness_incident.csv")}
fair_lab13 = {r["protected_group"]: r for r in read_csv("reports/lab13/fairness_by_group.csv")}
mit = {r["variant"]: r for r in read_csv("reports/e07/mitigation_comparison.csv")}
boot = read_json("reports/e07/bootstrap_gaps.json")["intervals_95"]
rec = decision["recommendation"]
month = {r["month"]: r for r in monthly}
month_eg = {r["month"]: r for r in monthly_eg}
git_log = subprocess.run(["git", "log", "--oneline", "-12"], cwd=PROJECT, capture_output=True, text=True, encoding="utf-8").stdout.strip()
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
              ("Base", "LAB13 sobre LAB11, LAB12 y E07, proyecto INF8239_U04_Gobernanza_DSS_Proyecto_Base_uv (uv, Python 3.12, Streamlit 1.64)"),
              ("Decisión final", "<b>Modificar y limitar</b> (sección 6)"),
          ])]
story.append(p("<b>Caso.</b> El Territorial Review DSS ordena casos territoriales sintéticos para que un analista decida cuáles revisar "
               "primero. El DSS solo prioriza y presenta evidencia: no declara emergencias, culpabilidad ni elegibilidad, ni interviene "
               "de forma automática. Este expediente integra la evidencia de LAB13: inventario de datos, datasheet, model card, RACI, "
               "monitoreo, runbook y un simulacro reproducible. Todas las cifras salen de archivos editables del repositorio (CSV, YAML y "
               "JSON), generados con semilla 42; ninguna se escribió a mano en este informe."))

# ---------------------------------------------------------------- 1. normativa
story += section("1. Obligación legal, marco voluntario y recomendación ética")
story.append(table([
    ["Tipo", "Instrumento", "Qué exige o propone", "Aplicación en este expediente"],
    ["Obligación legal", "Ley 172-13 de Protección de Datos Personales (República Dominicana)",
     "Calidad y finalidad de los datos, consentimiento o base legal, derechos de acceso, rectificación y supresión, y conservar los datos "
     "solo mientras sean necesarios", "Con datos reales, <i>case_id</i>, <i>zone</i>, <i>protected_group</i> y <i>age_band</i> serían datos "
     "personales. El inventario y la política de retención (sección 2) preparan ese cumplimiento. Con datos sintéticos la obligación no se activa"],
    ["Obligación legal", "Constitución de la República Dominicana", "Igualdad, intimidad y habeas data",
     "Una brecha sistemática contra un grupo obligaría a corregir. La apelación ante un supervisor independiente da una vía de revisión"],
    ["Marco voluntario", "NIST AI RMF 1.0", "GOVERN, MAP, MEASURE y MANAGE",
     "RACI y traspasos (GOVERN), inventario (MAP), monitoreo (MEASURE), runbook y simulacro (MANAGE)"],
    ["Marco voluntario", "Model Cards (Mitchell et al.) y Datasheets (Gebru et al.)", "Documentar propósito, evaluación, límites y datos",
     f"{code_path('docs/MODEL_CARD.md')} y {code_path('docs/DATASET_CARD.md')}, enlazados a sus fuentes"],
    ["Recomendación ética", "Criterio propio",
     "Va más allá de lo exigido", "Revisión humana de todos los casos; evidencia de incidentes sin filas de casos; brechas solo con "
     f"{mon['min_support']} o más casos por grupo; vigilar también la FPR del modelo mitigado; avisar a las personas afectadas aunque "
     "la causa sea técnica"],
], [0.17, 0.19, 0.27, 0.37]))
story.append(p("<b>Distinción.</b> La ley obliga, aunque aquí no se active por ser datos sintéticos. NIST, Model Cards y Datasheets son "
               "voluntarios: los adopto porque ordenan la evidencia. Las recomendaciones éticas son decisiones mías, y las justifico por "
               "el daño priorizado: no detectar un caso real o cargar a un grupo con alertas falsas."))

# ---------------------------------------------------------------- 2. inventario
story += section("2. Inventario, minimización y retención")
story.append(p(f"El inventario ({code_path('student_inputs/data_inventory.csv')}) cubre las 9 columnas del dataset y los 4 identificadores "
               "directos prohibidos. Una prueba verifica que coincida con el contrato y con las variables que entran al modelo."))
story.append(table([["Campo", "Categoría", "Modelo", "Auditoría", "Minimización", "Acceso"]] +
                   [[r["field"], r["category"], r["used_in_model"], r["used_in_audit"], r["minimization"], r["access"]] for r in inventory],
                   [0.18, 0.16, 0.09, 0.1, 0.28, 0.19], style_cell=tiny,
                   highlight_rows=[i + 1 for i, r in enumerate(inventory) if r["field"] == "protected_group"]))
story.append(p("<b>Minimización aplicada.</b> (1) <i>protected_group</i> no entra al modelo y solo lo ve el equipo de auditoría. (2) La edad "
               "llega en tramos, no como fecha de nacimiento. (3) La geografía se limita a 4 zonas amplias. (4) Los identificadores "
               "directos ni se recolectan: el contrato rechaza el lote antes de predecir. (5) La evidencia del simulacro guarda solo "
               "agregados y hashes, nunca filas de casos. Riesgo que queda: <i>zone</i> y <i>age_band</i> pueden actuar como proxy del grupo."))
story.append(table([["Artefacto", "Datos personales", "Retención", "Eliminación", "R / A"]] +
                   [[r["artifact"], r["contains_personal_data"], r["retention"], r["disposal"], f"{r['owner']} / {r['accountable']}"]
                    for r in retention], [0.22, 0.15, 0.24, 0.17, 0.22], style_cell=tiny))
story.append(p("<b>Criterio de retención.</b> Cada plazo se ata a una finalidad: rollback (modelo vigente y 2 anteriores), apelación (24 "
               "meses), auditoría (vida del sistema y 3 años) o investigación de incidentes (3 años). Pasado el plazo se borra o se "
               "conservan solo métricas agregadas. Los plazos son una propuesta de política interna y no salen de la Ley 172-13, que "
               "exige limitar la conservación pero no fija años."))

# ---------------------------------------------------------------- 3. datasheet y model card
story += section("3. Datasheet y Model Card trazables")
story.append(p(f"La versión evaluada es <b>{rec['model_version']}</b> (modelo, versión de scikit-learn y commit). La recomendación de "
               f"{code_path('reports/lab13/deployment_decision.json')} incluye esa versión, la política, las puertas fallidas y la acción "
               "humana requerida. La app la muestra en la sección «Recomendación gobernada»."))
gate_rows = [["Puerta", "Valor", "Umbral", "Resultado", "Fuente"],
             ["Recall global", f3(decision["metrics"]["recall"]), f"≥ {gates['min_recall']}", "Pasa", "deployment_decision.json"],
             ["Brecha de recall", f3(decision["gaps"]["recall_gap"]), f"≤ {gates['max_recall_gap']}", "Pasa", "deployment_decision.json"],
             ["Brecha de FPR", f3(decision["gaps"]["fpr_gap"]), f"≤ {gates['max_fpr_gap']}", "Pasa", "deployment_decision.json"],
             ["Latencia por caso", f"{decision['resources']['latency_ms']:.2f} ms", f"≤ {gates['max_latency_ms']} ms", "Pasa", "deployment_decision.json"],
             ["Tamaño del modelo", f"{decision['resources']['model_kb']:.1f} KB", f"≤ {gates['max_model_kb']} KB", "Pasa", "deployment_decision.json"],
             ["Recall G1", f3(fair_lab13["G1"]["recall"]), "vigilancia 0.68", "<b>Bajo</b>", "fairness_by_group.csv"]]
story.append(table(gate_rows, [0.2, 0.13, 0.16, 0.12, 0.39], highlight_rows=(6,)))
story.append(table([
    ["Afirmación", "Documento", "Evidencia que la respalda"],
    ["640 casos, 0 faltantes, sin identificadores directos", "Datasheet", "describe_dataset.py; tests/test_data.py; tests/test_privacy.py"],
    ["Corte temporal: entrenamiento hasta 2026-09-24, prueba de 160 casos", "Datasheet y Model Card", "src/inf8239_u04/data.py; describe_dataset.py"],
    ["Variables del modelo sin <i>protected_group</i>", "Datasheet e inventario", "data_inventory.csv; tests/test_e08.py"],
    ["Puertas en GO y recall de G1 bajo 0.68", "Model Card", "reports/lab13/deployment_decision.json y fairness_by_group.csv"],
    ["Intervalo de la brecha de recall (bootstrap)", "Model Card",
     f"reports/e07/bootstrap_gaps.json: {f3(boot['logistic_t0.50']['recall_gap']['p2.5'])} a {f3(boot['logistic_t0.50']['recall_gap']['p97.5'])}"],
    ["Fallas por mes y simulacro", "Model Card (sección E08)", "reports/e08/monitoring_by_month*.csv; reports/e08/POSTMORTEM.md"],
    ["Retención y responsable de los datos", "Datasheet", "retention_policy.csv; raci.csv"],
], [0.38, 0.2, 0.42]))

# ---------------------------------------------------------------- 4. RACI y traspasos
story += section("4. RACI y traspaso entre roles")
story.append(table([["Actividad", "Responsible", "Accountable", "Consulted", "Informed"]] +
                   [[r["activity"], r["R"], r["A"], r["C"], r["I"]] for r in raci], [0.24, 0.18, 0.2, 0.19, 0.19], style_cell=tiny))
story.append(p("Cada actividad tiene un solo Accountable; <i>validate_raci</i> rechaza una actividad con dos. Los traspasos "
               f"({code_path('student_inputs/handoffs.csv')}) indican qué recibe cada rol, con qué criterio lo acepta y quién firma. Una "
               "prueba comprueba que firma el Accountable de la actividad en la RACI y que los archivos de evidencia existen."))
story.append(table([["Traspaso", "De → a", "Criterio de aceptación", "Firma"]] +
                   [[h["stage"], f"{h['from_role']} → {h['to_role']}", h["acceptance_criteria"], h["sign_off"]] for h in handoffs],
                   [0.17, 0.27, 0.36, 0.2], style_cell=tiny))
story.append(p("<b>Punto crítico.</b> El traspaso 6 (operación a monitoreo) depende de que los analistas registren el resultado de cada "
               "revisión. Sin ese registro no hay etiquetas, y el recall y las brechas no se pueden medir. Por eso es el único traspaso "
               "que firma el Supervisor de analistas y no la Dirección ni el Líder del equipo de datos."))

# ---------------------------------------------------------------- 5. monitoreo, runbook y simulacro
story += section("5. Monitoreo, runbook y simulacro")
story.append(p(f"El plan ({code_path('configs/monitoring.yml')}) define 7 señales con frecuencia, responsable, Accountable y acción. Las "
               "señales que no requieren etiquetas (contrato, deriva, latencia y casos sin revisión) actúan de inmediato. Las de "
               "desempeño y equidad esperan a que los casos revisados tengan resultado."))
story.append(table([["Señal", "Frecuencia", "Etiquetas", "R / A", "Acción"]] +
                   [[s["name"], s["when"], "Sí" if s["needs_labels"] else "No", f"{s['owner']} / {s['accountable']}", s["action"]]
                    for s in mon["signals"]], [0.24, 0.14, 0.11, 0.24, 0.27], style_cell=tiny))
h2_rows = [["Mes", "n (G1/G2)", "Recall", "Brecha recall", "Brecha FPR", "Recall EG", "Brecha recall EG", "Brecha FPR EG"]]
for m in ("2026-09", "2026-10", "2026-11", "2026-12"):
    a, b = month[m], month_eg[m]
    ok = a["support_ok"] == "True"
    gap = lambda v: f3(v) if ok else f"<i>{f3(v)}</i>*"
    h2_rows.append([m, f"{a['n']} ({a['n_G1']}/{a['n_G2']})", f3(a["recall"]), gap(a["recall_gap"]), gap(a["fpr_gap"]),
                    f3(b["recall"]), gap(b["recall_gap"]), gap(b["fpr_gap"])])
story.append(p("<b>Monitoreo mensual del periodo de prueba</b> (modelo base y modelo mitigado de E07, EG):", h2))
story.append(table(h2_rows, [0.1, 0.14, 0.1, 0.13, 0.12, 0.11, 0.15, 0.15], highlight_rows=(2, 3)))
story.append(p(f"* Menos de {mon['min_support']} casos en algún grupo: la brecha se informa, pero no se interpreta. El PSI máximo frente "
               f"al entrenamiento es de {f3(max(drift.values()))} (<i>previous_incidents</i>), bajo el umbral de vigilancia de "
               f"{mon['thresholds']['psi_watch']:.2f}.", tiny))
story.append(p(f"<b>Lectura.</b> El GO agregado oculta fallas por mes. Con el modelo base, octubre tiene un recall de {f3(month['2026-10']['recall'])} "
               f"y noviembre, el único mes con soporte suficiente, una brecha de recall de {f3(month['2026-11']['recall_gap'])}, por encima "
               f"de {gates['max_recall_gap']}. El modelo mitigado corrige esa brecha ({f3(month_eg['2026-11']['recall_gap'])}), pero traslada "
               f"el costo a la FPR: la brecha de FPR sube a {f3(month_eg['2026-11']['fpr_gap'])} y G1 recibe más alertas falsas. La "
               "mitigación cambia quién carga el error y qué error carga; no lo elimina."))

story.append(p("<b>Simulacro reproducible</b> (<i>scripts/e08_incident_drill.py</i>)", h2))
story.append(p(f"<b>Escenario:</b> {drill['scenario']}. El fallo es técnico y neutral: no toca ningún atributo protegido."))
ib, ii, ir = d_base, d_inc, d_rec
story.append(table([
    ["Métrica", "Lote correcto", "Lote con fallo", "Lote corregido", "Umbral"],
    ["Recall global", f3(ib["metrics"]["recall"]), f3(ii["metrics"]["recall"]), f3(ir["metrics"]["recall"]), f"≥ {gates['min_recall']}"],
    ["Brecha de recall", f3(ib["gaps"]["recall_gap"]), f3(ii["gaps"]["recall_gap"]), f3(ir["gaps"]["recall_gap"]), f"≤ {gates['max_recall_gap']}"],
    ["Brecha de FPR", f3(ib["gaps"]["fpr_gap"]), f3(ii["gaps"]["fpr_gap"]), f3(ir["gaps"]["fpr_gap"]), f"≤ {gates['max_fpr_gap']}"],
    ["Recall G1 / G2", f"{f3(fair_lab13['G1']['recall'])} / {f3(fair_lab13['G2']['recall'])}",
     f"{f3(fair_inc['G1']['recall'])} / {f3(fair_inc['G2']['recall'])}", f"{f3(fair_lab13['G1']['recall'])} / {f3(fair_lab13['G2']['recall'])}", "—"],
    ["Decisión", ib["decision"]["status"], f"<b>{ii['decision']['status']}</b> ({', '.join(ii['decision']['failed'])})", ir["decision"]["status"], "—"],
], [0.2, 0.18, 0.26, 0.18, 0.18], highlight_rows=(5,)))
story.append(table([
    ["Fase del runbook", "Qué ocurrió en el simulacro", "Responsable"],
    ["Detección (contrato)", f"Lote con la columna email, {drill['contract_check'].replace(': ', ' antes de predecir (', 1)})", "Ingeniero de datos"],
    ["Detección (sin etiquetas)", f"PSI global {f3(drill['psi_previous_incidents'])}: solo vigilancia. Ceros en Oeste: "
     f"{100 * float(profile['Oeste']['share_zero_reference']):.0f} % en la referencia frente a {100 * float(profile['Oeste']['share_zero_batch']):.0f} % "
     f"en el lote. PSI por zona: Oeste {f3(profile['Oeste']['psi_previous_incidents'])}, pero también Norte {f3(profile['Norte']['psi_previous_incidents'])} "
     f"y Sur {f3(profile['Sur']['psi_previous_incidents'])} sin fallo (ruido por n pequeño)", "Ingeniero de ML"],
    ["Detección (con etiquetas)", f"REVIEW; puertas fallidas {', '.join(ii['decision']['failed'])}", "Ingeniero de ML"],
    ["Contención", "REVIEW, cola en FIFO y lote en cuarentena; la Dirección confirma el mismo día hábil",
     "Ingeniero de ML; Científico de datos (A: Dirección)"],
    ["Preservación", f"{len(manifest['files'])} archivos con SHA-256, versión {manifest['model_version']} y hash del modelo; sin filas de casos",
     "Científico de datos"],
    ["Comunicación", "Interna y a representantes de personas afectadas, con la vía de apelación; sin atribuir causas antes del análisis",
     "Responsable de producto"],
    ["Rollback y recuperación", "Lote corregido: GO de nuevo. El modelo se reactiva solo con una nueva firma de la Dirección", "Ingeniero de datos"],
    ["Postmortem", "6 acciones con responsable y fecha (reports/e08/POSTMORTEM.md)", "Científico de datos (A: Dirección)"],
], [0.2, 0.55, 0.25], style_cell=tiny))
story.append(p("<b>Lección.</b> Un fallo en una sola zona se diluye en el PSI global, igual que el recall global ocultaba el de G1. El PSI "
               "por zona lo detecta, pero con muestras pequeñas da falsos positivos. La señal limpia fue una regla de calidad de datos "
               "(proporción de ceros por zona frente a la referencia), que es la acción correctiva 1. Además, el fallo perjudicó más a "
               "G1 aunque no tocó el grupo: un error técnico neutral puede producir un daño desigual."))

# ---------------------------------------------------------------- 6. decisión
story += section("6. Decisión final")
story.append(table([
    ["Opción", "Decisión", "Razón"],
    ["Desplegar", "No", f"El GO agregado oculta fallas por mes (recall de octubre {f3(month['2026-10']['recall'])}; brecha de noviembre "
     f"{f3(month['2026-11']['recall_gap'])}). El simulacro muestra que un fallo de ingesta lleva el recall a {f3(ii['metrics']['recall'])}. Los datos son sintéticos"],
    ["Modificar", "<b>Sí</b>", "Modelo mitigado de E07, más una regla de calidad de datos por zona y monitoreo mensual de recall y FPR con soporte mínimo"],
    ["Limitar", "<b>Sí</b>", "Solo piloto, con revisión humana de todos los casos, FIFO con reglas como respaldo y sin uso para elegibilidad, "
     "intervención ni declaración de emergencias"],
    ["No utilizar", "No, por ahora", f"Se aplica si en el piloto se cumple la condición de retiro de LAB11. La brecha de FPR de {f3(month_eg['2026-11']['fpr_gap'])} "
     "del modelo mitigado en noviembre sería, en producción, un incidente de clase alta según el runbook"],
], [0.15, 0.13, 0.72], highlight_rows=(2, 3)))
story.append(p("<b>Responsable.</b> La Dirección de Gestión de Riesgo Territorial firma el despliegue, la suspensión y la reactivación "
               "(Accountable en la RACI). La recomendación del DSS es solo un insumo: la decisión es humana y queda registrada."))

# ---------------------------------------------------------------- 7. artefactos, pruebas y git
story += section("7. Artefactos, pruebas y Git")
story.append(table([
    ["Ruta", "Contenido"],
    ["student_inputs/", "Inventario, retención, RACI y traspasos (más los insumos de LAB11 y LAB12)"],
    ["configs/", "governance.yml (usos prohibidos y puertas) y monitoring.yml (plan de monitoreo)"],
    ["docs/", "Datasheet, Model Card, Runbook y declaración de IA"],
    ["src/inf8239_u04/monitoring.py", "PSI, reporte mensual por grupo y alertas"],
    ["scripts/e08_*.py", "Monitoreo y simulacro reproducibles"],
    ["reports/e08/", "Monitoreo, simulacro con manifiesto SHA-256, postmortem, capturas y salida de consola (run_log.txt)"],
    ["app.py", "Tablero Streamlit con propósito, límites, métricas, grupos, puertas, recomendación y acción humana"],
    ["tests/", f"{n_tests} pruebas, todas aprobadas: contratos, privacidad, equidad, gobernanza, app, mitigación, inventario, retención, traspasos, monitoreo y simulacro"],
], [0.3, 0.7]))
story.append(Preformatted("uv sync --frozen\nuv run pytest -q\nuv run python scripts/lab13_governance.py\nuv run python scripts/e08_monitoring.py\n"
                          "uv run python scripts/e08_incident_drill.py\nuv run streamlit run app.py", code))
story.append(p("<b>Historial de Git del proyecto</b> (al generar este PDF; la etiqueta <i>u04-lab13</i> marca el cierre de LAB13):", h2))
story.append(Preformatted(git_log, code))

# ---------------------------------------------------------------- 8. IA
story += section("8. Uso de inteligencia artificial")
story.append(label_table([
    ("Herramienta", "Claude Code (Claude Opus 5.5, de Anthropic) en Visual Studio Code, octubre de 2026."),
    ("Mi trabajo", "Ejecuté LAB13 en mi equipo (anexo, E1–E7): pruebas, pipeline de gobernanza, simulacro, tablero y exportación de "
     "dependencias. Completé la RACI y revisé los umbrales. Fijé los valores de gobernanza de E08: plazos de retención, criterios de "
     "cada traspaso, umbrales de PSI y la decisión final. Hice los commits y el push."),
    ("Prompts relevantes", "Verificar LAB13 contra el manual y corregir lo faltante. Completar E08 según el mandato y la rúbrica. "
     "Adaptar el formato del PDF de E07. Generar el anexo con mis capturas."),
    ("Apoyo recibido", "Recomendación trazable y validación de un único Accountable en LAB13; propuesta de inventario, retención, "
     "traspasos y plan de monitoreo; código de monitoreo, simulacro y pruebas; redacción del datasheet y del postmortem; generador de este PDF."),
    ("Verificaciones", f"Las {n_tests} pruebas pasan. Las cifras de este informe se leen de los CSV y JSON al generarlo; no se copiaron a "
     "mano. Comparé con reports/e08/run_log.txt. Los traspasos se validan contra la RACI de forma automática."),
    ("Correcciones", "(1) Las alertas omitían el recall mensual cuando un grupo tenía poco soporte; al corregirlo apareció la falla de "
     "octubre. (2) El PSI global no detectó el simulacro; se documentó en lugar de ocultarlo. (3) Se mostró que el PSI por zona da falsos "
     "positivos con muestras pequeñas. (4) Se midió el modelo mitigado y apareció el traslado del daño a la FPR. (5) Se recortó de las capturas "
     "una cuenta corporativa."),
    ("Responsabilidad", "Los valores del análisis (retención, criterios de aceptación, tolerancias y decisión final) son míos. Puedo "
     "explicar cada parte y asumo la responsabilidad de lo entregado."),
], label_width=0.2))

# ---------------------------------------------------------------- 9. referencias
story += section("9. Referencias")
story += [
    p("Congreso Nacional de la República Dominicana. (2013). <i>Ley núm. 172-13 que tiene por objeto la protección integral de los datos "
      "personales asentados en archivos, registros públicos, bancos de datos u otros medios técnicos de tratamiento de datos destinados a "
      "dar informes, sean estos públicos o privados</i>.", hanging),
    p("Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., &amp; Crawford, K. (2021). Datasheets for "
      "datasets. <i>Communications of the ACM, 64</i>(12), 86–92. https://doi.org/10.1145/3458723", hanging),
    p("Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., &amp; Gebru, T. (2019). "
      "Model cards for model reporting. En <i>Proceedings of the Conference on Fairness, Accountability, and Transparency</i> (pp. 220–229). "
      "https://doi.org/10.1145/3287560.3287596", hanging),
    p("National Institute of Standards and Technology. (2023). <i>Artificial Intelligence Risk Management Framework (AI RMF 1.0)</i> "
      "(NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1", hanging),
    p("Siddiqi, N. (2006). <i>Credit risk scorecards: Developing and implementing intelligent credit scoring</i>. Wiley. (Convención de "
      "umbrales de PSI 0.10 y 0.25)", hanging),
    p("Streamlit. (s. f.). <i>App testing</i> (st.testing.v1.AppTest). Documentación oficial. https://docs.streamlit.io/develop/api-reference/app-testing", hanging),
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
          ("Qué contiene", "Capturas de la ejecución de LAB13 en mi equipo (E1–E7) y la salida de consola de E08 (E8). Cada evidencia "
           "indica qué se realiza y qué parte del mandato o de la rúbrica respalda."),
      ])]
ev += section("Capturas de LAB13 · Gobernanza y DSS responsable")
ev.append(p("Ejecuté LAB13 en VS Code el 31 de octubre de 2026, en Unidad IV/Ejercicio 08. Solo recorté la barra de estado inferior de "
            "E1, E2, E3 y E7, que mostraba datos de una cuenta corporativa; el terminal no se modificó. Las capturas son del estado de "
            "LAB13 antes de las correcciones y de E08; el estado final se ve en la salida de consola E8."))
ev.append(evidence("E1.png", "E1. Pruebas y comprobación del entorno al iniciar LAB13",
    "<b>Qué se realiza:</b> <i>uv run pytest -q</i> da 12 pruebas aprobadas, el estado heredado de E07. <i>check_environment.py</i> "
    "confirma <i>dataset_status: valid</i>, con 640 filas y 9 columnas. En el explorador está abierta <i>raci.csv</i>, el primer paso de "
    "LAB13. <b>Rúbrica:</b> pruebas y Git. El contrato técnico se cumple, pero eso no demuestra que los datos sirvan para una decisión real."))
ev.append(evidence("E2.png", "E2. Pipeline de gobernanza (lab13_governance.py)",
    "<b>Qué se realiza:</b> el pipeline valida la RACI, carga los datos, entrena, audita y evalúa las cinco puertas: recall, brecha de "
    "recall, brecha de FPR, latencia y tamaño. Resultado: <i>GO</i> con <i>failed: []</i>. <b>Rúbrica:</b> Model Card trazable; esta "
    "decisión es la fuente de la sección 3 del informe."))
ev.append(evidence("E3.png", "E3. Simulacro de LAB13 (simulate_incident.py)",
    "<b>Qué se realiza:</b> el script del curso genera <i>reports/lab13/INCIDENT_POSTMORTEM.md</i> como plantilla con campos REPLACE, que "
    "después completé. En E08 lo sustituí por un simulacro reproducible que mide el impacto (sección 5 del informe y E8). "
    "<b>Rúbrica:</b> monitoreo, runbook y simulacro."))
ev.append(evidence("E4.png", "E4. Inicio del tablero (streamlit run app.py)",
    "<b>Qué se realiza:</b> Streamlit levanta el servidor en el puerto 8501. Aparece un aviso de que <i>use_container_width</i> está "
    "obsoleto; lo corregí en <i>app.py</i> (en Streamlit 1.64, <i>width</i> ya es <i>stretch</i> por defecto). <b>Rúbrica:</b> calidad "
    "documental y corrección verificable."))
ev.append(evidence("E5.png", "E5. Tablero del DSS en el navegador",
    "<b>Qué se realiza:</b> la app muestra el aviso de caso sintético, el propósito, los usos prohibidos, accuracy 0.719, recall 0.717, "
    "decisión GO, las métricas por grupo (recall G1 0.6531 frente a G2 0.7907) y las puertas. Después añadí el límite de autoridad y la "
    "«Recomendación gobernada» con versión, política, evidencia y acción humana. <b>Mandato:</b> el DSS asiste, pero no sustituye, la decisión humana."))
ev.append(evidence("E6.png", "E6. Pruebas al cerrar LAB13",
    "<b>Qué se realiza:</b> 19 pruebas aprobadas tras completar la RACI, la Model Card y el Runbook. Con las correcciones de LAB13 "
    f"(columna faltante, un único Accountable, trazabilidad y app) y las de E08 pasan a {n_tests} (E8). <b>Rúbrica:</b> pruebas y Git."))
ev.append(evidence("E7.png", "E7. Preparación de la publicación (uv export)",
    "<b>Qué se realiza:</b> el primer intento falla por un comando incompleto (<i>For more information, try '--help'</i>). El segundo "
    "resuelve 55 paquetes y genera <i>requirements.txt</i> con hashes para Streamlit Community Cloud, sin dependencias de desarrollo ni "
    "secretos. <b>Mandato:</b> publicación segura y reproducible."))
ev += section("E8. Salida de consola de E08")
ev.append(p("<b>Qué se realiza:</b> se ejecutan las pruebas, la comprobación del entorno, el pipeline de gobernanza, el monitoreo mensual "
            "(modelo base y mitigado), el simulacro y la protección del postmortem completado. La salida es texto copiado sin cambios de "
            "<i>reports/e08/run_log.txt</i>, reproducible con los mismos comandos. <b>Mandato:</b> evidencia editable, no solo capturas."))
# Long console lines are wrapped (not cut) so no output is lost at the page margin.
wrapped = "\n".join("\n    ".join(textwrap.wrap(line, 128, drop_whitespace=False)) or line
                    for line in run_log.replace("\r", "").strip().splitlines())
ev.append(Preformatted(wrapped, code))
ev.append(p("<b>Manifiesto de evidencia del simulacro</b> (<i>reports/e08/incident_drill/manifest.json</i>):", h2))
ev.append(Preformatted(json.dumps(manifest, indent=2), code))

doc = SimpleDocTemplate(str(OUT_EVID), pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.8 * inch, title="U04.E08 · Anexo de evidencias", author="Roque Alexis Ventura Vallejo")
doc.build(ev, onFirstPage=footer_for("U04.E08 · Anexo de evidencias"), onLaterPages=footer_for("U04.E08 · Anexo de evidencias"))
print("PDF:", OUT_EVID)
