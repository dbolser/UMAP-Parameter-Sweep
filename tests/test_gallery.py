import json
import re

from generate_gallery import extract_params, generate_gallery


def test_extract_params():
    assert extract_params("umap-0010-0.00100-cosine.png") == {
        "n_neighbors": "0010",
        "min_dist": "0.00100",
        "metric": "cosine",
    }


def test_extract_params_rejects_unexpected_names():
    assert extract_params("umap-0010.png") is None


def test_generate_gallery(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for size, name in [
        ("400", "umap-0002-0.00000-cosine.png"),
        ("8000", "umap-0010-0.10000-euclidean.png"),
    ]:
        (tmp_path / "Figures" / size).mkdir(parents=True, exist_ok=True)
        (tmp_path / "Figures" / size / name).touch()
    (tmp_path / "Figures" / "400" / "notes.txt").touch()  # Ignored

    generate_gallery()

    html = (tmp_path / "index.html").read_text()
    figures = json.loads(re.search(r"const figuresBySize = (\{.*\});", html).group(1))
    assert figures == {
        "400": [
            {
                "filename": "umap-0002-0.00000-cosine.png",
                "path": "Figures/400/umap-0002-0.00000-cosine.png",
                "n_neighbors": "0002",
                "min_dist": "0.00000",
                "metric": "cosine",
            }
        ],
        "8000": [
            {
                "filename": "umap-0010-0.10000-euclidean.png",
                "path": "Figures/8000/umap-0010-0.10000-euclidean.png",
                "n_neighbors": "0010",
                "min_dist": "0.10000",
                "metric": "euclidean",
            }
        ],
    }


def test_generate_gallery_without_figures(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    generate_gallery()
    assert not (tmp_path / "index.html").exists()
    assert "does not exist" in capsys.readouterr().out
