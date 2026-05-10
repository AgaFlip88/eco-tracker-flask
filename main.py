from flask import Flask, render_template, request
import sqlite3
import os
import sys

# --- CONFIGURAZIONE PERCORSI PER PYINSTALLER ---

def resource_path(relative_path):
    """ Ottiene il percorso assoluto delle risorse, funziona sia in locale che nell'exe """
    try:
        # PyInstaller crea una cartella temporanea in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Il database deve stare nella cartella dell'eseguibile per poter salvare i dati
if getattr(sys, 'frozen', False):
    # Se il programma è un EXE
    base_dir = os.path.dirname(sys.executable)
else:
    # Se il programma è un normale script .py
    base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, 'risultati.db')

# --- INIZIALIZZAZIONE DATABASE ---

def init_db():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risposte (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        messaggi INTEGER,
        chiamate INTEGER,
        streaming INTEGER,
        social INTEGER,
        gaming INTEGER,
        cloud INTEGER,
        dispositivo INTEGER,
        risultato_finale REAL
    )
    ''')
    connection.commit()
    connection.close()

init_db()
print(f"Database pronto in: {db_path}")

# Configurazione Flask con i percorsi corretti
app = Flask(__name__, 
            template_folder=resource_path('templates'),
            static_folder=resource_path('static'))

# --- FUNZIONI DI SUPPORTO ---

def result_calculate(q1, q2, q3, q4, q5, q6, q7):
    """Calcola l'impronta di CO2"""
    coef = {
        'msg': 1.0, 'call': 2.5, 'stream': 3.0, 
        'social': 2.2, 'game': 1.8, 'cloud': 1.2
    }
    totale = (q1 * coef['msg']) + (q2 * coef['call']) + (q3 * coef['stream']) + \
             (q4 * coef['social']) + (q5 * coef['game']) + (q6 * coef['cloud']) + q7
    return totale

def get_db_media(colonna):
    """Recupera la media dal database"""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT AVG({colonna}) FROM risposte")
        res = cur.fetchone()[0]
        conn.close()
        return round(res, 1) if res is not None else 0
    except Exception as e:
        print(f"Errore media: {e}")
        return 0

# --- ROTTE DEL SITO ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<q1>')
def calls(q1):
    m = get_db_media('messaggi')
    return render_template('calls.html', previous_data=q1, media=m)

@app.route('/<q1>/<q2>')
def streaming(q1, q2):
    m = get_db_media('chiamate')
    return render_template('streaming.html', previous_data=f"{q1}/{q2}", media=m)

@app.route('/<q1>/<q2>/<q3>')
def social(q1, q2, q3):
    m = get_db_media('streaming')
    return render_template('social.html', previous_data=f"{q1}/{q2}/{q3}", media=m)

@app.route('/<q1>/<q2>/<q3>/<q4>')
def gaming(q1, q2, q3, q4):
    m = get_db_media('social')
    return render_template('gaming.html', previous_data=f"{q1}/{q2}/{q3}/{q4}", media=m)

@app.route('/<q1>/<q2>/<q3>/<q4>/<q5>')
def cloud(q1, q2, q3, q4, q5):
    m = get_db_media('gaming')
    return render_template('cloud.html', previous_data=f"{q1}/{q2}/{q3}/{q4}/{q5}", media=m)

@app.route('/<q1>/<q2>/<q3>/<q4>/<q5>/<q6>')
def device(q1, q2, q3, q4, q5, q6):
    m = get_db_media('cloud')
    return render_template('device.html', previous_data=f"{q1}/{q2}/{q3}/{q4}/{q5}/{q6}", media=m)

@app.route('/<q1>/<q2>/<q3>/<q4>/<q5>/<q6>/<q7>')
def cinema(q1, q2, q3, q4, q5, q6, q7):
    return render_template('cinema.html', previous_data=f"{q1}/{q2}/{q3}/{q4}/{q5}/{q6}/{q7}")

@app.route('/<q1>/<q2>/<q3>/<q4>/<q5>/<q6>/<q7>/<q8>')
def pre_end(q1, q2, q3, q4, q5, q6, q7, q8):
    return render_template('pre_end.html', previous_data=f"{q1}/{q2}/{q3}/{q4}/{q5}/{q6}/{q7}/{q8}")

@app.route('/<q1>/<q2>/<q3>/<q4>/<q5>/<q6>/<q7>/<q8>/<q9>')
def end(q1, q2, q3, q4, q5, q6, q7, q8, q9):
    risultato = result_calculate(int(q1), int(q2), int(q3), int(q4), int(q5), int(q6), int(q7))
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('''INSERT INTO risposte 
                       (messaggi, chiamate, streaming, social, gaming, cloud, dispositivo, risultato_finale) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (int(q1), int(q2), int(q3), int(q4), int(q5), int(q6), int(q7), risultato))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Errore salvataggio DB: {e}")

    media_globale = get_db_media('risultato_finale')
    return render_template('end.html', result=round(risultato, 2), media_globale=media_globale)

if __name__ == "__main__":
    # debug=False è essenziale per PyInstaller
    app.run(host='127.0.0.1', port=5000, debug=False)