import uuid
from typing import override

from tinydb_serialization import Serializer


class UuidSerializer(Serializer):
    OBJ_CLASS = uuid.UUID

    @override
    def encode(self, obj):
        return str(obj)

    @override
    def decode(self, s):
        return uuid.UUID(s)
