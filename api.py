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


@app.route('/top-10-tari-densitate', methods=['GET'])
def top_10_density():
    cursor.execute('SELECT name, density FROM countries ORDER BY density DESC LIMIT 10')
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/top-10-tari-suprafata', methods=['GET'])
def top_10_area():
    cursor.execute('SELECT name, area FROM countries ORDER BY area DESC LIMIT 10')
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/tarile-cu-fus-orar', methods=['GET'])
def countries_by_timezone():
    fus_orar = request.args.get('fus_orar')
    if not fus_orar:
        return jsonify({"error": "The parameter 'fus_orar' is required"}), 400
    cursor.execute('SELECT name FROM countries WHERE UPPER(timezone) LIKE ?', (f"%{fus_orar.upper()}%",))
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/tarile-care-vorbesc', methods=['GET'])
def countries_by_language():
    limba = request.args.get('limba')
    if not limba:
        return jsonify({"error": "The parameter 'limba' is required"}), 400
    cursor.execute('SELECT name FROM countries WHERE UPPER(languages) LIKE ?', (f"%{limba.upper()}%",))
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/tarile-cu-sistem-politic', methods=['GET'])
def countries_by_regime():
    sistem_politic = request.args.get('sistem_politic')
    if not sistem_politic:
        return jsonify({"error": "The parameter 'sistem_politic' is required"}), 400
    cursor.execute('SELECT name FROM countries WHERE UPPER(regime) LIKE ?', (f"%{sistem_politic.upper()}%",))
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/tarile-vecine-pentru', methods=['GET'])
def country_neighbors():
    tara = request.args.get('tara')
    if not tara:
        return jsonify({"error": "The parameter 'tara' is required"}), 400
    cursor.execute('SELECT neighbors FROM countries WHERE UPPER(name) = ?', (tara.upper(),))
    results = cursor.fetchall()
    return jsonify(results)


@app.route('/capitala-tarii', methods=['GET'])
def country_capital():
    tara = request.args.get('tara')
    if not tara:
        return jsonify({"error": "The parameter 'tara' is required"}), 400
    cursor.execute('SELECT capital FROM countries WHERE UPPER(name) = ?', (tara.upper(),))
    results = cursor.fetchall()
    return jsonify(results)

if __name__ == '__main__':
    app.run()