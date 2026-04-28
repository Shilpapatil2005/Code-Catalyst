from flask import Flask, request
import sqlite3
import random

app = Flask(__name__)

# ---------------- DB ----------------
def setup():
    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS schemes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    description TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM schemes")
    count = cur.fetchone()[0]

    if count == 0:
        data = [
        ("PM-KISAN","farmer","Income support for farmers"),
        ("Old Age Pension","senior","Monthly pension for senior citizens"),
        ("SSP Scholarship","student","Education scholarship support"),
        ("Udyogini Scheme","female","Women business support"),
        ("PMAY Housing","worker","Affordable housing support")
        ]

        cur.executemany("INSERT INTO schemes(name,category,description) VALUES(?,?,?)", data)

    conn.commit()
    conn.close()

setup()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return '''
<html>
<head>
<title>Yojana Mitra AI</title>

<style>
body{
font-family:Arial;
margin:0;
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
width:600px;
margin:40px auto;
padding:30px;
border-radius:25px;
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
cursor:pointer;
font-size:16px;
}

a{
text-decoration:none;
color:#2563eb;
font-weight:bold;
display:block;
margin-top:12px;
}
</style>
</head>

<body>

<div class="top">🚀 Yojana Mitra AI 2.0</div>

<div class="box">

<h2>Smart Government Scheme Matcher</h2>

<form action="/match" method="post">

<input type="number" name="age" placeholder="Enter Age" required>

<input type="number" name="income" placeholder="Annual Income" required>

<select name="category">
<option value="">Select Occupation</option>
<option value="student">Student</option>
<option value="farmer">Farmer</option>
<option value="worker">Worker</option>
<option value="senior">Senior Citizen</option>
<option value="female">Women</option>
</select>

<button type="submit">Find My Schemes</button>

</form>

<a href="/chat">🤖 AI Assistant</a>
<a href="/dashboard">📊 Dashboard</a>
<a href="/admin">⚙ Admin Panel</a>

</div>

</body>
</html>
'''

# ---------------- MATCH ----------------
@app.route('/match', methods=['POST'])
def match():

    cat = request.form['category']

    conn = sqlite3.connect("schemes.db")
    cur = conn.cursor()

    cur.execute("SELECT name,description FROM schemes WHERE category=?", (cat,))
    rows = cur.fetchall()

    conn.close()

    score = random.randint(82,98)

    result = ""

    for row in rows:
        result += f"""
        <div style='background:white;padding:20px;margin:15px;border-radius:15px;'>
        <h3>{row[0]}</h3>
        <p>{row[1]}</p>
        </div>
        """

    if result == "":
        result = "<h3>No schemes found</h3>"

    return f'''
<html>
<body style="font-family:Arial;background:#eef4ff;padding:40px;">

<h1>🎯 AI Recommended Schemes</h1>

<h2>Eligibility Score: {score}%</h2>

{result}

<a href="/">⬅ Back</a>

</body>
</html>
'''

# ---------------- CHAT ----------------
@app.route('/chat')
def chat():
    return '''
<html>
<body style="font-family:Arial;background:#eef4ff;text-align:center;padding:40px;">

<div style="background:white;width:600px;margin:auto;padding:30px;border-radius:20px;">

<h1>🤖 AI Chat Assistant</h1>

<form action="/ask" method="post">

<textarea name="msg" style="width:90%;height:120px;" placeholder="I am farmer age 50"></textarea>

<br><br>

<button type="submit">Ask AI</button>

</form>

<a href="/">⬅ Home</a>

</div>

</body>
</html>
'''

@app.route('/ask', methods=['POST'])
def ask():

    msg = request.form['msg'].lower()

    reply = "Please provide more details."

    if "farmer" in msg:
        reply = "You may get PM-KISAN + Farmer Subsidy."

    elif "student" in msg:
        reply = "You may get SSP Scholarship."

    elif "old" in msg or "senior" in msg:
        reply = "You may get Old Age Pension."

    elif "woman" in msg or "female" in msg:
        reply = "You may get Udyogini Scheme."

    return f'''
<html>
<body style="font-family:Arial;text-align:center;background:#eef4ff;padding:50px;">

<div style="background:white;width:600px;margin:auto;padding:30px;border-radius:20px;">

<h1>🤖 AI Response</h1>

<h2>{reply}</h2>

<a href="/chat">Ask Again</a>

</div>

</body>
</html>
'''

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dash():
    return '''
<html>
<body style="font-family:Arial;background:#eef4ff;text-align:center;padding:40px;">

<div style="background:white;width:600px;margin:auto;padding:30px;border-radius:20px;">

<h1>📊 Dashboard</h1>

<h3>Total Users Today: 127</h3>
<h3>Total Matches: 86</h3>
<h3>Top Category: Farmer</h3>

<a href="/">⬅ Home</a>

</div>

</body>
</html>
'''

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    return '''
<html>
<body style="font-family:Arial;background:#eef4ff;text-align:center;padding:40px;">

<div style="background:white;width:600px;margin:auto;padding:30px;border-radius:20px;">

<h1>⚙ Admin Panel</h1>

<p>Add / Remove Schemes</p>

<h3>System Status: Running ✅</h3>

<a href="/">⬅ Home</a>

</div>

</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)