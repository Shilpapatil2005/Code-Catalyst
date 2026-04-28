from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return """
<html>
<head>
<title>Yojana Mitra AI</title>

<style>
body{
font-family:Arial;
background:linear-gradient(135deg,#dbeafe,#eff6ff);
text-align:center;
padding:40px;
margin:0;
}

.box{
background:white;
width:520px;
margin:auto;
padding:30px;
border-radius:20px;
box-shadow:0 0 15px rgba(0,0,0,0.2);
}

h1{
color:#2563eb;
margin-bottom:10px;
}

p{
color:#555;
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
</style>

</head>

<body>

<div class="box">

<h1>Yojana Mitra AI</h1>
<p>AI Based Government Scheme Matcher - Karnataka</p>

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

</div>

</body>
</html>
"""

@app.route('/match', methods=['POST'])
def match():

    age = int(request.form['age'])
    income = int(request.form['income'])
    gender = request.form['gender']
    occupation = request.form['occupation']

    cards = ""

    if occupation == "student":
        cards += """
        <div class='card'>
        🎓 <b>SSP Scholarship Karnataka</b><br>
        Helps students with tuition and education support.
        </div>
        """

    if occupation == "farmer":
        cards += """
        <div class='card'>
        🌾 <b>PM-KISAN Scheme</b><br>
        Financial support for eligible farmers.
        </div>
        """

    if occupation == "worker":
        cards += """
        <div class='card'>
        💼 <b>Skill India Program</b><br>
        Skill training and employment support.
        </div>
        """

    if age >= 60:
        cards += """
        <div class='card'>
        👴 <b>Old Age Pension</b><br>
        Monthly support for senior citizens.
        </div>
        """

    if gender == "female":
        cards += """
        <div class='card'>
        👩 <b>Udyogini Scheme</b><br>
        Support for women entrepreneurs.
        </div>
        """

    if income < 250000:
        cards += """
        <div class='card'>
        🏠 <b>PMAY Housing Scheme</b><br>
        Affordable housing support for low-income families.
        </div>
        """

    if cards == "":
        cards = "<p>No matching schemes found.</p>"

    return f"""
<html>
<head>
<title>Results</title>

<style>
body{{
font-family:Arial;
background:linear-gradient(135deg,#dbeafe,#eff6ff);
text-align:center;
padding:40px;
margin:0;
}}

.box{{
background:white;
width:650px;
margin:auto;
padding:30px;
border-radius:20px;
box-shadow:0 0 15px rgba(0,0,0,0.2);
}}

h1{{
color:#2563eb;
}}

.card{{
background:#f8fafc;
padding:15px;
margin:12px;
border-radius:12px;
text-align:left;
border-left:6px solid #2563eb;
font-size:18px;
}}

a{{
text-decoration:none;
background:#2563eb;
color:white;
padding:10px 20px;
border-radius:8px;
display:inline-block;
margin-top:15px;
}}
</style>

</head>

<body>

<div class="box">

<h1>🤖 AI Recommended Schemes</h1>

<p>Based on your profile, these schemes may help you:</p>

{cards}

<a href="/">Go Back</a>

</div>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)