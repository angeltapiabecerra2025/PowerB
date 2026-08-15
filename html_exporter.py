"""
Módulo para exportar el manual completo de Power BI a HTML/PDF.
"""

def generate_html_report(dataset_name, summary, all_visuals_dict):
    """
    Genera un documento HTML imprimible/descargable con todas las recetas categorizadas.
    """
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Catálogo Completo de Componentes Power BI - {dataset_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background-color: #0F172A;
            color: #E2E8F0;
            margin: 0;
            padding: 30px;
            line-height: 1.5;
        }}
        .header {{
            border-bottom: 2px solid #3B82F6;
            padding-bottom: 16px;
            margin-bottom: 25px;
        }}
        h1 {{
            color: #38BDF8;
            font-size: 26px;
            margin: 0 0 8px 0;
        }}
        .meta-info {{
            color: #94A3B8;
            font-size: 13px;
        }}
        .cat-title {{
            color: #F8FAFC;
            font-size: 20px;
            border-left: 4px solid #0284C7;
            padding-left: 10px;
            margin: 30px 0 15px 0;
        }}
        .card {{
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        }}
        .card-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid #334155;
            padding-bottom: 10px;
            margin-bottom: 12px;
        }}
        .card-header h3 {{
            margin: 0;
            font-size: 17px;
            color: #F8FAFC;
        }}
        .badge {{
            background-color: #2563EB;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 12.5px;
        }}
        th, td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #334155;
        }}
        th {{
            background-color: #0F172A;
            color: #38BDF8;
            text-transform: uppercase;
        }}
        .code-block {{
            background-color: #090D16;
            border-left: 4px solid #10B981;
            padding: 10px 14px;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            color: #34D399;
            font-size: 12px;
            margin: 10px 0;
        }}
        .tips-list {{
            padding-left: 18px;
            font-size: 12px;
        }}
        .tips-list li {{
            margin-bottom: 6px;
        }}
        @media print {{
            body {{ background-color: #fff; color: #000; padding: 15px; }}
            .card {{ background: #fff; border: 1px solid #ccc; box-shadow: none; color: #000; page-break-inside: avoid; }}
            .card-header h3 {{ color: #000; }}
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
            <strong>Muestra:</strong> {summary['sample_rows']:,} filas de {summary['total_original_rows']:,} totales | 
            <strong>Columnas:</strong> {summary['total_cols']}
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
                        <th>Columna a Utilizar</th>
                        <th>Propósito / Rol</th>
                    </tr>
                </thead>
                <tbody>
"""
            for fm in guide['field_mappings']:
                html_content += f"""
                    <tr>
                        <td><strong>{fm['well']}</strong></td>
                        <td><code>{fm['field']}</code></td>
                        <td>{fm['role']}</td>
                    </tr>
"""
            html_content += """
                </tbody>
            </table>
"""
            if guide.get('dax_code'):
                html_content += f"""
            <strong>🧮 Medida DAX Sugerida:</strong>
            <div class="code-block">{guide['dax_code']}</div>
"""
            html_content += """
            <strong>🎨 Pasos de Configuración y Formato:</strong>
            <ol class="tips-list">
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
