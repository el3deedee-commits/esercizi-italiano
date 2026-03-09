import streamlit as st
import random
import pandas as pd
import re

# 1. LINK DEL TUO FOGLIO GOOGLE
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/18jIREltozGiHiCnNljLHqRFF-oMnj-hDDJ5yhH3rWDk/export?format=csv"

st.set_page_config(page_title="ITALO! Quiz online", page_icon="🇮🇹")

# --- 2. FUNZIONE PER LO SFONDO (COLOSSEO) ---
def aggiungi_sfondo(url_immagine):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url_immagine}");
            background-attachment: fixed;
            background-size: cover;
        }}
        /* Il velo bianco (0.85 di opacità) per la leggibilità */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.85); 
            border-radius: 25px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Link immagine Colosseo
aggiungi_sfondo("https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996")

# --- 3. CARICAMENTO DATI (CON PROTEZIONE CELLE VUOTE) ---
@st.cache_data(ttl=60)
def carica_esercizi(url):
    try:
        df = pd.read_csv(url)
        # Rimuove righe dove l'argomento o la domanda sono vuoti
        df = df.dropna(subset=['argomento', 'domanda'])
        return df
    except:
        return pd.DataFrame()

df_completo = carica_esercizi(URL_FOGLIO)

if not df_completo.empty:
    # Menu laterale con protezione per errori di tipo (dropna + astype)
    st.sidebar.title("📚 Menu Lezioni")
    
    # Questo risolve l'errore TypeError: estrae, toglie i vuoti, trasforma in testo e ordina
    lista_argomenti = sorted(df_completo['argomento'].dropna().astype(str).unique().tolist())
    scelta_argomento = st.sidebar.selectbox("Scegli cosa studiare:", lista_argomenti)

    # Logica di selezione casuale delle 10 domande
    if 'argomento_attivo' not in st.session_state or st.session_state.argomento_attivo != scelta_argomento:
        st.session_state.argomento_attivo = scelta_argomento
        tutte_le_domande = df_completo[df_completo['argomento'] == scelta_argomento].to_dict('records')
        numero_da_estrarre = min(len(tutte_le_domande), 10)
        st.session_state.esercizi_scelti = random.sample(tutte_le_domande, numero_da_estrarre)
        st.session_state.indice = 0
        st.session_state.punteggio = 0
        st.session_state.totali = 0

    st.title(f"🏛️ {scelta_argomento}")
    st.metric(label="Punteggio", value=f"{st.session_state.punteggio} su {st.session_state.totali}")

    if st.session_state.esercizi_scelti:
        es = st.session_state.esercizi_scelti[st.session_state.indice]
        st.write(f"**Esercizio {st.session_state.indice + 1} di {len(st.session_state.esercizi_scelti)}**")
        
        testo_domanda = str(es['domanda'])
        match_opzioni = re.search(r'\[(.*?)\]', testo_domanda)
        
        # Gestione Risposta Multipla o Aperta
        if match_opzioni:
            domanda_pulita = testo_domanda.split('[')[0].strip()
            opzioni = [opt.strip() for opt in match_opzioni.group(1).split(',')]
            st.subheader(domanda_pulita)
            scelta = st.radio("Scegli la risposta:", opzioni, index=None, key=f"r_{st.session_state.indice}")
            
            if st.button("Verifica"):
                if scelta:
                    st.session_state.totali += 1
                    if scelta.lower() == str(es['risposta']).lower().strip():
                        st.success("Bravissimo! 🎉")
                        st.session_state.punteggio += 1
                    else:
                        st.error(f"Sbagliato. La risposta corretta era: {es['risposta']}")
                else:
                    st.warning("Seleziona un'opzione!")
        else:
            st.subheader(testo_domanda)
            risposta_utente = st.text_input("Scrivi qui la tua risposta:", key=f"i_{st.session_state.indice}").strip().lower()
            if st.button("Verifica"):
                st.session_state.totali += 1
                if risposta_utente == str(es['risposta']).lower().strip():
                    st.success("Ottimo lavoro! 🎉")
                    st.session_state.punteggio += 1
                else:
                    st.error(f"Sbagliato. La risposta era: {es['risposta']}")

        # Navigazione
        st.divider()
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Prossimo ➡️"):
                if st.session_state.indice < len(st.session_state.esercizi_scelti) - 1:
                    st.session_state.indice += 1
                    st.rerun()
                else:
                    st.balloons()
                    st.info("Lezione terminata! Puoi cambiare argomento dal menu.")
        with c3:
            if st.button("Nuova sfida 🔄"):
                st.session_state.argomento_attivo = None
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("In bocca al lupo con lo studio! 🇮🇹")
