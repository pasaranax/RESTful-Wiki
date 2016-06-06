'''
Created on 3 июня 2016 г.

@author: Михаил Булыгин <pasaranax@gmail.com>
'''

from elasticsearch import Elasticsearch
from flask import Flask, jsonify, make_response, request, abort


app = Flask(__name__)
es = Elasticsearch()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# Поиск по тексту статьи с параметром ?query=текст
@app.route("/wiki/", methods=["GET"])
def search():
    query = request.args.get("query")
    if not query:
        query = ""
    res = es.search(index="wiki", body={"query": {"match": {"text": query}}})
    return jsonify({"results": res["hits"]["hits"]})


# Поиск статей конкретного автора
@app.route("/wiki/author/<author>", methods=["GET"])
def get_author(author):
    res = es.search(index="wiki", body={"query": {"match": {"author": author}}})
    return jsonify({"results": res["hits"]["hits"]})


# Поиск статьи по ID
@app.route("/wiki/id/<article_id>", methods=["GET"])
def get_id(article_id):
    res = es.search(index="wiki", body={"query": {"match": {"_id": article_id}}})
    return jsonify({"results": res["hits"]["hits"]})

# Добавить статью под указанным ID
@app.route("/wiki/", methods=["POST"])
def post_article():
    body = request.json
    if not (body and "author" in body and "text" in body and "title" in body):
        abort(400)
    posted = es.index(index="wiki", doc_type="article", body=body)
    return jsonify({"results": posted}), 201

@app.route("/wiki/id/<article_id>", methods=["PUT"])
def edit_article(article_id):
    res = es.search(index="wiki", body={"query": {"match": {"_id": article_id}}})
    body = request.json
    if not (body and "author" in body and "text" in body and "title" in body):
        abort(400)
    if res["hits"]["total"] > 0:
        es.index(index="wiki", doc_type="article", body=body, id=article_id)
    return jsonify({"edited": "ok"})

# Удалить статью по ID
@app.route("/wiki/id/<article_id>", methods=["DELETE"])
def delete_article(article_id):
    res = es.search(index="wiki", body={"query": {"match": {"_id": article_id}}})
    if res["hits"]["total"] > 0:
        es.delete(index="wiki", id=article_id, doc_type="article")
    else:
        abort(404)
    return jsonify({"deleted": "ok"})
    

if __name__ == '__main__':
    app.run(debug=True)
    
    
    