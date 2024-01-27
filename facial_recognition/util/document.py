from tinydb.table import Document

from facial_recognition.model.face_data import FaceData


def to_face_data_list(document_list: list[dict]) -> list[FaceData]:
    return list(
        map(
            lambda document: FaceData(doc_id=document.doc_id, **document), document_list
        )
    )


def to_face_data(document: Document) -> FaceData:
    return FaceData(doc_id=document.doc_id, **document)
