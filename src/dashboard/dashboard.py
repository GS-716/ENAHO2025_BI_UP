"""
Dashboard ENAHO 2025 - Bienestar habitacional y servicios básicos
=================================================================
Versión narrativa y densa (grilla de 6 columnas). Reutiliza las funciones de
graficos_enaho_bienestar.py y les aplica un tema visual unificado.

Layout: banda de KPIs (5) + grilla maestra de 6 columnas. Cada gráfico declara
su ancho en sextos (span). Los encabezados de sección ocupan la fila completa.

Requisitos:  pip install dash
Entorno:     export NEON_USER="neondb_owner" ; export NEON_PASS="tu_password"
Ejecutar:    python app_dash_enaho.py   ->  http://127.0.0.1:8050
"""

import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from dotenv import load_dotenv

from dashboardgraficos import (
    conexion_db, cargar_base, GRAFICOS, pct_global, carencias_limpias,
)
load_dotenv()
# ---------------------------------------------------------------------------
# Paleta y tipografía
# ---------------------------------------------------------------------------
FUENTE = "Inter, system-ui, -apple-system, Segoe UI, sans-serif"
TINTA = "#1f2937"
GRIS = "#6b7280"
ACENTO = "#0e7490"
ALERTA = "#b91c1c"
BORDE = "#e8eaed"
FONDO = "#f1f3f5"
SOMBRA = "rgba(0,0,0,0.08) 0px 2px 6px"


# ---------------------------------------------------------------------------
# 1. Carga única
# ---------------------------------------------------------------------------
def cargar_datos():
    usuario = os.getenv("NEON_USER", "neondb_owner")
    contra = os.getenv("NEON_PASS")
    if not contra:
        raise SystemExit("Falta la variable de entorno NEON_PASS.")
    conn = conexion_db(usuario, contra)
    try:
        df = cargar_base(conn)
    finally:
        conn.close()
    for c in ["dominio", "estrato", "anio", "tipo_vivienda"]:
        if c in df.columns:
            df[c] = df[c].astype("string")
    # Corte limpio urbano/rural derivado del estrato (sin tocar el ETL):
    # los estratos "Área de Empadronamiento Rural ..." son rurales; el resto, urbanos.
    if "estrato" in df.columns:
        es_rural = df["estrato"].astype("string").str.contains("rural", case=False, na=False)
        df["area"] = np.where(es_rural, "Rural", "Urbano").astype("object")
        df["area"] = df["area"].astype("string")
    return df


DF = cargar_datos()
print(f"Base cargada: {len(DF):,} hogares (muestra)")

DOMINIOS = sorted([d for d in DF["dominio"].dropna().unique()])
ESTRATOS = sorted([e for e in DF["estrato"].dropna().unique()])
ANIOS = sorted([a for a in DF["anio"].dropna().unique()])
TIPOS_VIVIENDA = sorted([v for v in DF["tipo_vivienda"].dropna().unique()])
AREAS = [a for a in ["Urbano", "Rural"] if a in set(DF["area"].dropna().unique())]


# ---------------------------------------------------------------------------
# 2. Tema visual unificado + altura uniforme para una grilla pareja
# ---------------------------------------------------------------------------
def tema(fig, alto=330):
    fig.update_layout(
        font=dict(family=FUENTE, size=12, color=TINTA),
        title=dict(font=dict(size=14, color=TINTA), x=0.01, xanchor="left"),
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=52, r=22, t=46, b=40),
        height=alto,
        colorway=[ACENTO, ALERTA, "#64748b", "#0891b2", "#9ca3af"],
    )
    fig.update_xaxes(gridcolor="#f1f2f4", zeroline=False, linecolor=BORDE)
    fig.update_yaxes(gridcolor="#f1f2f4", zeroline=False, linecolor=BORDE)
    return fig


def fig_vacia(msg="Sin datos para los filtros seleccionados"):
    f = go.Figure()
    f.add_annotation(text=msg, showarrow=False, font=dict(size=13, color=GRIS))
    f.update_layout(template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
                    height=330, xaxis=dict(visible=False), yaxis=dict(visible=False),
                    margin=dict(l=20, r=20, t=20, b=20))
    return f


# ---------------------------------------------------------------------------
# 3. Estructura narrativa. Cada gráfico declara su ancho en sextos (span).
#    Las filas suman 6: (4+2), (4+2), (4+2), (3+3).
# ---------------------------------------------------------------------------
CAPTIONS = {
    "g1_cobertura_servicios":
        "De la sierra/selva (arriba) a la costa/Lima (abajo) la cobertura mejora. El agua segura es la carencia más extendida.",
    "g8_brecha_multidimensional":
        "La privación acumulada se concentra en sierra y selva.",
    "g6_agua_acceso_vs_continuidad":
        "Cobertura alta y pareja, pero la continuidad colapsa: tener conexión no garantiza recibir agua todo el día.",
    "g2_deficit_saneamiento":
        "El saneamiento sigue el mismo gradiente territorial.",
    "g5_materiales_precarios":
        "El piso es el elemento más crítico: la vivienda inadecuada es un problema de calidad, no de existencia.",
    "g4_prevalencia_nbi":
        "Vivienda inadecuada y falta de servicio higiénico lideran las NBI.",
    "g3_distribucion_carencias":
        "Pocos hogares tienen cero carencias (estimación sin TIC, cota inferior).",
    "g7_gasto_servicios":
        "El gasto en servicios reproduce la brecha territorial: Lima gasta casi el doble que la sierra.",
    "g9_priorizacion":
        "Eje X: severidad (% con brecha). Eje Y: magnitud (hogares con brecha, en absoluto). "
        "Tamaño: población del dominio. Arriba a la derecha = dónde priorizar la intervención.",
}

CONTENIDO = [
    {"tipo": "header", "kicker": "01 · Dónde está el problema",
     "titulo": "La brecha no es de vivienda, es territorial",
     "texto": "El problema no es la ausencia de vivienda, sino la inadecuación de sus condiciones y el acceso desigual a servicios."},
    {"tipo": "graf", "gid": "g1_cobertura_servicios", "span": 4},
    {"tipo": "graf", "gid": "g8_brecha_multidimensional", "span": 2},

    {"tipo": "header", "kicker": "02 · En qué dimensión",
     "titulo": "Agua, saneamiento y materiales",
     "texto": "La cobertura formal esconde déficits de continuidad y calidad concentrados fuera de la costa."},
    {"tipo": "graf", "gid": "g6_agua_acceso_vs_continuidad", "span": 4},
    {"tipo": "graf", "gid": "g2_deficit_saneamiento", "span": 2},
    {"tipo": "graf", "gid": "g5_materiales_precarios", "span": 4},
    {"tipo": "graf", "gid": "g4_prevalencia_nbi", "span": 2},

    {"tipo": "header", "kicker": "03 · Cuánto pesa",
     "titulo": "La privación se acumula y cuesta distinto",
     "texto": "La mayoría de hogares carga varias carencias a la vez, y el gasto en servicios reproduce la desigualdad."},
    {"tipo": "graf", "gid": "g3_distribucion_carencias", "span": 3},
    {"tipo": "graf", "gid": "g7_gasto_servicios", "span": 3},

    {"tipo": "header", "kicker": "04 · Hacia dónde priorizar",
     "titulo": "No todos los dominios pesan igual",
     "texto": "La severidad (qué porcentaje de hogares está privado) no basta para decidir dónde invertir: "
              "hay que cruzarla con la magnitud, cuántos hogares en términos absolutos. El cuadrante superior "
              "derecho concentra a la vez alta privación y muchos hogares: ahí debe priorizarse la intervención."},
    {"tipo": "graf", "gid": "g9_priorizacion", "span": 6},
]

FLAT_GIDS = [it["gid"] for it in CONTENIDO if it["tipo"] == "graf"]


# ---------------------------------------------------------------------------
# 4. Filtros
# ---------------------------------------------------------------------------
def filtrar(df, dominios, estratos, anios, tipos_vivienda, areas):
    d = df
    if dominios:
        d = d[d["dominio"].isin(dominios)]
    if estratos:
        d = d[d["estrato"].isin(estratos)]
    if anios:
        d = d[d["anio"].isin(anios)]
    if tipos_vivienda:
        d = d[d["tipo_vivienda"].isin(tipos_vivienda)]
    if areas and "area" in d.columns:
        d = d[d["area"].isin(areas)]
    return d


# ---------------------------------------------------------------------------
# 5. Componentes
# ---------------------------------------------------------------------------
def kpi_card(titulo, value_id, alerta=True):
    return html.Div(
        style={"textAlign": "center", "padding": "18px 14px", "background": "white",
               "borderRadius": "10px", "boxShadow": SOMBRA},
        children=[
            html.Div(id=value_id, style={"fontSize": "27px", "fontWeight": "700",
                     "color": ALERTA if alerta else ACENTO, "lineHeight": "1", "marginBottom": "6px"}),
            html.Div(titulo, style={"fontSize": "12px", "color": GRIS}),
        ],
    )


def graph_card(gid, span):
    return html.Div(
        style={"gridColumn": f"span {span}", "background": "white", "borderRadius": "10px",
               "boxShadow": SOMBRA, "padding": "12px 14px"},
        children=[
            html.P(CAPTIONS.get(gid, ""), style={"fontSize": "12.5px", "color": GRIS,
                   "margin": "0 2px 6px", "lineHeight": "1.45", "minHeight": "34px"}),
            dcc.Graph(id=f"graf-{gid}", config={"displaylogo": False, "displayModeBar": False}),
        ],
    )


def header_card(it):
    return html.Div(
        style={"gridColumn": "1 / -1", "marginTop": "10px"},
        children=[
            html.Div(it["kicker"], style={"fontSize": "11.5px", "fontWeight": "700", "color": ACENTO,
                     "textTransform": "uppercase", "letterSpacing": ".06em"}),
            html.H2(it["titulo"], style={"margin": "3px 0 4px", "fontSize": "20px", "color": TINTA}),
            html.P(it["texto"], style={"color": GRIS, "fontSize": "14px", "lineHeight": "1.5",
                   "maxWidth": "820px", "margin": "0"}),
        ],
    )


def render_item(it):
    return header_card(it) if it["tipo"] == "header" else graph_card(it["gid"], it["span"])


# ---------------------------------------------------------------------------
# 6. App
# ---------------------------------------------------------------------------
app = Dash(__name__)
server = app.server      
app.title = "ENAHO 2025 · Bienestar habitacional"


app.layout = html.Div(
    style={"background": FONDO, "minHeight": "100vh", "fontFamily": FUENTE},
    children=[html.Div(
        style={"maxWidth": "1280px", "margin": "0 auto", "padding": "26px 22px 56px"},
        children=[
            html.Div("ENAHO 2025 · Módulo 100", style={"fontSize": "11.5px", "fontWeight": "700",
                     "color": ACENTO, "textTransform": "uppercase", "letterSpacing": ".06em"}),
            html.H1("Condiciones de vivienda y acceso a servicios básicos en el Perú",
                    style={"margin": "6px 0 8px", "fontSize": "28px", "color": TINTA, "lineHeight": "1.2"}),
            html.P("El déficit habitacional peruano no es de techo, sino de calidad y de acceso desigual. "
                   "Este tablero recorre dónde se concentra la privación, qué la explica y cuánto pesa.",
                   style={"color": GRIS, "fontSize": "15px", "lineHeight": "1.55", "maxWidth": "820px",
                          "margin": "0 0 18px"}),

            # Alcance y método (cierra los huecos narrativos: TIC fuera, cota inferior)
            html.Div(
                style={"borderLeft": f"3px solid {ACENTO}", "background": "white", "borderRadius": "8px",
                       "boxShadow": SOMBRA, "padding": "12px 16px", "marginBottom": "16px"},
                children=[
                    html.Div("Alcance y método", style={"fontWeight": "700", "fontSize": "12px",
                             "color": ACENTO, "textTransform": "uppercase", "letterSpacing": ".05em",
                             "marginBottom": "4px"}),
                    html.P([
                        "Cubre ", html.B("vivienda y servicios básicos"),
                        " (agua, saneamiento, energía, materiales). La ",
                        html.B("conectividad (TIC) queda fuera"),
                        ": la variable de internet del ENAHO 2024-2025 mezcla conexión contratada con móvil "
                        "prepago y no es comparable con la cifra oficial de INEI; se deja como línea futura. "
                        "Las estimaciones de brecha y carencias son una ", html.B("cota inferior"),
                        " (se calculan sin TIC y con umbral de 2 o más carencias). Usa el filtro ",
                        html.B("Área (urbano/rural)"), " para evidenciar la desigualdad territorial.",
                    ], style={"color": GRIS, "fontSize": "13px", "lineHeight": "1.55", "margin": "0"}),
                ],
            ),

            # Filtros (barra fija)
            html.Div(
                style={"position": "sticky", "top": "0", "zIndex": "5", "display": "grid",
                       "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))", "gap": "12px",
                       "padding": "12px 14px",
                       "background": "rgba(255,255,255,.94)", "backdropFilter": "blur(6px)",
                       "borderRadius": "10px", "boxShadow": SOMBRA, "marginBottom": "16px"},
                children=[
                    html.Div([html.Label("Área", style={"fontWeight": "600", "fontSize": "12px", "color": GRIS}),
                              dcc.Dropdown(id="f-area", multi=True, placeholder="Todas",
                                           options=[{"label": a, "value": a} for a in AREAS])]),
                    html.Div([html.Label("Dominio", style={"fontWeight": "600", "fontSize": "12px", "color": GRIS}),
                              dcc.Dropdown(id="f-dominio", multi=True, placeholder="Todos",
                                           options=[{"label": d, "value": d} for d in DOMINIOS])]),
                    html.Div([html.Label("Estrato", style={"fontWeight": "600", "fontSize": "12px", "color": GRIS}),
                              dcc.Dropdown(id="f-estrato", multi=True, placeholder="Todos",
                                           options=[{"label": e, "value": e} for e in ESTRATOS])]),
                    html.Div([html.Label("Año", style={"fontWeight": "600", "fontSize": "12px", "color": GRIS}),
                              dcc.Dropdown(id="f-anio", multi=True, placeholder="Todos",
                                           options=[{"label": a, "value": a} for a in ANIOS])]),
                    html.Div([html.Label("Tipo de vivienda", style={"fontWeight": "600", "fontSize": "12px", "color": GRIS}),
                              dcc.Dropdown(id="f-tipo-vivienda", multi=True, placeholder="Todos",
                                           options=[{"label": v, "value": v} for v in TIPOS_VIVIENDA])]),
                ],
            ),

            # Banda de KPIs (5 columnas)
            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(5, 1fr)", "gap": "14px",
                            "marginBottom": "6px"},
                     children=[
                         kpi_card("Brecha multidimensional", "kpi-brecha"),
                         kpi_card("Sin agua segura", "kpi-agua"),
                         kpi_card("Sin saneamiento", "kpi-san"),
                         kpi_card("Material precario", "kpi-mat"),
                         kpi_card("Población de hogares", "kpi-pob", alerta=False),
                     ]),

            # Grilla maestra de 6 columnas (encabezados + gráficos)
            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(6, 1fr)", "gap": "14px",
                            "marginTop": "8px"},
                     children=[render_item(it) for it in CONTENIDO]),

            html.Div(style={"marginTop": "36px", "paddingTop": "16px", "borderTop": f"1px solid {BORDE}",
                            "color": "#9ca3af", "fontSize": "12px", "lineHeight": "1.6"},
                     children="Fuente: ENAHO 2025, Módulo 100 (INEI). Estimaciones ponderadas por factor de "
                              "expansión. La brecha multidimensional y las carencias se calculan sobre servicios "
                              "básicos sin incluir conectividad (TIC), por lo que representan una cota inferior."),
        ],
    )],
)


# ---------------------------------------------------------------------------
# 7. Callback
# ---------------------------------------------------------------------------
@app.callback(
    [Output(f"graf-{g}", "figure") for g in FLAT_GIDS]
    + [Output("kpi-brecha", "children"), Output("kpi-agua", "children"),
       Output("kpi-san", "children"), Output("kpi-mat", "children"), Output("kpi-pob", "children")],
    [Input("f-dominio", "value"), Input("f-estrato", "value"),
     Input("f-anio", "value"), Input("f-tipo-vivienda", "value"), Input("f-area", "value")],
)
def actualizar(dominios, estratos, anios, tipos_vivienda, areas):
    d = filtrar(DF, dominios, estratos, anios, tipos_vivienda, areas)

    figuras = []
    for gid in FLAT_GIDS:
        try:
            figuras.append(fig_vacia() if d.empty else tema(GRAFICOS[gid](d)))
        except Exception as e:
            figuras.append(fig_vacia(f"Error en {gid}: {e}"))

    if d.empty:
        return figuras + ["—", "—", "—", "—", "0"]

    pct_brecha = pct_global(carencias_limpias(d), "brecha_sin_tic_ind")
    pct_sin_agua = 100 - pct_global(d, "agua_segura_ind")
    pct_sin_san = 100 - pct_global(d, "saneamiento_adecuado_ind")
    pct_mat = pct_global(d, "vivienda_material_precario_ind")
    poblacion = int(d["factor_expansion"].dropna().sum())

    return figuras + [f"{pct_brecha:.1f}%", f"{pct_sin_agua:.1f}%", f"{pct_sin_san:.1f}%",
                      f"{pct_mat:.1f}%", f"{poblacion:,}"]


if __name__ == "__main__":
    app.run(debug=False, port=8050)