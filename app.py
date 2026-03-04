from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = 'records.db'

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/records')
def records():
    with sqlite3.connect(DB) as con:
        scores = con.execute(
            'SELECT name, score, date FROM records ORDER BY score DESC LIMIT 10'
        ).fetchall()
    return render_template('records.html', scores=scores)

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    name = data.get('name', 'Anonymous')
    score = data.get('score', 0)
    with sqlite3.connect(DB) as con:
        con.execute('INSERT INTO records (name, score) VALUES (?, ?)', (name, score))
    return jsonify({'status': 'ok'})

@app.route('/check_record')
def check_record():
    score = request.args.get('score', 0, type=int)
    with sqlite3.connect(DB) as con:
        top = con.execute(
            'SELECT score FROM records ORDER BY score DESC LIMIT 1'
        ).fetchone()
    is_record = top is None or score > top[0]
    return jsonify({'is_record': is_record})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)