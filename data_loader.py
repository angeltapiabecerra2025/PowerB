"""
Módulo de Carga, Muestreo de Filas y Gestión de procedencia de planillas Excel/CSV.
"""

import pandas as pd
import numpy as np
import os
import re

def load_data(uploaded_files, max_rows=1000):
    """
    Carga una o múltiples planillas Excel (.xlsx) o CSV (.csv).
    Limita el procesamiento a max_rows filas por rendimiento.
    """
    if not uploaded_files:
        return get_inmemory_fallback_data(max_rows)

    if not isinstance(uploaded_files, list):
        uploaded_files = [uploaded_files]

    dataframes = []
    sources_info = {}
    provenance_map = {}
    total_original_records = 0

    for file_item in uploaded_files:
        try:
            filename = getattr(file_item, "name", None)
            if not filename:
                filename = os.path.basename(str(file_item))
                
            if filename.endswith(('.xlsx', '.xls')):
                try:
                    xls = pd.ExcelFile(file_item)
                    sheet_names = xls.sheet_names
                    for sheet in sheet_names:
                        df_sheet = pd.read_excel(xls, sheet_name=sheet)
                        if not df_sheet.empty:
                            total_original_records += len(df_sheet)
                            df_sample = df_sheet.head(max_rows).copy()
                            sheet_src_name = f"{filename} [{sheet}]" if len(sheet_names) > 1 else filename
                            
                            for col in df_sample.columns:
                                if col not in provenance_map:
                                    provenance_map[col] = sheet_src_name
                                    
                            df_sample['_Origen_Archivo'] = sheet_src_name
                            dataframes.append(df_sample)
                            sources_info[sheet_src_name] = {
                                "rows": len(df_sheet),
                                "sample_rows": len(df_sample),
                                "cols": list(df_sheet.columns)
                            }
                except Exception:
                    df_single = pd.read_excel(file_item)
                    total_original_records += len(df_single)
                    df_sample = df_single.head(max_rows).copy()
                    for col in df_sample.columns:
                        if col not in provenance_map:
                            provenance_map[col] = filename
                    df_sample['_Origen_Archivo'] = filename
                    dataframes.append(df_sample)
                    sources_info[filename] = {
                        "rows": len(df_single),
                        "sample_rows": len(df_sample),
                        "cols": list(df_single.columns)
                    }

            elif filename.endswith('.csv'):
                try:
                    df_csv = pd.read_csv(file_item)
                except Exception:
                    df_csv = pd.read_csv(file_item, encoding='latin1', sep=None, engine='python')
                    
                total_original_records += len(df_csv)
                df_sample = df_csv.head(max_rows).copy()
                for col in df_sample.columns:
                    if col not in provenance_map:
                        provenance_map[col] = filename
                df_sample['_Origen_Archivo'] = filename
                dataframes.append(df_sample)
                sources_info[filename] = {
                    "rows": len(df_csv),
                    "sample_rows": len(df_sample),
                    "cols": list(df_csv.columns)
                }
        except Exception as e:
            print(f"Error procesando fuente {file_item}: {e}")

    if not dataframes:
        return get_inmemory_fallback_data(max_rows)

    # Combinación Inteligente y Detección de Relaciones
    if len(dataframes) == 1:
        master_df = dataframes[0]
        relationships = []
    else:
        master_df, relationships = auto_merge_and_detect_relationships(dataframes, provenance_map)

    # Limpieza de tipos de datos
    for col in master_df.columns:
        if str(col).startswith('_'):
            continue
        series = master_df[col]
        if series.dtype == 'object':
            numeric_series = pd.to_numeric(series.astype(str).str.replace('$', '').str.replace(',', '').str.strip(), errors='coerce')
            if numeric_series.notnull().sum() / max(len(series), 1) > 0.6:
                master_df[col] = numeric_series
            else:
                try:
                    parsed_dates = pd.to_datetime(series.head(30), errors='coerce')
                    if parsed_dates.notnull().sum() / min(len(series), 30) > 0.5:
                        master_df[col] = pd.to_datetime(series, errors='coerce')
                except Exception:
                    pass

    return master_df, sources_info, provenance_map, relationships, total_original_records

def auto_merge_and_detect_relationships(dfs, provenance_map):
    """
    Detecta llaves comunes (IDs, Códigos, Fechas, Ubicaciones) entre múltiples DataFrames y realiza un Merge inteligente.
    """
    relationships = []
    base_df = dfs[0].copy()
    
    for i in range(1, len(dfs)):
        next_df = dfs[i].copy()
        
        common_cols = list(set(base_df.columns).intersection(set(next_df.columns)))
        common_cols = [c for c in common_cols if not str(c).startswith('_')]
        
        join_key = None
        for col in common_cols:
            if any(k in col.lower() for k in ['id', 'codigo', 'código', 'code', 'key', 'region', 'región', 'pais', 'país', 'country', 'fecha', 'date']):
                join_key = col
                break
                
        if not join_key and common_cols:
            join_key = common_cols[0]
            
        if join_key:
            t1_name = provenance_map.get(base_df.columns[0], "Planilla 1")
            t2_name = provenance_map.get(next_df.columns[0], f"Planilla {i+1}")
            relationships.append({
                "table1": t1_name,
                "table2": t2_name,
                "key1": join_key,
                "key2": join_key,
                "type": "1 to Many (Auto-relacionado)"
            })
            base_df = pd.merge(base_df, next_df, on=join_key, how='outer', suffixes=('', f'_{i}'))
        else:
            base_df = pd.concat([base_df, next_df], axis=1)

    return base_df, relationships

def get_inmemory_fallback_data(max_rows=1000):
    """
    Genera un DataFrame de muestra garantizado en memoria si los archivos no están presentes.
    """
    data = {
        "Region": ["Norte", "Sur", "Centro", "Europa", "Sur", "Norte", "Centro", "Europa"],
        "Pais": ["United States", "Chile", "Mexico", "Spain", "Argentina", "United States", "Mexico", "Spain"],
        "Plataforma": ["PS4", "XOne", "Switch", "PC", "PS4", "Switch", "XOne", "PC"],
        "Ventas_Globales": [15400.0, 9800.0, 12600.0, 18200.0, 7400.0, 21000.0, 11500.0, 19500.0],
        "Unidades_Vendidas": [320, 210, 290, 410, 150, 480, 260, 430],
        "Costo_Operativo": [9200.0, 5400.0, 7100.0, 10500.0, 4200.0, 11800.0, 6800.0, 11100.0],
        "Margen_Pct": [40.2, 44.8, 43.6, 42.3, 43.2, 43.8, 40.9, 43.1],
        "Fecha": ["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05", "2024-05-18", "2024-06-22", "2024-07-11", "2024-08-30"]
    }
    df = pd.DataFrame(data)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    src_name = "sample_ventas_finanzas.xlsx"
    provenance_map = {col: src_name for col in df.columns}
    sources_info = {src_name: {"rows": len(df), "sample_rows": len(df), "cols": list(df.columns)}}
    return df, sources_info, provenance_map, [], len(df)

def classify_columns(df):
    """
    Clasifica las columnas de un DataFrame en Numéricas, Fechas, Categorías y Geográficas,
    excluyendo explícitamente columnas internas de metadata (_Origen_Archivo).
    """
    classification = {
        'numeric': [],
        'datetime': [],
        'categorical': [],
        'geographic': [],
        'percentage': []
    }
    
    geo_keywords = ['region', 'región', 'pais', 'país', 'country', 'city', 'ciudad', 'state', 'estado', 'zona', 'comuna', 'ubicacion', 'ubicación']
    
    for col in df.columns:
        if str(col).startswith('_'):
            continue
            
        col_lower = str(col).lower()
        series = df[col]
        
        if pd.api.types.is_datetime64_any_dtype(series):
            classification['datetime'].append(col)
        elif any(geo_kw in col_lower for geo_kw in geo_keywords):
            classification['geographic'].append(col)
        elif pd.api.types.is_numeric_dtype(series):
            if any(pct_kw in col_lower for pct_kw in ['pct', 'porcentaje', '%', 'tasa', 'rate', 'margen']):
                classification['percentage'].append(col)
            else:
                classification['numeric'].append(col)
        else:
            try:
                converted = pd.to_datetime(series.head(10), errors='coerce')
                if converted.notnull().sum() > 5:
                    classification['datetime'].append(col)
                    continue
            except Exception:
                pass
                
            classification['categorical'].append(col)
            
    return classification

def get_data_summary(df, total_original_records, provenance_map=None):
    """
    Genera un resumen estructurado para tableros ejecutivos.
    """
    provenance_map = provenance_map or {}
    classification = classify_columns(df)
    
    col_details = []
    for col in df.columns:
        if str(col).startswith('_'):
            continue
        c_type = "Categoría"
        if col in classification['numeric']:
            c_type = "Métrica Numérica"
        elif col in classification['percentage']:
            c_type = "Porcentaje / Ratio"
        elif col in classification['datetime']:
            c_type = "Fecha / Tiempo"
        elif col in classification['geographic']:
            c_type = "Ubicación Geográfica"
            
        col_details.append({
            "Columna": col,
            "Tipo": c_type,
            "No Nulos": int(df[col].notnull().sum()),
            "Únicos": int(df[col].nunique()),
            "Archivo Origen": provenance_map.get(col, "Planilla Principal")
        })
        
    summary = {
        "total_rows": len(df),
        "sample_rows": len(df),
        "total_original_records": total_original_records,
        "total_original_rows": total_original_records,
        "total_cols": len(df.columns) - len([c for c in df.columns if str(c).startswith('_')]),
        "classification": classification,
        "column_details": col_details
    }
    
    return summary, classification
