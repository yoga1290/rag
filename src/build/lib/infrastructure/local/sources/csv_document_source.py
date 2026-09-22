from __future__ import annotations

import csv
import mimetypes
import os
from collections.abc import Iterator
from pathlib import Path

from yoga1290.rag.domain.models.document import Document
from yoga1290.rag.domain.ports.document_source import DocumentSource


class CsvDocumentSource(DocumentSource):
    """
    DocumentSource implementation that reads document paths
    from a CSV file.
    """

    def __init__(
        self,
        csv_path: str = os.getenv(
            "LOCAL_CSV_DOCUMENTS_SOURCE_PATH",
            "documents/output.csv",
        ),
        document_column: str = os.getenv(
            "LOCAL_CSV_DOCUMENTS_SOURCE_FILEPATH_COLUMN",
            "attachments",
        ),
    ) -> None:
        self.csv_path = csv_path
        self.document_column = document_column

    def __iter__(self) -> Iterator[Document]:

        with open(
            self.csv_path,
            "r",
            encoding="utf-8",
            newline="",
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                file_path = row[self.document_column]

                if not file_path:
                    continue

                path = Path(file_path)

                yield Document(
                    id=file_path,
                    filename=file_path, # path.name,
                    content_type="application/octet-stream",
                    uri=file_path,
                    metadata={
                        "source": file_path,
                    },
                )

