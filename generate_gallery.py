#!/usr/bin/env python3
"""Generate an interactive HTML gallery for UMAP visualizations."""

import json
from pathlib import Path
from collections import defaultdict

FIGURES_DIR = Path("Figures")
OUTPUT_FILE = Path("index.html")


def extract_params(filename: str) -> dict:
    """Extract UMAP parameters from filename."""
    # Format: umap-{n_neighbors:04d}-{min_dist:.5f}-{metric}.png
    parts = filename.replace("umap-", "").replace(".png", "").split("-")
    if len(parts) >= 3:
        return {
            "n_neighbors": parts[0],
            "min_dist": parts[1],
            "metric": parts[2],
        }
    return None


def generate_gallery():
    """Generate HTML gallery from figures directory."""
    if not FIGURES_DIR.exists():
        print(f"Error: {FIGURES_DIR} does not exist. Run sweep.py first.")
        return

    # Collect all figures organized by dataset size
    figures_by_size = defaultdict(list)
    for size_dir in FIGURES_DIR.iterdir():
        if not size_dir.is_dir():
            continue

        size = size_dir.name
        pngs = sorted(size_dir.glob("umap-*.png"))

        for png in pngs:
            params = extract_params(png.name)
            if params:
                figures_by_size[size].append(
                    {
                        "filename": png.name,
                        "path": str(png.relative_to(".")),
                        **params,
                    }
                )

    if not figures_by_size:
        print("No UMAP figures found. Run sweep.py first.")
        return

    html = generate_html(figures_by_size)
    OUTPUT_FILE.write_text(html)
    print(f"Gallery generated: {OUTPUT_FILE}")
    print(f"Total figures: {sum(len(figs) for figs in figures_by_size.values())}")


def generate_html(figures_by_size: dict) -> str:
    """Generate HTML content for the gallery: an n_neighbors x min_dist matrix."""
    figures_json = json.dumps(figures_by_size)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UMAP Parameter Exploration Gallery</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}

        .container {{
            margin: 0 auto;
        }}

        header {{
            color: white;
            margin-bottom: 30px;
            text-align: center;
        }}

        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .controls {{
            background: white;
            border-radius: 10px;
            padding: 20px 25px;
            margin: 0 auto 30px;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}

        .control-group {{
            display: flex;
            flex-direction: column;
        }}

        label {{
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            font-size: 0.95em;
        }}

        select {{
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 5px;
            font-size: 1em;
        }}

        select:focus {{
            outline: none;
            border-color: #667eea;
        }}

        .matrix-wrap {{
            overflow-x: auto;
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        table.matrix {{
            border-collapse: collapse;
            margin: 0 auto;
        }}

        .matrix th {{
            color: #333;
            font-size: 0.9em;
            font-weight: 600;
            padding: 6px;
            white-space: nowrap;
        }}

        .matrix .axis {{
            color: #667eea;
        }}

        .matrix td {{
            padding: 2px;
        }}

        .matrix img {{
            display: block;
            width: 100%;
            min-width: 120px;
            aspect-ratio: 1;
            object-fit: contain;
            background: #f5f5f5;
        }}

        .matrix td.missing {{
            background: #fafafa;
        }}

        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
            font-size: 0.9em;
        }}

        footer a {{
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 UMAP Parameter Exploration</h1>
            <p>Rows: n_neighbors &middot; Columns: min_dist</p>
        </header>

        <div class="controls">
            <div class="control-group">
                <label for="sizeFilter">Dataset Size</label>
                <select id="sizeFilter"></select>
            </div>
            <div class="control-group">
                <label for="metricFilter">metric</label>
                <select id="metricFilter"></select>
            </div>
        </div>

        <div class="matrix-wrap">
            <table class="matrix" id="matrix"></table>
        </div>

        <footer>
            <p>Generated by UMAP Parameter Exploration Tool &middot; <a href="https://github.com/dbolser/UMAP-Parameter-Sweep">GitHub</a></p>
        </footer>
    </div>

    <script>
        const figuresBySize = {figures_json};
        const DEFAULT_SIZE = '8000';
        const DEFAULT_METRIC = 'cosine';

        const uniqueSorted = (values) => [...new Set(values)].sort((a, b) => parseFloat(a) - parseFloat(b) || a.localeCompare(b));
        const allFigures = Object.entries(figuresBySize).flatMap(([size, figs]) => figs.map(f => ({{...f, size}})));

        const sizeFilter = document.getElementById('sizeFilter');
        const metricFilter = document.getElementById('metricFilter');

        function fillSelect(select, values, preferred) {{
            values.forEach(v => select.add(new Option(v, v)));
            if (values.includes(preferred)) select.value = preferred;
        }}

        fillSelect(sizeFilter, uniqueSorted(allFigures.map(f => f.size)), DEFAULT_SIZE);
        fillSelect(metricFilter, uniqueSorted(allFigures.map(f => f.metric)), DEFAULT_METRIC);

        function updateMatrix() {{
            const figs = allFigures.filter(f => f.size === sizeFilter.value && f.metric === metricFilter.value);
            const rows = uniqueSorted(figs.map(f => f.n_neighbors));
            const cols = uniqueSorted(figs.map(f => f.min_dist));
            const lookup = new Map(figs.map(f => [`${{f.n_neighbors}}|${{f.min_dist}}`, f]));

            const header = `<tr><th class="axis">n_neighbors \\\\ min_dist</th>${{cols.map(c => `<th>${{parseFloat(c)}}</th>`).join('')}}</tr>`;
            const body = rows.map(r => `<tr><th>${{parseInt(r, 10)}}</th>${{cols.map(c => {{
                const f = lookup.get(`${{r}}|${{c}}`);
                return f
                    ? `<td><a href="${{f.path}}" target="_blank"><img src="${{f.path}}" alt="n_neighbors=${{parseInt(r, 10)}}, min_dist=${{parseFloat(c)}}" title="n_neighbors=${{parseInt(r, 10)}}, min_dist=${{parseFloat(c)}}" loading="lazy"></a></td>`
                    : '<td class="missing"></td>';
            }}).join('')}}</tr>`).join('');

            document.getElementById('matrix').innerHTML = header + body;
        }}

        sizeFilter.addEventListener('change', updateMatrix);
        metricFilter.addEventListener('change', updateMatrix);

        updateMatrix();
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    generate_gallery()
