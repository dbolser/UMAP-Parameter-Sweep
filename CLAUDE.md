# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UMAP parameter exploration tool to understand how `min_dist` affects point density in 2D projections. Main script generates visualizations across parameter combinations; results are published to an interactive GitHub Pages gallery.

See [README.md](./README.md) for full context and motivation.

## Key Files

- **test.py**: Main script. Generates UMAP visualizations with parameter sweep, automatically generates HTML gallery afterward
- **generate_gallery.py**: Builds interactive HTML dashboard from Figures directory
- **utils.py**: Timer decorator for execution logging
- **index.html**: GitHub Pages dashboard (auto-generated, deployed live)

## Commands

```bash
uv run test.py          # Generate all figures + gallery
uv run generate_gallery.py  # Regenerate gallery from existing figures
```

## Architecture Notes

- Figures saved to `Figures/{dataset_size}/` with encoded parameters in filename
- Random seed (42) for reproducibility
- Gallery uses client-side filtering (no backend needed)
- GitHub Pages deployment: commit `index.html` + `Figures/` to main branch
