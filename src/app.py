import re
import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Flask, render_template
from flask import jsonify
from flask.logging import create_logger
from flask_caching import Cache
template_dir = os.path.abspath('../templates/')
config = {
    "DEBUG": True,          
    "CACHE_TYPE": "null",  
    "CACHE_DEFAULT_TIMEOUT": 3600
}

app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'your secret key'
app.config.from_mapping(config)
cache = Cache(app)
logging = create_logger(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    logging.info("Connected Successfully to SQLite DB")
    return conn

def validate_url(url):
    regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    logging.info("Checking if the URL is Malformed")
    return re.match(regex, url) is not None

@app.route('/v1/urlinfo/<path:url_addr>')
@cache.cached(timeout=3600)
def get_url(url_addr):
    if url_addr[-1] == '/': url_addr = url_addr[:-1]
    if not validate_url(url_addr):
        return jsonify({
            "message": "Bad Request Error, check the URL",
            "safe": False
        }), 400
    conn = get_db_connection()
    mal_url = conn.execute('SELECT * FROM url_table WHERE url_addr = ?',
                     (url_addr,)).fetchone()
    conn.close()
    if mal_url is None:
        return jsonify({
            "message": "Access Allowed, NOT a Malware URL",
            "safe": True
        }), 200
    return jsonify({
            "message": "Error: Malware URL",
            "safe": False
        }), 403

@app.route('/')
@cache.cached(timeout=3600)
def index():
    conn = get_db_connection()
    url_table = conn.execute('SELECT * FROM url_table').fetchall()
    conn.close()
    return render_template('index.html', url_table=url_table)

@app.route('/delete/<path:url_addr>', methods = ('GET', ))
def deleteUrl(url_addr):
    conn = get_db_connection()
    conn.execute('DELETE FROM url_table WHERE url_addr = ?',
                     (url_addr,))
    logging.info("Deleted successfully from the DB")
    conn.commit()
    conn.close()
    
    return jsonify({
            "message": "Deleted",
        }), 200

@app.route('/create/', methods=('GET', 'POST'))
@cache.cached(timeout=3600)
def create():
    if request.method == 'POST':
        url_addr = request.form['title']
        content = request.form['content']
        # if url_addr[-1] == '/': url_addr = url_addr[:-1]
        if not url_addr:
            logging.error("Malware URL needs to be provided")
            flash('Malware URL is required!')
        elif not content:
            logging.error("Content needs to be provided")
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO url_table (url_addr, content) VALUES (?, ?)',
                         (url_addr, content))
            logging.info("Inserted data successfully into the DB")
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)