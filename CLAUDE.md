# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a UMAP (Uniform Manifold Approximation and Projection) parameter exploration tool. It generates and visualizes 2D projections of high-dimensional data using UMAP with various parameter combinations to understand how parameters affect dimensionality reduction output.

## Development Commands

**Run the main parameter exploration script:**
```bash
uv run test.py
```

This generates a grid of UMAP visualizations by testing combinations of:
- `n_neighbors`: (2, 5, 10, 20, 50, 100, 200)
- `min_dist`: (0, 0.0001)
- `metric`: (euclidean, cosine)

Results are saved as PNG files in `Figures/{data_size}/` and an interactive HTML gallery is automatically generated as `index.html`.

**Generate gallery manually (if needed):**
```bash
uv run generate_gallery.py
```

**Install dependencies:**
```bash
uv pip install -r requirements.txt
```

## Architecture

**Core Files:**
- `test.py` - Main script. Generates random data (8000 samples, 4 dimensions) and creates visualizations by calling `draw_umap()` with different parameter combinations. Execution is logged with timing information.
- `utils.py` - Utilities. Contains a `@timer` decorator that logs function execution time.
- `Figures/` - Output directory for generated PNG visualizations, organized by dataset size.

**Dependencies:**
- numpy - Numerical computations
- umap-learn - Dimensionality reduction
- matplotlib - Plotting
- seaborn - Statistical visualization styling

## Key Details

- Reproducibility: Random seed is fixed at 42 in `test.py`
- Logging: INFO level logging shows parameter combinations and execution times
- Figures directory is automatically created if it doesn't exist
- Each visualization filename encodes the parameters used: `umap-{n_neighbors:04d}-{min_dist:.5f}-{metric}.png`

## Hosting on GitHub Pages

The `index.html` gallery is automatically generated when you run `test.py` and can be hosted on GitHub Pages.

**Setup GitHub Pages:**
1. Go to repository Settings → Pages
2. Set the source to "Deploy from a branch"
3. Select the `main` branch and `/root` folder
4. Commit and push `index.html` and the `Figures/` directory to the repository
5. Your gallery will be available at `https://username.github.io/repo-name/`

**Note:** The gallery is fully client-side (JavaScript) with no backend required. All filtering and interaction happens in the browser.
