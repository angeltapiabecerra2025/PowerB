"""
Módulo generador masivo y combinatorio de componentes de Power BI con Inteligencia Contextual de Negocio y Casos de Estudio de Datos Reales.
"""

try:
    from modules.data_loader import classify_columns
    from modules.powerbi_formatter import POWERBI_VISUAL_CATALOG, generate_powerbi_guide
except (ModuleNotFoundError, ImportError):
    from data_loader import classify_columns
    from powerbi_formatter import POWERBI_VISUAL_CATALOG, generate_powerbi_guide

def build_executive_title_and_context(x_col, y_col, legend_col=None, visual_key=None, agg_func="SUM", provenance_map=None):
    """
    Genera un título ejecutivo contextualizado y una explicación sobre QUÉ INFORMA el gráfico en el contexto del negocio.
    """
    provenance_map = provenance_map or {}
    src_x = provenance_map.get(x_col, "")
    src_y = provenance_map.get(y_col, "")
    
    y_clean = str(y_col).lower()
    x_clean = str(x_col).lower()
    
    # 1. Determinar el contexto del Dominio de Datos
    domain = "General"
    if any(k in y_clean for k in ['venta', 'sales', 'monto', 'ingreso', 'revenue', 'facturacion', 'facturación']):
        domain = "Ventas y Facturación Comercial"
    elif any(k in y_clean for k in ['costo', 'cost', 'gasto', 'presupuesto', 'egreso', 'inversion']):
        domain = "Estructura de Costos y Control Presupuestario"
    elif any(k in y_clean for k in ['salario', 'sueldo', 'renta', 'desempeno', 'desempeño', 'score', 'evaluacion', 'evaluación', 'rrhh', 'personal']):
        domain = "Gestión de Talento Humano y Desempeño"
    elif any(k in y_clean for k in ['poblacion', 'población', 'habitantes', 'natalidad', 'personas', 'demografia', 'infant', 'mortality', 'expectancy', 'life', 'muertes']):
        domain = "Análisis de Salud Pública, Demografía y Vida"
    elif any(k in y_clean for k in ['unidades', 'cantidad', 'stock', 'inventario', 'pedidos', 'ordenes']):
        domain = "Volumen Operativo y Capacidad Logística"
    elif any(k in y_clean for k in ['margen', 'tasa', 'porcentaje', 'pct', '%', 'csat', 'retencion']):
        domain = "Ratios de Eficiencia y Calidad de Servicio"

    # 2. Formatear Título Ejecutivo Descriptivo
    if visual_key in ["bubble_map", "filled_map"]:
        exec_title = f"🌍 Distribución Geográfica de {y_col} por {x_col}"
        info_text = f"💡 **Qué informa este gráfico:** Sitúa en un mapa geográfico la magnitud acumulada de **{y_col}** en cada **{x_col}**. Permite visualizar los centros de mayor concentración territorial en el contexto de {domain.lower()}."
    elif visual_key in ["line_chart", "area_chart"]:
        exec_title = f"📈 Tendencia Histórica y Desglose de {y_col} por {x_col}"
        info_text = f"💡 **Qué informa este gráfico:** Muestra el comportamiento y variación de **{y_col}** a lo largo de **{x_col}**, permitiendo detectar patrones de variación y picos en el contexto de {domain.lower()}."
    elif visual_key in ["donut", "pie", "treemap"]:
        exec_title = f"🍩 Proporción y Peso Relativo de {y_col} por {x_col}"
        info_text = f"💡 **Qué informa este gráfico:** Representa la participación porcentual de cada **{x_col}** sobre el total de **{y_col}**, destacando los componentes líderes en {domain.lower()}."
    elif visual_key in ["single_card", "multi_card", "kpi_card", "gauge"]:
        exec_title = f"🔢 Indicador Clave (KPI): Total de {y_col}"
        info_text = f"💡 **Qué informa este indicador:** Resume la cifra monumental consolidada de **{y_col}**, sirviendo como métrica de alto nivel ejecutiva para evaluar el cumplimiento general en {domain.lower()}."
    elif visual_key == "waterfall":
        exec_title = f"📉 Análisis de Variación Cascada de {y_col} por {x_col}"
        info_text = f"💡 **Qué informa este gráfico:** Desglosa los aumentos y disminuciones secuenciales que experimenta **{y_col}** según **{x_col}**, situando el resultado acumulado en {domain.lower()}."
    elif visual_key == "scatter":
        exec_title = f"🔮 Correlación e Impacto: {x_col} vs {y_col}"
        info_text = f"💡 **Qué informa este gráfico:** Examina si existe una relación directa entre **{x_col}** y **{y_col}**, permitiendo identificar valores atípicos y patrones de comportamiento en {domain.lower()}."
    else:
        exec_title = f"📊 Comparativa de {y_col} por {x_col}"
        info_text = f"💡 **Qué informa este gráfico:** Compara los volúmenes totales de **{y_col}** desglosados entre las categorías de **{x_col}**, ofreciendo una visión clara de rendimiento para {domain.lower()}."

    if src_y and src_x and src_y != src_x and not str(src_x).startswith('_'):
        info_text += f" *(Datos entrelazados desde '{src_y}' y '{src_x}')*"

    return exec_title, info_text

def generate_all_possible_visuals(df, provenance_map=None, relationships=None):
    """
    Genera el catálogo exhaustivo y masivo de gráficos y tablas aplicables agrupados por categoría,
    filtrando estrictamente cualquier columna de metadatos del sistema (_Origen_Archivo).
    """
    provenance_map = provenance_map or {}
    relationships = relationships or []
    
    classification = classify_columns(df)
    
    # Filtrar columnas internas
    numerics = [c for c in classification['numeric'] if not str(c).startswith('_')]
    dates = [c for c in classification['datetime'] if not str(c).startswith('_')]
    categoricals = [c for c in classification['categorical'] if not str(c).startswith('_')]
    geographics = [c for c in classification['geographic'] if not str(c).startswith('_')]
    percentages = [c for c in classification['percentage'] if not str(c).startswith('_')]
    
    clean_cols = [c for c in df.columns if not str(c).startswith('_')]
    
    all_visuals = {
        "📊 Columnas y Barras": [],
        "📈 Tendencias y Tiempo": [],
        "🎴 Tarjetas e Indicadores KPI": [],
        "🔢 Tablas y Matrices": [],
        "🍩 Composición y Proporciones": [],
        "🗺️ Mapas y Geografía": [],
        "🔮 Análisis e Inteligencia": [],
        "🔍 Filtros e Interactividad": []
    }
    
    main_num = numerics[0] if numerics else (clean_cols[0] if clean_cols else "Valor")
    num_list = numerics[:4] if numerics else [main_num]
    cat_list = (geographics + categoricals)[:4] if (geographics + categoricals) else (clean_cols[:1] if clean_cols else ["Categoria"])
    date_list = dates[:2] if dates else (cat_list[:2] if cat_list else ["Registro"])
    
    def make_guide(v_key, x, y, legend=None, sec_y=None, agg="SUM"):
        return generate_powerbi_guide(
            visual_type_key=v_key,
            x_col=x, y_col=y, legend_col=legend, secondary_y=sec_y, agg_func=agg,
            provenance_map=provenance_map, relationships=relationships, df=df
        )

    # 1. 📊 Columnas y Barras
    for num_col in num_list:
        for cat_col in cat_list[:2]:
            sec_cat = [c for c in cat_list if c != cat_col]
            sec_cat_val = sec_cat[0] if sec_cat else None
            
            exec_title, context_desc = build_executive_title_and_context(cat_col, num_col, sec_cat_val, "stacked_column", "SUM", provenance_map)
            guide = make_guide("stacked_column", cat_col, num_col, legend=sec_cat_val)
            all_visuals["📊 Columnas y Barras"].append({
                "key": "stacked_column",
                "title": exec_title,
                "icon": "📊",
                "x_col": cat_col, "y_col": num_col, "legend_col": sec_cat_val, "secondary_y": None,
                "agg_func": "SUM", "guide": guide,
                "description": context_desc
            })
            
            exec_title_bar, context_desc_bar = build_executive_title_and_context(cat_col, num_col, None, "clustered_bar", "SUM", provenance_map)
            guide_bar = make_guide("clustered_bar", cat_col, num_col)
            all_visuals["📊 Columnas y Barras"].append({
                "key": "clustered_bar",
                "title": exec_title_bar,
                "icon": "📶",
                "x_col": cat_col, "y_col": num_col, "legend_col": None, "secondary_y": None,
                "agg_func": "SUM", "guide": guide_bar,
                "description": context_desc_bar
            })

    if len(num_list) >= 2:
        num1, num2 = num_list[0], num_list[1]
        cat_c = cat_list[0]
        exec_t_combo, ctx_combo = build_executive_title_and_context(cat_c, num1, None, "combo_line_column", "SUM", provenance_map)
        guide_combo = make_guide("combo_line_column", cat_c, num1, sec_y=num2)
        all_visuals["📊 Columnas y Barras"].append({
            "key": "combo_line_column",
            "title": exec_t_combo,
            "icon": "📈",
            "x_col": cat_c, "y_col": num1, "legend_col": None, "secondary_y": num2,
            "agg_func": "SUM", "guide": guide_combo,
            "description": ctx_combo
        })

    # 2. 📈 Tendencias y Tiempo
    for d_col in date_list:
        for num_col in num_list[:2]:
            leg_val = cat_list[0] if (cat_list and cat_list[0] != d_col) else None
            exec_t_line, ctx_line = build_executive_title_and_context(d_col, num_col, leg_val, "line_chart", "SUM", provenance_map)
            guide_line = make_guide("line_chart", d_col, num_col, legend=leg_val)
            all_visuals["📈 Tendencias y Tiempo"].append({
                "key": "line_chart",
                "title": exec_t_line,
                "icon": "📈",
                "x_col": d_col, "y_col": num_col, "legend_col": leg_val, "secondary_y": None,
                "agg_func": "SUM", "guide": guide_line,
                "description": ctx_line
            })
            
            exec_t_area, ctx_area = build_executive_title_and_context(d_col, num_col, None, "area_chart", "SUM", provenance_map)
            guide_area = make_guide("area_chart", d_col, num_col)
            all_visuals["📈 Tendencias y Tiempo"].append({
                "key": "area_chart",
                "title": exec_t_area,
                "icon": "📉",
                "x_col": d_col, "y_col": num_col, "legend_col": None, "secondary_y": None,
                "agg_func": "SUM", "guide": guide_area,
                "description": ctx_area
            })

    # 3. 🎴 Tarjetas e Indicadores KPI
    for num_col in num_list[:3]:
        exec_t_card, ctx_card = build_executive_title_and_context("Global", num_col, None, "single_card", "SUM", provenance_map)
        guide_card = make_guide("single_card", None, num_col, agg="SUM")
        all_visuals["🎴 Tarjetas e Indicadores KPI"].append({
            "key": "single_card",
            "title": exec_t_card,
            "icon": "🔢",
            "x_col": num_col, "y_col": num_col, "legend_col": None, "secondary_y": None,
            "agg_func": "SUM", "guide": guide_card,
            "description": ctx_card
        })

    exec_t_gauge, ctx_gauge = build_executive_title_and_context("Objetivo", main_num, None, "gauge", "AVERAGE", provenance_map)
    guide_gauge = make_guide("gauge", None, main_num, sec_y=num_list[1] if len(num_list) > 1 else None, agg="AVERAGE")
    all_visuals["🎴 Tarjetas e Indicadores KPI"].append({
        "key": "gauge",
        "title": exec_t_gauge,
        "icon": "⏱️",
        "x_col": main_num, "y_col": main_num, "legend_col": None, "secondary_y": num_list[1] if len(num_list) > 1 else None,
        "agg_func": "AVERAGE", "guide": guide_gauge,
        "description": ctx_gauge
    })

    # 4. 🔢 Tablas y Matrices
    for cat1 in cat_list[:2]:
        cat2 = cat_list[1] if len(cat_list) > 1 and cat_list[1] != cat1 else None
        exec_t_mat, ctx_mat = build_executive_title_and_context(cat1, main_num, cat2, "matrix", "SUM", provenance_map)
        guide_mat = make_guide("matrix", cat1, main_num, legend=cat2)
        all_visuals["🔢 Tablas y Matrices"].append({
            "key": "matrix",
            "title": exec_t_mat,
            "icon": "🔢",
            "x_col": cat1, "y_col": main_num, "legend_col": cat2, "secondary_y": num_list[1] if len(num_list) > 1 else None,
            "agg_func": "SUM", "guide": guide_mat,
            "description": ctx_mat
        })

    guide_tbl = make_guide("table", cat_list[0], main_num)
    all_visuals["🔢 Tablas y Matrices"].append({
        "key": "table",
        "title": f"📋 Matriz Registro por Registro: {main_num} y {cat_list[0]}",
        "icon": "📋",
        "x_col": cat_list[0], "y_col": main_num, "legend_col": cat_list[1] if len(cat_list) > 1 else None, "secondary_y": None,
        "agg_func": "SUM", "guide": guide_tbl,
        "description": f"💡 **Qué informa:** Muestra la lista detallada registro por registro para auditorías en profundidad."
    })

    # 5. 🍩 Composición y Proporciones
    for cat_c in cat_list[:2]:
        exec_t_donut, ctx_donut = build_executive_title_and_context(cat_c, main_num, None, "donut", "SUM", provenance_map)
        guide_donut = make_guide("donut", cat_c, main_num)
        all_visuals["🍩 Composición y Proporciones"].append({
            "key": "donut",
            "title": exec_t_donut,
            "icon": "🍩",
            "x_col": cat_c, "y_col": main_num, "legend_col": None, "secondary_y": None,
            "agg_func": "SUM", "guide": guide_donut,
            "description": ctx_donut
        })
        
        exec_t_tree, ctx_tree = build_executive_title_and_context(cat_c, main_num, None, "treemap", "SUM", provenance_map)
        guide_tree = make_guide("treemap", cat_c, main_num)
        all_visuals["🍩 Composición y Proporciones"].append({
            "key": "treemap",
            "title": exec_t_tree,
            "icon": "🟩",
            "x_col": cat_c, "y_col": main_num, "legend_col": None, "secondary_y": None,
            "agg_func": "SUM", "guide": guide_tree,
            "description": ctx_tree
        })

    # 6. 🗺️ Mapas y Geografía
    geo_cols = geographics if geographics else [c for c in categoricals if any(k in str(c).lower() for k in ['region', 'región', 'pais', 'país', 'ciudad', 'zona', 'comuna', 'country', 'city'])]
    if geo_cols:
        for g_col in geo_cols:
            exec_t_map, ctx_map = build_executive_title_and_context(g_col, main_num, None, "bubble_map", "SUM", provenance_map)
            guide_map = make_guide("bubble_map", g_col, main_num)
            all_visuals["🗺️ Mapas y Geografía"].append({
                "key": "bubble_map",
                "title": exec_t_map,
                "icon": "🌍",
                "x_col": g_col, "y_col": main_num, "legend_col": None, "secondary_y": None,
                "agg_func": "SUM", "guide": guide_map,
                "description": ctx_map
            })
            
            exec_t_filled, ctx_filled = build_executive_title_and_context(g_col, main_num, None, "filled_map", "SUM", provenance_map)
            guide_filled = make_guide("filled_map", g_col, main_num)
            all_visuals["🗺️ Mapas y Geografía"].append({
                "key": "filled_map",
                "title": exec_t_filled,
                "icon": "🗺️",
                "x_col": g_col, "y_col": main_num, "legend_col": None, "secondary_y": None,
                "agg_func": "SUM", "guide": guide_filled,
                "description": ctx_filled
            })
    else:
        g_col = cat_list[0]
        exec_t_map, ctx_map = build_executive_title_and_context(g_col, main_num, None, "bubble_map", "SUM", provenance_map)
        guide_map = make_guide("bubble_map", g_col, main_num)
        all_visuals["🗺️ Mapas y Geografía"].append({
            "key": "bubble_map",
            "title": exec_t_map,
            "icon": "🌍",
            "x_col": g_col, "y_col": main_num, "legend_col": None, "secondary_y": None,
            "agg_func": "SUM", "guide": guide_map,
            "description": ctx_map
        })

    # 7. 🔮 Análisis e Inteligencia Avanzada
    exec_t_wf, ctx_wf = build_executive_title_and_context(cat_list[0], main_num, None, "waterfall", "SUM", provenance_map)
    guide_wf = make_guide("waterfall", cat_list[0], main_num)
    all_visuals["🔮 Análisis e Inteligencia"].append({
        "key": "waterfall",
        "title": exec_t_wf,
        "icon": "📉",
        "x_col": cat_list[0], "y_col": main_num, "legend_col": None, "secondary_y": None,
        "agg_func": "SUM", "guide": guide_wf,
        "description": ctx_wf
    })
    
    if len(num_list) >= 2:
        exec_t_scat, ctx_scat = build_executive_title_and_context(num_list[0], num_list[1], cat_list[0], "scatter", "AVERAGE", provenance_map)
        guide_scat = make_guide("scatter", num_list[0], num_list[1], legend=cat_list[0])
        all_visuals["🔮 Análisis e Inteligencia"].append({
            "key": "scatter",
            "title": exec_t_scat,
            "icon": "🔮",
            "x_col": num_list[0], "y_col": num_list[1], "legend_col": cat_list[0], "secondary_y": num_list[1],
            "agg_func": "AVERAGE", "guide": guide_scat,
            "description": ctx_scat
        })
        
    exec_t_decomp, ctx_decomp = build_executive_title_and_context(cat_list[0], main_num, cat_list[1] if len(cat_list)>1 else None, "decomp_tree", "SUM", provenance_map)
    guide_decomp = make_guide("decomp_tree", cat_list[0], main_num, legend=cat_list[1] if len(cat_list)>1 else None)
    all_visuals["🔮 Análisis e Inteligencia"].append({
        "key": "decomp_tree",
        "title": exec_t_decomp,
        "icon": "🌳",
        "x_col": cat_list[0], "y_col": main_num, "legend_col": cat_list[1] if len(cat_list)>1 else None, "secondary_y": None,
        "agg_func": "SUM", "guide": guide_decomp,
        "description": ctx_decomp
    })

    # 8. 🔍 Filtros e Interactividad
    for f_col in (date_list + cat_list)[:3]:
        guide_slicer = make_guide("slicer_dropdown", f_col, main_num)
        all_visuals["🔍 Filtros e Interactividad"].append({
            "key": "slicer_dropdown",
            "title": f"🔍 Segmentador Interactivo: Filtro por {f_col}",
            "icon": "🔍",
            "x_col": f_col, "y_col": main_num, "legend_col": None, "secondary_y": None,
            "agg_func": "COUNT", "guide": guide_slicer,
            "description": f"💡 **Qué informa:** Permite filtrar dinámicamente todo el reporte según la dimensión {f_col}."
        })

    return all_visuals
