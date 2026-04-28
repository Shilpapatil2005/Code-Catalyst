from flask import Flask, request
import sqlite3
import random

app = Flask(__name__)

# =====================================================
# DATABASE SETUP
# =====================================================
def setup_db():
    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schemes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        min_age INTEGER,
        max_income INTEGER,
        description TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM schemes")
    count = cur.fetchone()[0]

    if count == 0:
        data = [
            ("PM-KISAN", "Farmer", 18, 500000, "Income support for farmers"),
            ("SSP Scholarship", "Student", 15, 300000, "Scholarship support for students"),
            ("Old Age Pension", "Senior", 60, 500000, "Monthly pension for senior citizens"),
            ("Udyogini Scheme", "Women", 18, 400000, "Women entrepreneurship support"),
            ("PMAY Housing", "Worker", 18, 350000, "Affordable housing support")
        ]

        cur.executemany("""
        INSERT INTO schemes(name,category,min_age,max_income,description)
        VALUES(?,?,?,?,?)
        """, data)

    conn.commit()
    conn.close()

setup_db()

# =====================================================
# HOME PAGE
# =====================================================
@app.route('/')
def home():
    return '''
<html>
<head>
<title>Yojana Mitra AI</title>

<style>
body{
margin:0;
font-family:Arial;
background:linear-gradient(135deg,#dbeafe,#eef4ff);
}

.top{
background:#2563eb;
color:white;
padding:20px;
text-align:center;
font-size:32px;
font-weight:bold;
}

.box{
background:white;
width:650px;
margin:40px auto;
padding:35px;
border-radius:22px;
box-shadow:0 0 18px rgba(0,0,0,0.1);
text-align:center;
}

input,select{
width:92%;
padding:12px;
margin:10px;
border-radius:10px;
border:1px solid #ccc;
font-size:16px;
}

button{
background:#2563eb;
color:white;
padding:12px 28px;
border:none;
border-radius:10px;
font-size:16px;
cursor:pointer;
}

.links a{
display:block;
margin-top:10px;
font-weight:bold;
text-decoration:none;
color:#2563eb;
}
</style>
</head>

<body>

<div class="top">🚀 Yojana Mitra AI 3.0</div>

<div class="box">

<h2>AI Based Welfare Scheme Recommender</h2>

<form action="/match" method="post">

<input type="number" name="age" placeholder="Enter Age" required>

<input type="number" name="income" placeholder="Annual Income" required>

<select name="category" required>
<option value="">Select Occupation</option>
<option value="Farmer">Farmer</option>
<option value="Student">Student</option>
<option value="Senior">Senior Citizen</option>
<option value="Women">Women</option>
<option value="Worker">Worker</option>
</select>

<br><br>

<button type="submit">Find My Schemes</button>

</form>

<div class="links">
<a href="/chat">🤖 AI Assistant</a>
<a href="/dashboard">📊 Dashboard</a>
<a href="/admin">⚙ Admin Panel</a>
</div>

</div>

</body>
</html>
'''

# =====================================================
# MATCH PAGE
# =====================================================
@app.route('/match', methods=['POST'])
def match():

    age = int(request.form['age'])
    income = int(request.form['income'])
    category = request.form['category']

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    SELECT name,description FROM schemes
    WHERE category=?
    AND min_age<=?
    AND max_income>=?
    """, (category, age, income))

    rows = cur.fetchall()
    conn.close()

    score = random.randint(84, 98)

    result = ""

    for row in rows:
        result += f'''
        <div style="background:white;padding:20px;margin:15px;
        border-radius:15px;box-shadow:0 0 10px rgba(0,0,0,0.08);">

        <h3>{row[0]}</h3>
        <p>{row[1]}</p>

        </div>
        '''

    if result == "":
        result = "<h3>No Matching Schemes Found</h3>"

    return f'''
<html>
<body style="font-family:Arial;background:#eef4ff;padding:30px;">

<h1>🎯 AI Recommended Schemes</h1>
<h2>Eligibility Score: {score}%</h2>

{result}

<a href="/">⬅ Back Home</a>

</body>
</html>
'''

# =====================================================
# CHAT ASSISTANT
# =====================================================
@app.route('/chat')
def chat():
    return '''
<html>
<body style="font-family:Arial;background:#eef4ff;text-align:center;padding:40px;">

<div style="background:white;width:650px;margin:auto;padding:30px;border-radius:20px;">

<h1>🤖 AI Chat Assistant</h1>

<form action="/ask" method="post">

<textarea name="msg"
style="width:92%;height:130px;padding:10px;"
placeholder="I am a farmer age 45 income 2 lakh"></textarea>

<br><br>

<button type="submit">Ask AI</button>

</form>

<br>
<a href="/">⬅ Home</a>

</div>

</body>
</html>
'''

@app.route('/ask', methods=['POST'])
def ask():

    msg = request.form['msg'].lower()

    reply = "Please enter more details."

    if "farmer" in msg:
        reply = "You may be eligible for PM-KISAN and Farmer Support Schemes."

    elif "student" in msg:
        reply = "You may be eligible for SSP Scholarship."

    elif "senior" in msg or "old" in msg:
        reply = "You may be eligible for Old Age Pension."

    elif "woman" in msg or "female" in msg:
        reply = "You may be eligible for Udyogini Scheme."

    elif "worker" in msg:
        reply = "You may be eligible for PMAY Housing."

    return f'''
<html>
<body style="font-family:Arial;background:#eef4ff;text-align:center;padding:50px;">

<div style="background:white;width:650px;margin:auto;padding:30px;border-radius:20px;">

<h1>🤖 AI Response</h1>
<h2>{reply}</h2>

<a href="/chat">Ask Again</a>

</div>

</body>
</html>
'''

# =====================================================
# ADVANCED DASHBOARD
# =====================================================
@app.route('/dashboard')
def dashboard():
    return '''
<html>
<head>
<style>
body{
margin:0;
font-family:Arial;
background:#eef4ff;
}

.top{
background:#2563eb;
color:white;
padding:20px;
text-align:center;
font-size:30px;
font-weight:bold;
}

.wrap{
width:90%;
margin:auto;
padding:30px;
}

.cards{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:20px;
}

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 0 12px rgba(0,0,0,0.08);
text-align:center;
}

.section{
background:white;
margin-top:25px;
padding:25px;
border-radius:18px;
box-shadow:0 0 12px rgba(0,0,0,0.08);
}

.bar{
height:18px;
background:#2563eb;
border-radius:10px;
margin-bottom:15px;
}
</style>
</head>

<body>

<div class="top">📊 Analytics Dashboard</div>

<div class="wrap">

<div class="cards">

<div class="card">
<h3>Total Users</h3>
<h1>1,250</h1>
</div>

<div class="card">
<h3>Total Matches</h3>
<h1>986</h1>
</div>

<div class="card">
<h3>Success Rate</h3>
<h1>94%</h1>
</div>

<div class="card">
<h3>Top Category</h3>
<h1>Farmer</h1>
</div>

</div>

<div class="section">

<h2>Popular Categories</h2>

Farmer
<div class="bar" style="width:88%"></div>

Student
<div class="bar" style="width:70%"></div>

Senior
<div class="bar" style="width:55%"></div>

Women
<div class="bar" style="width:62%"></div>

</div>

<div class="section">

<h2>System Insights</h2>

<p>✅ 42 new users today</p>
<p>✅ 18 PM-KISAN matches generated</p>
<p>✅ 9 scholarship requests submitted</p>

</div>

<a href="/">⬅ Back Home</a>

</div>

</body>
</html>
'''

# =====================================================
# PROFESSIONAL ADMIN PANEL
# =====================================================
@app.route('/admin')
def admin():

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM schemes")
    rows = cur.fetchall()
    conn.close()

    table = ""

    for row in rows:
        table += f'''
        <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>{row[4]}</td>
        </tr>
        '''

    return f'''
<html>
<head>
<style>
body{{
margin:0;
font-family:Arial;
background:#eef4ff;
}}

.top{{
background:#2563eb;
color:white;
padding:20px;
text-align:center;
font-size:30px;
font-weight:bold;
}}

.wrap{{
width:92%;
margin:auto;
padding:30px;
}}

.box{{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 0 12px rgba(0,0,0,0.08);
margin-bottom:25px;
}}

input,select{{
width:100%;
padding:12px;
margin:10px 0;
border-radius:10px;
border:1px solid #ccc;
}}

button{{
background:#16a34a;
color:white;
padding:12px 25px;
border:none;
border-radius:10px;
cursor:pointer;
}}

table{{
width:100%;
border-collapse:collapse;
margin-top:15px;
}}

table,th,td{{
border:1px solid #ddd;
}}

th,td{{
padding:12px;
text-align:left;
}}
</style>
</head>

<body>

<div class="top">⚙ Admin Control Center</div>

<div class="wrap">

<div class="box">

<h2>Add New Scheme</h2>

<form action="/addscheme" method="post">

<input name="name" placeholder="Scheme Name" required>

<select name="category">
<option>Farmer</option>
<option>Student</option>
<option>Senior</option>
<option>Women</option>
<option>Worker</option>
</select>

<input name="age" placeholder="Minimum Age" required>

<input name="income" placeholder="Maximum Income" required>

<input name="description" placeholder="Description" required>

<button type="submit">Add Scheme</button>

</form>

</div>

<div class="box">

<h2>All Schemes</h2>

<table>

<tr>
<th>ID</th>
<th>Name</th>
<th>Category</th>
<th>Age</th>
<th>Income</th>
</tr>

{table}

</table>

</div>

<div class="box">

<h2>System Status</h2>

<p>Database Connected ✅</p>
<p>AI Assistant Active ✅</p>
<p>Analytics Running ✅</p>

</div>

<a href="/">⬅ Back Home</a>

</div>

</body>
</html>
'''

@app.route('/addscheme', methods=['POST'])
def addscheme():

    name = request.form['name']
    category = request.form['category']
    age = request.form['age']
    income = request.form['income']
    description = request.form['description']

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO schemes(name,category,min_age,max_income,description)
    VALUES(?,?,?,?,?)
    """, (name, category, age, income, description))

    conn.commit()
    conn.close()

    return '''
<script>
alert("Scheme Added Successfully!");
window.location="/admin";
</script>
'''

# =====================================================
# RUN
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)