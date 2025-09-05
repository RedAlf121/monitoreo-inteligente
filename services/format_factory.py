from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

class FormatFactory:
    loader = {'pdf': PyPDFLoader, 'docx': Docx2txtLoader}

    @classmethod
    def get_loader(cls, format: str):
        return cls.loader.get(format)
