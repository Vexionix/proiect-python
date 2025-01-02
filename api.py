import sqlite3
from flask import Flask, jsonify, request

conn = sqlite3.connect('states_of_the_world.db', check_same_thread=False)
cursor = conn.cursor()

# Setup Flask application for API
app = Flask(__name__)


@app.route('/top-10-tari-populatie', methods=['GET'])
def top_10_population():
    """
    :return: JSON with top 10 countries with the highest population
    """
    cursor.execute(
        'SELECT name, population FROM countries '
        'ORDER BY population DESC LIMIT 10')
    results = cursor.fetchall()
    formatted_results = [
        {"name": row[0], "population": row[1]}
        for row in results]
    return jsonify(formatted_results)


@app.route('/top-10-tari-densitate', methods=['GET'])
def top_10_density():
    """
    :return: JSON with top 10 countries with the highest density
    """
    cursor.execute(
        'SELECT name, density FROM countries '
        'ORDER BY density DESC LIMIT 10')
    results = cursor.fetchall()
    formatted_results = [{"name": row[0], "people per km² (density)": row[1]}
                         for row in results]
    return jsonify(formatted_results)


@app.route('/top-10-tari-suprafata', methods=['GET'])
def top_10_area():
    """
    :return: JSON with top 10 countries with the highest area
    """
    cursor.execute(
        'SELECT name, area FROM countries ORDER BY area DESC LIMIT 10')
    results = cursor.fetchall()
    formatted_results = [{"name": row[0], "area (km²)": row[1]}
                         for row in results]
    return jsonify(formatted_results)


@app.route('/tarile-cu-fus-orar', methods=['GET'])
def countries_by_timezone():
    """
    This route requires an argument named "fus_orar" which represents
    the timezone to be searched.
    :return: 200 OK with JSON with the countries that have the given
    timezone if the argument is given, otherwise 400 BAD REQUEST and
    a descriptive message
    """
    fus_orar = request.args.get('fus_orar')
    if not fus_orar:
        return jsonify({"error": "The parameter 'fus_orar' is required"}), 400
    cursor.execute(
        'SELECT name FROM countries '
        'WHERE UPPER(timezone) LIKE ?', (f"%{fus_orar.upper()}%",))
    results = cursor.fetchall()
    formatted_results = [{"name": row[0]} for row in results]
    return jsonify(formatted_results)


@app.route('/tarile-care-vorbesc', methods=['GET'])
def countries_by_language():
    """
    This route requires an argument named "limba" which represents
    the language that has to be spoken by the searched countries.
    :return: 200 OK with JSON with the countries that speak the given
    language if the argument is given, otherwise 400 BAD REQUEST and
    a descriptive message
    """
    limba = request.args.get('limba')
    if not limba:
        return jsonify({"error": "The parameter 'limba' is required"}), 400
    cursor.execute(
        'SELECT name FROM countries '
        'WHERE UPPER(languages) LIKE ?', (f"%{limba.upper()}%",))
    results = cursor.fetchall()
    formatted_results = [{"name": row[0]} for row in results]
    return jsonify(formatted_results)


@app.route('/tarile-cu-sistem-politic', methods=['GET'])
def countries_by_regime():
    """
    This route requires an argument named "sistem_politic" which represents
    the regime that the searched countries follow.
    :return: 200 OK with JSON with the countries that have the given
    regime if the argument is given, otherwise 400 BAD REQUEST and
    a descriptive message
    """
    sistem_politic = request.args.get('sistem_politic')
    if not sistem_politic:
        return jsonify({
            "error": "The parameter 'sistem_politic' is required"}), 400
    cursor.execute(
        'SELECT name FROM countries WHERE UPPER(regime)'
        ' LIKE ?', (f"%{sistem_politic.upper()}%",))
    results = cursor.fetchall()
    formatted_results = [{"name": row[0]} for row in results]
    return jsonify(formatted_results)


@app.route('/tarile-vecine-pentru', methods=['GET'])
def country_neighbors():
    """
    This route requires an argument named "tara" which represents
    the name of the country the neighbors will be returned for.
    :return: 200 OK with JSON with the neighbors of the given country
    if the name argument is given, otherwise 400 BAD REQUEST and
    a descriptive message
    """
    tara = request.args.get('tara')
    if not tara:
        return jsonify({"error": "The parameter 'tara' is required"}), 400
    cursor.execute(
        'SELECT neighbors FROM countries '
        'WHERE UPPER(name) = ?', (tara.upper(),))
    results = cursor.fetchall()
    formatted_results = [{"neighbors": row[0]} for row in results]
    return jsonify(formatted_results)


@app.route('/capitala-tarii', methods=['GET'])
def country_capital():
    """
    This route requires an argument named "tara" which represents
    the name of the country the capital will be returned for.
    :return: 200 OK with JSON with the capital of the given country
    if the name argument is given, otherwise 400 BAD REQUEST and
    a descriptive message
    """
    tara = request.args.get('tara')
    if not tara:
        return jsonify({"error": "The parameter 'tara' is required"}), 400
    cursor.execute(
        'SELECT capital FROM countries '
        'WHERE UPPER(name) = ?', (tara.upper(),))
    results = cursor.fetchall()
    formatted_results = [{"capital": row[0]} for row in results]
    return jsonify(formatted_results)


if __name__ == '__main__':
    app.run()
