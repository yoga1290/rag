from yoga1290.rag.domain.models.document import Document
from yoga1290.rag.domain.models.parsed_document import ParsedDocument

from yoga1290.rag.domain.ports.document_parser import DocumentParser

class LocalDocumentParser(DocumentParser):
    def parse(self, document: Document) -> ParsedDocument:

        filepath = document.filename
        content_type = document.content_type
        if filepath.find(".txt") > -1:
            content_type = "text/plain"
        if filepath.find(".html") > -1:
            content_type = "text/html"
        if filepath.find(".pdf") > -1:
            content_type = "application/pdf"

        return ParsedDocument(
            document_id=document.id,
            text= self.processFile(document.filename),
            # pages=(page,),
            # tables=(table,),
            metadata={
                "filename": document.filename,
                "content_type": content_type,
                "parser": "yoga1290.rag.domain.ports.document_parser.LocalDocumentParser",
            },
        )
        # raise NotImplementedError

    def processFile(self, filepath):
        from langchain_community.document_loaders import PyPDFLoader
        #SEE https://reference.langchain.com/python/langchain-community/document_loaders/html/UnstructuredHTMLLoader
        from langchain_community.document_loaders.html import UnstructuredHTMLLoader
        
        if filepath.find(".txt") > -1:
            with open(filepath, 'r') as file:
                txt = file.read()
                return txt
                
        elif filepath.find(".pdf") > -1:
            loader= PyPDFLoader(filepath).load()
            for doc in loader:
                page_content = doc.page_content
                return page_content
                
        elif filepath.find(".html") > -1:
            loader = UnstructuredHTMLLoader(f'{filepath}').load()
            for doc in loader:
                page_content = doc.page_content
                return page_content
        else: return ''


