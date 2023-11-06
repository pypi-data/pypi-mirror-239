from schema.v1 import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointPrompt(_message.Message):
    __slots__ = ("x", "y", "is_positive")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    IS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    is_positive: bool
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., is_positive: bool = ...) -> None: ...

class Mask(_message.Message):
    __slots__ = ("coco_encoded_rle", "size")
    COCO_ENCODED_RLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    coco_encoded_rle: str
    size: _common_pb2.GridSize
    def __init__(self, coco_encoded_rle: _Optional[str] = ..., size: _Optional[_Union[_common_pb2.GridSize, _Mapping]] = ...) -> None: ...

class SegmentationInput(_message.Message):
    __slots__ = ("crop",)
    CROP_FIELD_NUMBER: _ClassVar[int]
    crop: _common_pb2.GridRect
    def __init__(self, crop: _Optional[_Union[_common_pb2.GridRect, _Mapping]] = ...) -> None: ...

class SegmentationPrompt(_message.Message):
    __slots__ = ("point_prompts",)
    POINT_PROMPTS_FIELD_NUMBER: _ClassVar[int]
    point_prompts: _containers.RepeatedCompositeFieldContainer[PointPrompt]
    def __init__(self, point_prompts: _Optional[_Iterable[_Union[PointPrompt, _Mapping]]] = ...) -> None: ...

class SegmentationOutput(_message.Message):
    __slots__ = ("mask",)
    MASK_FIELD_NUMBER: _ClassVar[int]
    mask: Mask
    def __init__(self, mask: _Optional[_Union[Mask, _Mapping]] = ...) -> None: ...

class SegmentationSample(_message.Message):
    __slots__ = ("input", "prompt", "output")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    input: SegmentationInput
    prompt: SegmentationPrompt
    output: SegmentationOutput
    def __init__(self, input: _Optional[_Union[SegmentationInput, _Mapping]] = ..., prompt: _Optional[_Union[SegmentationPrompt, _Mapping]] = ..., output: _Optional[_Union[SegmentationOutput, _Mapping]] = ...) -> None: ...

class Sample(_message.Message):
    __slots__ = ("image_url", "segmentation")
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    SEGMENTATION_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    segmentation: SegmentationSample
    def __init__(self, image_url: _Optional[str] = ..., segmentation: _Optional[_Union[SegmentationSample, _Mapping]] = ...) -> None: ...
