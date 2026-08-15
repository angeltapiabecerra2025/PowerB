import pandas as pd
import numpy as np
import io
import os
import streamlit as st

@st.cache_data(show_spinner="Procesando muestras de las planillas...")
def load_single_source_bytes(file_bytes, file_name, sheet_name=0, max_rows=1000):
    """
    Carga un único archivo/bytes y retorna DataFrame y lista de hojas.
    """
    if file_name.endswith('.csv'):
        df_full = pd.read_csv(io.BytesIO(file_bytes))
        sheets = ['Hoja Principal']
    else:
        xl = pd.ExcelFile(io.BytesIO(file_bytes))
        sheets = xl.sheet_names
        df_full = xl.parse(sheet_name if sheet_name in sheets else sheets[0])

    total_records = len(df_full)
    df = df_full.head(max_rows).copy() if total_records > max_rows else df_full.copy()

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: str(x) if pd.notnull(x) and str(x).strip() != "" else None)

    return df, sheets, total_records

def load_data(file_inputs, sheet_name=0, max_rows=1000):
    """
    Carga uno o MÚLTIPLES archivos/planillas Excel o CSV.
    Retorna:
    - master_df: DataFrame maestro unificado combinando relacionalmente o concatenando las planillas.
    - sources_info: Diccionario con la información detallada de cada archivo fuente.
    - provenance_map: Diccionario que mapea cada columna a su archivo de origen.
    - relationships: Lista de relaciones relacionales detectadas entre planillas.
    - total_original_records: Total de registros procesados.
    """
    if not isinstance(file_inputs, list):
        file_inputs = [file_inputs]

    sources_dict = {}
    sources_info = {}
    total_original_records = 0
    
    # 1. Leer todas las planillas cargadas
    for item in file_inputs:
        if isinstance(item, str):
            file_name = os.path.basename(item)
            if item.endswith('.csv'):
                df_full = pd.read_csv(item)
                sheets = ['Hoja Principal']
            else:
                xl = pd.ExcelFile(item)
                sheets = xl.sheet_names
                df_full = xl.parse(sheet_name if sheet_name in sheets else sheets[0])
            
            tot = len(df_full)
            df = df_full.head(max_rows).copy() if tot > max_rows else df_full.copy()
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].apply(lambda x: str(x) if pd.notnull(x) and str(x).strip() != "" else None)
        else:
            file_name = item.name
            df, sheets, tot = load_single_source_bytes(item.getvalue(), file_name, sheet_name, max_rows)

        # Guardar DataFrame sanitizado por fuente
        sources_dict[file_name] = df
        sources_info[file_name] = {
            'rows': len(df),
            'total_rows': tot,
            'cols': list(df.columns),
            'sheets': sheets
        }
        total_original_records += tot

    if not sources_dict:
        return pd.DataFrame(), {}, {}, [], 0

    # Si hay una sola fuente, retornar de forma directa
    if len(sources_dict) == 1:
        single_name = list(sources_dict.keys())[0]
        single_df = sources_dict[single_name]
        provenance_map = {col: single_name for col in single_df.columns}
        return single_df, sources_info, provenance_map, [], total_original_records

    # 2. Múltiples fuentes: Detectar Relaciones y Fusionar
    provenance_map = {}
    relationships = []
    source_names = list(sources_dict.keys())
    
    # Detectar claves comunes para relaciones relacionales
    for i in range(len(source_names)):
        for j in range(i + 1, len(source_names)):
            src1, src2 = source_names[i], source_names[j]
            cols1, cols2 = set(sources_dict[src1].columns), set(sources_dict[src2].columns)
            common = cols1.intersection(cols2)
            
            for key in common:
                key_str = str(key).lower()
                if 'id' in key_str or 'codigo' in key_str or 'rut' in key_str or 'cliente' in key_str or 'producto' in key_str or 'region' in key_str or 'fecha' in key_str:
                    relationships.append({
                        'table1': src1,
                        'key1': key,
                        'table2': src2,
                        'key2': key,
                        'type': 'Relación Detectada (Modelo Estrella 1 a Muchos)'
                    })

    # Construir DataFrame Maestro Unificado combinando inteligentemente por las llaves o joins
    master_df = None
    processed_sources = set()
    
    # Intentar Merge basado en relaciones encontradas
    for rel in relationships:
        t1, k1, t2, k2 = rel['table1'], rel['key1'], rel['table2'], rel['key2']
        if t1 not in processed_sources and t2 not in processed_sources:
            df1 = sources_dict[t1].copy()
            df2 = sources_dict[t2].copy()
            
            # Registrar procedencia antes del merge
            for col in df1.columns:
                provenance_map[col] = t1
            for col in df2.columns:
                if col not in provenance_map:
                    provenance_map[col] = t2
                    
            master_df = pd.merge(df1, df2, left_on=k1, right_on=k2, how='outer', suffixes=('', f'_{t2}'))
            processed_sources.add(t1)
            processed_sources.add(t2)
            break

    # Si no se pudo hacer merge por relación directa o quedan tablas sueltas
    if master_df is None:
        first_src = source_names[0]
        master_df = sources_dict[first_src].copy()
        for col in master_df.columns:
            provenance_map[col] = first_src
        processed_sources.add(first_src)

    # Agregar restantes mediante join por índice o concatenación
    for src in source_names:
        if src not in processed_sources:
            sub_df = sources_dict[src].copy()
            for col in sub_df.columns:
                # Evitar colisión de nombres
                final_col_name = col
                if col in master_df.columns:
                    final_col_name = f"{col} ({src})"
                    sub_df.rename(columns={col: final_col_name}, inplace=True)
                provenance_map[final_col_name] = src
                master_df[final_col_name] = sub_df[final_col_name]

    # Limpiar columnas duplicadas o totalmente nulas
    master_df = master_df.loc[:, ~master_df.columns.duplicated()].copy()

    return master_df, sources_info, provenance_map, relationships, total_original_records

def classify_columns(df):
    """
    Analiza y clasifica las columnas de un DataFrame para Business Intelligence.
    """
    classification = {
        'numeric': [],
        'datetime': [],
        'categorical': [],
        'geographic': [],
        'identifiers': [],
        'percentage': []
    }
    
    total_rows = len(df)
    geo_keywords = ['region', 'región', 'pais', 'país', 'ciudad', 'city', 'country', 'comuna', 'zona', 'ubicacion', 'ubicación', 'estado', 'state', 'provincia']
    
    for col in df.columns:
        col_str = str(col).lower()
        series = df[col].dropna()
        
        if series.empty:
            classification['categorical'].append(col)
            continue

        # 1. Identificadores
        if ('id' in col_str or 'rut' in col_str or 'codigo' in col_str or 'código' in col_str) and df[col].nunique() > total_rows * 0.7:
            classification['identifiers'].append(col)
            continue

        # 2. Geográficas
        if any(k in col_str for k in geo_keywords):
            classification['geographic'].append(col)
            continue

        # 3. Fechas
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            classification['datetime'].append(col)
            continue
            
        if 'fecha' in col_str or 'date' in col_str or 'año' in col_str or 'year' in col_str or 'mes' in col_str:
            try:
                parsed_dates = pd.to_datetime(series.head(30), errors='coerce')
                if parsed_dates.notnull().sum() > 15:
                    classification['datetime'].append(col)
                    continue
            except Exception:
                pass

        # 4. Numéricas y Porcentajes
        if pd.api.types.is_numeric_dtype(df[col]):
            if 'pct' in col_str or 'porcentaje' in col_str or 'margen' in col_str or '%' in col_str or 'tasa' in col_str:
                classification['percentage'].append(col)
            elif df[col].nunique() <= 10 and not any(k in col_str for k in ['precio', 'monto', 'total', 'ingreso', 'costo', 'salario', 'unidades', 'score', 'evaluacion', 'csat', 'sales']):
                classification['categorical'].append(col)
            else:
                classification['numeric'].append(col)
            continue
            
        # 5. Categórica por defecto
        classification['categorical'].append(col)
        
    return classification

def get_data_summary(df, total_original_records=None, provenance_map=None):
    """
    Retorna un resumen estadístico y de perfilamiento incluyendo procedencia de archivo.
    """
    provenance_map = provenance_map or {}
    summary = {
        'sample_rows': len(df),
        'total_original_rows': total_original_records or len(df),
        'total_cols': len(df.columns),
        'column_details': []
    }
    
    classification = classify_columns(df)
    
    for col in df.columns:
        col_type = 'Categoría'
        if col in classification['numeric']:
            col_type = 'Métrica (Número)'
        elif col in classification['datetime']:
            col_type = 'Fecha / Tiempo'
        elif col in classification['geographic']:
            col_type = 'Geográfico (Ubicación)'
        elif col in classification['percentage']:
            col_type = 'Porcentaje (%)'
        elif col in classification['identifiers']:
            col_type = 'Identificador (ID)'
            
        null_count = int(df[col].isnull().sum())
        unique_count = int(df[col].nunique())
        source_file = provenance_map.get(col, 'Planilla Principal')
        
        summary['column_details'].append({
            'Columna': col,
            'Archivo Origen': source_file,
            'Tipo BI': col_type,
            'Valores Únicos': unique_count,
            'Nulos': null_count,
            '% Nulos': round((null_count / max(len(df), 1)) * 100, 1)
        })
        
    return summary, classification
