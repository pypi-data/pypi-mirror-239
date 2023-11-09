import random

import numpy as np
from PIL import Image, ImageDraw

from chariot_transforms import bbox_ops
from chariot_transforms.augmentations.pil_transforms import (
    AutoContrast,
    Brightness,
    CenterCrop,
    Color,
    ColorJitter,
    Contrast,
    Cutout,
    Equalize,
    Gamma,
    Grayscale,
    HorizontalShear,
    Hue,
    Pad,
    Posterize,
    RandAugment,
    RandomAffine,
    RandomCrop,
    RandomGrayscale,
    RandomHorizontalFlip,
    RandomPerspective,
    RandomResize,
    RandomRotation,
    RandomVerticalFlip,
    Resize,
    ResizePreserveAspect,
    Rotation,
    Saturation,
    Sharpness,
    Solarize,
    TranslateX,
    TranslateY,
)

bbox_ops.DROP_BBOX_AREA_RATIO_THRES = 0.0

random.seed(7)


def random_bbox(img):
    ymin = random.randint(0, img.height - 40)
    ymax = random.randint(ymin + 20, img.height)
    xmin = random.randint(0, img.width - 40)
    xmax = random.randint(xmin + 20, img.width)

    return [ymin, xmin, ymax, xmax]


def _test_bbox_conversion(transform, atol: float = 3.5):
    """
    Test that bounding boxes get transformed properly with an image.
    It does this by doing the following 100 times:

    1. Create a PIL image with a random rectangle in it.
    2. Transform the image and bounding box of the rectangle
    3. Check that the resulting rectangle in the image is
    circumscribed by the transformed bounding box
    """
    for _ in range(100):
        img = Image.new("RGB", (200, 100))
        bbox = random_bbox(img)
        img_draw = ImageDraw.Draw(img)
        img_draw.rectangle([bbox[1], bbox[0], bbox[3], bbox[2]], fill="red")

        trans_img, trans_bbox_dict = transform(
            img, bbox_dict={"bboxes": [bbox], "classes": ["class"]}
        )
        # find pixels of the rectangle in the image
        ys, xs, _ = np.where(np.array(trans_img) > 20)

        if len(ys) == 0 or max(ys) - min(ys) < 1 or max(xs) - min(xs) < 1:
            # if no pixels (e.g. if rectangle got cropped out) check that
            # no bounding boxes come back
            assert len(trans_bbox_dict["bboxes"]) == 0
        elif max(ys) - min(ys) == 1 or max(xs) - min(xs) == 1:
            # a sliver
            assert len(trans_bbox_dict["bboxes"]) <= 1
        else:
            assert len(trans_bbox_dict["bboxes"]) != 0
            trans_bbox = trans_bbox_dict["bboxes"][0]
            np.testing.assert_allclose(
                [min(ys), min(xs), max(ys), max(xs)],
                trans_bbox,
                rtol=1e-3,
                atol=atol,
            )


def test_auto_contrast():
    _test_bbox_conversion(AutoContrast())


def test_brightness():
    _test_bbox_conversion(Brightness(0.7))


def test_saturation():
    _test_bbox_conversion(Saturation(0.7))


def test_center_crop():
    _test_bbox_conversion(CenterCrop(size=(12, 20)))


def test_color_jitter():
    _test_bbox_conversion(ColorJitter(0.2, 0.2, 0.2, 0.2))


def test_color():
    _test_bbox_conversion(Color(1.2))


def test_contrast():
    _test_bbox_conversion(Contrast(1.2))


def test_gamma():
    _test_bbox_conversion(Gamma(1.2))


def test_hue():
    _test_bbox_conversion(Hue(0.2))


def test_cutout():
    _test_bbox_conversion(Cutout(32))


def test_equalize():
    _test_bbox_conversion(Equalize())


def test_grayscale():
    _test_bbox_conversion(Grayscale(num_output_channels=3))


def test_horizontal_shear():
    _test_bbox_conversion(HorizontalShear(0.1))


def test_pad():
    _test_bbox_conversion(Pad(padding=(16, 14, 32, 6)))


def test_posterize():
    _test_bbox_conversion(Posterize(3))


def test_random_crop():
    _test_bbox_conversion(RandomCrop((100, 50)))


def test_random_horizontal_flip():
    _test_bbox_conversion(RandomHorizontalFlip())


def test_horizontal_flip():
    _test_bbox_conversion(RandomHorizontalFlip(1))


def test_random_resize():
    _test_bbox_conversion(RandomResize(scale_range_high=2, p=1.0), atol=3)


def test_random_vertical_flip():
    _test_bbox_conversion(RandomVerticalFlip())


def test_random_affine():
    _test_bbox_conversion(
        RandomAffine(
            degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.2), shear=(-10, 10)
        ),
        atol=10,
    )


def test_rand_augment_m_specified():
    _test_bbox_conversion(
        RandAugment(
            n=2,
            m=3,
            augs_to_remove=[
                "Invert",
                "Solarize",
                "Brightness",
                "Contrast",
                "HorizontalShear",
                "VerticalShear",
            ],
        ),
        atol=8.5,
    )


def test_rand_augment_m_not_specified():
    _test_bbox_conversion(
        RandAugment(
            n=3,
            augs_to_remove=[
                "Invert",
                "Solarize",
                "Brightness",
                "Contrast",
                "Rotation",
                "HorizontalShear",
                "VerticalShear",
                "TranslateY",
                "TranslateX",
            ],
        )
    )


def test_random_grayscale():
    _test_bbox_conversion(RandomGrayscale())


def test_random_perspective():
    _test_bbox_conversion(RandomPerspective(0.1), atol=11)


def test_random_rotation():
    _test_bbox_conversion(RandomRotation(10))


def test_resize():
    _test_bbox_conversion(Resize((32, 32)))


def test_resize_single_int():
    img = Image.new("RGB", (200, 100))
    new_img = Resize(32)(img)
    assert new_img.size == (32 * 200 / 100, 32)
    img = Image.new("RGB", (100, 200))
    new_img = Resize(32)(img)
    assert new_img.size == (32, 32 * 200 / 100)


def test_resize_preserve_aspect():
    _test_bbox_conversion(ResizePreserveAspect(new_h=32, new_w=32))


def test_rotation():
    _test_bbox_conversion(Rotation(10))


def test_sharpness():
    _test_bbox_conversion(Sharpness(0.5))


def test_solarize():
    _test_bbox_conversion(Solarize(256))


def test_translate_x():
    _test_bbox_conversion(TranslateX(0.4))


def test_translate_y():
    _test_bbox_conversion(TranslateY(0.4))
