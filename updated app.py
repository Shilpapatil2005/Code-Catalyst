from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def create_db():
    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schemes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        gender TEXT,
        min_age INTEGER,
        max_income INTEGER,
        description TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM schemes")
    count = cur.fetchone()[0]

    if count == 0:
        data = [
            ("PM-KISAN", "farmer", "any", 18, 500000, "Income support for farmers"),
            ("Old Age Pension", "senior", "any", 60, 500000, "Monthly pension for senior citizens"),
            ("SSP Scholarship", "student", "any", 17, 300000, "Scholarship support for students"),
            ("Udyogini Scheme", "worker", "female", 18, 500000, "Women entrepreneurship support"),
            ("PMAY Housing", "worker", "any", 18, 250000, "Affordable housing support")
        ]

        cur.executemany("""
        INSERT INTO schemes
        (name,category,gender,min_age,max_income,description)
        VALUES (?,?,?,?,?,?)
        """, data)

    conn.commit()
    conn.close()

create_db()

# ---------------- HOME PAGE ----------------
@app.route('/')
def home():
    return """
<html>
<head>
<title>Yojana Mitra AI</title>

<style>
body{
font-family:Arial;
background:#eef4ff;
margin:0;
padding:0;
}

.top{
background:#2563eb;
color:white;
padding:20px;
text-align:center;
font-size:30px;
font-weight:bold;
}

.box{
background:white;
width:550px;
margin:40px auto;
padding:30px;
border-radius:20px;
box-shadow:0 0 20px rgba(0,0,0,0.15);
text-align:center;
}

input,select{
width:90%;
padding:12px;
margin:10px;
border-radius:10px;
border:1px solid #ccc;
font-size:16px;
}

button{
background:#2563eb;
color:white;
padding:12px 25px;
border:none;
border-radius:10px;
font-size:16px;
cursor:pointer;
}

button:hover{
background:#1d4ed8;
}

a{
text-decoration:none;
color:#2563eb;
font-weight:bold;
}
</style>
</head>

<body>

<div class="top">Yojana Mitra AI</div>

<div class="box">

<h2>Smart Government Scheme Matcher</h2>

<form action="/match" method="post">

<input type="number" name="age" placeholder="Enter Age" required>

<input type="number" name="income" placeholder="Annual Income" required>

<select name="gender" required>
<option value="">Select Gender</option>
<option value="male">Male</option>
<option value="female">Female</option>
</select>

<select name="occupation" required>
<option value="">Select Occupation</option>
<option value="student">Student</option>
<option value="farmer">Farmer</option>
<option value="worker">Worker</option>
<option value="senior">Senior Citizen</option>
</select>

<br><br>

<button type="submit">Find My Schemes</button>

</form>

<br>
<a href="/admin">Open Admin Panel</a>

</div>

</body>
</html>
"""

# ---------------- MATCH ----------------
@app.route('/match', methods=['POST'])
def match():

    age = int(request.form['age'])
    income = int(request.form['income'])
    gender = request.form['gender']
    occupation = request.form['occupation']

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT name,description FROM schemes
    WHERE category=?
    AND min_age<=?
    AND max_income>=?
    AND (gender='any' OR gender=?)
    """, (occupation, age, income, gender))

    rows = cur.fetchall()
    conn.close()

    result = ""

    for row in rows:
        result += f"""
        <div class='card'>
        <h3>{row[0]}</h3>
        <p>{row[1]}</p>
        </div>
        """

    if result == "":
        result = "<h3>No matching schemes found.</h3>"

    return f"""
<html>
<head>
<style>
body{{font-family:Arial;background:#eef4ff;padding:30px;}}
.card{{background:white;padding:20px;margin:15px;border-radius:15px;box-shadow:0 0 10px rgba(0,0,0,0.1);}}
a{{text-decoration:none;color:white;background:#2563eb;padding:10px 18px;border-radius:10px;}}
</style>
</head>

<body>

<h1>AI Recommended Schemes</h1>

{result}

<br><br>
<a href="/">Go Back</a>

</body>
</html>
"""

# ---------------- ADMIN PAGE ----------------
@app.route('/admin')
def admin():

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("SELECT id,name,category FROM schemes")
    rows = cur.fetchall()

    conn.close()

    table_rows = ""

    for row in rows:
        table_rows += f"""
        <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td><a href='/delete/{row[0]}'>Delete</a></td>
        </tr>
        """

    return f"""
<html>
<head>
<style>
body{{
font-family:Arial;
background:#eef4ff;
padding:30px;
text-align:center;
}}

.box{{
background:white;
width:650px;
margin:auto;
padding:30px;
border-radius:20px;
box-shadow:0 0 15px rgba(0,0,0,0.15);
}}

input,select{{
width:90%;
padding:12px;
margin:8px;
border-radius:10px;
border:1px solid #ccc;
}}

button{{
background:#16a34a;
color:white;
padding:12px 20px;
border:none;
border-radius:10px;
cursor:pointer;
}}

table{{
margin:auto;
margin-top:20px;
border-collapse:collapse;
background:white;
}}

th,td{{
padding:10px;
border:1px solid #ccc;
}}
</style>
</head>

<body>

<div class="box">

<h1>Admin Panel</h1>

<form action="/addscheme" method="post">

<input type="text" name="name" placeholder="Scheme Name" required>

<select name="category">
<option value="student">Student</option>
<option value="farmer">Farmer</option>
<option value="worker">Worker</option>
<option value="senior">Senior</option>
</select>

<select name="gender">
<option value="any">Any</option>
<option value="male">Male</option>
<option value="female">Female</option>
</select>

<input type="number" name="age" placeholder="Minimum Age" required>

<input type="number" name="income" placeholder="Maximum Income" required>

<input type="text" name="description" placeholder="Description" required>

<br><br>

<button type="submit">Add Scheme</button>

</form>

<h2>All Schemes</h2>

<table>
<tr>
<th>ID</th>
<th>Name</th>
<th>Category</th>
<th>Action</th>
</tr>

{table_rows}

</table>

<br>
<a href="/">Back Home</a>

</div>

</body>
</html>
"""

# ---------------- ADD SCHEME ----------------
@app.route('/addscheme', methods=['POST'])
def addscheme():

    name = request.form['name']
    category = request.form['category']
    gender = request.form['gender']
    age = int(request.form['age'])
    income = int(request.form['income'])
    description = request.form['description']

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO schemes
    (name,category,gender,min_age,max_income,description)
    VALUES (?,?,?,?,?,?)
    """, (name,category,gender,age,income,description))

    conn.commit()
    conn.close()

    return """
    <h1>Scheme Added Successfully ✅</h1>
    <a href='/admin'>Back to Admin</a>
    """

# ---------------- DELETE SCHEME ----------------
@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM schemes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return """
    <h1>Scheme Deleted Successfully ✅</h1>
    <a href='/admin'>Back to Admin</a>
    """

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)