"""
Módulo exportador del Manual Completo e Instrucciones de Power BI en HTML autocontenido para descarga e impresión PDF.
"""

def generate_html_report(dataset_name, summary, all_visuals_dict):
    """
    Genera un informe HTML ejecutivo profesional y completo con todas las recetas y mapeos.
    """
    sample_rows = summary.get('sample_rows', summary.get('total_rows', 0))
    total_original_rows = summary.get('total_original_rows', summary.get('total_original_records', 0))
    total_cols = summary.get('total_cols', 0)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manual de Construcción Power BI - {dataset_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0F172A;
            color: #F8FAFC;
            margin: 0;
            padding: 40px;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
            border: 1px solid #334155;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 40px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #0284C7;
            margin-top: 0;
            font-size: 28px;
        }}
        .meta-info {{
            font-size: 14px;
            color: #94A3B8;
        }}
        .meta-info strong {{
            color: #F8FAFC;
        }}
        .cat-title {{
            font-size: 22px;
            color: #38BDF8;
            border-bottom: 2px solid #0284C7;
            padding-bottom: 8px;
            margin-top: 50px;
            margin-bottom: 25px;
        }}
        .card {{
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            page-break-inside: avoid;
        }}
        .card-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }}
        .card-header h3 {{
            margin: 0;
            color: #F8FAFC;
            font-size: 18px;
        }}
        .badge {{
            background-color: #0284C7;
            color: #FFF;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            margin-bottom: 15px;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{
            background-color: #0F172A;
            color: #38BDF8;
        }}
        .code-block {{
            background-color: #0F172A;
            color: #38BDF8;
            padding: 12px;
            border-radius: 6px;
            font-family: 'Consolas', monospace;
            font-size: 12px;
            border-left: 4px solid #0284C7;
            margin-top: 10px;
            white-space: pre-wrap;
        }}
        .step-list {{
            padding-left: 20px;
            font-size: 13px;
            color: #CBD5E1;
        }}
        @media print {{
            body {{ background-color: #fff; color: #000; padding: 0; }}
            .card {{ background-color: #fff; border: 1px solid #ccc; page-break-inside: avoid; }}
            .code-block {{ background-color: #f4f4f4; color: #000; border-left-color: #008000; }}
            th {{ background-color: #eee; color: #000; }}
            td {{ border-bottom: 1px solid #eee; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📑 Manual y Recetario Completo para Power BI Desktop</h1>
        <div class="meta-info">
            <strong>Planilla Analizada:</strong> {dataset_name} | 
            <strong>Muestra:</strong> {sample_rows:,} filas de {total_original_rows:,} totales | 
            <strong>Columnas:</strong> {total_cols}
        </div>
    </div>
"""

    for cat_name, visual_list in all_visuals_dict.items():
        html_content += f'<div class="cat-title">{cat_name}</div>'
        for vis in visual_list:
            guide = vis['guide']
            html_content += f"""
        <div class="card">
            <div class="card-header">
                <span>{vis['icon']}</span>
                <h3>{vis['title']}</h3>
                <span class="badge">{guide['visual_name']}</span>
            </div>
            <p style="font-size: 13px; color: #94A3B8;">{vis['description']}</p>
            
            <strong>🗂️ Mapeo de Campos en Power BI Desktop:</strong>
            <table>
                <thead>
                    <tr>
                        <th>Contenedor Power BI</th>
                        <th>Columna Planilla</th>
                        <th>Origen</th>
                    </tr>
                </thead>
                <tbody>
"""
            for fm in guide['field_mappings']:
                src_file = fm.get('source', 'Planilla Carga')
                html_content += f"""
                    <tr>
                        <td>{fm['well']}</td>
                        <td><code>{fm['field']}</code></td>
                        <td>{src_file}</td>
                    </tr>
"""
            html_content += """
                </tbody>
            </table>
"""
            if guide.get('dax_code'):
                html_content += f"""
            <strong>🧮 Código DAX Sugerido:</strong>
            <div class="code-block">{guide['dax_code']}</div>
"""
            html_content += """
            <strong>🎨 Pasos de Configuración:</strong>
            <ol class="step-list">
"""
            for tip in guide['format_tips']:
                html_content += f"<li>{tip}</li>"
            html_content += """
            </ol>
        </div>
"""

    html_content += """
</body>
</html>
"""
    return html_content
