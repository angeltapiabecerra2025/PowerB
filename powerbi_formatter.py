"""
Catálogo completo de los 30+ objetos visuales de Power BI Desktop y generador de guías paso a paso multitabla con reseñas de casos e interpretación de datos reales.
"""

import pandas as pd

POWERBI_VISUAL_CATALOG = {
    # 1. Columnas y Barras
    "stacked_column": {
        "name": "Gráfico de columnas apiladas",
        "icon": "📊",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X", "Eje Y", "Leyenda", "Información sobre herramientas"],
        "description": "Compara categorías a lo largo del tiempo o grupos mostrando el desglose apilado."
    },
    "clustered_column": {
        "name": "Gráfico de columnas agrupadas",
        "icon": "📊",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X", "Eje Y", "Leyenda"],
        "description": "Compara categorías lado a lado de forma clara sin apilar."
    },
    "hundred_pct_column": {
        "name": "Gráfico de columnas 100% apiladas",
        "icon": "📊",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X", "Eje Y", "Leyenda"],
        "description": "Muestra la proporción relativa (%) de cada categoría respecto al 100% total."
    },
    "stacked_bar": {
        "name": "Gráfico de barras apiladas horizontales",
        "icon": "📶",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje Y", "Eje X", "Leyenda"],
        "description": "Barras horizontales apiladas ideales para nombres largos."
    },
    "clustered_bar": {
        "name": "Gráfico de barras agrupadas horizontales",
        "icon": "📶",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje Y (Categoría)", "Eje X (Métrica)", "Leyenda"],
        "description": "Ideal para comparar categorías con nombres o etiquetas largas de forma horizontal."
    },
    "hundred_pct_bar": {
        "name": "Gráfico de barras 100% apiladas horizontales",
        "icon": "📶",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje Y", "Eje X", "Leyenda"],
        "description": "Muestra la composición en porcentaje horizontal sobre el 100%."
    },
    "combo_line_column": {
        "name": "Gráfico de líneas y columnas agrupadas",
        "icon": "📈",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X compartido", "Eje Y de columnas", "Eje Y de líneas", "Leyenda"],
        "description": "Combina volúmenes absolutos (ej: Ventas) con ratios o porcentajes (ej: Margen %)."
    },
    "combo_line_stacked": {
        "name": "Gráfico de líneas y columnas apiladas",
        "icon": "📈",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X compartido", "Eje Y de columnas", "Eje Y de líneas", "Leyenda"],
        "description": "Columnas apiladas combinadas con una línea de tendencia secundaria."
    },
    "ribbon_chart": {
        "name": "Gráfico de cintas (Ribbon Chart)",
        "icon": "🎀",
        "category": "📊 Columnas y Barras",
        "wells": ["Eje X", "Eje Y", "Leyenda"],
        "description": "Muestra qué categoría ocupa el primer lugar y cómo cambian los rangos en el tiempo."
    },

    # 2. Tendencias y Tiempo
    "line_chart": {
        "name": "Gráfico de líneas continuas",
        "icon": "📈",
        "category": "📈 Tendencias y Tiempo",
        "wells": ["Eje X (Fecha/Tiempo)", "Eje Y (Métrica)", "Leyenda"],
        "description": "La mejor opción para visualizar la evolución continua de métricas en el tiempo."
    },
    "area_chart": {
        "name": "Gráfico de áreas",
        "icon": "📉",
        "category": "📈 Tendencias y Tiempo",
        "wells": ["Eje X", "Eje Y", "Leyenda"],
        "description": "Visualiza el volumen acumulado y la tendencia de métricas temporales."
    },
    "stacked_area": {
        "name": "Gráfico de áreas apiladas",
        "icon": "📉",
        "category": "📈 Tendencias y Tiempo",
        "wells": ["Eje X", "Eje Y", "Leyenda"],
        "description": "Muestra la contribución apilada de cada serie sobre el área total."
    },

    # 3. Tarjetas e Indicadores KPI
    "single_card": {
        "name": "Tarjeta de campo único KPI",
        "icon": "🔢",
        "category": "🎴 Tarjetas e Indicadores KPI",
        "wells": ["Campos (Métrica clave)"],
        "description": "Muestra una sola cifra monumental y clara en la parte superior del tablero."
    },
    "multi_card": {
        "name": "Tarjeta de varios campos KPI",
        "icon": "🎴",
        "category": "🎴 Tarjetas e Indicadores KPI",
        "wells": ["Campos (Lista de KPIs)"],
        "description": "Agrupa múltiples métricas principales en un contenedor limpio multitabla."
    },
    "kpi_card": {
        "name": "Tarjeta KPI con Tendencia y Objetivo",
        "icon": "🎯",
        "category": "🎴 Tarjetas e Indicadores KPI",
        "wells": ["Valor indicador", "Eje de tendencia", "Objetivo del destino"],
        "description": "Muestra la métrica actual junto con su variación y tendencia de fondo."
    },
    "gauge": {
        "name": "Medidor (Gauge)",
        "icon": "⏱️",
        "category": "🎴 Tarjetas e Indicadores KPI",
        "wells": ["Valor", "Valor mínimo", "Valor máximo", "Valor de destino (Meta)"],
        "description": "Evalúa el avance del rendimiento actual respecto a un objetivo o meta fijada."
    },

    # 4. Tablas y Matrices
    "matrix": {
        "name": "Matriz con Formato Condicional",
        "icon": "🔢",
        "category": "🔢 Tablas y Matrices",
        "wells": ["Filas", "Columnas", "Valores"],
        "description": "Recrea tablas dinámicas con jerarquía desplegable (+/-) y escalas de color o barras de datos."
    },
    "table": {
        "name": "Tabla Detallada con Formato Alternado",
        "icon": "📋",
        "category": "🔢 Tablas y Matrices",
        "wells": ["Columnas de datos"],
        "description": "Lista transaccional registro por registro útil para auditoría y exportación a Excel."
    },

    # 5. Composición y Proporciones
    "donut": {
        "name": "Gráfico de anillos (Donut)",
        "icon": "🍩",
        "category": "🍩 Composición y Proporciones",
        "wells": ["Leyenda", "Valores"],
        "description": "Muestra la distribución porcentual entre 3 y 6 categorías principales con centro hueco."
    },
    "pie": {
        "name": "Gráfico de sectores (Pie)",
        "icon": "🥧",
        "category": "🍩 Composición y Proporciones",
        "wells": ["Leyenda", "Valores"],
        "description": "Representa proporciones sobre el total de un conjunto de datos."
    },
    "treemap": {
        "name": "Mapa de árbol (Treemap)",
        "icon": "🟩",
        "category": "🍩 Composición y Proporciones",
        "wells": ["Categoría", "Detalles", "Valores"],
        "description": "Muestra la composición mediante rectángulos proporcionales según el tamaño de la métrica."
    },
    "funnel": {
        "name": "Gráfico de embudo (Funnel)",
        "icon": "🔻",
        "category": "🍩 Composición y Proporciones",
        "wells": ["Categoría", "Valores"],
        "description": "Muestra las etapas secuenciales de un proceso o conversión de mayor a menor."
    },

    # 6. Mapas y Geografía
    "bubble_map": {
        "name": "Mapa de burbujas (Map)",
        "icon": "🌍",
        "category": "🗺️ Mapas y Geografía",
        "wells": ["Ubicación", "Latitud / Longitud", "Tamaño de burbuja", "Leyenda"],
        "description": "Ubica las métricas sobre un mapa geográfico interactivo con tamaño proporcional."
    },
    "filled_map": {
        "name": "Mapa de coropletas (Filled Map)",
        "icon": "🗺️",
        "category": "🗺️ Mapas y Geografía",
        "wells": ["Ubicación (País/Región)", "Saturación del color / Valores"],
        "description": "Pinta regiones o países enteros según la intensidad del valor de la métrica."
    },

    # 7. Análisis y Correlación
    "waterfall": {
        "name": "Gráfico de cascada (Waterfall)",
        "icon": "📉",
        "category": "🔮 Análisis e Inteligencia Avanzada",
        "wells": ["Categoría", "Valores (Y)"],
        "description": "Muestra cómo un importe cambia debido a incrementos y reducciones hasta el total."
    },
    "scatter": {
        "name": "Gráfico de dispersión (Scatter)",
        "icon": "🔮",
        "category": "🔮 Análisis e Inteligencia Avanzada",
        "wells": ["Eje X", "Eje Y", "Valores (Puntos)", "Tamaño de la burbuja"],
        "description": "Muestra la correlación o patrones entre 2 métricas continuas."
    },
    "decomp_tree": {
        "name": "Árbol de descomposición (Decomposition Tree)",
        "icon": "🌳",
        "category": "🔮 Análisis e Inteligencia Avanzada",
        "wells": ["Analizar (Métrica)", "Explicar por (Lista de Dimensiones)"],
        "description": "Permite desglosar de forma interactiva una métrica a través de múltiples dimensiones ad-hoc."
    },
    "key_influencers": {
        "name": "Influenciadores clave (Key Influencers AI)",
        "icon": "🤖",
        "category": "🔮 Análisis e Inteligencia Avanzada",
        "wells": ["Analizar", "Explicar por"],
        "description": "Utiliza inteligencia artificial de Power BI para descubrir qué factores influyen en una métrica."
    },

    # 8. Filtros y Segmentadores
    "slicer_date": {
        "name": "Segmentador de datos por Rango de Fecha",
        "icon": "📅",
        "category": "🔍 Filtros e Interactividad",
        "wells": ["Campo Fecha"],
        "description": "Permite filtrar todo el reporte mediante un selector de rango de fechas interactivo."
    },
    "slicer_dropdown": {
        "name": "Segmentador desplegable por Dimensión",
        "icon": "🔍",
        "category": "🔍 Filtros e Interactividad",
        "wells": ["Campo Categoría"],
        "description": "Filtra dinámicamente el reporte eligiendo categorías de una lista desplegable."
    }
}

def generate_data_case_study(df, x_col, y_col, legend_col=None, agg_func="SUM"):
    """
    Extrae casos reales de los datos cargados y genera una reseña interpretativa con ejemplos concretos.
    """
    default_res = {
        "total_analyzed": "0.00",
        "examples": [],
        "business_recommendation": "Selecciona una columna métrica numérica para ver el desglose por casos reales de uso."
    }

    if df is None or df.empty or not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
        return default_res

    try:
        df_clean = df.copy()
        df_clean[y_col] = pd.to_numeric(df_clean[y_col], errors='coerce').fillna(0.0)
        df_clean[x_col] = df_clean[x_col].fillna("Sin Registro").astype(str)
        
        agg_type = 'sum' if agg_func == 'SUM' else ('mean' if agg_func == 'AVERAGE' else 'count')
        grouped = df_clean.groupby(x_col, as_index=False)[y_col].agg(agg_type)
        grouped[y_col] = pd.to_numeric(grouped[y_col], errors='coerce').fillna(0.0)
        
        if grouped.empty:
            return default_res

        top_grouped = grouped.sort_values(by=y_col, ascending=False).head(3)
        total_val = float(grouped[y_col].sum())
        
        examples_list = []
        for idx, row in top_grouped.iterrows():
            cat_val = str(row[x_col])
            num_val = float(row[y_col])
            pct = round((num_val / max(total_val, 1.0)) * 100, 1) if total_val > 0 else 0.0
            
            examples_list.append({
                "category": cat_val,
                "value_raw": num_val,
                "value_formatted": f"{num_val:,.2f}",
                "percentage": f"{pct}%",
                "interpretation": f"📌 **Caso Ejemplo '{cat_val}'**: Registra un valor real de **{num_val:,.2f}** ({pct}% del acumulado). En la toma de decisiones, este elemento representa un pilar clave en la medición de **{y_col}**."
            })
            
        top_cat = str(top_grouped.iloc[0][x_col]) if not top_grouped.empty else "Categoría Principal"
        top_num = float(top_grouped.iloc[0][y_col]) if not top_grouped.empty else 0.0
        top_pct = round((top_num / max(total_val, 1.0)) * 100, 1) if total_val > 0 and not top_grouped.empty else 0.0
        
        business_recommendation = (
            f"🎯 **Recomendación de Decisión en Power BI**: Los datos reales muestran que **'{top_cat}'** lidera con **{top_num:,.2f}** ({top_pct}% del total). "
            f"En Power BI Desktop se recomienda configurar **Alertas de Rendimiento** y un **Formato Condicional de Color** para destacar inmediatamente este caso sobre los demás registros."
        )
        
        return {
            "total_analyzed": f"{total_val:,.2f}",
            "examples": examples_list,
            "business_recommendation": business_recommendation
        }
    except Exception:
        return default_res

def generate_powerbi_guide(visual_type_key, x_col, y_col, legend_col=None, secondary_y=None, agg_func="SUM", provenance_map=None, relationships=None, df=None):
    """
    Genera la pauta estructurada completa para Power BI Desktop especificando procedencia de cada archivo y casos de ejemplo reales.
    """
    provenance_map = provenance_map or {}
    relationships = relationships or []
    spec = POWERBI_VISUAL_CATALOG.get(visual_type_key, POWERBI_VISUAL_CATALOG["stacked_column"])
    
    src_x = provenance_map.get(x_col, "Planilla 1")
    src_y = provenance_map.get(y_col, "Planilla 1")
    src_legend = provenance_map.get(legend_col, "Planilla 1") if legend_col else None
    src_sec_y = provenance_map.get(secondary_y, "Planilla 1") if secondary_y else None
    
    is_multi_table = (src_x != src_y) or (legend_col and src_legend != src_x) or (secondary_y and src_sec_y != src_y)

    table_name_y = src_y.replace('.xlsx', '').replace('.csv', '').replace(' ', '_')
    table_name_x = src_x.replace('.xlsx', '').replace('.csv', '').replace(' ', '_')

    # Generación de Código DAX multitabla
    dax_code = ""
    if agg_func == "SUM":
        dax_code = f"Total_{y_col} = SUM('{table_name_y}'[{y_col}])"
    elif agg_func == "AVERAGE":
        dax_code = f"Promedio_{y_col} = AVERAGE('{table_name_y}'[{y_col}])"
    elif agg_func == "COUNT":
        dax_code = f"Conteo_{y_col} = COUNTROWS('{table_name_y}')"
    elif agg_func == "DISTINCTCOUNT":
        dax_code = f"ConteoUnico_{y_col} = DISTINCTCOUNT('{table_name_y}'[{y_col}])"
    else:
        dax_code = f"Medida_{y_col} = {agg_func}('{table_name_y}'[{y_col}])"
        
    secondary_dax = ""
    if secondary_y:
        secondary_dax = f"Ratio_{secondary_y} = AVERAGE('{src_sec_y.replace('.xlsx', '').replace('.csv', '')}'[{secondary_y}])"
        
    if is_multi_table:
        secondary_dax += f"\n-- Explicación DAX Multitabla:\n-- Para relacionar la dimensión [{x_col}] de '{src_x}' con la métrica [{y_col}] de '{src_y}', usa una relación 1 a Muchos o la función RELATED()."

    field_mappings = []
    
    if visual_type_key in ["stacked_column", "clustered_column", "hundred_pct_column", "ribbon_chart"]:
        field_mappings.append({"well": "Eje X", "field": f"{x_col}", "source": src_x, "role": f"Categoría / Fecha (Desde '{src_x}')"})
        field_mappings.append({"well": "Eje Y", "field": f"{y_col}", "source": src_y, "role": f"Métrica numérico ({agg_func}) (Desde '{src_y}')"})
        if legend_col:
            field_mappings.append({"well": "Leyenda", "field": f"{legend_col}", "source": src_legend, "role": f"Desglose por grupos (Desde '{src_legend}')"})

    elif visual_type_key in ["stacked_bar", "clustered_bar", "hundred_pct_bar"]:
        field_mappings.append({"well": "Eje Y", "field": x_col, "source": src_x, "role": f"Categoría horizontal (Desde '{src_x}')"})
        field_mappings.append({"well": "Eje X", "field": y_col, "source": src_y, "role": f"Métrica ({agg_func}) (Desde '{src_y}')"})
        if legend_col:
            field_mappings.append({"well": "Leyenda", "field": legend_col, "source": src_legend, "role": f"Desglose por grupos (Desde '{src_legend}')"})

    elif visual_type_key in ["combo_line_column", "combo_line_stacked"]:
        field_mappings.append({"well": "Eje X compartido", "field": x_col, "source": src_x, "role": f"Eje temporal o dimensión (Desde '{src_x}')"})
        field_mappings.append({"well": "Eje Y de columnas", "field": y_col, "source": src_y, "role": f"Métrica volumen ({agg_func}) (Desde '{src_y}')"})
        if secondary_y:
            field_mappings.append({"well": "Eje Y de líneas", "field": secondary_y, "source": src_sec_y, "role": f"Métrica tasa/ratio (Desde '{src_sec_y}')"})
        if legend_col:
            field_mappings.append({"well": "Leyenda", "field": legend_col, "source": src_legend, "role": f"Categoría (Desde '{src_legend}')"})

    elif visual_type_key in ["line_chart", "area_chart", "stacked_area"]:
        field_mappings.append({"well": "Eje X", "field": x_col, "source": src_x, "role": f"Secuencia fecha/tiempo (Desde '{src_x}')"})
        field_mappings.append({"well": "Eje Y", "field": y_col, "source": src_y, "role": f"Evolución numérica ({agg_func}) (Desde '{src_y}')"})
        if legend_col:
            field_mappings.append({"well": "Leyenda", "field": legend_col, "source": src_legend, "role": f"Series por grupo (Desde '{src_legend}')"})

    elif visual_type_key == "matrix":
        field_mappings.append({"well": "Filas", "field": x_col, "source": src_x, "role": f"Jerarquía principal (Desde '{src_x}')"})
        if legend_col:
            field_mappings.append({"well": "Columnas", "field": legend_col, "source": src_legend, "role": f"Dimensiones columnas (Desde '{src_legend}')"})
        field_mappings.append({"well": "Valores", "field": y_col, "source": src_y, "role": f"Valor numérico ({agg_func}) (Desde '{src_y}')"})

    elif visual_type_key in ["donut", "pie", "funnel"]:
        field_mappings.append({"well": "Leyenda / Categoría", "field": x_col, "source": src_x, "role": f"Categorías (Desde '{src_x}')"})
        field_mappings.append({"well": "Valores", "field": y_col, "source": src_y, "role": f"Proporción ({agg_func}) (Desde '{src_y}')"})

    elif visual_type_key in ["bubble_map", "filled_map"]:
        field_mappings.append({"well": "Ubicación", "field": x_col, "source": src_x, "role": f"Ubicación geográfica (Desde '{src_x}')"})
        field_mappings.append({"well": "Tamaño / Color", "field": y_col, "source": src_y, "role": f"Métrica geográfica ({agg_func}) (Desde '{src_y}')"})

    elif visual_type_key == "decomp_tree":
        field_mappings.append({"well": "Analizar", "field": y_col, "source": src_y, "role": f"Métrica principal ({agg_func}) (Desde '{src_y}')"})
        field_mappings.append({"well": "Explicar por", "field": x_col, "source": src_x, "role": f"Dimensión 1 (Desde '{src_x}')"})

    elif visual_type_key in ["single_card", "multi_card", "kpi_card"]:
        field_mappings.append({"well": "Campos", "field": y_col, "source": src_y, "role": f"Valor KPI ({agg_func}) (Desde '{src_y}')"})
        if secondary_y:
            field_mappings.append({"well": "Campos / Meta", "field": secondary_y, "source": src_sec_y, "role": f"Valor KPI 2 (Desde '{src_sec_y}')"})

    else:
        field_mappings.append({"well": "Campo principal", "field": x_col, "source": src_x, "role": f"Dimensión (Desde '{src_x}')"})
        if y_col:
            field_mappings.append({"well": "Valores", "field": y_col, "source": src_y, "role": f"Métrica ({src_y})"})

    # Generar casos de estudio interpretativos con datos reales si df está presente
    case_study = generate_data_case_study(df, x_col, y_col, legend_col, agg_func)

    format_tips = [
        f"1. Abre **Power BI Desktop** y carga tus planillas: `{src_x}` y `{src_y}`.",
    ]
    
    if is_multi_table:
        format_tips.append(f"2. 🔗 **Vista de Modelo (Relación de Tablas)**: Dirígete a la pestaña 'Modelo' a la izquierda y arrastra la llave común entre las tablas `{src_x}` y `{src_y}` (ej: ID_Cliente o Código) para establecer la relación 1 a Muchos.")
        format_tips.append(f"3. Selecciona el objeto visual **'{spec['name']}'** desde la paleta de Visualizaciones.")
        format_tips.append(f"4. Arrastra la columna `{x_col}` desde la tabla **'{src_x}'** al contenedor **{field_mappings[0]['well']}**.")
        format_tips.append(f"5. Arrastra la columna `{y_col}` desde la tabla **'{src_y}'** al contenedor **Valores**.")
    else:
        format_tips.append(f"2. Selecciona el objeto visual **'{spec['name']}'** desde la paleta de Visualizaciones.")
        format_tips.append(f"3. Arrastra los campos desde la tabla **'{src_x}'** a sus contenedores asignados.")

    format_tips.append(f"6. En el panel de formato, activa **Etiquetas de datos** y ajusta el ordenamiento por `{y_col}`.")

    return {
        "visual_name": spec["name"],
        "icon": spec["icon"],
        "category": spec["category"],
        "description": spec["description"],
        "field_mappings": field_mappings,
        "dax_code": dax_code,
        "secondary_dax": secondary_dax,
        "format_tips": format_tips,
        "is_multi_table": is_multi_table,
        "case_study": case_study
    }
