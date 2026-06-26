"""
Gráficos de insights - Datamart ENAHO 2025 (Módulo 100)
Bienestar habitacional y acceso a servicios básicos de los hogares peruanos.
"""

import os
import psycopg2
import numpy as np
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

PLANTILLA = "plotly_white"

load_dotenv()
# ---------------------------------------------------------------------------
# 1. Conexión
# ---------------------------------------------------------------------------
def conexion_db(usuario, contra):
    conn = psycopg2.connect(
        host="ep-delicate-block-ac01qt33-pooler.sa-east-1.aws.neon.tech",
        dbname="neondb",
        user=usuario,
        password=contra,
        sslmode="require",
    )
    return conn


# ---------------------------------------------------------------------------
# 2. Carga de la tabla base (un solo SELECT reutilizable por todos los gráficos)
# ---------------------------------------------------------------------------
QUERY_BASE = """
    SELECT
        g.dominio,
        g.estrato,
        g.dominio_cod,
        g.estrato_cod,
        v.tipo_vivienda_cod,
        v.tipo_vivienda,
        t.anio,
        t.mes,
        t.periodo,
        f.factor_expansion,
        f.total_carencias_bienestar_habitacional,
        f.agua_red_publica_ind,
        f.agua_potable_ind,
        f.agua_todos_dias_ind,
        f.agua_segura_ind,
        f.saneamiento_adecuado_ind,
        f.tiene_electricidad_ind,
        f.combustible_limpio_ind,
        f.combustible_solido_ind,
        f.tiene_internet_ind,
        f.tiene_celular_ind,
        f.sin_tic_ind,
        f.nbi_vivienda_inadecuada_ind,
        f.nbi_hacinamiento_ind,
        f.nbi_sin_servicio_higienico_ind,
        f.nbi_ninios_no_asisten_ind,
        f.nbi_alta_dependencia_ind,
        f.pared_precaria_ind,
        f.piso_precario_ind,
        f.techo_precario_ind,
        f.vivienda_material_precario_ind,
        f.brecha_multidimensional_ind,
        f.horas_agua_dia,
        f.dias_agua_semana,
        f.gasto_mensual_servicios_estimado,
        f.gasto_anual_servicios_total
    FROM dm_enaho2025.fact_hogar_bienestar f
    JOIN dm_enaho2025.dim_geografia g ON f.geografia_key = g.geografia_key
    JOIN dm_enaho2025.dim_vivienda  v ON f.vivienda_key  = v.vivienda_key
    JOIN dm_enaho2025.dim_tiempo    t ON f.tiempo_key    = t.tiempo_key
"""


def cargar_base(conn):
    df = pd.read_sql(QUERY_BASE, conn)
    return df


# ---------------------------------------------------------------------------
# 3. Helpers de agregación ponderada
# ---------------------------------------------------------------------------
def pct_ponderado(df, ind_col, group_cols):
    """% ponderado de hogares con indicador = 1, por grupo."""
    d = df.dropna(subset=[ind_col, "factor_expansion"])
    out = (
        d.groupby(group_cols)[[ind_col, "factor_expansion"]]
        .apply(lambda x: 100 * np.average(x[ind_col], weights=x["factor_expansion"]))
        .reset_index(name="pct")
    )
    return out


def pct_global(df, ind_col):
    """% ponderado de hogares con indicador = 1 (sin agrupar)."""
    d = df.dropna(subset=[ind_col, "factor_expansion"])
    if d.empty:
        return 0.0
    return 100 * np.average(d[ind_col], weights=d["factor_expansion"])


def media_ponderada(df, val_col, group_cols):
    """Promedio ponderado de una variable continua, por grupo."""
    d = df.dropna(subset=[val_col, "factor_expansion"])
    out = (
        d.groupby(group_cols)[[val_col, "factor_expansion"]]
        .apply(lambda x: np.average(x[val_col], weights=x["factor_expansion"]))
        .reset_index(name="media")
    )
    return out


def dist_ponderada(df, cat_col):
    """Distribución (% de hogares) por categoría, ponderada."""
    d = df.dropna(subset=[cat_col, "factor_expansion"])
    g = d.groupby(cat_col)["factor_expansion"].sum()
    return (100 * g / g.sum()).reset_index(name="pct")


def carencias_limpias(df):
    """Reconstruye las 6 carencias SIN internet desde columnas ya presentes en
    el df base, y agrega total_carencias_sin_tic y brecha_sin_tic_ind."""
    d = df.copy()
    d["c_materiales"]   = d["vivienda_material_precario_ind"]
    d["c_hacinamiento"] = d["nbi_hacinamiento_ind"]
    d["c_agua"]         = (d["agua_segura_ind"] == 0).astype("Int64")
    d["c_saneamiento"]  = (d["saneamiento_adecuado_ind"] == 0).astype("Int64")
    d["c_electricidad"] = (d["tiene_electricidad_ind"] == 0).astype("Int64")
    d["c_combustible"]  = (d["combustible_limpio_ind"] == 0).astype("Int64")
    cols = ["c_materiales", "c_hacinamiento", "c_agua",
            "c_saneamiento", "c_electricidad", "c_combustible"]
    d["total_carencias_sin_tic"] = d[cols].astype("float").sum(axis=1).astype("Int64")
    d["brecha_sin_tic_ind"] = (d["total_carencias_sin_tic"] >= 2).astype("Int64")
    return d


def _estilizar(fig, eje_x=None, eje_y=None):
    fig.update_layout(
        template=PLANTILLA,
        font=dict(size=13),
        margin=dict(l=70, r=40, t=70, b=50),
        title_x=0.5,
    )
    if eje_x:
        fig.update_xaxes(title_text=eje_x)
    if eje_y:
        fig.update_yaxes(title_text=eje_y)
    return fig


# ---------------------------------------------------------------------------
# 4. Gráficos
# ---------------------------------------------------------------------------
def g1_cobertura_servicios(df):
    """Heatmap: cobertura de servicios y condiciones de vivienda por dominio.
    (Se reemplazó la columna Internet por Materiales adecuados.)"""
    d = df.copy()
    d["_materiales_adecuados"] = (d["vivienda_material_precario_ind"] == 0).astype("Int64")
    servicios = {
        "agua_segura_ind": "Agua segura",
        "saneamiento_adecuado_ind": "Saneamiento",
        "tiene_electricidad_ind": "Electricidad",
        "combustible_limpio_ind": "Comb. limpio",
        "_materiales_adecuados": "Materiales",
    }
    columnas = []
    for col, label in servicios.items():
        t = pct_ponderado(d, col, ["dominio"]).set_index("dominio")["pct"].rename(label)
        columnas.append(t)
    mat = pd.concat(columnas, axis=1)
    mat = mat.loc[mat.mean(axis=1).sort_values().index]
    fig = px.imshow(
        mat,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        labels=dict(color="% hogares"),
        title="Cobertura de servicios y condiciones de vivienda por dominio (% de hogares)",
    )
    return _estilizar(fig, eje_x="Indicador", eje_y="Dominio")


def g2_deficit_saneamiento(df):
    """Barras: déficit de saneamiento por dominio (hogares sin saneamiento adecuado).
    Reemplaza al gráfico de brecha digital, que dependía de internet."""
    d = df.copy()
    d["_sin_saneamiento"] = (d["saneamiento_adecuado_ind"] == 0).astype("Int64")
    t = pct_ponderado(d, "_sin_saneamiento", ["dominio"]).sort_values("pct")
    fig = px.bar(
        t, x="pct", y="dominio", orientation="h", text="pct",
        title="Déficit de saneamiento: hogares sin saneamiento adecuado por dominio",
        color="pct", color_continuous_scale="Reds",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="% de hogares sin saneamiento adecuado", eje_y="")


def g2_alt_combustible_solido(df):
    """Alternativa al reemplazo de g2: uso de combustible sólido por dominio.
    No está en el registro; cámbiala por g2 si prefieres el ángulo de energía."""
    t = pct_ponderado(df, "combustible_solido_ind", ["dominio"]).sort_values("pct")
    fig = px.bar(
        t, x="pct", y="dominio", orientation="h", text="pct",
        title="Pobreza energética: hogares que cocinan con combustible sólido por dominio",
        color="pct", color_continuous_scale="OrRd",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="% de hogares con combustible sólido", eje_y="")


def g3_distribucion_carencias(df):
    """Barras: distribución de hogares por número de carencias (servicios básicos, sin TIC)."""
    d = carencias_limpias(df).dropna(subset=["total_carencias_sin_tic"]).copy()
    d["cat"] = d["total_carencias_sin_tic"].clip(upper=4).astype(int)
    dist = dist_ponderada(d, "cat")
    etiquetas = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4+"}
    dist["cat_label"] = dist["cat"].map(etiquetas)
    fig = px.bar(
        dist, x="cat_label", y="pct", text="pct",
        title="Distribución de hogares por número de carencias (servicios básicos, sin TIC)",
        color="pct", color_continuous_scale="OrRd",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="Número de carencias", eje_y="% de hogares")


def g4_prevalencia_nbi(df):
    """Barras: prevalencia de cada Necesidad Básica Insatisfecha (NBI)."""
    nbis = {
        "nbi_vivienda_inadecuada_ind": "Vivienda inadecuada",
        "nbi_hacinamiento_ind": "Hacinamiento",
        "nbi_sin_servicio_higienico_ind": "Sin servicio higiénico",
        "nbi_ninios_no_asisten_ind": "Niños no asisten",
        "nbi_alta_dependencia_ind": "Alta dependencia econ.",
    }
    filas = [{"NBI": lab, "pct": pct_global(df, col)} for col, lab in nbis.items()]
    t = pd.DataFrame(filas).sort_values("pct")
    fig = px.bar(
        t, x="pct", y="NBI", orientation="h", text="pct",
        title="Prevalencia de NBI (% de hogares)",
        color="pct", color_continuous_scale="Reds",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="% de hogares", eje_y="")


def g5_materiales_precarios(df):
    """Barras agrupadas: % de hogares con material precario por elemento y dominio."""
    mats = {
        "pared_precaria_ind": "Pared",
        "piso_precario_ind": "Piso",
        "techo_precario_ind": "Techo",
    }
    partes = []
    for col, lab in mats.items():
        t = pct_ponderado(df, col, ["dominio"])
        t["Elemento"] = lab
        partes.append(t)
    big = pd.concat(partes, ignore_index=True)
    orden = (
        big.groupby("dominio")["pct"].sum().sort_values(ascending=False).index.tolist()
    )
    fig = px.bar(
        big, x="dominio", y="pct", color="Elemento", barmode="group",
        category_orders={"dominio": orden},
        title="Materiales precarios de la vivienda por dominio",
    )
    return _estilizar(fig, eje_x="Dominio", eje_y="% de hogares")


def g6_agua_acceso_vs_continuidad(df):
    """Dispersión: cobertura de agua (red pública) vs continuidad (horas/día)."""
    cob = pct_ponderado(df, "agua_red_publica_ind", ["dominio"]).rename(
        columns={"pct": "cobertura"}
    )
    hrs = media_ponderada(df, "horas_agua_dia", ["dominio"]).rename(
        columns={"media": "horas"}
    )
    tam = (
        df.dropna(subset=["factor_expansion"])
        .groupby("dominio")["factor_expansion"].sum()
        .reset_index(name="hogares")
    )
    m = cob.merge(hrs, on="dominio").merge(tam, on="dominio")
    fig = px.scatter(
        m, x="cobertura", y="horas", size="hogares", text="dominio",
        title="Agua: cobertura por red pública vs continuidad del servicio",
        color="dominio",
    )
    fig.update_traces(textposition="top center")
    fig.add_hline(
        y=18.5, line_dash="dash", line_color="gray",
        annotation_text="Continuidad nacional 2024 (18.5 h/día)",
        annotation_position="bottom right",
    )
    fig.update_layout(showlegend=False)
    return _estilizar(fig, eje_x="% hogares con agua por red pública", eje_y="Horas de agua por día")


def g7_gasto_servicios(df):
    """Barras: gasto mensual promedio en servicios por dominio."""
    t = media_ponderada(df, "gasto_mensual_servicios_estimado", ["dominio"]).sort_values("media")
    fig = px.bar(
        t, x="media", y="dominio", orientation="h", text="media",
        title="Gasto mensual promedio en servicios por dominio",
        color="media", color_continuous_scale="Tealgrn",
    )
    fig.update_traces(texttemplate="S/ %{text:.0f}", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="Gasto mensual promedio (S/)", eje_y="")


def g8_brecha_multidimensional(df):
    """Barras: % de hogares con brecha multidimensional por dominio (servicios básicos, sin TIC)."""
    d = carencias_limpias(df)
    t = pct_ponderado(d, "brecha_sin_tic_ind", ["dominio"]).sort_values("pct")
    fig = px.bar(
        t, x="pct", y="dominio", orientation="h", text="pct",
        title="Brecha multidimensional de servicios básicos por dominio",
        color="pct", color_continuous_scale="Reds",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="% de hogares", eje_y="")


def g9_priorizacion(df):
    """Burbujas: severidad (% de hogares con brecha) vs magnitud (hogares con
    brecha, en absoluto) por dominio. Tamaño = población de hogares del dominio.
    El cuadrante superior derecho (alta severidad + muchos hogares) es la
    prioridad de intervención. Cierra el relato: pasa de describir a proponer."""
    d = carencias_limpias(df).dropna(subset=["factor_expansion", "brecha_sin_tic_ind"])
    filas = []
    for dom, g in d.groupby("dominio"):
        f = g["factor_expansion"]
        if f.sum() == 0:
            continue
        filas.append({
            "dominio": dom,
            "severidad": 100 * np.average(g["brecha_sin_tic_ind"], weights=f),
            "hogares_brecha": float((g["brecha_sin_tic_ind"] * f).sum()),
            "poblacion": float(f.sum()),
        })
    m = pd.DataFrame(filas)
    if m.empty:
        return px.scatter(title="Sin datos")
    fig = px.scatter(
        m, x="severidad", y="hogares_brecha", size="poblacion", text="dominio",
        color="severidad", color_continuous_scale="Reds", size_max=55,
        title="Priorización: severidad vs magnitud de la brecha por dominio",
    )
    fig.update_traces(textposition="top center",
                      hovertemplate="<b>%{text}</b><br>Severidad: %{x:.1f}%"
                                    "<br>Hogares con brecha: %{y:,.0f}<extra></extra>")
    # Líneas de cuadrante en los promedios
    fig.add_vline(x=m["severidad"].mean(), line_dash="dash", line_color="gray")
    fig.add_hline(y=m["hogares_brecha"].mean(), line_dash="dash", line_color="gray")
    fig.add_annotation(xref="paper", yref="paper", x=0.99, y=0.99, xanchor="right",
                       yanchor="top", showarrow=False, text="Prioridad de intervención",
                       font=dict(size=11, color="#b91c1c"))
    fig.update_yaxes(tickformat="~s")
    fig.update_coloraxes(showscale=False)
    return _estilizar(fig, eje_x="% de hogares con brecha (severidad)",
                      eje_y="Hogares con brecha (magnitud)")


# Registro de gráficos (útil para iterar y, más adelante, para el Dash)
GRAFICOS = {
    "g1_cobertura_servicios": g1_cobertura_servicios,
    "g2_deficit_saneamiento": g2_deficit_saneamiento,
    "g3_distribucion_carencias": g3_distribucion_carencias,
    "g4_prevalencia_nbi": g4_prevalencia_nbi,
    "g5_materiales_precarios": g5_materiales_precarios,
    "g6_agua_acceso_vs_continuidad": g6_agua_acceso_vs_continuidad,
    "g7_gasto_servicios": g7_gasto_servicios,
    "g8_brecha_multidimensional": g8_brecha_multidimensional,
    "g9_priorizacion": g9_priorizacion,
}


# ---------------------------------------------------------------------------
# 5. Ejecución
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    usuario = os.getenv("NEON_USER", "neondb_owner")
    contra = os.getenv("NEON_PASS")
    if not contra:
        raise SystemExit(
            "Define la variable de entorno NEON_PASS antes de correr "
            "(no escribas la contraseña en el código)."
        )

    conn = conexion_db(usuario, contra)
    df = cargar_base(conn)
    print(f"Filas cargadas: {len(df):,}")

    for nombre, func in GRAFICOS.items():
        fig = func(df)
        fig.show()
        # fig.write_html(f"{nombre}.html")  # opcional: guardar a disco

    conn.close()