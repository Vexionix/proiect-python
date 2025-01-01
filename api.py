import sqlite3
from flask import Flask, jsonify, request

conn = sqlite3.connect('states_of_the_world.db', check_same_thread=False)
cursor = conn.cursor()

# Setup Flask application for API
app = Flask(__name__)


@app.route('/top-10-tari-populatie', methods=['GET'])
def top_10_population():
    cursor.execute('SELECT name, population FROM countries ORDER BY population DESC LIMIT 10')
    results = cursor.fetchall()
    return jsonify(results)

@app.route('/top-10-tari-suprafata', methods=['GET'])
def top_10_area():
    cursor.execute('SELECT name, area FROM countries ORDER BY area DESC LIMIT 10')
    results = cursor.fetchall()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)