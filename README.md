# Impronta Digitale

**Impronta Digitale** è un'applicazione web interattiva realizzata con **Python** e **Flask** che permette agli utenti di calcolare l'impatto ambientale (espresso in grammi di CO2) derivante dalle loro abitudini digitali quotidiane.

## Funzionamento
Il sito guida l'utente attraverso una serie di domande relative a:
* **Messaggistica**: Invio di messaggi e audio.
* **Chiamate**: Durata delle chiamate e videochiamate.
* **Streaming**: Utilizzo di piattaforme streaming.
* **Social Media**: Tempo trascorso sui social.
* **Gaming**: Sessioni di gaming online.
* **Cloud**: Utilizzo di servizi di archiviazione.
* **Hardware**: Tipologia di dispositivo principale utilizzato.

Al termine del test, l'applicazione calcola il risultato totale e lo confronta con la media globale degli altri utenti registrati nel database.

## Stack Tecnologico
* **Backend**: Python 3.x con framework Flask.
* **Database**: SQLite per il salvataggio dei risultati e il calcolo delle medie.
* **Frontend**: HTML5 e CSS3 (utilizzando Jinja2 per i template dinamici).

## Struttura del Progetto
* `main.py`: Il cuore dell'applicazione. Gestisce le rotte, il calcolo dell'impronta di CO2 tramite coefficienti specifici e l'integrazione con il database.
* `templates/`: Contiene i file HTML per le domande e la pagina dei risultati.
* `static/css/`: Contiene i fogli di stile per il design.
* `risultati.db`: Database SQLite che memorizza le risposte anonime per generare statistiche in tempo reale.

## Installazione e Avvio
1. Opzione Rapida (Consigliata per Windows)
   Se sei su Windows, non serve installare nulla:
   * Vai nei 'Tag' e scarica: 'Main.py' e 'risultati.db'
   * Assicurati che il file risultati.db sia nella stessa cartella di main.exe.
   * Fai doppio clic su main.exe.
   * premi CTRL e tasto destro su: http://127.0.0.1:5000.
Altrimenti continua a leggere:

1. Preparazione dell'ambiente

Si consiglia l'uso di Visual Studio Code come editor di codice. Assicurati di aver installato l'estensione ufficiale di Python.

2.  **Installa Flask**:
    ```bash
    pip install flask
    ```

(Nota: sqlite3 non richiede installazione in quanto incluso in Python )

3.  **Avvia l'applicazione**:
    ```bash
    python main.py
    ```
    Il sito sarà accessibile all'indirizzo: `http://127.0.0.1:5000`.


        
## Logica di Calcolo
L'impronta viene calcolata in `main.py` utilizzando i seguenti coefficienti di emissione stimati per categoria:

* **Messaggi**: 1.0g CO2
* **Chiamate**: 2.5g CO2
* **Streaming**: 3.0g CO2
* **Social**: 2.2g CO2
* **Gaming**: 1.8g CO2
* **Cloud**: 1.2g CO2
