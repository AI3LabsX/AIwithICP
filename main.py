import json
import os
import typing as t
from pathlib import Path

import PyPDF2
import openai
from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings

from utils import PROJECT_ROOT
from utils.env import env
from utils.logger import logger

openai.api_key = os.environ.get('OPENAI_API_KEY')


def get_all_docs(path: str | Path):
    return [file for file in os.listdir(path)]


def get_vectorstore(faiss_name: str, embeddings: OpenAIEmbeddings) -> FAISS:
    vectorStores = FAISS.load_local(faiss_name, embeddings)
    return vectorStores


def create_json_context(data_path: Path | str):
    data = {}
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):

            with open(data_path.joinpath(str(file)), 'rb') as f:
                # creating a pdf reader object
                doc = PyPDF2.PdfReader(f)
                page_content = doc.pages
                pages_c = []
                for i in page_content:
                    pages_c.append(i.extract_text())
                data[file] = "".join(pages_c)
    json_data = json.dumps(data, indent=4)
    with open("data_content.json", 'w') as json_file:
        json_file.write(json_data)


def generate_qa(query: str, vectorstore, language) -> str:
    knowledge = []
    docs = vectorstore.max_marginal_relevance_search(query, k=10)
    for doc in docs:
        knowledge.append(doc)
    logger.info(docs)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are ICP AI bot to answer question based on documents from ICP official docs. Output "
                           "the key points for answer. First always output the DDocument filename before key points "

            },
            {
                "role": "system",
                "content": f"Content from Vector Store based on relevance of query: {knowledge}"
            },

            {
                "role": "user",
                "content": f"User Question: {query}. "
            },
            {
                "role": "system",
                "content": f"Generate Answer in Language: {language}"
            },
            {
                "role": "user",
                "content": f"Documents Source {[doc.metadata['source'] for doc in docs]}"
            }
        ],

        temperature=0,
        max_tokens=2000,
        top_p=0.4,
        frequency_penalty=1.5,
        presence_penalty=1
    )
    bot_response = response['choices'][0]['message']['content']
    return bot_response


def load_json_data(json_path: str | Path) -> t.Dict[str, t.Any] | t.List[str]:
    """
    Loads json data    :param json_path: path to json
    :return: Dict or List with data
    """
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def read_generate(filename, json_context, language):
    data = load_json_data(PROJECT_ROOT.joinpath(json_context))
    content = data.get(filename)
    logger.info(filename)

    MAX_TOKENS = 12000  # Adjust as needed

    content_chunks = [content[i:i + MAX_TOKENS] for i in range(0, len(content), MAX_TOKENS)]

    intermediate_summaries = []
    for chunk in content_chunks:
        messages = [
            {"role": "system", "content": "Create detailed summary of the ICP document from Context."},
            {"role": "system", "content": f"Context from the doc: {chunk}"},
            {"role": "system", "content": f"Generate Answer in Language: {language}"},
            {"role": "user", "content": f"Documents Source {filename}"}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            temperature=0,
            max_tokens=2000,
            top_p=0.4,
            frequency_penalty=1.5,
            presence_penalty=1
        )

        intermediate_summaries.append(response['choices'][0]['message']['content'])

    # If there are multiple chunks, create a final summary from the intermediate summaries
    if len(content_chunks) > 1:
        final_summary_content = " ".join(intermediate_summaries)
        final_summary_messages = [
            {"role": "system", "content": "Create a concise summary from the intermediate summaries."},
            {"role": "system", "content": f"Intermediate Summaries: {final_summary_content}"},
            {"role": "user",
             "content": "Please provide a concise and clear summary based on the provided intermediate summaries. You "
                        "can be detailed with key points from summaries."}
        ]

        final_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=final_summary_messages,
            temperature=0,
            max_tokens=2000,
            top_p=0.4,
            frequency_penalty=1.5,
            presence_penalty=1
        )

        return final_response['choices'][0]['message']['content']
    else:
        return intermediate_summaries[0]


def generate_build(project, vectorStore, language):
    knowledge = []
    query = f"I want to build {project} project on ICP blockchain can generate me main step to do that with examples " \
            f"of potential projects in that category ({project}.) "
    docs = vectorStore.max_marginal_relevance_search(query, k=10)
    for doc in docs:
        knowledge.append(doc)
    logger.info(docs)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": ""

            },
            {
                "role": "system",
                "content": f"Content from Vector Store based on relevance of query: {knowledge}"
            },

            {
                "role": "user",
                "content": f"User Question: {query}. "
            },
            {
                "role": "system",
                "content": f"Generate Answer in Language: {language}"
            },
            {
                "role": "system",
                "content": "When possible use link to refer user to go deeper, if links are presented in docs"
            }
        ],

        temperature=0,
        max_tokens=2000,
        top_p=0.4,
        frequency_penalty=1.5,
        presence_penalty=1
    )
    bot_response = response['choices'][0]['message']['content']
    return bot_response
