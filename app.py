import streamlit as st
import random
import pandas as pd
import re

# 1. LINK DEL TUO FOGLIO GOOGLE
URL_FOGLIO = "https://docs.google.com/spreadsheets/d/18jIREltozGiHiCnNljLHqRFF-oMnj-hDDJ5yhH3rWDk/export?format=csv"

# Configurazione della pagina
st.set_page_config(page_title="ITALO! Quiz online", page_icon="🇮🇹")

# --- 2. FUNZIONE PER LO SFONDO ---
def aggiungi_sfondo(url_immagine):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.75), rgba(255,255,255,0.75)), url("{url_immagine}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center;
        }}
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.5); 
            border-radius: 25px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .istruzione-testo {{
            color: #0047AB;
            font-weight: bold;
            font-style: italic;
            font-size: 1.15em;
            margin-top: 15px;
            margin-bottom: 5px;
            display: block;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

aggiungi_sfondo("https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1996")

# --- 3. PROTEZIONE CON PASSWORD ---
st.sidebar.title("🔐 Accesso Riservato")
password_segreta = "italo2026"  # <--- CAMBIA QUESTA QUANDO VUOI
inserimento = st.sidebar.text_input("Inserisci la password:", type="password")

if inserimento != password_segreta:
    st.title("🇮🇹 ITALO! Quiz online")
    st.info("Benvenuto! Per favore, inserisci la password nella barra laterale per accedere agli esercizi delle lezioni.")
    st.stop() # Interrompe l'app qui finché la password non è corretta

# --- SE LA PASSWORD È CORRETTA, MOSTRA IL RESTO ---
st.title("ITALO! Quiz online")
st.write("Gli esercizi per le nostre lezioni.")

# --- 4. CARICAMENTO DATI ---
@st.cache_data(ttl=60)
def carica_esercizi(url):
    try:
        df = pd.read_csv(url)
        df = df.dropna(subset=['argomento', 'domanda'])
        return df
    except:
        return pd.DataFrame()

df_completo = carica_esercizi(URL_FOGLIO)

if not df_completo.empty:
    st.sidebar.markdown("---")
    st.sidebar.title("📚 Menu Lezioni")
    lista_argomenti = sorted(df_completo['argomento'].dropna().astype(str).unique().tolist())
    scelta_argomento = st.sidebar.selectbox("Scegli cosa studiare:", lista_argomenti)

    if 'argomento_attivo' not in st.session_state or st.session_state.argomento_attivo != scelta_argomento:
        st.session_state.argomento_attivo = scelta_argomento
        tutte_le_domande = df_completo[df_completo['argomento'] == scelta_argomento].to_dict('records')
        numero_da_estrarre = min(len(tutte_le_domande), 10)
        st.session_state.esercizi_scelti = random.sample(tutte_le_domande, numero_da_estrarre)
        st.session_state.indice = 0
        st.session_state.punteggio = 0
        st.session_state.totali = 0
        st.session_state.finito = False

    st.subheader(f"🏛️ Sezione: {scelta_argomento}")
    st.metric(label="Punteggio attuale", value=f"{st.session_state.punteggio} su {st.session_state.totali}")

    if st.session_state.esercizi_scelti and not st.session_state.finito:
        es = st.session_state.esercizi_scelti[st.session_state.indice]
        st.write(f"---")
        st.write(f"**Esercizio {st.session_state.indice + 1} di {len(st.session_state.esercizi_scelti)}**")
        
        if 'istruzione' in es and pd.notna(es['istruzione']):
            st.markdown(f"<span class='istruzione-testo'>{es['istruzione']}</span>", unsafe_allow_html=True)
        
        testo_domanda = str(es['domanda'])
        match_opzioni = re.search(r'\[(.*?)\]', testo_domanda)
        
        if match_opzioni:
            domanda_pulita = testo_domanda.split('[')[0].strip()
            opzioni = [opt.strip() for opt in match_opzioni.group(1).split(',')]
            st.markdown(f"### {domanda_pulita}")
            scelta = st.radio("Seleziona la risposta:", opzioni, index=None, key=f"r_{st.session_state.indice}")
            
            if st.button("Verifica"):
                if scelta:
                    st.session_state.totali += 1
                    if scelta.lower() == str(es['risposta']).lower().strip():
                        st.success("Bravissimo! 🎉")
                        st.session_state.punteggio += 1
                    else:
                        st.error(f"Sbagliato. La risposta corretta era: {es['risposta']}")
                else: st.warning("Seleziona un'opzione!")
        else:
            st.markdown(f"### {testo_domanda}")
            risposta_utente = st.text_input("Scrivi qui la tua risposta:", key=f"i_{st.session_state.indice}").strip().lower()
            if st.button("Verifica"):
                if risposta_utente:
                    st.session_state.totali += 1
                    if risposta_utente == str(es['risposta']).lower().strip():
                        st.success("Ottimo lavoro! 🎉")
                        st.session_state.punteggio += 1
                    else:
                        st.error(f"Sbagliato. La risposta era: {es['risposta']}")
                else: st.warning("Scrivi una risposta!")

        st.divider()
        if st.button("Prossimo ➡️"):
            if st.session_state.indice < len(st.session_state.esercizi_scelti) - 1:
                st.session_state.indice += 1
                st.rerun()
            else:
                st.session_state.finito = True
                st.rerun()

    elif st.session_state.finito:
        st.balloons()
        audio_url = "https://www.myinstants.com/media/sounds/applause_8.mp3"
        st.components.v1.html(f"<audio autoplay><source src='{audio_url}' type='audio/mp3'></audio>", height=0)
        st.header("🎊 Lezione Completata!")
        st.subheader(f"Hai ottenuto un punteggio di {st.session_state.punteggio} su {len(st.session_state.esercizi_scelti)}")
        if st.button("Ricomincia o cambia lezione 🔄"):
            st.session_state.argomento_attivo = None
            st.session_state.finito = False
            st.rerun()
