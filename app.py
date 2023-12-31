from pathlib import Path

from flask import Flask, render_template, request, jsonify, abort
from langchain.embeddings import OpenAIEmbeddings

from main import get_all_docs, read_generate, load_json_data, get_vectorstore, generate_qa, generate_build
from utils import PROJECT_ROOT

app = Flask(__name__)


@app.route('/')
def index():
    try:
        docs = get_all_docs(PROJECT_ROOT.joinpath("READ"))
        languages = load_json_data(PROJECT_ROOT.joinpath("lan.json"))
        projects = load_json_data(PROJECT_ROOT.joinpath("projects.json"))  # Load projects from projects.json
        return render_template("index.html", docs=docs, languages=languages, projects=projects)
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error


@app.route('/generate_summary_page')
def generate_summary_page():
    filename = request.args.get('filename')
    language = request.args.get('language')
    if not filename or not language:
        abort(400)  # Bad Request
    return render_template('generate_summary_page.html', filename=filename, language=language)


@app.route('/qa_page')
def qa_page():
    filename = request.args.get('filename')
    language = request.args.get('language')
    if not filename or not language:
        abort(400)  # Bad Request
    return render_template('qa_page.html', filename=filename, language=language)


@app.route('/build_page')
def build_page():
    project = request.args.get('project')
    language = request.args.get('language')
    if not project or not language:
        abort(400)  # Bad Request
    return render_template('build_page.html', project=project, language=language)


@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    try:
        filename = request.json.get('filename')
        json_context = PROJECT_ROOT.joinpath("data_content.json")
        language = request.json.get('language')
        if not filename or not language:
            abort(400)  # Bad Request
        response = read_generate(filename, json_context, language)
        return jsonify(response=response)
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error


@app.route('/generate_response', methods=['POST'])
def generate_response():
    try:
        query = request.json.get('query')
        filename = request.json.get('filename')
        language = request.json.get('language')
        if not query or not filename or not language:
            abort(400)  # Bad Request
        embeddings = OpenAIEmbeddings()
        faiss = Path(PROJECT_ROOT).joinpath("Data", filename)
        vectorstore = get_vectorstore(str(faiss), embeddings)
        response = generate_qa(query, vectorstore, language)
        return jsonify(response=response)
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error


@app.route('/icp_build', methods=['POST'])
def icp_build():
    try:
        language = request.json.get('language')
        project = request.json.get('project')

        if not language or not project:
            abort(400)  # Bad Request: Missing required parameters
        embeddings = OpenAIEmbeddings()
        faiss = Path(PROJECT_ROOT).joinpath("BUILD", "ICP_BUILD")
        vectorstore = get_vectorstore(str(faiss), embeddings)
        response = generate_build(project, vectorstore, language)

        return jsonify(response=response)
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Internal Server Error


if __name__ == '__main__':
    app.run(debug=True)
