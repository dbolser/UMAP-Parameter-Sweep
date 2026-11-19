# TODO

Ideas for testing how UMAP parameters and density affect structure. See [LITERATURE.md](./LITERATURE.md) for background.

## Why the current sweep isn't enough

The input is uniform random points in a 4D cube, which has **no structure**. The ideal 2D plot is an evenly filled blob with smooth colour gradients. Any clumps or threads are UMAP inventing structure.

So the current sweep is a good **null test** (which settings make up structure?), but it can't show where the *best* structure is, because there is nothing real to recover.

## 1. Plant known structure

Generate data where we know the right answer:

- **Clusters with sub-clusters:** for example 5 clusters of 4 sub-clusters each, to test local and global structure together.
- **A continuous manifold:** a curve, ring or Swiss roll, to test whether UMAP breaks smooth structure into fake clusters.
- **Uneven density:** clusters of different tightness and size, to test whether the plot reflects density.
- **Realistic dimensions:** about 20 informative dimensions padded with noise up to about 768, then normalised to the unit sphere so the data looks like real embedding vectors.

## 2. Score, don't eyeball

Measure each embedding against the planted truth:

- **Local structure:** kNN recall (the share of each point's true neighbours still nearby in 2D), or `sklearn.manifold.trustworthiness`.
- **Cluster recovery:** cluster the embedding with HDBSCAN, then compute the adjusted Rand index (ARI) against the planted labels.
- **Global structure:** Spearman correlation between true and embedded distances, measured between cluster centres.
- **Null check:** run the same scores on structureless data, to see how much "structure" each setting invents.

## 3. Vary density properly

- Sweep N over 1k, 10k and 100k, keeping the same underlying structure.
- For each N, draw a **heatmap of score** over `n_neighbors` × `min_dist`.
- If the best spot moves as N grows, the heatmaps will show it directly.
- Also try `n_neighbors` as a **fraction of N** (for example 0.1%, 1%), not just a fixed count.

## 4. Compare options

- `densmap=True`: does keeping density help or hurt cluster recovery?
- `init="spectral"` vs `init="pca"`: how much does initialisation matter?
- Reducing to around 50 dimensions with PCA first vs using the raw 768 dimensions.
- 2D vs 5–10D output, scored on cluster recovery. Only 2D is for viewing.
- Optionally PaCMAP or t-SNE as a baseline.

## 5. Try real data

- Run the best settings on real embedding vectors, for example sentence embeddings of a public text dataset with known topic labels.
- Check that what worked on planted data transfers to real data.

## 6. Gallery improvements

- A score heatmap view next to the image matrix.
- Side-by-side comparison of chosen parameter combinations.
- Sliders for size and metric in place of the dropdowns.

## Housekeeping

- The sweep regenerates all 336 figures each run. Skip existing files, or cache embeddings, to make re-runs cheap.
