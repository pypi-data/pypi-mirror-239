import os
from gpt4all import Embed4All
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

from langchain.embeddings.openai import OpenAIEmbeddings


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
    vect_db = Chroma.from_documents(documents, 
                                    embedding=Embed4All(), 
                                    persist_directory="./conv_anal/data/gnp")
    vect_db.persist()

if __name__ == "__main__":
    generate_vector_db(os.path.join(os.path.expanduser("~"), "temp/gnp"))
