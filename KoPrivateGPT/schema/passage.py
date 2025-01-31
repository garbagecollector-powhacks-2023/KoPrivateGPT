from typing import Optional, Union

from langchain.load.serializable import Serializable
from langchain.schema import Document
from pydantic import Field
from uuid import UUID, uuid4


class Passage(Serializable):
    """Class for storing a passage and metadatas"""
    id: Union[UUID, str] = Field(default_factory=uuid4)
    content: str
    filepath: str
    previous_passage_id: Optional[UUID]
    next_passage_id: Optional[UUID]
    metadata_etc: dict = Field(default_factory=dict)

    def to_document(self) -> Document:
        metadata = self.metadata_etc.copy()
        metadata['id'] = self.id
        metadata['content'] = self.content
        metadata['filepath'] = self.filepath
        metadata['previous_passage_id'] = self.previous_passage_id
        metadata['next_passage_id'] = self.next_passage_id
        return Document(page_content=self.content, metadata=metadata)

    def to_dict(self):
        return {
            "_id": self.id,
            "content": self.content,
            "filepath": self.filepath,
            "previous_passage_id": self.previous_passage_id,
            "next_passage_id": self.next_passage_id,
            "metadata_etc": self.metadata_etc
        }

    def __eq__(self, other):
        if isinstance(other, Passage):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
