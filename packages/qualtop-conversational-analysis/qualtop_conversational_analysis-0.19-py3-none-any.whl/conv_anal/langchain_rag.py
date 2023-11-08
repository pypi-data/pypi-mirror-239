import os
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from langchain.embeddings import GPT4AllEmbeddings


def generate_single_doc_db(pdf_path):
    assert os.path.exists(pdf_path)

    pdf_loader = PyPDFLoader(pdf_path)
    docs = pdf_loader.load()
    print(f"Loading document...")
    documents = pdf_loader.load()
    
    print(f"\nStarting document splitting...")
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, 
                                                   chunk_overlap=100)
    documents = text_splitter.split_documents(documents)
    
    print(f"\nCreating BERT embeddings...")
    # Embed
    persist_directory = os.path.join(os.path.expanduser("~"),
                                     ".cache/embeddings",
                                     "data/gnp_single")
    vect_db = Chroma.from_documents(documents, 
                                    embedding=GPT4AllEmbeddings(), 
                                    persist_directory=persist_directory)
    vect_db.persist()

def generate_vector_db(pdf_folder):
    assert os.path.exists(pdf_folder)
    documents = []
    for root, folder, filenames in os.walk(pdf_folder):
        i=1
        for fname in filenames:
            if not "pdf" in fname or fname.endswith("txt"):
                continue
            file_path = os.path.join(root, fname)
            pdf_loader = PyPDFLoader(file_path)
            docs = pdf_loader.load()
            documents.extend(pdf_loader.load())
            print(f"Loaded document {i}...")
            i += 1

    print(f"\nStarting document splitting...")
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, 
                                                   chunk_overlap=100)
    documents = text_splitter.split_documents(documents)
    
    print(f"\nCreating BERT embeddings...")
    # Embed
    persist_directory = os.path.join(os.path.expanduser("~"),
                                     ".cache/embeddings",
                                     "data/gnp")
    vect_db = Chroma.from_documents(documents, 
                                    embedding=GPT4AllEmbeddings(), 
                                    persist_directory=persist_directory)
    vect_db.persist()

if __name__ == "__main__":
    generate_single_doc_db(os.path.join(os.path.expanduser("~"), 
                                        "temp/gnp",
                                        "example.pdf"))
    generate_vector_db(os.path.join(os.path.expanduser("~"), 
                                    "temp/gnp"))
