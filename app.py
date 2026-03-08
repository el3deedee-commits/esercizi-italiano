import streamlit as st
import random
import pandas as pd
import re

# LINK DEL TUO FOGLIO GOOGLE
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/18jIREltozGiHiCnNljLHqRFF-oMnj-hDDJ5yhH3rWDk/export?format=csv"

st.set_page_config(page_title="ITALO! Quiz online", page_icon="🇮🇹")

st.title("ITALO! Quiz online")
st.write("Gli esercizi per le nostre lezioni.")

@st.cache_data(ttl=60)
def carica_esercizi(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error("Errore nel caricamento del foglio!")
        return pd.DataFrame()

df_completo = carica_esercizi(URL_FOGLIO)

if not df_completo.empty:
    st.sidebar.title("📚 Menu Lezioni")
    lista_argomenti = sorted(df_completo['argomento'].unique().tolist())
    scelta_argomento = st.sidebar.selectbox("Scegli cosa studiare:", lista_argomenti)

    # Inizializzazione sessione
    if 'argomento_attivo' not in st.session_state or st.session_state.argomento_attivo != scelta_argomento:
        st.session_state.argomento_attivo = scelta_argomento
        tutte_le_domande = df_completo[df_completo['argomento'] == scelta_argomento].to_dict('records')
        numero_da_estrarre = min(len(tutte_le_domande), 10)
        st.session_state.esercizi_scelti = random.sample(tutte_le_domande, numero_da_estrarre)
        st.session_state.indice = 0
        st.session_state.punteggio = 0
        st.session_state.totali = 0
        st.session_state.risposta_data = False

    st.title(f"Lezione: {scelta_argomento}")
    st.metric(label="Punteggio", value=f"{st.session_state.punteggio} su {st.session_state.totali}")

    if st.session_state.esercizi_scelti:
        es = st.session_state.esercizi_scelti[st.session_state.indice]
        st.info(f"Esercizio {st.session_state.indice + 1} di {len(st.session_state.esercizi_scelti)}")
        
        testo_domanda = es['domanda']
        
        # LOGICA PER CAPIRE SE È MULTIPLA
        match_opzioni = re.search(r'\[(.*?)\]', testo_domanda)
        
        if match_opzioni:
            # Domanda a risposta multipla
            domanda_pulita = testo_domanda.split('[')[0].strip()
            opzioni = [opt.strip() for opt in match_opzioni.group(1).split(',')]
            st.subheader(domanda_pulita)
            
            scelta = st.radio("Seleziona la risposta corretta:", opzioni, index=None, key=f"radio_{st.session_state.indice}")
            
            if st.button("Verifica Risposta") and scelta:
                st.session_state.totali += 1
                if scelta.lower() == str(es['risposta']).lower():
                    st.success("Corretto! 🎉")
                    st.session_state.punteggio += 1
                else:
                    st.error(f"Sbagliato. La risposta corretta era: {es['risposta']}")
        else:
            # Domanda aperta
            st.subheader(testo_domanda)
            risposta_utente = st.text_input("Scrivi la risposta:", key=f"input_{st.session_state.indice}").strip().lower()
            
            if st.button("Verifica Risposta"):
                st.session_state.totali += 1
                if risposta_utente == str(es['risposta']).lower():
                    st.success("Corretto! 🎉")
                    st.session_state.punteggio += 1
                else:
                    st.error(f"Sbagliato. Era: {es['risposta']}")

        # Navigazione
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Prossimo ➡️"):
                if st.session_state.indice < len(st.session_state.esercizi_scelti) - 1:
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.balloons()
                    st.success("Ottimo lavoro! Hai completato la lezione.")
        with col2:
            if st.button("Reset / Mischia 🔄"):
                st.session_state.argomento_attivo = None
                st.rerun()
