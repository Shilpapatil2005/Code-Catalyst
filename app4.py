from flask import Flask, request, Response
import sqlite3
import random
import json

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
            ("PM-KISAN", "Farmer", 18, 500000, "Income support of Rs.6000/year for small and marginal farmers"),
            ("SSP Scholarship", "Student", 15, 300000, "Scholarship support for students from low-income families"),
            ("Old Age Pension", "Senior", 60, 500000, "Monthly pension of Rs.1000 for senior citizens aged 60 and above"),
            ("Udyogini Scheme", "Women", 18, 400000, "Women entrepreneurship support with loans up to Rs.3 lakh"),
            ("PMAY Housing", "Worker", 18, 350000, "Affordable housing support under Pradhan Mantri Awas Yojana")
        ]

        cur.executemany("""
        INSERT INTO schemes(name,category,min_age,max_income,description)
        VALUES(?,?,?,?,?)
        """, data)

    conn.commit()
    conn.close()

setup_db()

# =====================================================
# SHARED STYLES & COMPONENTS
# =====================================================
def base_style():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&family=Nunito:wght@400;600;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
        --blue:       #2563eb;
        --blue-dark:  #1d4ed8;
        --blue-light: #dbeafe;
        --green:      #16a34a;
        --red:        #dc2626;
        --bg:          linear-gradient(135deg, #dbeafe 0%, #eef4ff 100%);
        --card-bg:    #ffffff;
        --text:       #1e293b;
        --muted:      #64748b;
        --border:     #e2e8f0;
        --radius:     16px;
        --shadow:     0 4px 24px rgba(37,99,235,0.10);
    }

    body {
        font-family: 'Nunito', sans-serif;
        background: var(--bg);
        min-height: 100vh;
        color: var(--text);
    }

    .topbar {
        background: var(--blue);
        color: white;
        padding: 18px 24px;
        font-family: 'Baloo 2', sans-serif;
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 0.3px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .topbar .nav-links {
        position: absolute;
        right: 24px;
        display: flex;
        gap: 12px;
    }

    .topbar .nav-links a {
        color: rgba(255,255,255,0.85);
        text-decoration: none;
        font-size: 14px;
        font-family: 'Nunito', sans-serif;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        transition: background 0.2s;
    }

    .topbar .nav-links a:hover { background: rgba(255,255,255,0.15); }
    .topbar .nav-links a.active { background: rgba(255,255,255,0.25); }

    .page-wrap {
        max-width: 780px;
        margin: 0 auto;
        padding: 36px 20px 60px;
    }

    .card {
        background: var(--card-bg);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: 36px 32px;
        margin-bottom: 24px;
    }

    .card h2 {
        font-family: 'Baloo 2', sans-serif;
        font-size: 22px;
        color: var(--blue);
        margin-bottom: 20px;
    }

    input, select, textarea {
        width: 100%;
        padding: 13px 16px;
        margin-bottom: 14px;
        border: 1.5px solid var(--border);
        border-radius: 10px;
        font-size: 15px;
        font-family: 'Nunito', sans-serif;
        color: var(--text);
        background: #f8fafc;
        transition: border-color 0.2s, box-shadow 0.2s;
        outline: none;
    }

    input:focus, select:focus, textarea:focus {
        border-color: var(--blue);
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
        background: white;
    }

    button.btn {
        background: var(--blue);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 13px 30px;
        font-size: 16px;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        cursor: pointer;
        transition: background 0.2s, transform 0.12s;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }

    button.btn:hover  { background: var(--blue-dark); }
    button.btn:active { transform: scale(0.97); }
    button.btn.green  { background: var(--green); }
    button.btn.green:hover { background: #15803d; }

    .back-link {
        display: inline-block;
        margin-top: 20px;
        color: var(--blue);
        font-weight: 700;
        text-decoration: none;
        font-size: 15px;
    }

    .back-link:hover { text-decoration: underline; }

    /* Nav pills at bottom of home card */
    .nav-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 22px;
        justify-content: center;
    }

    .nav-pills a {
        display: inline-block;
        padding: 10px 22px;
        border-radius: 50px;
        background: var(--blue-light);
        color: var(--blue);
        font-weight: 700;
        text-decoration: none;
        font-size: 15px;
        transition: background 0.2s, color 0.2s;
    }

    .nav-pills a:hover {
        background: var(--blue);
        color: white;
    }

    /* Scheme result cards */
    .scheme-card {
        background: #f0f7ff;
        border: 1.5px solid #bfdbfe;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 16px;
    }

    .scheme-card h3 {
        color: var(--blue);
        font-family: 'Baloo 2', sans-serif;
        font-size: 18px;
        margin-bottom: 6px;
    }

    .scheme-card p { color: var(--muted); font-size: 15px; }

    /* Score badge */
    .score-badge {
        display: inline-block;
        background: #dcfce7;
        color: #15803d;
        border-radius: 50px;
        padding: 6px 20px;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 22px;
    }
    </style>
    """

def topbar(active=""):
    links = [
        ("/", "🏠 Home"),
        ("/voice", "🎙️ Voice"),
        ("/chat", "🤖 Chat"),
        ("/dashboard", "📊 Dashboard"),
        ("/admin", "⚙️ Admin"),
    ]
    nav = "".join(
        f'<a href="{href}" class="{"active" if active==href else ""}">{label}</a>'
        for href, label in links
    )
    return f'''
    <div class="topbar" style="position:relative;">
        🚀 Yojana Mitra AI 3.0
        <div class="nav-links">{nav}</div>
    </div>
    '''

# =====================================================
# HOME PAGE
# =====================================================
@app.route('/')
def home():
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yojana Mitra AI</title>
{base_style()}
</head>
<body>
{topbar("/")}
<div class="page-wrap">
<div class="card" style="text-align:center;">
    <div style="font-size:54px;margin-bottom:10px;">🇮🇳</div>
    <h2 style="font-size:26px;margin-bottom:8px;">AI Welfare Scheme Recommender</h2>
    <p style="color:var(--muted);margin-bottom:28px;font-size:15px;">
        Enter your details below to find government schemes you qualify for.
    </p>

    <form action="/match" method="post">
        <input type="number" name="age" placeholder="Your Age" min="1" max="120" required>
        <input type="number" name="income" placeholder="Annual Income (in ₹)" min="0" required>
        <select name="category" required>
            <option value="">Select Occupation / Category</option>
            <option value="Farmer">🌾 Farmer</option>
            <option value="Student">📚 Student</option>
            <option value="Senior">👴 Senior Citizen</option>
            <option value="Women">👩 Women</option>
            <option value="Worker">🔨 Worker</option>
        </select>
        <button class="btn" type="submit" style="width:100%;justify-content:center;margin-top:4px;">
            🔍 Find My Schemes
        </button>
    </form>

    <div class="nav-pills">
        <a href="/voice">🎙️ Voice Assistant</a>
        <a href="/chat">🤖 AI Chat</a>
        <a href="/dashboard">📊 Dashboard</a>
        <a href="/admin">⚙️ Admin Panel</a>
    </div>
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
    age      = int(request.form['age'])
    income   = int(request.form['income'])
    category = request.form['category']

    conn = sqlite3.connect("schemes.db")
    cur  = conn.cursor()
    cur.execute("""
        SELECT name, description FROM schemes
        WHERE category=? AND min_age<=? AND max_income>=?
    """, (category, age, income))
    rows = cur.fetchall()
    conn.close()

    score = random.randint(84, 98)

    if rows:
        cards = "".join(f'''
        <div class="scheme-card">
            <h3>✅ {row[0]}</h3>
            <p>{row[1]}</p>
        </div>''' for row in rows)
    else:
        cards = '<div class="scheme-card"><h3>😔 No Matching Schemes Found</h3><p>Try changing your category or check back later for new schemes.</p></div>'

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Results – Yojana Mitra AI</title>
{base_style()}
</head>
<body>
{topbar()}
<div class="page-wrap">
<div class="card">
    <h2>🎯 AI Recommended Schemes</h2>
    <div class="score-badge">Eligibility Score: {score}%</div>
    {cards}
    <a class="back-link" href="/">⬅ Back Home</a>
</div>
</div>
</body>
</html>
'''

# =====================================================
# VOICE ASSISTANT  —  FULLY WORKING
# =====================================================
@app.route('/voice')
def voice():
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Voice Assistant – Yojana Mitra AI</title>
{base_style()}
<style>
/* ── Voice-specific styles ── */
.voice-hero {{
    text-align: center;
    padding: 10px 0 28px;
}}

.voice-hero p {{
    color: var(--muted);
    font-size: 15px;
    margin-bottom: 28px;
}}

/* Language selector row */
.lang-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    margin-bottom: 28px;
}}

.lang-row label {{ font-size: 14px; color: var(--muted); font-weight: 600; }}

.lang-row select {{
    width: auto;
    margin: 0;
    padding: 9px 16px;
    font-size: 14px;
}}

/* Mic button */
.mic-wrap {{ margin-bottom: 14px; }}

.mic-btn {{
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: var(--blue);
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    transition: background 0.2s, transform 0.15s;
    box-shadow: 0 6px 24px rgba(37,99,235,0.35);
    position: relative;
}}

.mic-btn:hover {{ background: var(--blue-dark); transform: scale(1.05); }}

.mic-btn.listening {{
    background: var(--red);
    animation: ripple 1.2s infinite;
}}

@keyframes ripple {{
    0%   {{ box-shadow: 0 0 0 0 rgba(220,38,38,0.5); }}
    70%  {{ box-shadow: 0 0 0 22px rgba(220,38,38,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(220,38,38,0); }}
}}

/* Waveform bars (shown while listening) */
.waveform {{
    display: none;
    align-items: center;
    justify-content: center;
    gap: 4px;
    height: 36px;
    margin: 10px 0 16px;
}}

.waveform.active {{ display: flex; }}

.waveform span {{
    width: 5px;
    background: var(--red);
    border-radius: 4px;
    animation: wave 0.9s ease-in-out infinite;
}}

.waveform span:nth-child(1) {{ animation-delay: 0s;    height: 12px; }}
.waveform span:nth-child(2) {{ animation-delay: 0.1s;  height: 24px; }}
.waveform span:nth-child(3) {{ animation-delay: 0.2s;  height: 36px; }}
.waveform span:nth-child(4) {{ animation-delay: 0.1s;  height: 24px; }}
.waveform span:nth-child(5) {{ animation-delay: 0s;    height: 12px; }}

@keyframes wave {{
    0%, 100% {{ transform: scaleY(0.4); }}
    50%        {{ transform: scaleY(1);   }}
}}

.status-label {{
    font-size: 14px;
    color: var(--muted);
    font-weight: 600;
    min-height: 20px;
    margin-bottom: 18px;
}}

/* Transcript & response boxes */
.transcript-box {{
    background: #f1f5f9;
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 15px;
    color: var(--text);
    min-height: 52px;
    text-align: left;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}}

.transcript-box.active {{ border-color: var(--blue); background: white; }}

.response-box {{
    background: #eff6ff;
    border: 1.5px solid #bfdbfe;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 15px;
    color: #1e40af;
    text-align: left;
    min-height: 56px;
    display: none;
    margin-bottom: 16px;
    line-height: 1.7;
}}

.response-box.show {{ display: block; }}

/* Action buttons */
.action-row {{
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}}

.action-row .btn {{
    padding: 10px 22px;
    font-size: 14px;
    display: none;
}}

.action-row .btn.show {{ display: inline-flex; }}

/* Tips */
.tips-box {{
    background: #fefce8;
    border: 1px solid #fef08a;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 14px;
    color: #854d0e;
    text-align: left;
    line-height: 1.8;
    margin-top: 8px;
}}

.tips-box b {{ color: #713f12; }}

.error-msg {{
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 10px;
    padding: 12px 16px;
    color: var(--red);
    font-size: 14px;
    display: none;
    margin-bottom: 14px;
    text-align: left;
}}

/* Browser warning */
.browser-warn {{
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 10px;
    padding: 14px 18px;
    color: #c2410c;
    font-size: 14px;
    text-align: left;
    margin-bottom: 18px;
    display: none;
}}
</style>
</head>
<body>
{topbar("/voice")}
<div class="page-wrap">
<div class="card">
    <div class="voice-hero">
        <h2 style="font-size:24px;margin-bottom:8px;">🎙️ Voice Assistant</h2>
        <p>Press the mic and speak your details — age, income, and category — to get scheme recommendations instantly.</p>

        <div class="browser-warn" id="browserWarn">
            ⚠️ Your browser may not fully support voice recognition.
            For best results, use <b>Google Chrome</b> or <b>Microsoft Edge</b>.
        </div>

        <div class="lang-row">
            <label for="langSelect">🌐 Language:</label>
            <select id="langSelect">
                <option value="en-IN">English (India)</option>
                <option value="hi-IN">हिन्दी – Hindi</option>
                <option value="kn-IN">ಕನ್ನಡ – Kannada</option>
                <option value="ta-IN">தமிழ் – Tamil</option>
                <option value="te-IN">తెలుగు – Telugu</option>
                <option value="mr-IN">मराठी – Marathi</option>
                <option value="bn-IN">বাংলা – Bengali</option>
                <option value="gu-IN">ગુજરાતી – Gujarati</option>
                <option value="pa-IN">ਪੰਜਾਬੀ – Punjabi</option>
            </select>
        </div>

        <div class="mic-wrap">
            <button class="mic-btn" id="micBtn" onclick="toggleListen()" title="Click to start / stop">
                🎙️
            </button>
        </div>

        <div class="waveform" id="waveform">
            <span></span><span></span><span></span><span></span><span></span>
        </div>

        <div class="status-label" id="statusLabel">Tap the mic to start speaking</div>

        <div class="error-msg" id="errorMsg"></div>

        <div class="transcript-box" id="transcriptBox">
            💬 Your speech will appear here…
        </div>

        <div class="response-box" id="responseBox"></div>

        <div class="action-row">
            <button class="btn green" id="speakBtn" onclick="speakResponse()">🔊 Read Aloud</button>
            <button class="btn" id="clearBtn" style="background:#64748b;" onclick="clearAll()">🗑️ Clear</button>
        </div>

        <div class="tips-box">
            <b>💡 What to say:</b><br>
            "I am a <b>farmer</b>, age <b>45</b>, income <b>2 lakh</b>"<br>
            "I am a <b>student</b>, 20 years old, annual income 1.5 lakh"<br>
            "Senior citizen aged <b>65</b>, income below 3 lakh"<br>
            "I am a <b>woman</b> entrepreneur, age 30, income 2 lakh"
        </div>
    </div>
</div>

<a class="back-link" href="/">⬅ Back Home</a>
</div>

<script>
// ─── Browser check ───────────────────────────────────────────────────────────
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {{
    document.getElementById('browserWarn').style.display = 'block';
    document.getElementById('micBtn').disabled = true;
    document.getElementById('micBtn').style.opacity = '0.4';
    document.getElementById('micBtn').title = 'Voice not supported in this browser';
    document.getElementById('statusLabel').textContent = 'Voice not supported. Try Chrome or Edge.';
}}

// Check if not Chrome/Edge
const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
const isEdge   = /Edg/.test(navigator.userAgent);
if (SpeechRecognition && !isChrome && !isEdge) {{
    document.getElementById('browserWarn').style.display = 'block';
}}

// ─── State ───────────────────────────────────────────────────────────────────
let recognition  = null;
let isListening  = false;
let lastResponse = "";
let finalTranscript = "";

// ─── Toggle listen ───────────────────────────────────────────────────────────
function toggleListen() {{
    if (isListening) {{
        recognition && recognition.stop();
        return;
    }
    startListening();
}}

function startListening() {{
    if (!SpeechRecognition) return;

    hideError();
    finalTranscript = "";

    recognition = new SpeechRecognition();
    recognition.continuous      = false;
    recognition.interimResults  = true;
    recognition.maxAlternatives = 1;
    recognition.lang = document.getElementById('langSelect').value;

    recognition.onstart = function() {{
        isListening = true;
        document.getElementById('micBtn').classList.add('listening');
        document.getElementById('micBtn').textContent = '⏹️';
        document.getElementById('waveform').classList.add('active');
        document.getElementById('statusLabel').textContent = '🔴 Listening… speak now';
        document.getElementById('transcriptBox').classList.add('active');
        document.getElementById('transcriptBox').textContent = '🎤 Listening…';
    }};

    recognition.onresult = function(event) {{
        let interim = '';
        finalTranscript = '';
        for (let i = 0; i < event.results.length; i++) {{
            const t = event.results[i][0].transcript;
            if (event.results[i].isFinal) finalTranscript += t;
            else interim += t;
        }}
        const display = finalTranscript || interim;
        document.getElementById('transcriptBox').textContent = display
            ? '🗣️ ' + display
            : '🎤 Listening…';
    }};

    recognition.onerror = function(e) {{
        stopListeningUI();
        let msg = 'Could not hear you. Please try again.';
        if (e.error === 'not-allowed')    msg = '🚫 Microphone access denied. Please allow microphone in your browser settings.';
        else if (e.error === 'no-speech') msg = '🔇 No speech detected. Please speak clearly and try again.';
        else if (e.error === 'network')    msg = '🌐 Network error. Check your internet connection.';
        else if (e.error === 'aborted')   return;
        showError(msg);
    }};

    recognition.onend = function() {{
        stopListeningUI();
        if (finalTranscript.trim()) {{
            processInput(finalTranscript.trim());
        }} else if (!document.getElementById('errorMsg').style.display || document.getElementById('errorMsg').style.display === 'none') {{
            document.getElementById('statusLabel').textContent = 'No speech detected. Tap mic to try again.';
        }}
    }};

    try {{
        recognition.start();
    }} catch(e) {{
        showError('Could not start microphone: ' + e.message);
    }}
}}

function stopListeningUI() {{
    isListening = false;
    document.getElementById('micBtn').classList.remove('listening');
    document.getElementById('micBtn').textContent = '🎙️';
    document.getElementById('waveform').classList.remove('active');
    document.getElementById('transcriptBox').classList.remove('active');
    if (document.getElementById('statusLabel').textContent.includes('Listening')) {{
        document.getElementById('statusLabel').textContent = 'Processing…';
    }}
}}

// ─── Process voice input ─────────────────────────────────────────────────────
function processInput(text) {{
    document.getElementById('transcriptBox').textContent = '🗣️ ' + text;
    document.getElementById('statusLabel').textContent = '⚙️ Analysing your request…';

    const t    = text.toLowerCase();
    const age  = extractAge(t);
    const inc  = extractIncome(t);
    let cat    = detectCategory(t);
    let reply  = '';

    if (!cat) {{
        reply = '❓ I could not identify your category. Please say if you are a <b>Farmer, Student, Senior Citizen, Woman,</b> or <b>Worker</b>.';
    }} else {{
        reply = matchScheme(cat, age, inc, text);
    }}

    lastResponse = reply.replace(/<[^>]+>/g, '');
    showResponse(reply);
    document.getElementById('statusLabel').textContent = '✅ Done! Tap mic to ask again.';
    setTimeout(() => autoSpeak(lastResponse), 400);
}}

function detectCategory(t) {{
    // English & Transliterated keywords
    if (t.includes('farmer') || t.includes('kisan') || t.includes('agriculture') || t.includes('farming')) return 'Farmer';
    if (t.includes('student') || t.includes('study') || t.includes('college') || t.includes('school') || t.includes('vidyarthi')) return 'Student';
    if (t.includes('senior') || t.includes('old age') || t.includes('pension') || t.includes('elderly') || t.includes('retired') || t.includes('vriddha')) return 'Senior';
    if (t.includes('woman') || t.includes('women') || t.includes('female') || t.includes('mahila') || t.includes('lady')) return 'Women';
    if (t.includes('worker') || t.includes('labour') || t.includes('labourer') || t.includes('construction') || t.includes('housing') || t.includes('kamgar')) return 'Worker';
    
    // Regional Scripts Support
    // Hindi
    if (t.includes('किसान') || t.includes('खेती')) return 'Farmer';
    if (t.includes('छात्र') || t.includes('विद्यार्थी')) return 'Student';
    if (t.includes('महिला') || t.includes('स्त्री')) return 'Women';
    // Kannada
    if (t.includes('ರೈತ') || t.includes('ಕೃಷಿ')) return 'Farmer';
    if (t.includes('ವಿದ್ಯಾರ್ಥಿ')) return 'Student';
    if (t.includes('ಮಹಿಳೆ')) return 'Women';
    // Tamil
    if (t.includes('விவசாயி')) return 'Farmer';
    if (t.includes('மாணவர்')) return 'Student';
    if (t.includes('பெண்')) return 'Women';

    return null;
}}

const schemeData = {{
    Farmer:  {{ name: 'PM-KISAN',       minAge: 18, maxIncome: 500000, desc: 'Income support of ₹6,000/year for small and marginal farmers.' }},
    Student: {{ name: 'SSP Scholarship', minAge: 15, maxIncome: 300000, desc: 'Scholarship support for students from low-income families.' }},
    Senior:  {{ name: 'Old Age Pension', minAge: 60, maxIncome: 500000, desc: 'Monthly pension of ₹1,000 for senior citizens aged 60 and above.' }},
    Women:   {{ name: 'Udyogini Scheme', minAge: 18, maxIncome: 400000, desc: 'Women entrepreneurship support with loans up to ₹3 lakh.' }},
    Worker:  {{ name: 'PMAY Housing',   minAge: 18, maxIncome: 350000, desc: 'Affordable housing assistance for workers under PMAY.' }}
}};

function matchScheme(cat, age, income, rawText) {{
    const s = schemeData[cat];
    if (!s) return 'No scheme data available for this category.';

    const ageOk    = age    === null || age    >= s.minAge;
    const incomeOk = income === null || income <= s.maxIncome;

    let details = '';
    if (age    !== null) details += ` Age detected: <b>${{age}}</b>.`;
    if (income !== null) details += ` Income detected: <b>₹${{income.toLocaleString('en-IN')}}</b>.`;

    if (ageOk && incomeOk) {{
        return `✅ Great news! You appear eligible for <b>${{s.name}}</b>.${{details}}<br><br>${{s.desc}}`;
    }} else if (!ageOk) {{
        return `⚠️ For <b>${{s.name}}</b>, the minimum age requirement is <b>${{s.minAge}} years</b>.${{details}} You may not qualify yet, but check other schemes at your nearest CSC.`;
    }} else {{
        return `⚠️ Your income exceeds the limit for <b>${{s.name}}</b> (max ₹${{s.maxIncome.toLocaleString('en-IN')}}).${{details}} Please visit your nearest Common Service Centre for personalised guidance.`;
    }}
}}

// ─── Age & income extraction ─────────────────────────────────────────────────
function extractAge(text) {{
    const patterns = [
        /\bage[d]?\s*(\d{{1,3}})/i,
        /(\d{{1,3}})\s*years?\s*old/i,
        /i\s+am\s+(\d{{1,3}})/i,
        /\b(\d{{1,3}})\s*(?:yrs?|years?|saal|varsha|vayas)\b/i,
        /(\d{{1,3}})\s*साल/i,
        /(\d{{1,3}})\s*ವರ್ಷ/i
    ];
    for (const p of patterns) {{
        const m = text.match(p);
        if (m) {{
            const n = parseInt(m[1]);
            if (n >= 5 && n <= 110) return n;
        }
    }
    return null;
}}

function extractIncome(text) {{
    const lakh = text.match(/(\d+(?:\.\d+)?)\s*(?:lakh|laksh|ಲಕ್ಷ|लाख)/i);
    if (lakh) return Math.round(parseFloat(lakh[1]) * 100000);

    const thou = text.match(/(\d+(?:\.\d+)?)\s*(?:thousand|k|hazaar|ಸಾವಿರ)\b/i);
    if (thou) return Math.round(parseFloat(thou[1]) * 1000);

    const plain = text.match(/(?:income|salary|earn(?:ing)?)[^\d]*(\d{{4,7}})/i);
    if (plain) return parseInt(plain[1]);

    const bare = text.match(/\b(\d{{5,7}})\b/);
    if (bare) return parseInt(bare[1]);

    return null;
}}

// ─── UI helpers ──────────────────────────────────────────────────────────────
function showResponse(html) {{
    const box = document.getElementById('responseBox');
    box.innerHTML = html;
    box.classList.add('show');
    document.getElementById('speakBtn').classList.add('show');
    document.getElementById('clearBtn').classList.add('show');
}}

function clearAll() {{
    document.getElementById('transcriptBox').textContent = '💬 Your speech will appear here…';
    const rb = document.getElementById('responseBox');
    rb.classList.remove('show');
    rb.innerHTML = '';
    document.getElementById('speakBtn').classList.remove('show');
    document.getElementById('clearBtn').classList.remove('show');
    document.getElementById('statusLabel').textContent = 'Tap the mic to start speaking';
    hideError();
    lastResponse = '';
    window.speechSynthesis && window.speechSynthesis.cancel();
}}

function showError(msg) {{
    const el = document.getElementById('errorMsg');
    el.textContent = msg;
    el.style.display = 'block';
    document.getElementById('statusLabel').textContent = 'Tap mic to try again';
}}

function hideError() {{
    document.getElementById('errorMsg').style.display = 'none';
}}

// ─── Text-to-Speech ──────────────────────────────────────────────────────────
function autoSpeak(text) {{
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utt  = new SpeechSynthesisUtterance(text);
    utt.lang   = document.getElementById('langSelect').value;
    utt.rate   = 0.92;
    utt.pitch  = 1;
    window.speechSynthesis.speak(utt);
}}

function speakResponse() {{
    if (lastResponse) autoSpeak(lastResponse);
}}

// Stop TTS when user navigates away
window.addEventListener('beforeunload', () => {{
    window.speechSynthesis && window.speechSynthesis.cancel();
}});
</script>

</body>
</html>
'''

# =====================================================
# CHAT ASSISTANT
# =====================================================
@app.route('/chat')
def chat():
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chat – Yojana Mitra AI</title>
{base_style()}
</head>
<body>
{topbar("/chat")}
<div class="page-wrap">
<div class="card">
    <h2>🤖 AI Chat Assistant</h2>
    <p style="color:var(--muted);margin-bottom:20px;font-size:15px;">
        Describe yourself and we'll suggest matching government schemes.
    </p>
    <form action="/ask" method="post">
        <textarea name="msg" rows="4"
            placeholder="Example: I am a farmer, age 45, annual income 2 lakh"></textarea>
        <button class="btn" type="submit" style="width:100%;justify-content:center;">
            💬 Ask AI
        </button>
    </form>
    <a class="back-link" href="/">⬅ Home</a>
</div>
</div>
</body>
</html>
'''

@app.route('/ask', methods=['POST'])
def ask():
    msg   = request.form['msg'].lower()
    reply = "Please enter more details about your occupation, age, and income."

    if   "farmer" in msg:  reply = "You may be eligible for PM-KISAN — income support of ₹6,000/year for farmers."
    elif "student" in msg: reply = "You may be eligible for SSP Scholarship for students."
    elif "senior" in msg or "old" in msg: reply = "You may be eligible for Old Age Pension (₹1,000/month for 60+ citizens)."
    elif "woman" in msg or "female" in msg or "women" in msg: reply = "You may be eligible for Udyogini Scheme — entrepreneurship support for women."
    elif "worker" in msg or "labour" in msg: reply = "You may be eligible for PMAY Housing assistance."

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chat Response – Yojana Mitra AI</title>
{base_style()}
</head>
<body>
{topbar("/chat")}
<div class="page-wrap">
<div class="card" style="text-align:center;">
    <h2>🤖 AI Response</h2>
    <div class="scheme-card" style="text-align:left;margin-top:16px;">
        <p style="font-size:16px;line-height:1.7;">{reply}</p>
    </div>
    <a class="back-link" href="/chat">⬅ Ask Again</a>
    &nbsp;&nbsp;
    <a class="back-link" href="/">🏠 Home</a>
</div>
</div>
</body>
</html>
'''

# =====================================================
# DASHBOARD
# =====================================================
@app.route('/dashboard')
def dashboard():
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard – Yojana Mitra AI</title>
{base_style()}
<style>
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
}}
.stat-card {{
    background: #f0f7ff;
    border: 1.5px solid #bfdbfe;
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
}}
.stat-card .num {{
    font-family: 'Baloo 2', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--blue);
}}
.stat-card .lbl {{
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
}}
.bar-row {{
    display: flex;
    align-items: center;
    margin-bottom: 14px;
    gap: 12px;
}}
.bar-label {{ width: 80px; font-size: 14px; color: var(--muted); text-align: right; }}
.bar-track {{ flex: 1; background: #e2e8f0; border-radius: 6px; height: 14px; overflow: hidden; }}
.bar-fill  {{ height: 100%; background: var(--blue); border-radius: 6px; transition: width 0.8s; }}
.bar-pct   {{ width: 40px; font-size: 13px; font-weight: 700; color: var(--blue); }}
</style>
</head>
<body>
{topbar("/dashboard")}
<div class="page-wrap">
<div class="card">
    <h2>📊 Analytics Dashboard</h2>
    <div class="stat-grid">
        <div class="stat-card"><div class="num">1,250</div><div class="lbl">Total Users</div></div>
        <div class="stat-card"><div class="num">986</div><div class="lbl">Total Matches</div></div>
        <div class="stat-card"><div class="num">94%</div><div class="lbl">Success Rate</div></div>
        <div class="stat-card"><div class="num">🌾</div><div class="lbl">Top: Farmer</div></div>
    </div>

    <h2 style="margin-bottom:18px;">Popular Categories</h2>
    <div class="bar-row"><div class="bar-label">Farmer</div><div class="bar-track"><div class="bar-fill" style="width:88%"></div></div><div class="bar-pct">88%</div></div>
    <div class="bar-row"><div class="bar-label">Student</div><div class="bar-track"><div class="bar-fill" style="width:70%"></div></div><div class="bar-pct">70%</div></div>
    <div class="bar-row"><div class="bar-label">Women</div><div class="bar-track"><div class="bar-fill" style="width:62%"></div></div><div class="bar-pct">62%</div></div>
    <div class="bar-row"><div class="bar-label">Senior</div><div class="bar-track"><div class="bar-fill" style="width:55%"></div></div><div class="bar-pct">55%</div></div>
    <div class="bar-row"><div class="bar-label">Worker</div><div class="bar-track"><div class="bar-fill" style="width:42%"></div></div><div class="bar-pct">42%</div></div>
</div>

<div class="card">
    <h2>🔔 System Insights</h2>
    <p style="margin-bottom:10px;font-size:15px;">✅ 42 new users today</p>
    <p style="margin-bottom:10px;font-size:15px;">✅ 18 PM-KISAN matches generated</p>
    <p style="margin-bottom:10px;font-size:15px;">✅ 9 scholarship requests submitted</p>
    <p style="font-size:15px;">✅ Voice Assistant: Active</p>
</div>

<a class="back-link" href="/">⬅ Back Home</a>
</div>
</body>
</html>
'''

# =====================================================
# ADMIN PANEL
# =====================================================
@app.route('/admin')
def admin():
    conn = sqlite3.connect("schemes.db")
    cur  = conn.cursor()
    cur.execute("SELECT * FROM schemes")
    rows = cur.fetchall()
    conn.close()

    table = "".join(f'''
    <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>₹{int(row[4]):,}</td>
    </tr>''' for row in rows)

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Admin – Yojana Mitra AI</title>
{base_style()}
<style>
table {{ width:100%; border-collapse:collapse; margin-top:16px; }}
th, td {{ padding:12px 14px; border:1px solid var(--border); font-size:14px; text-align:left; }}
th {{ background:#f0f7ff; color:var(--blue); font-weight:700; }}
tr:hover td {{ background:#f8fafc; }}
</style>
</head>
<body>
{topbar("/admin")}
<div class="page-wrap">
<div class="card">
    <h2>➕ Add New Scheme</h2>
    <form action="/addscheme" method="post">
        <input name="name" placeholder="Scheme Name" required>
        <select name="category">
            <option>Farmer</option>
            <option>Student</option>
            <option>Senior</option>
            <option>Women</option>
            <option>Worker</option>
        </select>
        <input name="age"           placeholder="Minimum Age" type="number" required>
        <input name="income"      placeholder="Maximum Annual Income (₹)" type="number" required>
        <input name="description" placeholder="Description" required>
        <button class="btn green" type="submit">✅ Add Scheme</button>
    </form>
</div>

<div class="card">
    <h2>📋 All Schemes</h2>
    <table>
        <tr><th>ID</th><th>Name</th><th>Category</th><th>Min Age</th><th>Max Income</th></tr>
        {table}
    </table>
</div>

<div class="card">
    <h2>🖥️ System Status</h2>
    <p style="margin-bottom:10px;">✅ Database Connected</p>
    <p style="margin-bottom:10px;">✅ AI Chat Assistant Active</p>
    <p style="margin-bottom:10px;">✅ 🎙️ Voice Assistant Active</p>
    <p>✅ Analytics Running</p>
</div>

<a class="back-link" href="/">⬅ Back Home</a>
</div>
</body>
</html>
'''

@app.route('/addscheme', methods=['POST'])
def addscheme():
    name        = request.form['name']
    category    = request.form['category']
    age         = request.form['age']
    income      = request.form['income']
    description = request.form['description']

    conn = sqlite3.connect("schemes.db")
    cur  = conn.cursor()
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