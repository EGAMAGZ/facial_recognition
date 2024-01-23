import uuid

from tinydb_serialization import Serializer


class UuidSerializer(Serializer):
    OBJ_CLASS = uuid.UUID

    def encode(self, obj):
        return str(obj)

    def decode(self, s):
        return uuid.UUID(s)
