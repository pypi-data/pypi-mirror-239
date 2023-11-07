# -*- coding:utf-8 -*-
import os
import openai
import pickle
import tiktoken

from datetime import datetime

import argparse

from scipy import spatial

import pandas as pd

from conv_anal.gentera import generate_db_summaries, generate_db_row_based_summaries
from conv_anal.infer_data import analyse_dataset

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

def calculate_embeddings(text_dataset):
    embeddings = []
    for batch_start in range(0, len(text_dataset), BATCH_SIZE):
        batch_end = batch_start + BATCH_SIZE
        batch = text_dataset[batch_start:batch_end]
        print(f"Batch {batch_start} to {batch_end-1}")
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
        for i, be in enumerate(response["data"]):
            assert i == be["index"]  # double check embeddings are in same order as input
        batch_embeddings = [e["embedding"] for e in response["data"]]
        embeddings.extend(batch_embeddings)
    
    df = pd.DataFrame({"text": text_dataset, "embedding": embeddings})
    return df

# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

def num_tokens(text, model):
    """Return the number of tokens in a string."""
    if "llama" in model or "mistral" in model:
        encoding = tiktoken.get_encoding("gpt2")
    else:
        encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def create_query_message_with_context(query, df, model, token_budget, introduction=""):
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""

    if "llama" in model or "mistral" in model:
        token_budget_error = 100
    else:
        token_budget_error = 0

    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    message = introduction
    question = f"\n\nPregunta: {query}"
    message += f'\n\nBase de datos de empleado:\n"""'
    for string in strings:
        next_article = f'\n{string}\n'
        total_tokens = num_tokens(message + next_article + f'\n"""' + question, model=model)
        total_tokens += token_budget_error
        if total_tokens > token_budget:
            break
        else:
            message += next_article
    return message + f'\n"""' + question

def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""

    if "llama" in model or "mistral" in model:
        token_budget_error = 100
    else:
        token_budget_error = 0

    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'Usa la base de datos de empleado siguiente para responder la pregunta. Si la respuesta no se puede encontrar en la información de empleado, escribe "No encontré la respuesta."'
    question = f"\n\nPregunta: {query}"
    message = introduction
    message += f'\n\nBase de datos de empleado:\n"""'
    for string in strings:
        next_article = f'\n{string}\n'
        total_tokens = num_tokens(message + next_article + f'\n"""' + question, model=model)
        total_tokens += token_budget_error
        if total_tokens > token_budget:
            break
        else:
            message += next_article
    return message + f'\n"""' + question

def ask(
    query: str,
    df: pd.DataFrame,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 1000,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "Respondes preguntas sobre empleados de una empresa."},
        {"role": "user", "content": message},
    ]

    print(f"Starts api call {datetime.now().strftime('%y-%m-%d %H:%M')}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=500,
        temperature=0,
        request_timeout=60
    )
    print(f"Ends api call {datetime.now().strftime('%y-%m-%d %H:%M')}")
    response_message = response["choices"][0]["message"]["content"]
    return response_message

def main(interactive=True, question="", document_type="rows"):
    # Setup openai
    openai_key=os.environ["OPENAI_API_KEY"]
    openai.api_key = openai_key

    # Get categorical information
    df, description = analyse_dataset("conv_anal/data/gentera/gentera.csv")
    categorical_assertions = [s.strip().replace("registros", 
                                                "colaboradores") \
                                                       for s in description.split("\n") \
                                                           if "registros" in s]
  
    # Get information
    if document_type=="rows":
        db_summaries = generate_db_row_based_summaries()
        db_summaries += categorical_assertions
        embeddings_path = "./conv_anal/bin/db_embeddings_row.bin"
    else:
        db_summaries, _ = generate_db_summaries(fine_grain=True)
        db_summaries += categorical_assertions
        embeddings_path = "./conv_anal/bin/db_embeddings.bin"

    # Get embeddings
    try:
        db_embeddings = pd.read_pickle(embeddings_path)
    except:
        db_embeddings = calculate_embeddings(db_summaries)
        db_embeddings.to_pickle(embeddings_path, compression="infer")

    if interactive:
        print("Consulta la base de datos:\n")
        while interactive:
            question = input("Pregunta> ")
            if question.lower() == "quit":
                interactive = False
            else:
                response = ask(question, df=db_embeddings)
                print(response)
    else:
        assert len(question) > 0
        return ask(question, df=db_embeddings)
    return

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", type=str,
                        help="Question about the database")
    args = parser.parse_args()
    if args.question == None:
        main(document_type="rows")
    else:
        print(main(interactive=False, question=args.question))
