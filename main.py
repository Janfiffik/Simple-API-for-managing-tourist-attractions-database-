from flask import Flask, request, jsonify, render_template
import sqlite3

PATH = "data/data.db"

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route("/all", methods=["POST", "GET"])
def all_loc():
    connection = sqlite3.connect(PATH)
    db = connection.cursor()
    data = db.execute("""SELECT * from Locations""").fetchall()
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/add", methods=["POST", "GET", "PUT"])
def add_loc():
    try:
        new_loc = request.get_json()
        connection = sqlite3.connect(PATH)
        db = connection.cursor()
        db.execute("""INSERT INTO Locations VALUES (:NAME, :LOC, :REGION, :CITY, :TYPE)""", new_loc)
        connection.commit()
        connection.close()

        connection = sqlite3.connect(PATH)
        db = connection.cursor()
        data = db.execute("""SELECT * from Locations""").fetchall()
        connection.commit()
        connection.close()
        return jsonify(data)

    except sqlite3.IntegrityError:
        connection = sqlite3.connect(PATH)
        db = connection.cursor()
        data = db.execute("""SELECT * from Locations""").fetchall()
        connection.commit()
        connection.close()
        return jsonify(f"Location already exist.{data}")


@app.route("/column_data/<column>", methods=["GET"])
def column_data(column):
    connection = sqlite3.connect(PATH)
    db = connection.cursor()
    data = db.execute(f"""SELECT DISTINCT {column} from Locations """).fetchall()
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/filter_by/column/<column>/name/<name>", methods=["POST", "GET"])
def filter_by(column, name):
    connection = sqlite3.connect(PATH)
    db = connection.cursor()
    data = db.execute(f"""SELECT * from Locations WHERE {column}='{name}'""").fetchall()
    connection.commit()
    connection.close()
    return jsonify(data)


@app.route("/update/<name>", methods=["PATCH"])
def update_data(name):
    update_loc = request.get_json()
    connection = sqlite3.connect(PATH)
    db = connection.cursor()
    data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()

    if not data:
        return jsonify("That name doesn't exist.")

    else:
        try:
            new_name = str(update_loc["NAME"])
        except KeyError:
            new_name = name

        try:
            new_loc = str(update_loc["LOC"])
        except KeyError:
            data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()
            connection.commit()
            new_loc = data[1]

        try:
            new_region = str(update_loc['REGION'])
        except KeyError:
            data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()
            connection.commit()
            new_region = data[2]

        try:
            new_city = str(update_loc['CITY'])
        except KeyError:
            data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()
            connection.commit()
            new_city = data[3]
        try:
            new_type = str(update_loc['TYPE'])
        except KeyError:
            data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()
            connection.commit()
            new_type = data[1]

        db.execute("""UPDATE {} SET NAME=?, LOC=?, REGION=?, CITY=?, TYPE=? WHERE NAME = ?""".format("Locations"),
                   (new_name, new_loc, new_region, new_city, new_type, name)
                   )

        connection.commit()
        connection.close()
        return jsonify("Data was updated")


@app.route("/remove_attraction/<name>", methods=["GET", "DELETE"])
def delete_attraction(name):
    connection = sqlite3.connect(PATH)
    db = connection.cursor()
    data = db.execute(f"""SELECT * from Locations WHERE NAME='{name}'""").fetchone()
    connection.commit()
    connection.close()
    if not data:
        return jsonify("Attraction is not in database.")
    else:
        connection = sqlite3.connect(PATH)
        db = connection.cursor()
        db.execute(f"""delete from Locations WHERE NAME='{name}'""")
        connection.commit()
        connection.close()
        return jsonify("Attraction was removed.")


@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")


@app.route("/doc", methods=["POST", "GET"])
def documentation():
    return render_template("documentation.html")

if __name__ == "__main__":
    app.run(debug=True)
