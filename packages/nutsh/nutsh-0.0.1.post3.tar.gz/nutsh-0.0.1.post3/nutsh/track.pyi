from .lib.logging import init_logging as init_logging
from .proto.schema.v1.train_pb2 import Mask as Mask
from .proto.service.v1 import track_pb2_grpc as track_pb2_grpc
from .track_grpc import TrackService as TrackService, Tracker as Tracker
from _typeshed import Incomplete
from typing import Callable

class Service:
    workspace: Incomplete
    on_reqeust: Incomplete
    def __init__(self, workspace: str, on_reqeust: Callable[[str, Mask], Tracker]) -> None: ...
    def start(self, port: int) -> None: ...
