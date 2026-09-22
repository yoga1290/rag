from collections.abc import Iterator
from abc import ABC, abstractmethod
from yoga1290.rag.domain.models.document import Document


class DocumentSource:
    """
    Port for retrieving documents from an external source.

    Implementations may read from:
      - Local filesystem
      - S3
      - Azure Blob Storage
      - Google Cloud Storage
      - Databricks Volumes
      - Database
      - Message queue
      - HTTP/API
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Document]:
        """
        Iterate over documents available from the source.

        Returns:
            Iterator of Document objects.
        """
        raise NotImplementedError