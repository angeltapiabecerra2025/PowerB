"""
Módulo recomendador inteligente de componentes visuales de Power BI.
Analiza la estructura de la planilla y genera las mejores representaciones visuales.
"""

from modules.data_loader import classify_columns
from modules.powerbi_formatter import generate_powerbi_guide

def Recommend_powerbi_visuals(df):
    """
    Dada una planilla (DataFrame), genera una lista de recomendaciones de visuales de Power BI
    con sus datos, gráficos previsualizados y guías instructivas paso a paso.
    """
    classification = classify_columns(df)
    
    numerics = classification['numeric']
    dates = classification['datetime']
    categoricals = classification['categorical']
    percentages = classification['percentage']
    
    recommendations = []
    
    # 1. Recomendación: Tarjetas KPI de Encabezado Ejecutivo
    if numerics:
        main_num = numerics[0]
        sec_num = numerics[1] if len(numerics) > 1 else (percentages[0] if percentages else None)
        
        guide = generate_powerbi_guide(
            visual_type_key="multi_card",
            x_col=None,
            y_col=main_num,
            secondary_y=sec_num,
            agg_func="SUM"
        )
        recommendations.append({
            "id": "rec_kpi",
            "title": "1. Cabecera de KPIs Principales (Tarjetas Multi-campo)",
            "visual_key": "multi_card",
            "x_col": main_num,
            "y_col": main_num,
            "secondary_y": sec_num,
            "legend_col": None,
            "agg_func": "SUM",
            "guide": guide,
            "purpose": "Proporcionar métricas globales de alto nivel al abrir el reporte."
        })

    # 2. Recomendación: Tendencia Temporal (Combo o Barras Apiladas por Fecha/Año/Mes)
    time_col = dates[0] if dates else (categoricals[0] if categoricals else None)
    if time_col and numerics:
        main_num = numerics[0]
        sec_num = percentages[0] if percentages else (numerics[1] if len(numerics) > 1 else None)
        legend_cat = categoricals[0] if categoricals and categoricals[0] != time_col else None
        
        visual_type = "combo_line_column" if sec_num else "stacked_column"
        
        guide = generate_powerbi_guide(
            visual_type_key=visual_type,
            x_col=time_col,
            y_col=main_num,
            legend_col=legend_cat if visual_type == "stacked_column" else None,
            secondary_y=sec_num if visual_type == "combo_line_column" else None,
            agg_func="SUM"
        )
        
        recommendations.append({
            "id": "rec_trend",
            "title": f"2. Análisis de Evolución Temporal ({time_col})",
            "visual_key": visual_type,
            "x_col": time_col,
            "y_col": main_num,
            "secondary_y": sec_num,
            "legend_col": legend_cat if visual_type == "stacked_column" else None,
            "agg_func": "SUM",
            "guide": guide,
            "purpose": "Analizar cómo evoluciona la métrica en el tiempo y compararla con ratios o desgloses."
        })

    # 3. Recomendación: Matriz Desplegable con Formato Condicional
    if len(categoricals) >= 1 and numerics:
        cat1 = categoricals[0]
        cat2 = categoricals[1] if len(categoricals) > 1 else None
        main_num = numerics[0]
        sec_num = numerics[1] if len(numerics) > 1 else (percentages[0] if percentages else None)
        
        guide = generate_powerbi_guide(
            visual_type_key="matrix",
            x_col=cat1,
            y_col=main_num,
            legend_col=cat2,
            secondary_y=sec_num,
            agg_func="SUM"
        )
        
        recommendations.append({
            "id": "rec_matrix",
            "title": f"3. Matriz de Rendimiento Multidimensional ({cat1}" + (f" vs {cat2}" if cat2 else "") + ")",
            "visual_key": "matrix",
            "x_col": cat1,
            "y_col": main_num,
            "secondary_y": sec_num,
            "legend_col": cat2,
            "agg_func": "SUM",
            "guide": guide,
            "purpose": "Permitir análisis profundos tipo tabla dinámica con barras de datos o escalas de color."
        })

    # 4. Recomendación: Gráfico de Anillos (Donut) para Composición
    if categoricals and numerics:
        cat_donut = categoricals[0] if len(categoricals) == 1 else categoricals[-1]
        main_num = numerics[0]
        
        guide = generate_powerbi_guide(
            visual_type_key="donut",
            x_col=cat_donut,
            y_col=main_num,
            agg_func="SUM"
        )
        
        recommendations.append({
            "id": "rec_donut",
            "title": f"4. Distribución Porcentual por {cat_donut} (Gráfico de Anillos)",
            "visual_key": "donut",
            "x_col": cat_donut,
            "y_col": main_num,
            "secondary_y": None,
            "legend_col": None,
            "agg_func": "SUM",
            "guide": guide,
            "purpose": "Visualizar la participación de mercado o distribución proporcional de las top categorías."
        })

    # 5. Recomendación: Gráfico de Cascada (Waterfall) o Dispersión (Scatter)
    if len(numerics) >= 2 and categoricals:
        cat_wf = categoricals[0]
        main_num = numerics[0]
        sec_num = numerics[1]
        
        guide = generate_powerbi_guide(
            visual_type_key="scatter",
            x_col=main_num,
            y_col=sec_num,
            legend_col=cat_wf,
            agg_func="AVERAGE"
        )
        
        recommendations.append({
            "id": "rec_scatter",
            "title": f"5. Análisis de Correlación ({main_num} vs {sec_num})",
            "visual_key": "scatter",
            "x_col": main_num,
            "y_col": sec_num,
            "secondary_y": sec_num,
            "legend_col": cat_wf,
            "agg_func": "AVERAGE",
            "guide": guide,
            "purpose": "Identificar patrones, valores atípicos y correlación entre dos variables continuas."
        })
    elif categoricals and numerics:
        cat_wf = categoricals[0]
        main_num = numerics[0]
        guide = generate_powerbi_guide(
            visual_type_key="waterfall",
            x_col=cat_wf,
            y_col=main_num,
            agg_func="SUM"
        )
        recommendations.append({
            "id": "rec_waterfall",
            "title": f"5. Puente de Variación por {cat_wf} (Gráfico de Cascada)",
            "visual_key": "waterfall",
            "x_col": cat_wf,
            "y_col": main_num,
            "secondary_y": None,
            "legend_col": None,
            "agg_func": "SUM",
            "guide": guide,
            "purpose": "Explicar los incrementos y reducciones que componen el total final."
        })

    # 6. Recomendación: Segmentadores de Datos (Slicers)
    if categoricals or dates:
        slicer_cols = (dates[:1] + categoricals[:2])
        recommendations.append({
            "id": "rec_slicers",
            "title": "6. Panel de Filtros Interactivos (Segmentadores de Datos)",
            "visual_key": "slicer",
            "x_col": slicer_cols[0],
            "y_col": numerics[0] if numerics else slicer_cols[0],
            "secondary_y": None,
            "legend_col": None,
            "agg_func": "COUNT",
            "guide": {
                "visual_name": "Segmentador de datos (Slicer)",
                "icon": "🔍",
                "category": "Filtro Interactivo",
                "description": "Permite filtrar todo el reporte de forma dinámica.",
                "field_mappings": [
                    {"well": "Campo de filtro 1", "field": col, "role": "Filtro interactivo"} for col in slicer_cols
                ],
                "dax_code": "-- No requiere medidas DAX. Opera como filtro sobre el modelo de datos.",
                "secondary_dax": "",
                "format_tips": [
                    "1. Añade un objeto visual **Segmentador de datos** en el margen superior o lateral.",
                    "2. Arrastra el campo seleccionado (ej: Fecha o Región).",
                    "3. En el panel de formato -> **Configuración del segmentador** -> Estilo, selecciona **'Lista desplegable'** o **'Entre'** para fechas."
                ]
            },
            "purpose": "Garantizar la interactividad y exploración dinámica del informe."
        })

    return recommendations
