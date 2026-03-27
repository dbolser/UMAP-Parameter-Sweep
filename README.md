# UMAP Parameter Sweep

An exploration of how UMAP hyperparameters affect dimensionality reduction visualizations, with a focus on understanding the relationship between `min_dist` and point density.

**[📊 View the Interactive Gallery](https://dbolser.github.io/UMAP-Parameter-Sweep/)**

## Motivation

When working with large datasets, it's often impractical to tune UMAP parameters on the full data. This project explores how parameter choices—particularly `min_dist`—affect the density structure of projections, enabling you to:

1. Understand how `min_dist` controls point density in the embedding space
2. Build intuition about parameter choices on a smaller, tractable dataset
3. Scale that intuition to larger datasets by adjusting `min_dist` proportionally to account for increased point density

By visualizing how different `min_dist` values affect clustering and spreading of points across various `n_neighbors` and distance metrics, you can make more informed choices when optimizing on full-scale data.

## Quick Start

```bash
# Install dependencies
uv sync

# Generate visualizations
uv run test.py

# This creates an interactive HTML gallery at index.html
```

## How It Works

- `test.py`: Generates UMAP visualizations across a parameter grid (n_neighbors, min_dist, metric)
- `generate_gallery.py`: Creates an interactive HTML dashboard for exploring results
- `Figures/`: Output directory with PNG visualizations organized by dataset size
- `index.html`: Interactive gallery with filtering by parameter values

## Project Structure

- **Parameters tested**:
  - `n_neighbors`: 2, 5, 10, 20, 50, 100, 200
  - `min_dist`: 0, 0.0001 (and 0.001, 0.01, 0.1, 0.25, 0.5, 0.99 for earlier dataset sizes)
  - `metric`: euclidean, cosine

- **Dataset sizes**: 400, 800, 8000 samples (4-dimensional random data)

## Gallery Features

The [interactive gallery](https://dbolser.github.io/UMAP-Parameter-Sweep/) lets you:
- Filter visualizations by dataset size, n_neighbors, min_dist, and metric
- Observe how each parameter affects point density and structure
- Quickly explore the entire hyperparameter space

See [CLAUDE.md](./CLAUDE.md) for development notes.

## Future Improvements

This is a first draft. Potential enhancements for making the visualization more fit-for-purpose:

- **2D parameter grid**: Display plots in a grid layout where one axis represents `n_neighbors` and the other `min_dist`, making parameter relationships more intuitive
- **Natural controls**: Replace filter dropdowns with sliders and axis selection for more direct exploration of the parameter space
- **Side-by-side comparison**: Ability to compare specific parameter combinations directly
- **Density analysis**: Quantitative metrics overlaid on visualizations to complement visual inspection
