"""
Módulo para renderizar gráficos Plotly con estética idéntica a Power BI Desktop en Fondo Blanco / Claro.
Soporta mapas geográficos interactivos reales (scatter_geo / choropleth) por países y regiones.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Paleta corporativa Power BI Fluent UI
POWERBI_PALETTE = [
    "#0284C7",  # Azul Power BI
    "#F97316",  # Naranja Coral
    "#14B8A6",  # Turquesa
    "#8B5CF6",  # Púrpura
    "#EC4899",  # Magenta
    "#06B6D4",  # Cyan
    "#EAB308",  # Amarillo Dorado
    "#1E3A8A"   # Azul Marino
]

PBI_LIGHT_LAYOUT = dict(
    font=dict(family="Segoe UI, Inter, Arial, sans-serif", size=12, color="#0F172A"),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#F8FAFC",
    height=380,
    margin=dict(l=45, r=30, t=45, b=45),
    title=dict(font=dict(color="#0F172A", size=14, family="Segoe UI")),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="#334155", size=11)
    )
)

# Coordenadas geográficas de respaldo para regiones y ciudades conocidas
GEO_COORDINATES = {
    # Países / Regiones
    "chile": (-35.6751, -71.5430),
    "argentina": (-38.4161, -63.6167),
    "colombia": (4.5709, -74.2973),
    "mexico": (23.6345, -102.5528),
    "méxico": (23.6345, -102.5528),
    "peru": (-9.1900, -75.0152),
    "perú": (-9.1900, -75.0152),
    "españa": (40.4637, -3.7492),
    "spain": (40.4637, -3.7492),
    "estados unidos": (37.0902, -95.7129),
    "united states": (37.0902, -95.7129),
    "usa": (37.0902, -95.7129),
    "brazil": (-14.2350, -51.9253),
    "brasil": (-14.2350, -51.9253),
    
    # Ciudades / Regiones de Chile
    "santiago": (-33.4489, -70.6693),
    "valparaíso": (-33.0472, -71.6127),
    "valparaiso": (-33.0472, -71.6127),
    "concepción": (-36.8201, -73.0444),
    "concepcion": (-36.8201, -73.0444),
    "antofagasta": (-23.6509, -70.3975),
    "coquimbo": (-29.9533, -71.3436),
    "los lagos": (-41.4717, -72.9360),
    "araucanía": (-38.7359, -72.5904),
    "araucania": (-38.7359, -72.5904),
    "metropolitana": (-33.4489, -70.6693),
    "rm": (-33.4489, -70.6693),
    "norte": (-23.6509, -70.3975),
    "sur": (-41.4717, -72.9360),
    "centro": (-33.4489, -70.6693),

    # Estados EE.UU.
    "california": (36.7783, -119.4179),
    "texas": (31.9686, -99.9018),
    "florida": (27.6648, -81.5158),
    "new york": (40.7128, -74.0060),
    "washington": (47.7511, -120.7401)
}

def format_number_human(val):
    if val is None or pd.isna(val):
        return "0"
    abs_val = abs(val)
    if abs_val >= 1e9:
        return f"{val/1e9:,.2f}B"
    elif abs_val >= 1e6:
        return f"{val/1e6:,.2f}M"
    elif abs_val >= 1e3:
        return f"{val/1e3:,.1f}K"
    else:
        return f"{val:,.2f}"

def build_plotly_chart(df, visual_key, x_col, y_col, legend_col=None, secondary_y=None, agg_func="SUM"):
    if df.empty or not x_col or not y_col or x_col not in df.columns or y_col not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text="Sin datos suficientes para este componente", showarrow=False, font=dict(size=13, color="#475569"))
        fig.update_layout(**PBI_LIGHT_LAYOUT)
        return fig
        
    df_plot = df.copy()
    df_plot[x_col] = df_plot[x_col].fillna("Sin Registro").astype(str)
    if legend_col and legend_col in df_plot.columns:
        df_plot[legend_col] = df_plot[legend_col].fillna("General").astype(str)
        
    df_plot[y_col] = pd.to_numeric(df_plot[y_col], errors='coerce').fillna(0)
    if secondary_y and secondary_y in df_plot.columns:
        df_plot[secondary_y] = pd.to_numeric(df_plot[secondary_y], errors='coerce').fillna(0)
    
    agg_op = 'sum' if agg_func == 'SUM' else ('mean' if agg_func == 'AVERAGE' else 'count')
    agg_dict = {y_col: agg_op}
    if secondary_y and secondary_y in df_plot.columns:
        agg_dict[secondary_y] = 'mean'
        
    group_cols = [x_col]
    if legend_col and legend_col in df_plot.columns and legend_col != x_col:
        group_cols.append(legend_col)
        
    try:
        grouped = df_plot.groupby(group_cols, as_index=False).agg(agg_dict)
    except Exception:
        grouped = df_plot.head(20)

    try:
        # 1. Columnas y Barras
        if visual_key in ["stacked_column", "clustered_column", "hundred_pct_column", "ribbon_chart"]:
            barmode = "stack" if visual_key in ["stacked_column", "ribbon_chart"] else ("group" if visual_key == "clustered_column" else "relative")
            top_x = grouped.groupby(x_col)[y_col].sum().nlargest(12).index
            grouped_top = grouped[grouped[x_col].isin(top_x)]
            
            if legend_col and legend_col in grouped_top.columns:
                fig = px.bar(grouped_top, x=x_col, y=y_col, color=legend_col, barmode=barmode, color_discrete_sequence=POWERBI_PALETTE)
            else:
                fig = px.bar(grouped_top, x=x_col, y=y_col, color_discrete_sequence=[POWERBI_PALETTE[0]])
            fig.update_traces(marker_line_width=0, texttemplate='%{y:.2s}', textposition='auto', textfont=dict(color="#FFFFFF", size=11))

        elif visual_key in ["stacked_bar", "clustered_bar", "hundred_pct_bar"]:
            top_x = grouped.groupby(x_col)[y_col].sum().nlargest(10).index
            grouped_top = grouped[grouped[x_col].isin(top_x)]
            barmode = "stack" if visual_key == "stacked_bar" else ("group" if visual_key == "clustered_bar" else "relative")
            fig = px.bar(grouped_top, y=x_col, x=y_col, orientation='h', barmode=barmode, color_discrete_sequence=[POWERBI_PALETTE[0]])
            fig.update_traces(texttemplate='%{x:.2s}', textposition='auto', textfont=dict(color="#FFFFFF", size=11))

        elif visual_key in ["combo_line_column", "combo_line_stacked"]:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            top_x = grouped.groupby(x_col)[y_col].sum().nlargest(10).index
            grouped_combo = grouped[grouped[x_col].isin(top_x)]
            
            fig.add_trace(go.Bar(x=grouped_combo[x_col], y=grouped_combo[y_col], name=f"{y_col}", marker_color=POWERBI_PALETTE[0]), secondary_y=False)
            if secondary_y and secondary_y in grouped_combo.columns:
                fig.add_trace(go.Scatter(x=grouped_combo[x_col], y=grouped_combo[secondary_y], name=f"{secondary_y}", mode="lines+markers", line=dict(color=POWERBI_PALETTE[1], width=3)), secondary_y=True)
                fig.update_yaxes(title_text=secondary_y, secondary_y=True, showgrid=False, title_font=dict(color=POWERBI_PALETTE[1]), tickfont=dict(color="#334155"))
            fig.update_yaxes(title_text=f"{y_col}", secondary_y=False, title_font=dict(color="#0F172A"), tickfont=dict(color="#334155"))

        # 2. Líneas y Áreas
        elif visual_key in ["line_chart", "area_chart", "stacked_area"]:
            top_x = grouped.head(30)
            if visual_key == "line_chart":
                fig = px.line(top_x, x=x_col, y=y_col, color=legend_col if legend_col in top_x.columns else None, markers=True, color_discrete_sequence=POWERBI_PALETTE)
            else:
                fig = px.area(top_x, x=x_col, y=y_col, color=legend_col if legend_col in top_x.columns else None, color_discrete_sequence=POWERBI_PALETTE)

        # 3. Tarjetas y Medidor
        elif visual_key == "single_card":
            val = df_plot[y_col].sum() if agg_func == "SUM" else df_plot[y_col].mean()
            fig = go.Figure(go.Indicator(
                mode="number", value=val,
                number={'font': {'size': 42, 'color': '#0284C7'}, 'valueformat': ',.2f'},
                title={"text": f"<b>{y_col}</b><br><span style='font-size:0.85em;color:#475569'>Total ({agg_func})</span>"}
            ))

        elif visual_key in ["multi_card", "kpi_card"]:
            val1 = df_plot[y_col].sum() if agg_func == "SUM" else df_plot[y_col].mean()
            val2 = df_plot[secondary_y].mean() if secondary_y and secondary_y in df_plot.columns else (df_plot[y_col].mean() * 1.1)
            fig = go.Figure()
            fig.add_trace(go.Indicator(mode="number+delta" if visual_key == "kpi_card" else "number", value=val1, number={'font': {'size': 32, 'color': '#0284C7'}, 'valueformat': ',.2f'}, title={"text": f"<b>{y_col}</b>"}, domain={'x': [0, 0.48], 'y': [0, 1]}))
            fig.add_trace(go.Indicator(mode="number", value=val2, number={'font': {'size': 32, 'color': '#F97316'}, 'valueformat': ',.2f'}, title={"text": f"<b>{secondary_y or 'Meta'}</b>"}, domain={'x': [0.52, 1], 'y': [0, 1]}))

        elif visual_key == "gauge":
            val = df_plot[y_col].mean()
            max_val = max(val * 1.5, 10.0)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=val,
                number={'font': {'color': '#0F172A'}},
                gauge={'axis': {'range': [0, max_val], 'tickfont': {'color': '#334155'}}, 'bar': {'color': "#0284C7"}},
                title={'text': f"<b>{y_col} (Promedio)</b>", 'font': {'color': '#0F172A'}}
            ))

        # 4. Tablas y Matrices
        elif visual_key == "matrix":
            if legend_col and legend_col in grouped.columns:
                pivot = grouped.pivot(index=x_col, columns=legend_col, values=y_col).fillna(0)
                fig = px.imshow(pivot.iloc[:10, :8], text_auto=".2s", color_continuous_scale="Blues")
                fig.update_coloraxes(showscale=False)
            else:
                top_df = grouped.sort_values(by=y_col, ascending=False).head(8)
                fig = go.Figure(data=[go.Table(
                    header=dict(values=[f"<b>{x_col}</b>", f"<b>{y_col}</b>"], fill_color='#0284C7', align='left', font=dict(color='white', size=12)),
                    cells=dict(values=[top_df[x_col], [format_number_human(v) for v in top_df[y_col]]], fill_color='#F8FAFC', align='left', font=dict(color='#0F172A', size=11))
                )])

        elif visual_key == "table":
            cols_to_show = [c for c in [x_col, y_col, legend_col] if c and c in df_plot.columns]
            top_df = df_plot[cols_to_show].head(8)
            fig = go.Figure(data=[go.Table(
                header=dict(values=[f"<b>{c}</b>" for c in top_df.columns], fill_color='#F1F5F9', align='left', font=dict(color='#0284C7', size=12)),
                cells=dict(values=[top_df[c] for c in top_df.columns], fill_color='#FFFFFF', align='left', font=dict(color='#1E293B', size=11))
            )])

        # 5. Composición (Donut, Pie, Treemap, Funnel)
        elif visual_key in ["donut", "pie"]:
            top_pie = grouped.groupby(x_col, as_index=False)[y_col].sum().nlargest(5, y_col)
            hole = 0.5 if visual_key == "donut" else 0
            fig = px.pie(top_pie, names=x_col, values=y_col, hole=hole, color_discrete_sequence=POWERBI_PALETTE)
            fig.update_traces(textinfo='percent+label', textfont_size=11, textfont_color="#0F172A")

        elif visual_key == "treemap":
            top_tree = grouped.groupby(x_col, as_index=False)[y_col].sum().nlargest(10, y_col)
            top_tree = top_tree[top_tree[y_col] > 0]
            if not top_tree.empty:
                fig = px.treemap(top_tree, path=[x_col], values=y_col, color_discrete_sequence=POWERBI_PALETTE)
            else:
                fig = px.bar(grouped.head(8), x=x_col, y=y_col, color_discrete_sequence=POWERBI_PALETTE)

        elif visual_key == "funnel":
            top_funnel = grouped.groupby(x_col, as_index=False)[y_col].sum().nlargest(6, y_col)
            fig = px.funnel(top_funnel, x=y_col, y=x_col, color_discrete_sequence=POWERBI_PALETTE)

        # 6. MAPAS GEOGRÁFICOS INTERACTIVOS POR PAÍS / REGIÓN (Scatter Geo / Scatter Mapbox)
        elif visual_key in ["bubble_map", "filled_map"]:
            geo_df = grouped.groupby(x_col, as_index=False)[y_col].sum().head(20)
            
            # Mapeo de coordenadas o nombres de países
            lats, lons = [], []
            has_coords = False
            for val in geo_df[x_col]:
                val_clean = str(val).strip().lower()
                if val_clean in GEO_COORDINATES:
                    lat, lon = GEO_COORDINATES[val_clean]
                    lats.append(lat)
                    lons.append(lon)
                    has_coords = True
                else:
                    lats.append(None)
                    lons.append(None)

            if has_coords:
                geo_df['lat'] = lats
                geo_df['lon'] = lons
                valid_geo = geo_df.dropna(subset=['lat', 'lon'])
                
                if visual_key == "filled_map":
                    fig = px.scatter_geo(
                        valid_geo, lat='lat', lon='lon', hover_name=x_col, size=y_col, color=y_col,
                        color_continuous_scale="Blues", projection="natural earth",
                        title=f"🌍 Mapa Geográfico de Distribución por {x_col}"
                    )
                else:
                    fig = px.scatter_geo(
                        valid_geo, lat='lat', lon='lon', hover_name=x_col, size=y_col, color=y_col,
                        color_continuous_scale="Viridis", projection="natural earth",
                        title=f"🌍 Mapa de Burbujas Ubicación: {x_col}"
                    )
                fig.update_coloraxes(showscale=False)
                fig.update_geos(showcountries=True, countrycolor="#CBD5E1", showcoastlines=True, coastlinecolor="#94A3B8")
            else:
                # Si los nombres son códigos o nombres de países como 'United States', 'Chile', usar locationmode
                if visual_key == "filled_map":
                    fig = px.choropleth(
                        geo_df, locations=x_col, locationmode="country names", color=y_col,
                        color_continuous_scale="Blues", title=f"🗺️ Mapa Coropletas Mundial: {x_col}"
                    )
                    fig.update_coloraxes(showscale=False)
                else:
                    fig = px.scatter_geo(
                        geo_df, locations=x_col, locationmode="country names", size=y_col, color=y_col,
                        color_continuous_scale="Tealgrn", title=f"🌍 Mapa de Burbujas por {x_col}"
                    )
                    fig.update_coloraxes(showscale=False)

        # 7. Inteligencia Avanzada
        elif visual_key in ["decomp_tree", "key_influencers"]:
            top_tree = grouped.groupby(x_col, as_index=False)[y_col].sum().nlargest(8, y_col)
            fig = px.bar(top_tree, y=x_col, x=y_col, orientation='h', color=y_col, color_continuous_scale="Tealgrn", title=f"🌳 Descomposición por {x_col}")
            fig.update_coloraxes(showscale=False)

        # 8. Cascada y Scatter
        elif visual_key == "waterfall":
            wf_data = grouped.groupby(x_col, as_index=False)[y_col].sum().head(7)
            fig = go.Figure(go.Waterfall(
                orientation="v", measure=["relative"] * len(wf_data),
                x=wf_data[x_col], textposition="outside",
                text=[format_number_human(v) for v in wf_data[y_col]], y=wf_data[y_col],
                connector={"line": {"color": "#64748B"}},
                decreasing={"marker": {"color": "#EF4444"}},
                increasing={"marker": {"color": "#10B981"}}
            ))

        elif visual_key == "scatter":
            sample_df = df_plot.head(100)
            sec_col = secondary_y if secondary_y and secondary_y in sample_df.columns else y_col
            fig = px.scatter(sample_df, x=x_col, y=sec_col, color=legend_col if legend_col and legend_col in sample_df.columns else None, color_discrete_sequence=POWERBI_PALETTE)

        elif visual_key in ["slicer_date", "slicer_dropdown"]:
            unique_vals = list(df_plot[x_col].dropna().unique()[:5])
            fig = go.Figure()
            fig.add_annotation(
                text=f"🔍 <b>Filtro Interactivo por {x_col}</b><br><br>Valores en filtro: {', '.join([str(v) for v in unique_vals])}...",
                showarrow=False, font=dict(size=13, color="#0284C7")
            )

        else:
            top_bar = grouped.head(8)
            fig = px.bar(top_bar, x=x_col, y=y_col, color_discrete_sequence=POWERBI_PALETTE)

    except Exception:
        # Fallback defensivo
        top_fallback = df_plot.head(10)
        fig = px.bar(top_fallback, x=x_col, y=y_col, color_discrete_sequence=POWERBI_PALETTE)

    # APLICAR CONFIGURACIÓN DE ALTO CONTRASTE OSCURO SOBRE FONDO BLANCO
    fig.update_layout(**PBI_LIGHT_LAYOUT)
    fig.update_xaxes(
        showgrid=True, gridcolor='#E2E8F0', title_text=x_col,
        title_font=dict(color='#0F172A', size=12),
        tickfont=dict(color='#334155', size=11),
        tickangle=-30
    )
    fig.update_yaxes(
        showgrid=True, gridcolor='#E2E8F0',
        title_font=dict(color='#0F172A', size=12),
        tickfont=dict(color='#334155', size=11)
    )
    
    return fig
