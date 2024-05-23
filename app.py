import sqlite3
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField

app = Flask(__name__)
app.debug = True
app.secret_key = 'tak_TOE_CRAZYYY!!'

db_cesta = "D:/Software+programko/WA/flask_poznamky/data.db"

class PoznamkaForm(FlaskForm):
    ''' Vytvoří formulář pro vložení poznámky '''
    text_poznamky = TextAreaField()


@app.route('/')
def zobraz_poznamky():
    ''' Zobrazí všechny poznámky uživatele '''
    con = sqlite3.connect(db_cesta)
    cur = con.cursor()
    cur.execute("SELECT rowid, telo, vlozeno FROM poznamky")
    poznamky = cur.fetchall()
    con.close()
    return render_template('index.html', poznamky=poznamky)


@app.route('/nova', methods=['GET', 'POST'])
def nova_poznamka():
    ''' Vytvoří novou poznámku '''
    form = PoznamkaForm()
    text_poznamky = form.text_poznamky.data
    if form.validate_on_submit():
        con = sqlite3.connect(db_cesta)
        cur = con.cursor()
        cur.execute("INSERT INTO poznamky(telo) VALUES(?)", (text_poznamky,))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('nova.html', form=form)


@app.route('/upravit/<int:id_poznamky>', methods=['GET','POST'])
def upravit_poznamku(id_poznamky):
    ''' Upraví existující poznámku '''
    con = sqlite3.connect(db_cesta)
    cur = con.cursor()
    cur.execute("SELECT telo FROM poznamky WHERE rowid = ?", (id_poznamky,))
    existujici_text = cur.fetchone()[0]
    con.close()
    form = PoznamkaForm(text_poznamky=existujici_text)
    if form.validate_on_submit():
        text_poznamky = form.text_poznamky.data
        con = sqlite3.connect(db_cesta)
        cur = con.cursor()
        cur.execute("UPDATE poznamky SET telo = ? WHERE rowid = ?", (text_poznamky, id_poznamky))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('nova.html', form=form)


@app.route('/smazat/<int:id_poznamky>')
def smazat_poznamku(id_poznamky):
    ''' Smaže existujcí poznámku '''
    con = sqlite3.connect(db_cesta)
    cur = con.cursor()
    cur.execute("DELETE FROM poznamky WHERE rowid = ?", (id_poznamky,))
    con.commit()
    con.close()
    return redirect('/')

if __name__ == '__main__':
    app.run()
