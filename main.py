from flask import Flask, render_template, url_for, request
import sqlite3

app = Flask(__name__)

# HOME PAGE
@app.route("/material_entry", methods = ['POST'])
def material_entry():
    name_entry = request.form.get("material_name")
    weight_entry = int(request.form.get("material_weight"))
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("UPDATE processing SET weight = weight + ? WHERE Name = ?", (weight_entry, name_entry))
    conn.commit()
    return render_template('home.html')
    

# ______________________________________________________________________________________________________________

# PROCESSING PAGE

@app.route("/process_entry", methods = ['POST'])
def process_entry():
    name_entry = request.form.get("material_name")
    weight_entry = int(request.form.get("material_weight"))
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("UPDATE processing SET weight = weight - ? WHERE Name = ?", (weight_entry, name_entry))
    conn.commit()
    cur.execute("UPDATE plating SET weight = weight + ? WHERE Name = ?", (weight_entry, name_entry))
    conn.commit()

    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS Number FROM processing WHERE NOT weight = 0.0")
    rows=cur.fetchall()

    return render_template('processing.html', rows=rows)


# ______________________________________________________________________________________________________________

# PLATING PAGE

@app.route("/plating_entry", methods = ['POST'])
def plating_entry():
    name_entry = request.form.get("material_name")
    weight_entry = int(request.form.get("material_weight"))
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("UPDATE plating SET weight = weight - ? WHERE Name = ?", (weight_entry, name_entry))
    conn.commit()
    cur.execute("UPDATE topack SET weight = weight + ? WHERE Name = ?", (weight_entry, name_entry))
    conn.commit()

    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS Number FROM plating WHERE NOT weight = 0.0")
    rows=cur.fetchall()

    return render_template('plating.html', rows=rows)

# ______________________________________________________________________________________________________________

# TOPACK PAGE
def mat_dictionary():
    mylist=[(1,'Material 1',0.035,0,0), (2,'Material 2',0.021,0,0), (3,'Material 3',0.013,0,0), (4,'Material 4',0.035,0,0), (5,'Material 5',0.065,0,0), (6,'Material 6',0.036,0,0), (7,'Material 7',0.05,0,0), (8,'Material 8',0.024,0,0), (9,'Material 9',0.017,0,0), (10,'Material 10',0.035,0,0), (11,'Material 11',0.006,0,0), (12,'Material 12',0.012,0,0), (13,'Material 13',0.017,0,0), (14,'Material 14',0.005,0,0), (15,'Material 15',0.0044,0,0), (16,'Material 16',0.057,0,0), (17,'Material 17',0.007,0,0), (18,'Material 18',0.24,0,0), (19,'Material 19',0.0237,0,0), (20,'Material 20',0.18,0,0), (21,'Material 21',0.095,0,0), (22,'Material 22',0.09,0,0),(23,'Material 23',0.058,0,0), (24,'Material 24',0.02,0,0), (25,'Material 25',0.087,0,0), (26,'Material 26',0.058,0,0), (27,'Material 27',0.098,0,0), (28,'Material 28',0.042,0,0), (29,'Material 29',0.021,0,0), (30,'Material 30',0.021,0,0), (31,'Material 31',0.122,0,0)]
    list1 = []
    list2 = []
    for i in mylist:
        list1.append(i[1])
        list2.append(i[2])
    d={}
    for key in list1: 
        for value in list2: 
            d[key] = value 
            list2.remove(value) 
            break  
    return d


@app.route("/topack_entry", methods = ['POST'])
def topack_entry():
    name_entry = request.form.get("material_name")
    weight_entry = float(request.form.get("material_weight"))

    b = mat_dictionary()
    wei = b[name_entry]
    wei1 = round(wei * weight_entry)

    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("UPDATE topack SET weight = weight - ? WHERE Name = ?", (wei1, name_entry))
    conn.commit()

    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS quantity FROM topack WHERE NOT weight = 0.0")
    rows=cur.fetchall()

    return render_template('topack.html', rows=rows)




@app.route("/")
def layout():
    return render_template('layout.html')


@app.route("/home")
def home():
    return render_template('home.html')



# PROCESSING TABLE SQL 
# SHOW PROCESSING TABLE
@app.route("/processing")
def processing():

    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS Number FROM processing WHERE NOT weight = 0.0")
    rows=cur.fetchall()

    return render_template('processing.html', rows=rows)


# SHOW PLATING TABLE
@app.route("/plating")
def plating():
    
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS Number FROM plating WHERE NOT weight = 0.0")
    rows=cur.fetchall()
    return render_template('plating.html', rows=rows)

# SHOW TOPACK TABLE

@app.route("/topack")
def ready():
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("SELECT id, Name, weight, ROUND(weight/wt) AS quantity FROM topack WHERE NOT weight = 0.0")
    rows=cur.fetchall()
    return render_template('topack.html', rows=rows)

# SHOW TOTAL TABLE

@app.route("/total")
def total():
    conn=sqlite3.connect('material.db')
    cur=conn.cursor()
    cur.execute("SELECT Name, SUM(weight), ROUND(SUM(weight/wt)) FROM (SELECT * FROM processing UNION ALL SELECT * FROM plating UNION ALL SELECT * FROM topack) where not weight = 0.0 GROUP BY Name ")
    rows=cur.fetchall()
    return render_template('total.html', rows=rows)




if __name__ == '__main__':
    app.run(debug=True)


