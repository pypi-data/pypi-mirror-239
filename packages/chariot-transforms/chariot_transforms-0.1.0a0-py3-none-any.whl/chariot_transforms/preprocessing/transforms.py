import inspect
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import List, Tuple, Union

import numpy as np
import torch
import torchvision.transforms.functional as F
from PIL import Image, ImageOps
from torch.nn.functional import interpolate, pad
from torchvision.transforms.functional import InterpolationMode

from chariot_transforms.preprocessing.clahe import equalize_adapthist
from chariot_transforms.preprocessing.histogram_tools import linear_stretch


class PILTransform:
    """Base class for transforms of PIL images and, optionally, PyTorch image tensors
    as well as associated bounding box and segmentation mask annotations. Subclasses
    are used both for training time data augmentation as well as (training and
    inference time) resizing transformations. These latter transformations
    subclass the `PreprocessingTransform` class.

    At a minimum, the method `convert_img`, which operates on PIL images, must
    be implemented for any subclass. For supporting converting annotations,
    the methods `_convert_bbox` and/or `_convert_mask` should be implemented.

    For transformations that can and should be done on the GPU (typically resizing
    transformations at inference time), the `convert_img_pt` method should be
    implemented, which operates on PyTorch image tensors.
    """

    def __call__(self, img, mask=None, bbox_dict=None):
        """
        Parameters
        ----------
        img : Image.Image
            image
        mask : Image.Imagee
            segmentation mask
        bbox_dict : dict
            dict with keys "bboxes" and "classes"

        Returns
        -------
        Image.Image or tuple
            If only img is passed then the return is the transformed image. Otherwise it is
            a tuple with the first item the transformed image and the other items
            the transformed annotations.
        """
        if isinstance(img, torch.Tensor):
            ret = [self.convert_img_pt(img)]
        else:
            ret = [self.convert_img(img)]
        if mask is not None:
            ret.append(self._convert_mask(mask))
        if bbox_dict is not None:
            new_bbox_dict = {"bboxes": [], "classes": []}
            for bbox, label in zip(bbox_dict["bboxes"], bbox_dict["classes"]):
                new_bbox = self._convert_bbox(bbox)
                if new_bbox is not None:
                    new_bbox_dict["bboxes"].append(new_bbox)
                    new_bbox_dict["classes"].append(label)

            ret.append(new_bbox_dict)

        return tuple(ret) if len(ret) > 1 else ret[0]

    def _convert_bbox(self, bbox):
        """
        Parameters
        ----------
        bbox : list
            of the form [ymin, xmin, ymax, xmax]

        Returns
        -------
        list or None
            list of the new bounding box of the form [ymin, xmin, ymax, xmax]
            or None (e.g. if the transform is a random crop that crops out bbox)
        """
        raise NotImplementedError

    def _convert_mask(self, mask):
        """
        Parameters
        ----------
        mask : PIL.Image.Image

        Returns
        -------
        PIL.Image.Image
            the transformed mask
        """
        raise NotImplementedError

    def convert_img(self, img):
        """
        Parameters
        ----------
        img : PIL.Image.Image

        Returns
        -------
        PIL.Image.Image
            the transformed image
        """
        raise NotImplementedError

    def convert_img_pt(self, img):
        """Transforms a PyTorch image tensor. This method is needed for those
        transforms that are the pil_transform attribute of a teddy model (so
        transforms just used in training or for data augmentation do not need
        to implement this method). This allows support for complex model pipelines
        where the same GPU tensor of a raw image can get passed around to different
        models that require different pre-processing, which can be done directly
        on the GPU tensor instead of going back and forth between PIL (CPU) objects
        and (GPU) tensors.

        Parameters
        ----------
        img : torch.tensor
            should have shape [N, C, H, W]

        Returns
        -------
        torch.tensor
            the transformed image
        """
        raise NotImplementedError

    def set_magnitude(self, magnitude: float) -> None:
        """This is an optional method that only applies for transforms used with
        a "strength" controlled by a single float parameter and used
        in techniques such as RandAugment.
        """
        raise NotImplementedError


class LiskovCheckerMeta(ABCMeta):
    """Enforces that subclasses adhere to the Liskov Substitution Principle,
    i.e. that for functions which they have in common, subclass function parameters
    constitute a superset of those of the base class, which ensures that a
    consistent baseline API is provided. While this should be SOP regardless, this
    metaclass can be used to enforce LSP in particularly critical inheritance chains.
    """

    def __init__(cls, name, bases, attrs):
        errors = []
        for base_cls in bases:
            for meth_name in getattr(base_cls, "__abstractmethods__", ()):
                orig_argspec = inspect.getfullargspec(
                    getattr(base_cls, meth_name)
                )
                target_argspec = inspect.getfullargspec(
                    getattr(cls, meth_name)
                )
                is_bad = False
                for attr in ["args", "kwonlyargs"]:
                    if not set(getattr(orig_argspec, attr)).issubset(
                        getattr(target_argspec, attr)
                    ):
                        is_bad = True
                        break
                for attr in ["varargs", "varkw"]:
                    if (
                        getattr(target_argspec, attr) is None
                        and getattr(orig_argspec, attr) is not None
                    ):
                        is_bad = True
                        break
                if is_bad:
                    errors.append(
                        f"Abstract method {meth_name!r} not implemented with correct signature in {cls.__name__!r}. "
                        f"Expected {orig_argspec}."
                    )
        if errors:
            raise TypeError("\n".join(errors))
        super().__init__(name, bases, attrs)


class PreprocessingTransform(PILTransform, metaclass=LiskovCheckerMeta):
    """These are the transforms which can be used as the pil_transform attribute of a model. It provides a common API
    for transforms which are used for reducing images to the size of a given NN and then transforming outputs (such as bounding boxes)
    back into the original image space.

    n.b.: The reason for having this class separate from  `PILTransform` is that transforms in teddy inherit
    from `PILTransform` but not all of them are scaling transforms (for example, a random crop).
    """

    def __init__(
        self,
        histogram_equalization: bool = False,
        histogram_linear_stretch: float = None,
    ):
        """
        Parameters
        ----------
        histogram_linear_stretch: float
            If provided, image histograms will be stretched and this percentage of the histogram's tail will be clipped.
            E.g. if `histogram_linear_stretch==2` then the lowest and highest 2% of the histogram will be clipped.
            This value must be in [0, 50); it is recommended that this value is in the range of [0, 5].
            Note: if histogram_linear_stretch is not None and histogram_equalization is True the linear stretch
            always occurs before the histogram equalization.
        histogram_equalization: bool
            A flag to indicate whether CLAHE preprocessing should be applied to the imagery.
            Note: if histogram_linear_stretch is not None and histogram_equalization is True the linear stretch
            always occurs before the histogram equalization.
        """
        self.histogram_equalization = histogram_equalization
        self.histogram_linear_stretch = histogram_linear_stretch

    def __call__(self, img, mask=None, bbox_dict=None):
        if (
            self.histogram_equalization
            or self.histogram_linear_stretch is not None
        ):
            # these both map array to array
            img_arr = np.array(img)

            if self.histogram_linear_stretch is not None:
                img_arr = (
                    linear_stretch(img_arr, self.histogram_linear_stretch)
                    * 255
                ).astype("uint8")

            if self.histogram_equalization:
                img_arr = (
                    equalize_adapthist(img_arr, nbins=256) * 255
                ).astype("uint8")
            img = Image.fromarray(img_arr)

        return super().__call__(img=img, mask=mask, bbox_dict=bbox_dict)

    @abstractmethod
    def convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        raise NotImplementedError

    @abstractmethod
    def convert_coords(self, coords, img_h, img_w, invert=False):
        raise NotImplementedError

    def _convert_bbox(self, bbox):
        return self.convert_bbox(bbox)

    def _convert_mask(self, mask):
        return self.convert_img(mask)

    def invert_torch_output(self, x, img_h, img_w):
        """Inverts a mask to the original image size. This is used when we need to get the mask
        back to the original image shape in the case of a segmentation model's whose PIL transform
        resizes an image before passing through the network.

        Parameters
        ----------
        x : torch.Tensor
            should be shape [C, H, W] or [N, C, H, W]
        img_h : int
            height to resize to
        img_w : int
            width to resize to

        Returns
        -------
        torch.Tensor
            will be of shape [C, img_h, img_w] or [N, C, img_h, img_w]
        """
        singleton_passed = False
        if len(x.shape) == 3:
            x = x.unsqueeze(0)
            singleton_passed = True
        assert len(x.shape) == 4
        ret = interpolate(x, size=(img_h, img_w), mode="nearest")
        return ret.squeeze(0) if singleton_passed else ret


# to make the name change backwards compatible
ScalingTransform = PreprocessingTransform


class TrivialPILTransform(PILTransform):
    """Class for transforms that act trivially on annotations."""

    def _convert_bbox(self, bbox):
        return bbox

    def _convert_mask(self, mask):
        return mask


class IdentityPILTransform(TrivialPILTransform, PreprocessingTransform):
    """Transform used for models that do not need any image pre-processing.
    Used as the default parameter for the pil_transform attribute of teddy
    models. For all class methods the output is the input.
    """

    def convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        return bbox

    def convert_img(self, img):
        return img

    def convert_img_pt(self, img):
        return img

    def convert_coords(self, coords, img_h, img_w, invert=False):
        return coords

    def set_magnitude(self, magnitude: float) -> None:
        return

    def __eq__(self, other):
        return isinstance(other, IdentityPILTransform)

    def invert_torch_output(self, x, img_h, img_w):
        # We override base class method for speed since this is just
        # the identity transform.
        return x


class Resize(PreprocessingTransform):
    """Resize the input PIL Images to a given size or specified min/max size.

    This class method is able to resize torch tensors directly (on CPU or GPU)
    via its convert_img_pt method. Note that because of the way PIL and PyTorch
    resize, they may not always agree, i.e. if t is a Resize object then
    ToTensor()(t.convert_img(img)) and t.convert_img_pt(ToTensor()(img))
    will likely be different.
    """

    def __init__(
        self,
        size: Union[List[int], int] = None,
        min_size: int = None,
        max_size: int = None,
        interpolation: InterpolationMode = InterpolationMode.BILINEAR,
        histogram_equalization: bool = False,
        histogram_linear_stretch: float = None,
    ) -> None:
        """
        Parameters
        ----------
        size : sequence or int
            Desired output size. If size is a sequence like
            (h, w), output size will be matched to this. If size is an int,
            smaller edge of the image will be matched to this number.
            i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
        min_size : int
            Desired minimum size of single dimension (height or width) of an image.
        max_size : int
            Desired maximum size of single dimension (height or width) of an image.
        interpolation : int
            Desired interpolation. Default is ``InterpolationMode.BILINEAR``


        Note: Exactly one of size or (min_size and max_size) must be set.
        If size is set, every image will be resized to match the specified size.
        If (instead) min_size and max_size are set, each input image will be resized so that
        either the resized_min_size matches the specified min_size or the
        resized_max_size matches the specified max_size, whichever results in the resized image
        having smaller area.  It is not guaranteed that the resized image will satisfy both
        (weak) constraints: i.e. that resized_max_size <= max_size and resized_min_size <= min_size.
        """

        assert bool(min_size) == bool(
            max_size
        ), "If you set one of min_size or max_size, you must set both (and be positive integers)."
        assert bool(size) != bool(
            min_size
        ), "You must set either size or (min_size and max_size)."
        if size is not None:
            assert isinstance(size, int) or (
                isinstance(size, Iterable) and len(size) == 2
            )
        else:
            assert min_size > 0, "min_size must be a positive integer"
            assert max_size >= min_size, "max_size must be at least min_size"

        self.size = size
        self.interpolation = interpolation
        self.min_size = min_size
        self.max_size = max_size

        super().__init__(
            histogram_equalization=histogram_equalization,
            histogram_linear_stretch=histogram_linear_stretch,
        )

    def get_new_size(self, img_shape: Tuple[int, int]) -> Tuple[int, int]:
        """
        Parameters
        ----------
        img_shape
            tuple of the form (height, width)

        Returns
        -------
        Tuple[int, int]
            the height and width of the resized image
        """
        if self.size is not None:
            if isinstance(self.size, int):
                return (
                    (self.size * img_shape[0] / img_shape[1], self.size)
                    if img_shape[0] > img_shape[1]
                    else (self.size, self.size * img_shape[1] / img_shape[0])
                )
            return self.size
        else:
            # both self.min_size and self.max_size are set...
            # determine current min/max lengths.
            current_min_side_length = min(img_shape)
            current_max_side_length = max(img_shape)

            # compute possible resizing ratios (scales)
            tight_min_ratio = self.min_size / current_min_side_length
            tight_max_ratio = self.max_size / current_max_side_length

            # best ratio is the smaller of the two
            ratio = min(tight_min_ratio, tight_max_ratio)

            return (int(img_shape[0] * ratio), int(img_shape[1] * ratio))

    def _calc_resize(self, img_shape):
        new_size = self.get_new_size(img_shape)
        size = (np.array(new_size, dtype=int)).astype(float)
        return size[0] / img_shape[0], size[1] / img_shape[1]

    def convert_img(self, img):
        # set resize for converting bounding boxes
        self.orig_size = (img.height, img.width)
        size = (
            self.size
            if self.size is not None
            else self.get_new_size(self.orig_size)
        )
        return F.resize(img, size, self.interpolation)

    def convert_img_pt(self, img):
        if len(img.shape) != 4:
            raise ValueError("img must be a rank 4 tensor")
        # set resize for converting bounding boxes
        self.orig_size = tuple(img.shape[2:4])
        size = (
            self.size
            if self.size is not None
            else self.get_new_size(self.orig_size)
        )
        return interpolate(img, size, mode="bilinear", align_corners=False)

    def convert_mask(self, mask, invert=False):
        if invert:
            raise ValueError("inversion not supported")
        return self.convert_img(mask)

    def convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        """Converts a bounding box. If invert is False then transforms the
        bounding box from an img_h x img_w image to the bounding box for the
        resized self.new_h x self.new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        bbox : list
            of the form [ymin, xmin, ymax, xmax]
        img_h : int
            if None then will use self.img_h
        img_w : int
            if None then will use self.img_w
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        list
            list of integers of the transformed bounding box.
        """

        if not hasattr(self, "orig_size") and not (img_h and img_w):
            raise Exception(
                "Must call convert_img before convert_bbox or pass img_h and img_w"
            )
        orig_size = (img_h, img_w) if (img_h and img_w) else self.orig_size
        resize = self._calc_resize(orig_size)
        exp = -1 if invert else 1
        return [
            resize[0] ** exp,
            resize[1] ** exp,
            resize[0] ** exp,
            resize[1] ** exp,
        ] * np.array(bbox)

    def convert_coords(self, coords, img_h, img_w, invert=False):
        """Converts coordinates. If invert is False then transforms the
        coordinates from an img_h x img_w image to the coordinates for the
        resized new_h x new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        coords : np.ndarray
            of shape N(x...)x2 of the form [[y_0, x_0], [y_1, x_1], ...]
        img_h : int
        img_w : int
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        np.ndarray
            array of the transformed coordinates.
        """
        exp = -1 if invert else 1
        resize = np.array(self._calc_resize((img_h, img_w))) ** exp
        new_coords = np.array(coords) * resize
        return new_coords

    def __repr__(self):
        if self.size is not None:
            return (
                self.__class__.__name__
                + "(size={0}, interpolation={1})".format(
                    self.size, self.interpolation
                )
            )
        else:
            return (
                self.__class__.__name__
                + "(min_size={0}, max_size={1}, interpolation={2})".format(
                    self.min_size, self.max_size, self.interpolation
                )
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.size == other.size
            and self.interpolation == other.interpolation
            and self.min_size == other.min_size
            and self.max_size == other.max_size
        )


class ResizePreserveAspect(PreprocessingTransform):
    """Class for resizing an image and bounding boxes to (new_h, new_w)
    by preserving aspect ratio and padding as necessary.

    This class method is able to resize torch tensors directly (on CPU or GPU)
    via its convert_img_pt method. Note that because of the way PIL and PyTorch
    resize, they may not always agree, i.e. if t is a ResizePreserveAspect
    object then ToTensor()(t.convert_img(img)) and
    t.convert_img_pt(ToTensor()(img)) will likely be different.
    """

    def __init__(
        self,
        new_h: int,
        new_w: int,
        fill: Union[int, Tuple[int, int, int]] = 0,
        histogram_equalization: bool = False,
        histogram_linear_stretch: float = None,
    ):
        """
        Parameters
        ----------
        new_h : int
            height to resize to
        new_w : int
            width to resize to
        fill : int or Tuple[int, int, int]
            the fill color to use for the padding
        """
        self.new_h = new_h
        self.new_w = new_w
        self.fill = fill

        super().__init__(
            histogram_equalization=histogram_equalization,
            histogram_linear_stretch=histogram_linear_stretch,
        )

    def convert_bbox(self, bbox, img_h=None, img_w=None, invert=False):
        """Converts a bounding box. If invert is False then transforms the
        bounding box from an img_h x img_w image to the bounding box for the
        resized self.new_h x self.new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        bbox : list
            of the form [ymin, xmin, ymax, xmax]
        img_h : int
            if None then will use self.img_h
        img_w : int
            if None then will use self.img_w
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        list
            list of integers of the transformed bounding box.
        """

        img_w = img_w or self.img_w
        img_h = img_h or self.img_h

        new_w = self.new_w
        new_h = self.new_h

        if img_w / img_h <= new_w / new_h:
            # padding was added to increase width
            act_w = int(img_w / img_h * new_h)  # image width without padding
            x_offset = (new_w - act_w) // 2
            x_scale = act_w / img_w

            y_offset = 0
            y_scale = new_h / img_h
        else:
            # padding was added to increase height
            act_h = int(img_h / img_w * new_w)  # image height without padding
            y_offset = (new_h - act_h) // 2
            y_scale = act_h / img_h

            x_offset = 0
            x_scale = new_w / img_w

        if invert:
            return [
                (bbox[0] - y_offset) / y_scale,
                (bbox[1] - x_offset) / x_scale,
                (bbox[2] - y_offset) / y_scale,
                (bbox[3] - x_offset) / x_scale,
            ]
        return [
            y_scale * bbox[0] + y_offset,
            x_scale * bbox[1] + x_offset,
            y_scale * bbox[2] + y_offset,
            x_scale * bbox[3] + x_offset,
        ]

    def convert_coords(self, coords, img_h, img_w, invert=False):
        """Converts coordinates. If invert is False then transforms the
        coordinates from an img_h x img_w image to the coordinates for the
        resized new_h x new_w image. If invert is True then it will do the
        conversion in the opposite direction.

        Parameters
        ----------
        coords : np.ndarray
            of shape N(x...)x2 of the form [[y_0, x_0], [y_1, x_1], ...]
        img_h : int
        img_w : int
        invert : bool
            whether or not to return the inverse operation

        Returns
        -------
        np.ndarray
            array of the transformed coordinates.
        """

        new_w = self.new_w
        new_h = self.new_h

        if img_w / img_h <= new_w / new_h:
            # padding was added to increase width
            act_w = int(img_w / img_h * new_h)  # image width without padding
            x_offset = (new_w - act_w) // 2
            x_scale = act_w / img_w

            y_offset = 0
            y_scale = new_h / img_h
        else:
            # padding was added to increase height
            act_h = int(img_h / img_w * new_w)  # image height without padding
            y_offset = (new_h - act_h) // 2
            y_scale = act_h / img_h

            x_offset = 0
            x_scale = new_w / img_w

        new_coords = np.zeros(coords.shape, dtype=coords.dtype)
        if invert:
            new_coords[..., 0] = (coords[..., 0] - y_offset) / y_scale
            new_coords[..., 1] = (coords[..., 1] - x_offset) / x_scale
        else:
            new_coords[..., 0] = coords[..., 0] * y_scale + y_offset
            new_coords[..., 1] = coords[..., 1] * x_scale + x_offset

        return new_coords

    def convert_img(self, img):
        w, h = img.size
        self.img_w, self.img_h = w, h

        if w / h <= self.new_w / self.new_h:
            act_w = int(w / h * self.new_h)
            new_img = img.resize((act_w, self.new_h), Image.BILINEAR)
            border = self.new_w - act_w
            # add border // 2 on the left and border - border // 2 on the right
            new_img = ImageOps.expand(
                new_img, (border // 2, 0, border - border // 2, 0), self.fill
            )
        else:
            act_h = int(h / w * self.new_w)
            new_img = img.resize((self.new_w, act_h), Image.BILINEAR)
            border = self.new_h - act_h
            # add border // 2 on the top and border - border // 2 on the bottom
            new_img = ImageOps.expand(
                new_img, (0, border // 2, 0, border - border // 2), self.fill
            )
        return new_img

    def convert_img_pt(self, img):
        h, w = img.shape[2:4]

        if w / h <= self.new_w / self.new_h:
            act_w = int(w / h * self.new_h)
            new_img = interpolate(img, (self.new_h, act_w), mode="bilinear")
            border = self.new_w - act_w
            # add border // 2 on the left and border - border // 2 on the right
            new_img = pad(new_img, (border // 2, border - border // 2))
        else:
            act_h = int(h / w * self.new_w)
            new_img = interpolate(img, (act_h, self.new_w), mode="bilinear")
            border = self.new_h - act_h
            # add border // 2 on the top and border - border // 2 on the bottom
            new_img = pad(new_img, (0, 0, border // 2, border - border // 2))
        return new_img

    def convert_mask(self, mask, invert=False):
        if invert:
            raise ValueError("Inversion not supported")
        return self.convert_img(mask)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.new_h == other.new_h
            and self.new_w == other.new_w
        )
