from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id TEXT PRIMARY KEY,
            device_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Check if the visitorId exists in the database
@app.route('/check_visitor/<visitor_id>')
def check_visitor(visitor_id):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('SELECT device_name FROM visitors WHERE visitor_id = ?', (visitor_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({'exists': True, 'device_name': result[0]})
    else:
        return jsonify({'exists': False})

# Save the device name if the visitorId does not exist
@app.route('/save_device', methods=['POST'])
def save_device():
    visitor_id = request.form['visitorId']
    device_name = request.form['deviceName']

    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('INSERT INTO visitors (visitor_id, device_name) VALUES (?, ?)', (visitor_id, device_name))
    conn.commit()
    conn.close()

    return redirect(url_for('check_visitor', visitor_id=visitor_id))

# Serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True, host='0.0.0.0', port=5000)
