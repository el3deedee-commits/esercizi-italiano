import streamlit as st
import random

# Configurazione della pagina
st.set_page_config(page_title="Palestra di Italiano", page_icon="🇮🇹")

st.title("🇮🇹 Benvenuti alla Palestra di Italiano!")
st.write("Esercitati con la grammatica in modo semplice e veloce.")

# Database degli esercizi (puoi ampliarlo quanto vuoi)
esercizi = [
    {"domanda": "Io ___ (mangiare) una mela.", "risposta": "mangio", "tipo": "Presente Indicativo"},
    {"domanda": "Loro ___ (andare) al cinema ieri.", "risposta": "sono andati", "tipo": "Passato Prossimo"},
    {"domanda": "Il contrario di 'alto' è ___.", "risposta": "basso", "tipo": "Vocabolario"},
    {"domanda": "Noi ___ (essere) stanchi dopo la lezione.", "risposta": "eravamo", "tipo": "Imperfetto"}
]

# Inizializzazione dello stato della sessione per mantenere l'esercizio corrente
if 'indice' not in st.session_state:
    st.session_state.indice = random.randint(0, len(esercizi) - 1)
    st.session_state.feedback = ""

# Layout dell'esercizio
es = esercizi[st.session_state.indice]

st.subheader(f"Categoria: {es['tipo']}")
st.info(es['domanda'])

# Input dello studente
risposta_utente = st.text_input("Scrivi la tua risposta qui:").strip().lower()

if st.button("Verifica"):
    if risposta_utente == es['risposta'].lower():
        st.success("Corretto! Bravissimo/a! 🎉")
    else:
        st.error(f"Sbagliato. La risposta corretta era: **{es['risposta']}**")

# Bottone per cambiare esercizio
if st.button("Prossimo esercizio ➡️"):
    st.session_state.indice = random.randint(0, len(esercizi) - 1)
    st.rerun()

st.sidebar.header("Informazioni")

st.sidebar.write("Questa app è stata creata per scopi didattici gratuiti.")
