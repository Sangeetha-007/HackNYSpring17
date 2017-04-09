"""
have pickle be a temp db for the api

"""
from flask import Flask, jsonify, abort, request
import pickle

app=Flask(__name__)


data = pickle.load( open("procs.p", "rb" ) )


@app.route('/t/<string:ticker>')
def giveTicker(ticker):
    if ticker in data:
        print ticker
        return jsonify(data[ticker])
    else:
        return abort(404)

@app.route('/all')
def giveAll():
    return jsonify(data.keys())


@app.route("/u/<string:ticker>", methods=["GET"])
def getTicker(ticker):
    r = request.json
    print(r , ticker)
    return jsonify("good pickle")


if __name__ == "__main__":
    app.run(debug=True)
