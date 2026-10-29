import numpy as np
import pytest

from sweep import align, make_data


def test_make_data_shape_and_range():
    data = make_data(400)
    assert data.shape == (400, 4)
    assert data.min() >= 0 and data.max() < 1


def test_make_data_is_deterministic():
    np.testing.assert_array_equal(make_data(400), make_data(400))


def test_smaller_datasets_are_prefixes_of_larger():
    np.testing.assert_array_equal(make_data(400), make_data(8000)[:400])


@pytest.mark.parametrize("angle", [0, 90, 180, 270, 37])
@pytest.mark.parametrize("mirror", [False, True])
def test_align_undoes_rotation_and_reflection(angle, mirror):
    data = make_data(400)
    target = data[:, :2] - data[:, :2].mean(axis=0)

    theta = np.radians(angle)
    rotation = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    if mirror:
        rotation = rotation @ np.diag([1, -1])
    embedding = data[:, :2] @ rotation + [5, -3]  # Rotated, maybe mirrored, and shifted

    np.testing.assert_allclose(align(embedding, data), target, atol=1e-10)


def test_align_preserves_pairwise_distances():
    data = make_data(400)
    embedding = np.random.default_rng(0).normal(size=(400, 2))

    def distances(u):
        return np.linalg.norm(u[:, None] - u[None, :], axis=-1)

    np.testing.assert_allclose(distances(align(embedding, data)), distances(embedding))
