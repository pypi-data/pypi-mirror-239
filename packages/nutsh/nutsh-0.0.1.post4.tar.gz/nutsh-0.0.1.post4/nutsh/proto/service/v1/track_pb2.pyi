from schema.v1 import train_pb2 as _train_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackRequest(_message.Message):
    __slots__ = ("first_image_uri", "first_image_mask", "subsequent_image_uris")
    FIRST_IMAGE_URI_FIELD_NUMBER: _ClassVar[int]
    FIRST_IMAGE_MASK_FIELD_NUMBER: _ClassVar[int]
    SUBSEQUENT_IMAGE_URIS_FIELD_NUMBER: _ClassVar[int]
    first_image_uri: str
    first_image_mask: _train_pb2.Mask
    subsequent_image_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, first_image_uri: _Optional[str] = ..., first_image_mask: _Optional[_Union[_train_pb2.Mask, _Mapping]] = ..., subsequent_image_uris: _Optional[_Iterable[str]] = ...) -> None: ...

class TrackResponse(_message.Message):
    __slots__ = ("subsequent_image_masks",)
    SUBSEQUENT_IMAGE_MASKS_FIELD_NUMBER: _ClassVar[int]
    subsequent_image_masks: _containers.RepeatedCompositeFieldContainer[_train_pb2.Mask]
    def __init__(self, subsequent_image_masks: _Optional[_Iterable[_Union[_train_pb2.Mask, _Mapping]]] = ...) -> None: ...

class FrameMask(_message.Message):
    __slots__ = ("frame_index", "mask")
    FRAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    frame_index: int
    mask: _train_pb2.Mask
    def __init__(self, frame_index: _Optional[int] = ..., mask: _Optional[_Union[_train_pb2.Mask, _Mapping]] = ...) -> None: ...
