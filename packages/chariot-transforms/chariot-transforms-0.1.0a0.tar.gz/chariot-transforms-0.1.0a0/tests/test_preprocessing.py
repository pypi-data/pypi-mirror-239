import numpy as np
import pytest
import torch
from PIL import Image
from torchvision.transforms import ToPILImage

from chariot_transforms.preprocessing import Resize, ResizePreserveAspect
from chariot_transforms.preprocessing.clahe import equalize_adapthist
from chariot_transforms.preprocessing.histogram_tools import linear_stretch


@pytest.fixture
def img_tensor() -> torch.Tensor:
    return torch.rand(3, 50, 150)


@pytest.fixture
def img(img_tensor) -> Image.Image:
    return ToPILImage()(img_tensor)


@pytest.fixture
def mask() -> Image.Image:
    return Image.fromarray(
        np.random.randint(0, 255, size=(50, 150), dtype=np.uint8)
    )


@pytest.fixture
def img_arr() -> np.ndarray:
    rng = np.random.RandomState(2023)
    return rng.randint(0, 256, (50, 50, 3), dtype=np.uint8)


def test_clahe_dtype(img_arr: np.ndarray):
    """Check that we get the same CLAHE normalized output for uint8 image arrays as
    float arrays
    """
    out1 = equalize_adapthist(img_arr)
    out2 = equalize_adapthist(img_arr.astype(np.float32) / 255.0)

    np.testing.assert_almost_equal(out1, out2, decimal=6)


def test_linear_stretch_dtype(img_arr: np.ndarray):
    """Check that we get the same linear stretch normalized output for uint8 image arrays as
    float arrays
    """
    out1 = linear_stretch(img_arr, 0.6)
    out2 = linear_stretch(img_arr.astype(np.float32) / 255.0, 0.6)

    np.testing.assert_almost_equal(out1, out2, decimal=6)


def test_resize_torch_error(img_tensor):
    resize = Resize((60, 30))
    with pytest.raises(ValueError) as exc_info:
        resize.convert_img_pt(img_tensor)

    assert "img must be a rank 4 tensor" in str(exc_info)


def test_resize_shapes(img_tensor: torch.Tensor, img: Image.Image):
    for s in [(60, 60), (200, 500)]:
        for cls in [Resize, ResizePreserveAspect]:
            resizer = cls(s) if cls == Resize else cls(*s)
            out_pil = resizer(img)
            out_tensor = resizer(img_tensor.unsqueeze(0))

            # Image.size is (width, height)
            assert out_pil.size == (s[1], s[0])
            assert out_tensor.shape[2:4] == s


def test_variable_shapes(img_tensor: torch.Tensor, img: Image.Image):
    for min_size, max_size in [
        (20, 30),
        (25, 75),
        (35, 200),
        (65, 100),
        (100, 250),
        (175, 300),
    ]:
        resizer = Resize(min_size=min_size, max_size=max_size)
        out_pil = resizer(img)
        out_tensor = resizer(img_tensor.unsqueeze(0))

        # Checks on PIL image
        assert (min(out_pil.size) == min_size) or (
            max(out_pil.size) == max_size
        ), f"min_size: {min_size}, max_size: {max_size}"
        assert (
            max(out_pil.size) <= max_size
        ), f"maximum output size too large, min_size: {min_size}, max_size: {max_size}"

        # Same checks on Tensor output
        assert (min(out_tensor.shape[2:4]) == min_size) or (
            max(out_tensor.shape[2:4]) == max_size
        ), "min_size: {0}, max_size: {1}".format(min_size, max_size)
        assert (
            max(out_tensor.shape[2:4]) <= max_size
        ), f"maximum output size too large, min_size: {min_size}, max_size: {max_size}"


def test_shapes_with_mask(img: Image.Image, mask: Image.Image):
    for s in [(60, 60), (200, 500)]:
        for cls in [Resize, ResizePreserveAspect]:
            resizer = cls(s) if cls == Resize else cls(*s)
            out_pil, out_mask = resizer(img, mask=mask)

            # Confirm masks are resized correctly.
            assert out_pil.size == (s[1], s[0])
            assert out_mask.size == (s[1], s[0])


def test_resize_invert_torch_output():
    t = Resize((10, 12))

    x = torch.rand((2, 3, 10, 12))
    y = t.invert_torch_output(x, 20, 80)

    assert tuple(y.shape) == (2, 3, 20, 80)
    assert len(y.unique()) == len(x.unique())
    # check the elements are the same (note .unique() returns
    # sorted items)
    for a, b in zip(y.unique(), x.unique()):
        assert a.item() == b.item()

    # repeat with single image
    x = torch.rand((3, 10, 12))
    y = t.invert_torch_output(x, 20, 80)

    assert tuple(y.shape) == (3, 20, 80)
    assert len(y.unique()) == len(x.unique())
    for a, b in zip(y.unique(), x.unique()):
        assert a.item() == b.item()


def test_resize_preserve_aspect_torch_output():
    t = ResizePreserveAspect(new_h=10, new_w=12)
    x = torch.rand((2, 3, 10, 12))
    y = t.invert_torch_output(x, 20, 80)
    assert tuple(y.shape) == (2, 3, 20, 80)

    assert len(y.unique()) == len(x.unique())

    # check the elements are the same (note .unique() returns
    # sorted items)
    for a, b in zip(y.unique(), x.unique()):
        assert a.item() == b.item()

    # repeat with single image
    x = torch.rand((3, 10, 12))
    y = t.invert_torch_output(x, 20, 80)

    assert tuple(y.shape) == (3, 20, 80)
    assert len(y.unique()) == len(x.unique())
    for a, b in zip(y.unique(), x.unique()):
        assert a.item() == b.item()
