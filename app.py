import streamlit as st
import random
import pandas as pd

# 1. INSERISCI QUI IL TUO LINK DI GOOGLE FOGLI
# Ricorda: deve finire con /export?format=csv
URL_FOGLIO = "IL_TUO_LINK_QUI"

# Configurazione della pagina
st.set_page_config(page_title="ITALO! Quiz online", page_icon="🇮🇹")

st.title("ITALO! Quiz online")
st.write("Gli esercizi per le nostre lezioni.")

# Funzione per caricare i dati dal foglio
@st.cache_data(ttl=60) # Aggiorna i dati ogni 60 secondi
def carica_esercizi(url):
    try:
        df = pd.read_csv(url)
        return df.to_dict('records')
    except Exception as e:
        st.error("Errore nel caricamento del foglio. Controlla il link!")
        return []

esercizi = carica_esercizi(URL_FOGLIO)

# Inizializzazione delle variabili di sessione
if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'punteggio' not in st.session_state:
    st.session_state.punteggio = 0
if 'totali' not in st.session_state:
    st.session_state.totali = 0

if esercizi:
    # Mostra il punteggio
    st.metric(label="Punteggio Corretto", value=f"{st.session_state.punteggio} su {st.session_state.totali}")

    # Selezione esercizio
    es = esercizi[st.session_state.indice]
    st.subheader(f"Categoria: {es['tipo']}")
    st.info(es['domanda'])

    # Input studente
    risposta_utente = st.text_input("Scrivi la tua risposta qui:").strip().lower()

    if st.button("Verifica"):
        st.session_state.totali += 1
        if risposta_utente == str(es['risposta']).lower():
            st.session_state.punteggio += 1
            st.success("Corretto! Bravissimo/a! 🎉")
        else:
            st.error(f"Sbagliato. La risposta corretta era: **{es['risposta']}**")

    # Bottoni di controllo
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Prossimo esercizio ➡️"):
            st.session_state.indice = random.randint(0, len(esercizi) - 1)
            st.rerun()
    with col2:
        if st.button("Reset Punteggio 🔄"):
            st.session_state.punteggio = 0
            st.session_state.totali = 0
            st.rerun()
else:
    st.warning("Aggiungi degli esercizi al tuo Foglio Google per iniziare!")

st.sidebar.header("Informazioni")
st.sidebar.write("App didattica collegata a Google Sheets.")
