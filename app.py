import codecs
import json
from fakenews_model import predict_article
from fakenews_model import train_model
from scraping import Scraping
from nlp import tokenize, pos_tag, rm_stop_words, bag_of_words, lemmatization, stemming, tfidf
from db import user_collection, scraping_collection
from textblob import TextBlob
import re
from json import JSONEncoder
import threading
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)

CORS(app)


@app.route('/process_text', methods=['POST'])
def process_text():
    _json = request.get_json(force=True)
    if not "method" in _json or not "text" in _json:
        return not_found()
    text = _json['text']
    method = _json['method']
    result = None

    if method == "tokenization":
        result = tokenize(text)
    elif method == "pos_tag":
        result = pos_tag(tokenize(text))
    elif method == "rm_stop_words":
        result = rm_stop_words(text)
    elif method == "lemmatization":
        result = lemmatization(text)
    elif method == "tfidf":
        result = tfidf(text)
    elif method == "stemming":
        result = stemming(text)
    elif method == "bag_of_words":  # expecting an array of texts
        result = bag_of_words(text)
        result = tfidf(text)
    elif method == "stemming":
        result = stemming(text)
    elif method == "bag_of_words":  # expecting an array of texts
        result = bag_of_words(text)
    elif method == "stemming":
        result = stemming(text)
    elif method == "bag_of_words":  # expecting an array of texts
        result = bag_of_words(text)
    response = jsonify({"data": result})
    return response


@app.route('/emotion', methods=['POST'])
def emotion():
    _json = request.get_json(force=True)
    if not "text" in _json:
        return not_found()
    text = _json['text']
    s = TextBlob(text)
    emotion = s.sentiment.polarity
    if emotion == 0:
        res = "neutral"
    elif emotion > 0:
        res = "positive"
    else:
        res = "negative"
    response = jsonify({"success": True, "data": res})

    return response


@app.route('/scrap', methods=['POST'])
def add():
    _json = request.get_json(force=True)
    if not "de" in _json or not "a" in _json:
        return not_found()
    de = _json['de']
    a = _json['a']
    rows = Scraping(de, a)
    for row in rows:
        regex = re.compile('[^a-z A-Z,?/!\ ]')
        row['title'] = regex.sub('', row['title'])
        row['text'] = regex.sub('', row['text'])
        scraping_collection.insert(
            {'link': row['link'], 'title': row['title'], 'text': row['text']})
        row['title'] = regex.sub('', row['title'])
        row['text'] = regex.sub('', row['text'])
        scraping_collection.insert(
            {'link': row['link'], 'title': row['title'], 'text': row['text']})

    response = jsonify({"success": True, "data": "scrapted"})
    return response


@app.route('/data', methods=['GET'])
def get_all_data():
    data = user_collection.find()
    resp = dumps(data)
    return resp


@app.route('/data/<id>', methods=['GET'])
def get_data(id):
    data = user_collection.find_one({'_id': ObjectId(id)})
    resp = dumps(data)
    return resp


@app.route('/data', methods=['POST'])
def save_new_data():
    _json = request.get_json(force=True)
    print(_json)
    _name = _json['name']
    if _name and request.method == 'POST':
        user_collection.insert_one({"name": _name})
        resp = jsonify('Data added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/data/<id>', methods=['DELETE'])
def delete_user(id):
    user_collection.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Data deleted successfully!')
    resp.status_code = 200
    return resp


@app.route('/predict/fakenews', methods=['POST'])
def predict():
    _json = request.get_json(force=True)
    if not "article" in _json:
        return not_found()
    article = _json['article']

    return jsonify({"isFake":  predict_article(article)})


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    app.run(port=8000, debug=True)
