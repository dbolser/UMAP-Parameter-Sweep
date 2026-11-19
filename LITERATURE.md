# UMAP Hyperparameters, Density and Structure: A Short Literature Report

**Question:** how should `n_neighbors` and `min_dist` be set to get the most real structure out of dense, high-dimensional embedding vectors, and does the best setting shift as the number of points grows?

## The short answer

1. **UMAP's layout is a balance of pull and push.** Most "structure versus wash-out" effects come from where the parameters put you on that balance.
2. **UMAP normalises away input density by design.** Density only shows up through crowding in the 2D plot, unless you ask for it explicitly (densMAP).
3. **Global layout comes mostly from initialisation**, not from the algorithm.
4. **A 2D plot can invent structure.** Judge parameters with scores against known ground truth, not by eye.

## Key papers

### McInnes, Healy & Melville (2018): the UMAP paper
[arXiv:1802.03426](https://arxiv.org/abs/1802.03426)

- Builds a fuzzy k-nearest-neighbour graph, then lays it out in 2D.
- Each point's neighbour distances are rescaled locally. That makes the graph roughly **density-independent**: sparse and dense regions look alike.
- `n_neighbors` is a **count**, not a radius. As N grows, a fixed count covers a smaller share of the data, so the view becomes more local.
- `min_dist` acts **only in the output plot**. It sets how tightly points may pack in 2D and does nothing to the neighbour graph.

### Kobak & Linderman (2021): initialisation drives global structure
*Initialization is critical for preserving global data structure in both t-SNE and UMAP.* Nature Biotechnology 39, 156–157. ([preprint](https://www.biorxiv.org/content/10.1101/2019.12.19.877522v1))

- UMAP's apparent advantage over t-SNE on global structure comes from its **informative initialisation**, not the algorithm.
- With random initialisation, UMAP preserves global structure as poorly as t-SNE.
- **For us:** this is why the sweep now uses `init="pca"`.

### Böhm, Berens & Kobak (2022): the attraction–repulsion spectrum
*Attraction-Repulsion Spectrum in Neighbor Embeddings.* JMLR 23(95), 1–32. ([paper](https://www.jmlr.org/papers/v23/21-0055.html))

- t-SNE, UMAP, ForceAtlas2 and Laplacian eigenmaps all sit on one spectrum, from strong repulsion to strong attraction.
- **More repulsion** gives sharper discrete clusters and better kNN recall.
- **More attraction** shows continuous manifolds better.
- UMAP sits on the attraction side of t-SNE, because its negative sampling weakens repulsion.
- **For us:** the "extreme values wash out structure" effect seen in the sweep is movement along this spectrum.

### Narayan, Berger & Cho (2021): densMAP
*Assessing single-cell transcriptomic variability through density-preserving data visualization.* Nature Biotechnology 39, 765–774. ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8195812))

- Standard UMAP and t-SNE throw away local density, so a tight group and a loose group can look the same size.
- densMAP adds a term that keeps each point's local radius from the input in the plot.
- Available in umap-learn as `densmap=True`.
- **For us:** the most direct tool for asking how density affects the picture.

### Wang, Huang, Rudin & Shaposhnik (2021): how DR tools work, plus PaCMAP
*Understanding How Dimension Reduction Tools Work.* JMLR 22(201), 1–73. ([paper](https://jmlr.org/papers/v22/20-1061.html))

- Compares t-SNE, UMAP, TriMap and PaCMAP on synthetic data with known structure.
- Shows how loss-function design trades local structure against global structure.
- Introduces PaCMAP, which aims to keep both.
- **For us:** a model for the experiment we want to run, with planted structure and clear scoring.

### Chari & Pachter (2023): a sceptic's view
*The specious art of single-cell genomics.* PLOS Computational Biology 19(8), e1011288. ([paper](https://ideas.repec.org/a/plo/pcbi00/1011288.html))

- 2D embeddings heavily distort distances and neighbourhoods.
- Don't draw conclusions from the picture alone.
- **For us:** a reminder to score embeddings, not just look at them.

## Practical notes for dense, high-dimensional embeddings

- **Metric:** use cosine for text or image embedding vectors.
- **Starting values:** `n_neighbors` 15–50. Use `min_dist` ≈ 0 when the output feeds clustering, and larger values for looking at it.
- **Output dimensions:** use 5–10 for clustering (BERTopic, for example, defaults to `n_components=5`, `min_dist=0.0`, cosine), and 2D only for viewing.
- **Very high input dimensions:** distances bunch together and "hub" points appear, i.e. points that are near neighbours of many others (Radovanović et al. 2010, *Hubs in Space*, JMLR 11). Reducing to around 50 dimensions with PCA first is a common, cheap fix.
- **Reproducibility:** fixing `random_state` makes runs repeatable but disables parallelism, so it's slower.

## Docs worth reading

- [umap-learn: Basic UMAP Parameters](https://umap-learn.readthedocs.io/en/latest/parameters.html)
- [umap-learn: Using UMAP for Clustering](https://umap-learn.readthedocs.io/en/latest/clustering.html)
- [umap-learn: Better Preserving Local Density with DensMAP](https://umap-learn.readthedocs.io/en/latest/densmap_demo.html)
