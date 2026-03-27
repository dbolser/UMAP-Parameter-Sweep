# https://umap-learn.readthedocs.io/en/latest/parameters.html

import numpy as np

# import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import umap

from pathlib import Path

from utils import timer

import logging

logging.basicConfig(level=logging.INFO)
# matplotlib.use("TkAgg")

sns.set_theme(style="white", context="poster", rc={"figure.figsize": (8, 8)})

np.random.seed(42)

size = 8000
data = np.random.rand(size, 4)
data.shape


figures_dir = Path(f"Figures/{size}")

if not figures_dir.exists():
    figures_dir.mkdir(parents=True)


@timer
def draw_umap(n_neighbors=15, min_dist=0.1, metric="euclidean", title=""):
    fit = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=2,
        metric=metric,
    )
    u = fit.fit_transform(data)
    fig = plt.figure()

    ax = fig.add_subplot(111)
    ax.scatter(u[:, 0], u[:, 1], c=data)

    plt.title(title, fontsize=18)
    plt.savefig(figures_dir / f"umap-{n_neighbors:0>4}-{min_dist:0.5f}-{metric}.png")
    # plt.show()


for n in (2, 5, 10, 20, 50, 100, 200):
    # for d in (0, 0.001, 0.01, 0.1, 0.25, 0.5, 0.99):
    for d in (0, 0.0001):
        for m in ("euclidean", "cosine"):
            title = f"n_neighbors = {n:0>4}, min_dist = {d:0.5f}, metric = {m[0:3]}"
            logging.info(title)
            draw_umap(n_neighbors=n, min_dist=d, metric=m, title=title)

# Generate HTML gallery
logging.info("Generating gallery...")
from generate_gallery import generate_gallery

generate_gallery()
