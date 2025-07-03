from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.agent.model_factory import ModelFactory
from models.agent.prompt_factory import extraction_prompt,filter_prompt
from langchain_core.output_parsers import StrOutputParser
from services.format_factory import FormatFactory

def get_format(file_path: str) -> str:
    return file_path.split(".")[-1]

def load_document(file_path: str) -> str:
    file_format = get_format(file_path)
    LoaderClass = FormatFactory.get_loader(file_format)
    if LoaderClass is None:
        raise ValueError(f"Formato de archivo no soportado: {file_format}")
    loader = LoaderClass(file_path)
    documents = loader.load()
    if not documents or all(not getattr(doc, "page_content", "").strip() for doc in documents):
        raise ValueError("El documento está vacío")
    return documents

def process_rules(document):
    parser = StrOutputParser()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(document)
    
    llm = ModelFactory.build_groq_model(model_name="qwen-qwq-32b")

    combined_rules = extract_rules(llm,parser, chunks)
    
    filtered_rules = filter_rules(parser, llm, combined_rules)
    
    return filtered_rules

def extract_rules(llm,parser,chunks):
    prompt = extraction_prompt()

    extraction_chain = prompt | llm | parser

    extracted_rules = []
    for chunk in chunks:
        rules = extraction_chain.invoke({"text": chunk.page_content})
        extracted_rules.append(rules)
    
    combined_rules = "\n\n".join(extracted_rules)
    return combined_rules

def filter_rules(parser, llm, combined_rules):
    prompt = filter_prompt()

    filter_chain = prompt | llm | parser
    filtered_rules = filter_chain.invoke({"rules": combined_rules})
    return filtered_rules

