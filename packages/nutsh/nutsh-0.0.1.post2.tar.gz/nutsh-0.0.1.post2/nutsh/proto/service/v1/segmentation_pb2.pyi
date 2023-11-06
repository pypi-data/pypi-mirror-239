from schema.v1 import common_pb2 as _common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IntrospectRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IntrospectResponse(_message.Message):
    __slots__ = ("decoder_uuid", "decoder_feed_js")
    DECODER_UUID_FIELD_NUMBER: _ClassVar[int]
    DECODER_FEED_JS_FIELD_NUMBER: _ClassVar[int]
    decoder_uuid: str
    decoder_feed_js: str
    def __init__(self, decoder_uuid: _Optional[str] = ..., decoder_feed_js: _Optional[str] = ...) -> None: ...

class EmbedImageRequest(_message.Message):
    __slots__ = ("original_image", "decoder_uuid", "crop")
    ORIGINAL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    DECODER_UUID_FIELD_NUMBER: _ClassVar[int]
    CROP_FIELD_NUMBER: _ClassVar[int]
    original_image: bytes
    decoder_uuid: str
    crop: _common_pb2.GridRect
    def __init__(self, original_image: _Optional[bytes] = ..., decoder_uuid: _Optional[str] = ..., crop: _Optional[_Union[_common_pb2.GridRect, _Mapping]] = ...) -> None: ...

class EmbedImageResponse(_message.Message):
    __slots__ = ("embedded_image_npy",)
    EMBEDDED_IMAGE_NPY_FIELD_NUMBER: _ClassVar[int]
    embedded_image_npy: bytes
    def __init__(self, embedded_image_npy: _Optional[bytes] = ...) -> None: ...

class GetDecoderRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDecoderResponse(_message.Message):
    __slots__ = ("decoder_onnx", "uuid")
    DECODER_ONNX_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    decoder_onnx: bytes
    uuid: str
    def __init__(self, decoder_onnx: _Optional[bytes] = ..., uuid: _Optional[str] = ...) -> None: ...
