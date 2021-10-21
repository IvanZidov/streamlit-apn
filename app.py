import altair as alt
import numpy_financial as npf
import pandas as pd
import streamlit as st
import pickle

# Load Data
with open(r"./skupine.p", "rb") as input_file:
    skupine = pickle.load(input_file)
with open(r"./naselja.p", "rb") as input_file:
    naselja = pickle.load(input_file)

st.set_page_config(
    page_title="APN kredit kalkulator",
    page_icon="🏠",
    # layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #    'Get Help': 'https://www.extremelycoolapp.com/help',
    #    'Report a bug': "https://www.extremelycoolapp.com/bug",
    #    'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

st.write(
    """
# APN kredit kalkulator
"""
)
st.write("---")

st.image("./image.jpg", use_column_width=True)
st.write(
    "[Photo by Tierra Mallorca](https://unsplash.com/@tierramallorca?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)"
)




# Giving Choices

if "states" not in st.session_state:
    st.session_state.states = []
if "kredit_no" not in st.session_state:
    st.session_state.kredit_no = 0

with st.container():
    VRSTA_KREDITA = st.radio("Vrsta kredita:", ("APN", "Običan stambeni"))
    CIJENA = st.number_input("Cijena nekretnine (€): ", value=98000, min_value=0)
    KAPARA = st.number_input("Kapara (€): ", value=8000, min_value=0)
    if VRSTA_KREDITA == "APN":
        KAMATA = st.number_input("Kamata (%): ", value=2.10, format="%.2f", min_value=0.00)
    else:
        KAMATA = st.number_input("Kamata (%): ", value=2.90, format="%.2f", min_value=0.00)
    TRAJANJE = st.slider("Godina otplate: ", 15, 30, value=15)

    GODINA_POTPORE = 0
    MJESTO = ""
    VISINA_SUBVENCIJE = 0
    if VRSTA_KREDITA == "APN":

        with st.expander("Postavke APN-a", expanded=True):
            GODINA_POTPORE = st.radio("Godina subvencije APN-a:", (5, 7, 9))
            MJESTO = st.selectbox("Mjesto", [""] + sorted(list(naselja.keys())))
            VISINA_SUBVENCIJE = st.number_input(
                "Visina subvencije: ", value=naselja.get(MJESTO, 0.36), format="%.2f", min_value=0.30, max_value=0.51
            )

    with st.expander("Dodatne postavke"):
        POREZ = st.radio("Porez:", ("Da", "Ne"))
        IZNOS_KREDITA = st.number_input("Iznos kredita: ", value=round(CIJENA - KAPARA), min_value=0)
        SUBVENCIJA = st.number_input("Dodatna subvencija: ", value=0, min_value=0)
        TECAJ_EURA = st.number_input("Tečaj eura: ", value=7.51, format="%.2f", min_value=0.00)

CREDIT_CONFIG = {
   "VRSTA_KREDITA" : VRSTA_KREDITA,
   "CIJENA" : CIJENA,
   "KAPARA" : KAPARA,
   "KAMATA" : KAMATA,
   "TRAJANJE" : TRAJANJE,
   "GODINA_POTPORE" : GODINA_POTPORE,
   "MJESTO" : MJESTO,
   "VISINA_SUBVENCIJE" : VISINA_SUBVENCIJE,
   "POREZ" : POREZ,
   "IZNOS_KREDITA" : IZNOS_KREDITA,
   "SUBVENCIJA" : SUBVENCIJA,
   "TECAJ_EURA" : TECAJ_EURA,
}






st.write("---")

#### Kalkulacija



MJESECNA_RATA = npf.pmt(KAMATA / 100 / 12, TRAJANJE * 12, -(IZNOS_KREDITA))
MJESECNA_RATA = round(MJESECNA_RATA,2)

UKUPNI_TROSKOVI = KAPARA
if POREZ == "Da":
    CIJENA_POREZA = round(CIJENA * 0.03, 2)
    UKUPNI_TROSKOVI += CIJENA_POREZA
CIJENA_AKVIZICIJE = round(CIJENA * 0.005, 2)
UKUPNI_TROSKOVI += CIJENA_AKVIZICIJE
UKUPNI_TROSKOVI -= SUBVENCIJA
UKUPNI_TROSKOVI = round(UKUPNI_TROSKOVI, 2)

UKUPNI_IZNOS_POTPORE = 0
MJESECNA_RATA_APN = MJESECNA_RATA
MJESECNA_POTPORA = 0

if VRSTA_KREDITA == "APN":
    if IZNOS_KREDITA > 100000:
        MJESECNA_RATA_APN = (100000 / IZNOS_KREDITA) * MJESECNA_RATA * (
            1 - VISINA_SUBVENCIJE
        ) + (1 - (100000 / IZNOS_KREDITA)) * MJESECNA_RATA
    else:
        MJESECNA_RATA_APN = MJESECNA_RATA * (1 - VISINA_SUBVENCIJE)
    MJESECNA_RATA_APN = round(MJESECNA_RATA_APN,2)

    MJESECNA_POTPORA = MJESECNA_RATA - MJESECNA_RATA_APN
    MJESECNA_POTPORA = round(MJESECNA_POTPORA,2)
    UKUPNI_IZNOS_POTPORE = round(MJESECNA_POTPORA * GODINA_POTPORE * 12, 2)

UKUPNI_KREDIT = round(MJESECNA_RATA * TRAJANJE * 12, 2)
UKUPNE_KAMATE = round(UKUPNI_KREDIT - IZNOS_KREDITA, 2)
UKUPNO_PLACENO = round(UKUPNI_KREDIT - UKUPNI_IZNOS_POTPORE, 2)
UKUPNA_CIJENA_NEKRETNINE = UKUPNO_PLACENO + UKUPNI_TROSKOVI

CREDIT_SUMMARY = {
    "MJESECNA_RATA" : MJESECNA_RATA,
    "UKUPNI_TROSKOVI" : UKUPNI_TROSKOVI,
    "MJESECNA_RATA_APN" : MJESECNA_RATA_APN,
    "MJESECNA_POTPORA" : MJESECNA_POTPORA,
    "UKUPNI_IZNOS_POTPORE" : UKUPNI_IZNOS_POTPORE,
    "UKUPNI_KREDIT" : UKUPNI_KREDIT,
    "UKUPNE_KAMATE" : UKUPNE_KAMATE,
    "UKUPNO_PLACENO" : UKUPNO_PLACENO,
    "UKUPNA_CIJENA_NEKRETNINE" : UKUPNA_CIJENA_NEKRETNINE
}

#### Prikaz

st.write("""## Mjesečna rata""")
if VRSTA_KREDITA=="APN":
    col1, col2 = st.columns(2)
    col1.metric(
                "Anuitet u eurima za vrijeme APN-a",
                value=str(round(MJESECNA_RATA_APN, 2)) + " €",
                delta="-" + str(round(MJESECNA_POTPORA, 2)) + " €",
                delta_color="inverse",
            )

    col2.metric(
            "Anuitet u eurima", value=str(round(MJESECNA_RATA, 2)) + " €"
    )
else:
    st.metric(
            "Anuitet u eurima", value=str(round(MJESECNA_RATA, 2)) + " €"
    )
st.write("---")
st.write("""## Ukupno""")
col1, col2 = st.columns(2)
col1.metric(
    "Ukupna cijena nekretnine:",
    value=str(UKUPNA_CIJENA_NEKRETNINE) + " €",
    delta=str(round(UKUPNA_CIJENA_NEKRETNINE - CIJENA, 2)) + " €",
    delta_color="inverse",
)

col2.metric("Ukupni iznos potpore:", value=str(UKUPNI_IZNOS_POTPORE+SUBVENCIJA) + " €")

st.write("---")

with st.expander("Više informacija"):
    st.write("""## Početni troškovi""")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kapara", value=str(KAPARA) + " €")
    if POREZ == "Da":
        col2.metric("Porez", value=str(round(CIJENA * 0.03, 2)) + " €")
    else:
        col2.metric("Porez", value="0 €")
    col3.metric("Administrativni troškovi", value=str(round(CIJENA * 0.005, 2)) + " €")
    if SUBVENCIJA>0:
        col4.metric("Dodatna subvencija", value="-"+str(SUBVENCIJA) + " €")
    else:
        col4.metric("Dodatna subvencija", value=str(SUBVENCIJA) + " €")

    #st.write("""#### Ukupni troškovi""")
    #st.metric("", value=str(round(UKUPNI_TROSKOVI, 2)) + " €")

    st.write("---")

    st.write("""## Mjesečna rata""")

    col1, col2 = st.columns(2)
    col1.metric(
        "Anuitet u kunama", value=str(round(MJESECNA_RATA * TECAJ_EURA, 2)) + " kn"
    )
    col2.metric("Anuitet u eurima", value=str(round(MJESECNA_RATA, 2)) + " 💶")

    if VRSTA_KREDITA == "APN":
        
        st.write("""#### Mjesečna rata APN""")

        col1, col2 = st.columns(2)
        col1.metric(
            "Anuitet u kunama APN",
            value=str(round(MJESECNA_RATA_APN * TECAJ_EURA, 2)) + " kn",
            delta="-" + str(round(MJESECNA_POTPORA * TECAJ_EURA, 2)) + " kn",
            delta_color="inverse",
        )
        col2.metric(
            "Anuitet u eurima APN",
            value=str(round(MJESECNA_RATA_APN, 2)) + " 💶",
            delta="-" + str(round(MJESECNA_POTPORA, 2)) + " €",
            delta_color="inverse",
        )


    st.write("---")

    st.write("""## Ukupni iznosi:""")
    st.write("""#### O kreditu""")
    col1, col2 = st.columns(2)
    col1.metric("Ukupni iznos kredita:", value=str(UKUPNI_KREDIT) + " €")
    col2.metric("Ukupne kamate:", value=str(UKUPNE_KAMATE) + " €")

    #st.write("---")
    #st.write("""## Ukupna APN subvencija""")
    st.write("""#### Potpora i troškovi""")
    col1, col2 = st.columns(2)
    col1.metric("Ukupni iznos potpore:", value=str(UKUPNI_IZNOS_POTPORE+SUBVENCIJA) + " €")
    col2.metric("Ukupni troškovi", value=str(round(UKUPNI_TROSKOVI, 2)) + " €")
    #st.write("""### Ukupno plaćeno banci:""")
    #st.metric("Ukupno plaćeno banci:", value=str(UKUPNO_PLACENO) + " €")

    st.write("---")

    st.write("""# Ukupna cijena nekretnine:""")
    st.metric(
        "Ukupna cijena nekretnine:",
        value=str(UKUPNA_CIJENA_NEKRETNINE) + " €",
        delta=str(round(UKUPNA_CIJENA_NEKRETNINE - CIJENA, 2)) + " €",
        delta_color="inverse",
    )




increment = st.button("Save")
if increment:
    st.session_state.kredit_no += 1
    CREDIT_SUMMARY["IME"] = "Model"+str(st.session_state.kredit_no)
    st.session_state.states.append({**CREDIT_CONFIG, **CREDIT_SUMMARY})

reset = st.button("Reset")
if reset:
    st.session_state.states = []


import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

if st.session_state.states != []:

    df = pd.DataFrame(
        st.session_state.states
        )

    c = alt.Chart(df).mark_bar().encode(
        x='IME',
        y='UKUPNA_CIJENA_NEKRETNINE',
        tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']
    )

    st.altair_chart(c, use_container_width=True)

    d = alt.Chart(df).transform_fold(
        ['MJESECNA_RATA', 'MJESECNA_RATA_APN']
        ).mark_bar().encode(
        x=alt.X('key:N', axis=alt.Axis(title='')),
        y=alt.Y('value:Q', axis=alt.Axis(title='Rata u €')),
        color=alt.Color('key:N',title=""),
        column = alt.Column("IME:N", title='Krediti'),
        tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']

        ).properties(
            width='container'
        )
    
    st.altair_chart(d, use_container_width=True)