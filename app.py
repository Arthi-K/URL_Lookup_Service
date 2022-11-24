import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_url(url_addr):
    conn = get_db_connection()
    mal_url = conn.execute('SELECT * FROM url_table WHERE url_addr = ?',
                        (url_addr,)).fetchone()
    conn.close()
    if mal_url is None:
        abort(404)
    return mal_url 


@app.route('/')
def index():
    conn = get_db_connection()
    url_table = conn.execute('SELECT * FROM url_table').fetchall()
    conn.close()
    return render_template('index.html', url_table=url_table)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        url_addr = request.form['title']
        content = request.form['content']

        if not url_addr:
            flash('Malware URL is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO url_table (url_addr, content) VALUES (?, ?)',
                         (url_addr, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# ...

@app.route('/<string:url_addr>/edit/', methods=('GET', 'POST'))
def edit(url_addr):
    url_addr = get_url(url_addr)

    if request.method == 'POST':
        mal_url = request.form['title']
        content = request.form['content']

        if not mal_url:
            flash('URL is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE url_table SET content = ?'
                         ' WHERE url_addr = ?',
                         (content,url_addr))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', url_addr=url_addr)


if __name__ == "__main__":
    app.run(debug=True)