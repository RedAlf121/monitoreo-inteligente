from langchain_community.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader
def get_format(file_path: str) -> str:
    return file_path.split(".")[-1]

class FormatFactory:
    loader: dict = {'pdf': UnstructuredPDFLoader, 'docx': UnstructuredWordDocumentLoader}

    @classmethod
    def get_loader(cls, format: str):
        return cls.loader.get(format)

def load_document(file_path: str) -> str:
    format = get_format(file_path)
    loader = FormatFactory.get_loader(format)
    if not loader:
        return f"Unsupported document format: {format}"
    document = loader(file_path)
    print(document)
    return f"Document at {file_path} was read successfully in {format} format."

