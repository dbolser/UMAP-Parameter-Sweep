# https://umap-learn.readthedocs.io/en/latest/parameters.html

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import umap
from scipy.linalg import orthogonal_procrustes

from generate_gallery import generate_gallery
from utils import timer

logging.basicConfig(level=logging.INFO)

sns.set_theme(style="white", context="poster", rc={"figure.figsize": (8, 8)})

SIZES = (400, 800, 8000)
N_NEIGHBORS = (2, 5, 10, 20, 50, 100, 200)
MIN_DISTS = (0, 0.0001, 0.001, 0.01, 0.1, 0.25, 0.5, 0.99)
METRICS = ("euclidean", "cosine")


def make_data(size):
    """Uniform random points in the 4D unit cube, plotted as RGBA.

    Reseeding per size means smaller datasets are prefixes of larger ones.
    """
    np.random.seed(42)
    return np.random.rand(size, 4)


def align(u, data):
    """Rotate/reflect the embedding so red runs left-to-right and green bottom-to-top.

    UMAP's orientation is arbitrary; Procrustes against the input's first two
    (RGB) dimensions gives every plot, at every size, the same orientation.
    """
    u = u - u.mean(axis=0)
    target = data[:, :2] - data[:, :2].mean(axis=0)
    rotation, _ = orthogonal_procrustes(u, target)
    return u @ rotation


@timer
def draw_umap(data, figures_dir, n_neighbors=15, min_dist=0.1, metric="euclidean", title=""):
    fit = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=2,
        metric=metric,
        init="pca",  # Deterministic start, so layouts don't flip between runs
    )
    u = align(fit.fit_transform(data), data)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(u[:, 0], u[:, 1], c=data)

    plt.title(title, fontsize=18)
    plt.savefig(figures_dir / f"umap-{n_neighbors:0>4}-{min_dist:0.5f}-{metric}.png")
    plt.close(fig)


def main():
    for size in SIZES:
        data = make_data(size)
        figures_dir = Path(f"Figures/{size}")
        figures_dir.mkdir(parents=True, exist_ok=True)

        for n in N_NEIGHBORS:
            for d in MIN_DISTS:
                for m in METRICS:
                    title = f"n_neighbors = {n:0>4}, min_dist = {d:0.5f}, metric = {m[0:3]}"
                    logging.info(f"size = {size}, {title}")
                    draw_umap(data, figures_dir, n_neighbors=n, min_dist=d, metric=m, title=title)

    logging.info("Generating gallery...")
    generate_gallery()


if __name__ == "__main__":
    main()
