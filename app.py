import streamlit as st
import pandas as pd
import numpy as np
import os
import streamlit.components.v1 as components

from modules.data_loader import load_data, classify_columns, get_data_summary
from modules.powerbi_formatter import POWERBI_VISUAL_CATALOG, generate_powerbi_guide
from modules.chart_builder import build_plotly_chart
from modules.visual_generator import generate_all_possible_visuals
from modules.html_exporter import generate_html_report

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Power BI Assistant - Galería Épica & Inteligencia de Negocio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para experiencia BI Corporativa en Fondo Blanco Total
CUSTOM_CSS = """
<style>
    /* REGLA UNIVERSAL DE FUENTES EN NEGRO DE ALTO CONTRASTE */
    html, body, .stApp, .stApp * {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    .stApp {
        background-color: #F8FAFC !important;
    }

    p, span, label, h1, h2, h3, h4, h5, h6, caption, small {
        color: #0F172A !important;
    }

    /* ESTILOS DE PESTAÑAS (TABS) EN NEGRO / AZUL */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        border-bottom: 2px solid #E2E8F0 !important;
        padding: 4px 8px 0 8px !important;
        border-radius: 8px 8px 0 0 !important;
    }

    div[data-testid="stTabs"] button[role="tab"],
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 18px !important;
        margin-right: 4px !important;
    }

    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] button[role="tab"] span,
    div[data-testid="stTabs"] button[role="tab"] div,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #0F172A !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 3px solid #0284C7 !important;
        background-color: #E0F2FE !important;
        border-radius: 6px 6px 0 0 !important;
    }

    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] span,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] div {
        color: #0284C7 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stTabs"] button[role="tab"]:hover p,
    div[data-testid="stTabs"] button[role="tab"]:hover span {
        color: #0284C7 !important;
    }
    
    /* SIDEBAR EN BLANCO LUMINOSO */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    
    [data-testid="stSidebar"] .stCaption, 
    [data-testid="stSidebar"] small {
        color: #475569 !important;
    }

    /* FILE UPLOADER Y BOTÓN DE AYUDA */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #0284C7 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08) !important;
    }
    
    [data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    [data-testid="stFileUploaderDropzone"] button {
        background: #0284C7 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #0369A1 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stFileUploaderDropzone"] button * {
        color: #FFFFFF !important;
    }

    [data-testid="stFileUploaderDropzone"] button [data-testid="stIconMaterial"],
    [data-testid="stFileUploaderDropzone"] button span:first-child:not(:only-child) {
        display: none !important;
    }

    [data-testid="stWidgetLabel"] button,
    button[aria-label="help"],
    [data-testid="stTooltipIcon"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        width: auto !important;
        height: auto !important;
    }
    
    [data-testid="stWidgetLabel"] button *,
    [data-testid="stTooltipIcon"] * {
        color: #0284C7 !important;
    }
    
    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #0F172A !important;
    }
    
    .bi-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }
    .bi-title {
        color: #0284C7 !important;
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .bi-subtitle {
        color: #334155 !important;
        font-size: 14px;
        margin: 0;
    }
    
    /* RECUADRO DE CONTEXTO DE NEGOCIO EJECUTIVO */
    .context-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0 12px 0;
        font-size: 13px;
        color: #0F172A !important;
        line-height: 1.45;
    }
    
    .case-box {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
        font-size: 12.5px;
        color: #78350F !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        box-shadow: 0 2px 6px rgba(2, 132, 199, 0.25) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button * {
        color: #FFFFFF !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.35) !important;
    }

    .sample-badge {
        background: #ECFDF5;
        color: #047857 !important;
        border: 1px solid #A7F3D0;
        font-weight: 600;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 8px;
    }
    
    .rel-badge {
        background: #EFF6FF;
        color: #1D4ED8 !important;
        border: 1px solid #BFDBFE;
        font-weight: 600;
        font-size: 12px;
        padding: 6px 14px;
        border-radius: 8px;
        margin: 6px 0;
    }

    .source-tag {
        background: #F1F5F9;
        color: #0284C7;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
    }
    
    .field-map-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 12.5px;
    }
    .field-map-table th {
        background-color: #F1F5F9;
        color: #0284C7 !important;
        text-align: left;
        padding: 8px 12px;
        border-bottom: 2px solid #CBD5E1;
    }
    .field-map-table td {
        padding: 8px 12px;
        border-bottom: 1px solid #E2E8F0;
        color: #0F172A !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Datasets de muestra integrados
BASE_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL = os.path.join(BASE_DIR, "sample_data", "sample_ventas_finanzas.xlsx")
SAMPLE_CSV = os.path.join(BASE_DIR, "sample_data", "sample_rrhh_desempeno.csv")

# ---------------------------------------------------------
# POP-UP MODAL (DIALOG) PARA MOSTRAR LA GUÍA POWER BI CON CASOS DE EJEMPLO
# ---------------------------------------------------------
@st.dialog("📖 Guía de Construcción & Interpretación en Power BI", width="large")
def show_powerbi_guide_modal(visual_info):
    guide = visual_info["guide"]
    case_study = guide.get("case_study", {})
    
    st.markdown(f"### {visual_info['icon']} {visual_info['title']}")
    st.markdown(f"**Componente Power BI:** `{guide['visual_name']}` | **Categoría:** `{guide['category']}`")
    
    st.markdown(f'<div class="context-box">{visual_info["description"]}</div>', unsafe_allow_html=True)
    
    # 📌 SECCIÓN DE RESEÑA E INTERPRETACÓN DE EJEMPLOS DE DATOS REALES
    if case_study and case_study.get("examples"):
        st.markdown("#### 📌 Reseña e Interpretación de Datos Reales (Ejemplos Caso de Uso)")
        for ex in case_study["examples"]:
            st.markdown(f"- {ex['interpretation']}")
            
        if case_study.get("business_recommendation"):
            st.markdown(f'<div class="case-box">{case_study["business_recommendation"]}</div>', unsafe_allow_html=True)
            
    if guide.get("is_multi_table"):
        st.info("🔗 **Componente Multitabla:** Esta visualización entrelaza datos de múltiples archivos/planillas distintas. Sigue los pasos de la Vista de Modelo a continuación.")
        
    st.divider()
    
    col_m1, col_m2 = st.columns([0.58, 0.42])
    
    with col_m1:
        st.markdown("#### 🗂️ Mapeo de Campos y Archivo de Origen")
        rows_html = ""
        for fm in guide["field_mappings"]:
            src_file = fm.get("source", "Planilla Carga")
            rows_html += f"""
            <tr>
                <td><strong>{fm['well']}</strong></td>
                <td><code>{fm['field']}</code></td>
                <td><span class="source-tag">📄 {src_file}</span></td>
            </tr>
            """
        
        table_html = f"""
        <table class="field-map-table">
            <thead>
                <tr>
                    <th>Contenedor Power BI</th>
                    <th>Columna Planilla</th>
                    <th>Archivo Origen</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    with col_m2:
        if guide.get("dax_code"):
            st.markdown("#### 🧮 Código DAX Sugerido")
            st.code(guide["dax_code"], language="dax")
            if guide.get("secondary_dax"):
                st.code(guide["secondary_dax"], language="dax")
                
        st.markdown("#### 🎨 Pasos de Configuración")
        for tip in guide["format_tips"]:
            st.markdown(f"- {tip}")

# ---------------------------------------------------------
# SIDEBAR: Carga Múltiple de Planillas y Modelo Relacional
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/cf/New_Power_BI_Logo.svg", width=45)
    st.title("⚡ Power BI Assistant")
    st.caption("Sube una o MÚLTIPLES planillas para entrelazar sus datos.")
    
    st.divider()
    st.subheader("1. Cargar Planillas de Datos")
    
    uploaded_files = st.file_uploader(
        "Subir una o varias planillas Excel (.xlsx) o CSV (.csv)",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
        key="uploaded_file_main",
        help="Sube una o múltiples planillas para entrelazar sus datos en un modelo de Power BI."
    )
    
    st.markdown("**O prueba combinando los datasets de ejemplo:**")
    col_s1, col_s2, col_s3 = st.columns(3)
    use_sample_excel = col_s1.button("📊 Ventas", key="btn_sample_excel", use_container_width=True)
    use_sample_csv = col_s2.button("👥 RRHH", key="btn_sample_csv", use_container_width=True)
    use_multi_sample = col_s3.button("🔗 Ambas", key="btn_sample_multi", use_container_width=True)
    
    # Manejo del origen de datos
    active_data_source = []
    if uploaded_files:
        active_data_source = uploaded_files
    elif use_multi_sample or ('sample_choice' in st.session_state and st.session_state.sample_choice == 'multi'):
        st.session_state.sample_choice = 'multi'
        active_data_source = [SAMPLE_EXCEL, SAMPLE_CSV]
    elif use_sample_csv or ('sample_choice' in st.session_state and st.session_state.sample_choice == 'csv'):
        st.session_state.sample_choice = 'csv'
        active_data_source = [SAMPLE_CSV]
    else:
        st.session_state.sample_choice = 'excel'
        active_data_source = [SAMPLE_EXCEL]

    # Cargar DataFrame Maestro, Procedencias y Relaciones
    if active_data_source:
        try:
            df, sources_info, provenance_map, relationships, total_original_records = load_data(
                active_data_source, max_rows=1000
            )
            data_summary, classification = get_data_summary(df, total_original_records, provenance_map=provenance_map)
            
            st.divider()
            st.subheader("📈 Resumen del Modelo Multitabla")
            
            st.markdown(f'<div class="sample-badge">📂 {len(sources_info)} Planilla(s) | ⚡ {len(df):,} de {total_original_records:,} filas</div>', unsafe_allow_html=True)
            
            if relationships:
                st.markdown("#### 🔗 Relaciones Detectadas")
                for rel in relationships:
                    st.markdown(f'<div class="rel-badge">🔗 <strong>{rel["table1"]}</strong> [{rel["key1"]}] ↔️ <strong>{rel["table2"]}</strong> [{rel["key2"]}]</div>', unsafe_allow_html=True)
            
            st.metric("Total Columnas Combinadas", f"{data_summary['total_cols']}")
            st.metric("Métricamente Numéricas", len(classification['numeric']))
            st.metric("Dimensiones Categoría", len(classification['categorical']))
            st.metric("Variables Geográficas", len(classification['geographic']))
            
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            st.stop()

# ---------------------------------------------------------
# HEADER PRINCIPAL
# ---------------------------------------------------------
sources_names_str = ", ".join(list(sources_info.keys())) if sources_info else "Planillas Personalizadas"

st.markdown(f"""
<div class="bi-header">
    <div class="bi-title">
        <span>⚡</span> Galería Épica & Inteligencia de Negocio Power BI
    </div>
    <div class="bi-subtitle">
        Planillas activas: <strong>{sources_names_str}</strong> ({len(df):,} filas muestreadas) | Visualiza combinaciones con reseña de datos reales, contexto ejecutivo de negocio e instrucciones paso a paso para Power BI Desktop.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GENERAR CATÁLOGO MULTIVARIABLE Y COMBINATORIO COMPLETO
# ---------------------------------------------------------
all_visuals_dict = generate_all_possible_visuals(df, provenance_map=provenance_map, relationships=relationships)

# Definir Pestañas de la Galería
gallery_categories = list(all_visuals_dict.keys())
all_tabs = gallery_categories + ["🎨 Creador Libre", "📑 Manual Completo (.HTML / PDF)", "🔍 Modelo & Procedencia"]

active_tabs = st.tabs(all_tabs)

# =========================================================
# PESTAÑAS 1 A 8: GALERÍA DE COMPONENTES POR CATEGORÍA
# =========================================================
for idx, cat_name in enumerate(gallery_categories):
    with active_tabs[idx]:
        st.subheader(f"{cat_name}")
        st.caption(f"Explora todos los componentes de la categoría '{cat_name}' situados en su contexto de negocio con interpretación de datos reales.")
        
        visual_list = all_visuals_dict[cat_name]
        
        for row_idx in range(0, len(visual_list), 2):
            cols = st.columns(2)
            for i, col in enumerate(cols):
                if row_idx + i < len(visual_list):
                    vis_info = visual_list[row_idx + i]
                    with col:
                        st.markdown(f"#### {vis_info['icon']} {vis_info['title']}")
                        
                        # Recuadro de Contexto de Negocio e Interpretación
                        st.markdown(f'<div class="context-box">{vis_info["description"]}</div>', unsafe_allow_html=True)
                        
                        fig = build_plotly_chart(
                            df,
                            visual_key=vis_info["key"],
                            x_col=vis_info["x_col"],
                            y_col=vis_info["y_col"],
                            legend_col=vis_info.get("legend_col"),
                            secondary_y=vis_info.get("secondary_y"),
                            agg_func=vis_info.get("agg_func", "SUM")
                        )
                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            key=f"chart_gal_{idx}_{row_idx}_{i}_{vis_info['key']}"
                        )
                        
                        if st.button(
                            f"📖 Ver Receta & Guía Power BI",
                            key=f"btn_modal_{idx}_{row_idx}_{i}_{vis_info['key']}",
                            use_container_width=True
                        ):
                            show_powerbi_guide_modal(vis_info)
                            
                        st.divider()

# =========================================================
# PESTAÑA: CREADOR LIBRE PERSONALIZADO
# =========================================================
with active_tabs[len(gallery_categories)]:
    st.subheader("🎨 Creador Libre Interactivo Multitabla")
    st.caption("Selecciona cualquier combinación personalizada de columnas de tus planillas cargadas.")
    
    col_controls, col_display = st.columns([0.35, 0.65])
    
    all_cols = list(df.columns)
    numeric_cols = classification['numeric'] + classification['percentage']
    if not numeric_cols:
        numeric_cols = all_cols
        
    with col_controls:
        st.markdown("#### ⚙️ Configura tu Componente")
        
        visual_type_options = {key: spec["name"] for key, spec in POWERBI_VISUAL_CATALOG.items()}
        selected_visual_key = st.selectbox(
            "1. Tipo de Componente de Power BI:",
            options=list(visual_type_options.keys()),
            format_func=lambda k: f"{POWERBI_VISUAL_CATALOG[k]['icon']} {POWERBI_VISUAL_CATALOG[k]['name']}",
            key="builder_select_visual_key"
        )
        
        x_selected = st.selectbox("2. Eje X / Categoría / Filas:", options=all_cols, index=0, key="builder_select_x_col")
        st.caption(f"📍 Origen: `{provenance_map.get(x_selected, 'Planilla')}`")
        
        y_selected = st.selectbox("3. Eje Y / Métrica principal:", options=numeric_cols, index=0 if numeric_cols else 0, key="builder_select_y_col")
        st.caption(f"📍 Origen: `{provenance_map.get(y_selected, 'Planilla')}`")

        legend_selected = st.selectbox("4. Leyenda / Columnas (Opcional):", options=["Ninguna"] + all_cols, index=0, key="builder_select_legend_col")
        if legend_selected == "Ninguna":
            legend_selected = None
            
        sec_y_selected = st.selectbox("5. Eje Y Secundario (Opcional):", options=["Ninguna"] + numeric_cols, index=0, key="builder_select_sec_y_col")
        if sec_y_selected == "Ninguna":
            sec_y_selected = None
            
        agg_selected = st.selectbox("6. Agregación:", options=["SUM", "AVERAGE", "COUNT", "DISTINCTCOUNT"], index=0, key="builder_select_agg_func")

    with col_display:
        st.markdown("#### 👁️ Previsualización Resultante")
        
        fig_custom = build_plotly_chart(
            df,
            visual_key=selected_visual_key,
            x_col=x_selected,
            y_col=y_selected,
            legend_col=legend_selected,
            secondary_y=sec_y_selected,
            agg_func=agg_selected
        )
        st.plotly_chart(
            fig_custom,
            use_container_width=True,
            key="plotly_chart_builder_free"
        )
        
        custom_guide = generate_powerbi_guide(
            visual_type_key=selected_visual_key,
            x_col=x_selected,
            y_col=y_selected,
            legend_col=legend_selected,
            secondary_y=sec_y_selected,
            agg_func=agg_selected,
            provenance_map=provenance_map,
            relationships=relationships,
            df=df
        )
        
        custom_vis_info = {
            "key": selected_visual_key,
            "title": POWERBI_VISUAL_CATALOG[selected_visual_key]["name"],
            "icon": POWERBI_VISUAL_CATALOG[selected_visual_key]["icon"],
            "description": f"💡 **Qué informa:** Mapeo personalizado de {y_selected} desglosado por {x_selected}.",
            "guide": custom_guide
        }
        
        if st.button("📖 Abrir Pop-up de Receta Power BI para esta Configuración", key="btn_builder_modal", use_container_width=True):
            show_powerbi_guide_modal(custom_vis_info)

# =========================================================
# PESTAÑA: MANUAL EJECUTIVO COMPLETO
# =========================================================
with active_tabs[len(gallery_categories) + 1]:
    st.subheader("📑 Manual Ejecutivo Completo para Power BI")
    st.caption("Descarga la guía entera en formato HTML/PDF para consultar todos los componentes de una sola vez.")
    
    html_report = generate_html_report(sources_names_str, data_summary, all_visuals_dict)
    
    st.download_button(
        label="📥 Descargar Manual Completo de la Galería (.HTML / PDF)",
        data=html_report,
        file_name=f"Manual_PowerBI_Galeria_Multitabla.html",
        mime="text/html",
        key="btn_download_manual_html",
        use_container_width=True
    )
    
    st.divider()
    st.markdown("### Vista Previa del Manual Completo")
    components.html(html_report, height=600, scrolling=True)

# =========================================================
# PESTAÑA: MODELO & PROCEDENCIA DE LOS DATOS
# =========================================================
with active_tabs[len(gallery_categories) + 2]:
    st.subheader("🔍 Modelo de Datos y Procedencia de Planillas")
    st.caption("Inspecciona la lista de planillas cargadas, relaciones detectadas y origen exacto de cada columna.")
    
    col_p1, col_p2 = st.columns([0.55, 0.45])
    with col_p1:
        st.markdown(f"#### 📂 Planillas Cargadas ({len(sources_info)} Fuentes)")
        for src_name, info in sources_info.items():
            st.markdown(f"📄 **{src_name}**: {info['rows']:,} filas muestreadas | {len(info['cols'])} columnas")
            st.caption(f"Columnas: {', '.join(info['cols'])}")
            st.divider()
            
        st.markdown(f"#### 📋 Muestra de Datos Maestra Combinada ({len(df):,} filas)")
        df_preview = df.copy()
        for col in df_preview.columns:
            if df_preview[col].dtype == 'object':
                df_preview[col] = df_preview[col].astype(str)
        st.dataframe(df_preview, use_container_width=True)
        
    with col_p2:
        st.markdown("#### 🏷️ Detalle de Columnas y Archivo de Origen")
        summary_df = pd.DataFrame(data_summary['column_details'])
        st.dataframe(summary_df, use_container_width=True)
