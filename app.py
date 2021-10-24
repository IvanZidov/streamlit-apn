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
    layout="wide",
    initial_sidebar_state="expanded",
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

#st.image("./image.jpg", use_column_width=True)
#st.write(
#    "[Photo by Tierra Mallorca](https://unsplash.com/@tierramallorca?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)"
#)



# Giving Choices

if "states" not in st.session_state:
    st.session_state.states = []
if "kredit_no" not in st.session_state:
    st.session_state.kredit_no = 0





CIJENA = st.sidebar.number_input("Cijena nekretnine (€): ", value=98000, min_value=0)
KAPARA = st.sidebar.number_input("Kapara (€): ", value=8000, min_value=0)
GODINA_POTPORE = 0
MJESTO = ""
VISINA_SUBVENCIJE = 0
with st.sidebar.expander("Postavke APN-a", expanded=True):
    GODINA_POTPORE = st.radio("Godina subvencije APN-a:", (5, 7, 9))
    MJESTO = st.selectbox("Mjesto", [""] + sorted(list(naselja.keys())))
    VISINA_SUBVENCIJE = st.number_input(
        "Visina subvencije: ", value=naselja.get(MJESTO, 0.36), format="%.2f", min_value=0.30, max_value=0.51
    )
with st.sidebar.expander("Dodatne postavke"):
    POREZ = st.radio("Porez:", ("Da", "Ne"))
    IZNOS_KREDITA = st.number_input("Iznos kredita: ", value=round(CIJENA - KAPARA), min_value=0)
    TECAJ_EURA = st.number_input("Tečaj eura: ", value=7.51, format="%.2f", min_value=0.00)


stupac1,stupac2 = st.columns(2)
VRSTA_KREDITA_1 = stupac1.radio("Vrsta kredita:", ("APN", "Običan stambeni"))
if VRSTA_KREDITA_1 == "APN":
    KAMATA_1 = stupac1.number_input("Kamata (%): ", value=2.10, format="%.2f", min_value=0.00)
else:
    KAMATA_1 = stupac1.number_input("Kamata (%): ", value=2.90, format="%.2f", min_value=0.00)
TRAJANJE_1 = stupac1.slider("Godina otplate: ", 15, 30, value=15)

VRSTA_KREDITA_2 = stupac2.radio("Vrsta kredita:", ("APN", "Običan stambeni"),key="2",index=1)
if VRSTA_KREDITA_2 == "APN":
    KAMATA_2 = stupac2.number_input("Kamata (%): ", value=2.10, format="%.2f", min_value=0.00,key="2")
else:
    KAMATA_2 = stupac2.number_input("Kamata (%): ", value=2.90, format="%.2f", min_value=0.00,key="2")
TRAJANJE_2 = stupac2.slider("Godina otplate: ", 15, 30, value=15,key="2")



CREDIT_CONFIG = {
   "VRSTA_KREDITA" : VRSTA_KREDITA_1,
   "CIJENA" : CIJENA,
   "KAPARA" : KAPARA,
   "KAMATA" : KAMATA_1,
   "TRAJANJE" : TRAJANJE_1,
   "GODINA_POTPORE" : GODINA_POTPORE,
   "MJESTO" : MJESTO,
   "VISINA_SUBVENCIJE" : VISINA_SUBVENCIJE,
   "POREZ" : POREZ,
   "IZNOS_KREDITA" : IZNOS_KREDITA,
   "TECAJ_EURA" : TECAJ_EURA,
}

CREDIT_CONFIG2 = {
   "VRSTA_KREDITA" : VRSTA_KREDITA_2,
   "CIJENA" : CIJENA,
   "KAPARA" : KAPARA,
   "KAMATA" : KAMATA_2,
   "TRAJANJE" : TRAJANJE_2,
   "GODINA_POTPORE" : GODINA_POTPORE,
   "MJESTO" : MJESTO,
   "VISINA_SUBVENCIJE" : VISINA_SUBVENCIJE,
   "POREZ" : POREZ,
   "IZNOS_KREDITA" : IZNOS_KREDITA,
   "TECAJ_EURA" : TECAJ_EURA,
}

st.write("---")
#st.write(list(CREDIT_CONFIG.values()))
#### Kalkulacija



class Kredit:
    def __init__(self,config):
        self.config = config
        self.summary = {}
        for key,value in self.config.items():
            if type(value)==str:
                exec(f"""self.{key} = '{value}'""".format(key,value))
            else:
                exec(f"""self.{key} = {value}""".format(key,value))

    def calculate_credit(self):

        
        MJESECNA_RATA = npf.pmt(self.KAMATA / 100 / 12, self.TRAJANJE * 12, -(self.IZNOS_KREDITA))
        MJESECNA_RATA = round(MJESECNA_RATA,2)

        UKUPNI_TROSKOVI = self.KAPARA
        if self.POREZ == "Da":
            CIJENA_POREZA = round(self.CIJENA * 0.03, 2)
            UKUPNI_TROSKOVI += CIJENA_POREZA
        CIJENA_AKVIZICIJE = round(self.CIJENA * 0.005, 2)
        UKUPNI_TROSKOVI += CIJENA_AKVIZICIJE
        UKUPNI_TROSKOVI = round(UKUPNI_TROSKOVI, 2)

        UKUPNI_IZNOS_POTPORE = 0
        MJESECNA_RATA_APN = MJESECNA_RATA
        MJESECNA_POTPORA = 0

        if self.VRSTA_KREDITA == "APN":
            if self.IZNOS_KREDITA > 100000:
                MJESECNA_RATA_APN = (100000 / self.IZNOS_KREDITA) * MJESECNA_RATA * (
                    1 - self.VISINA_SUBVENCIJE
                ) + (1 - (100000 / self.IZNOS_KREDITA)) * MJESECNA_RATA
            else:
                MJESECNA_RATA_APN = MJESECNA_RATA * (1 - self.VISINA_SUBVENCIJE)
            MJESECNA_RATA_APN = round(MJESECNA_RATA_APN,2)

            MJESECNA_POTPORA = MJESECNA_RATA - MJESECNA_RATA_APN
            MJESECNA_POTPORA = round(MJESECNA_POTPORA,2)
            UKUPNI_IZNOS_POTPORE = round(MJESECNA_POTPORA * self.GODINA_POTPORE * 12, 2)

        UKUPNI_KREDIT = round(MJESECNA_RATA * self.TRAJANJE * 12, 2)
        UKUPNE_KAMATE = round(UKUPNI_KREDIT - self.IZNOS_KREDITA, 2)
        UKUPNO_PLACENO = round(UKUPNI_KREDIT - UKUPNI_IZNOS_POTPORE, 2)
        UKUPNA_CIJENA_NEKRETNINE = UKUPNO_PLACENO + UKUPNI_TROSKOVI

        summary = {
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
        self.summary = summary
        for key,value in self.summary.items():
            if type(value)==str:
                exec(f"""self.{key} = '{value}'""".format(key,value))
            else:
                exec(f"""self.{key} = {value}""".format(key,value))
        #st.write(summary)
        return summary
    
    def show_results(self,container):
    #### Prikaz

        container.write("""## Mjesečna rata""")
        if self.VRSTA_KREDITA=="APN":
            
            container.metric(
                        "Anuitet u eurima za vrijeme APN-a",
                        value=str(round(self.MJESECNA_RATA_APN, 2)) + " €",
                        delta="-" + str(round(self.MJESECNA_POTPORA, 2)) + " €",
                        delta_color="inverse",
                    )

            container.metric(
                    "Anuitet u eurima", value=str(round(self.MJESECNA_RATA, 2)) + " €"
            )
        else:
            container.metric(
                    "Anuitet u eurima", value=str(round(self.MJESECNA_RATA, 2)) + " €",
                    delta="0 €",
                    delta_color="inverse"
            )
            container.metric(
                    "Anuitet u eurima", value=str(round(self.MJESECNA_RATA, 2)) + " €"
            )
        #st.write("---")
        container.write("""## Ukupno""")
        container.metric(
            "Ukupna cijena nekretnine:",
            value=str(self.UKUPNA_CIJENA_NEKRETNINE) + " €",
            delta=str(round(self.UKUPNA_CIJENA_NEKRETNINE - self.CIJENA, 2)) + " €",
            delta_color="inverse",
        )

        container.metric("Ukupni iznos potpore:", value=str(self.UKUPNI_IZNOS_POTPORE) + " €")

        container.write("---")

        with container.expander("Više informacija"):
            st.write("""## Početni troškovi""")
            st.metric("Kapara", value=str(self.KAPARA) + " €")
            if self.POREZ == "Da":
                st.metric("Porez", value=str(round(self.CIJENA * 0.03, 2)) + " €")
            else:
                st.metric("Porez", value="0 €")
            st.metric("Administrativni troškovi", value=str(round(self.CIJENA * 0.005, 2)) + " €")


            #st.write("""#### Ukupni troškovi""")
            #st.metric("", value=str(round(UKUPNI_TROSKOVI, 2)) + " €")

            st.write("---")

            st.write("""## Mjesečna rata""")

            

            if self.VRSTA_KREDITA == "APN":
                

                st.metric(
                    "Anuitet u kunama prvih " + str(self.GODINA_POTPORE) + " godina",
                    value=str(round(self.MJESECNA_RATA_APN * self.TECAJ_EURA, 2)) + " kn",
                    delta="-" + str(round(self.MJESECNA_POTPORA * self.TECAJ_EURA, 2)) + " kn",
                    delta_color="inverse",
                )
                st.metric(
                    "Anuitet u eurima prvih " + str(self.GODINA_POTPORE) + " godina",
                    value=str(round(self.MJESECNA_RATA_APN, 2)) + " 💶",
                    delta="-" + str(round(self.MJESECNA_POTPORA, 2)) + " €",
                    delta_color="inverse",
                )
            
            else:
                st.metric(
                    "Anuitet u kunama prvih " + str(self.GODINA_POTPORE) + " godina",
                    value=str(round(self.MJESECNA_RATA_APN * self.TECAJ_EURA, 2)) + " kn",
                    delta="0 kn",
                )
                st.metric(
                    "Anuitet u eurima prvih " + str(self.GODINA_POTPORE) + " godina",
                    value=str(round(self.MJESECNA_RATA, 2)) + " 💶",
                    delta="0 €",
                )

            st.metric(
                "Anuitet u kunama", value=str(round(self.MJESECNA_RATA * self.TECAJ_EURA, 2)) + " kn"
            )
            st.metric("Anuitet u eurima", value=str(round(self.MJESECNA_RATA, 2)) + " 💶")

            st.write("---")

            st.write("""## Ukupni iznosi:""")
            st.write("""#### O kreditu""")
            st.metric("Ukupni iznos kredita:", value=str(self.UKUPNI_KREDIT) + " €")
            st.metric("Ukupne kamate:", value=str(self.UKUPNE_KAMATE) + " €")

            #st.write("---")
            #st.write("""## Ukupna APN subvencija""")
            st.write("""#### Potpora i troškovi""")
            st.metric("Ukupni iznos potpore:", value=str(self.UKUPNI_IZNOS_POTPORE) + " €")
            st.metric("Ukupni troškovi", value=str(round(self.UKUPNI_TROSKOVI, 2)) + " €")
            #st.write("""### Ukupno plaćeno banci:""")
            #st.metric("Ukupno plaćeno banci:", value=str(UKUPNO_PLACENO) + " €")

            st.write("---")

            st.write("""# Ukupna cijena nekretnine:""")
            st.metric(
                "Ukupna cijena nekretnine:",
                value=str(self.UKUPNA_CIJENA_NEKRETNINE) + " €",
                delta=str(round(self.UKUPNA_CIJENA_NEKRETNINE - self.CIJENA, 2)) + " €",
                delta_color="inverse",
            )
        
#increment = container.button("Spremi kredit")
#if increment:
#    container.session_state.kredit_no += 1
#    CREDIT_SUMMARY["IME"] = "Kredit"+str(container.session_state.kredit_no)
#    container.session_state.states.append({**CREDIT_CONFIG, **CREDIT_SUMMARY})
#    container.success('Uspješno spremljen kredit!')


col1, col2 = st.columns(2)

kredit1 = Kredit(CREDIT_CONFIG)
kredit2 = Kredit(CREDIT_CONFIG2)

CREDIT_SUMMARY = kredit1.calculate_credit()
CREDIT_SUMMARY2 = kredit2.calculate_credit()

kredit1.show_results(col1)
kredit2.show_results(col2)

#st.write(CREDIT_SUMMARY)
#st.write(CREDIT_SUMMARY2)


#CREDIT_SUMMARY = calculate_credit(CREDIT_CONFIG)
for key,value in CREDIT_SUMMARY.items():
    if type(value)==str:
        exec(f"""{key} = '{value}'""".format(key,value))
    else:
        exec(f"""{key} = {value}""".format(key,value))





import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.write("---")

with st.expander("Vizualizacije"):
    st.empty()
    CREDIT_SUMMARY["IME"] = "Kredit 1"
    CREDIT_SUMMARY2["IME"] = "Kredit 2"
    df = pd.DataFrame(
        [{**CREDIT_CONFIG, **CREDIT_SUMMARY}] + [{**CREDIT_CONFIG2, **CREDIT_SUMMARY2}]
        )

    c = alt.Chart(df).mark_bar().encode(
        x='IME',
        y='UKUPNA_CIJENA_NEKRETNINE',
        color = "IME:N",
        tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']
    )

    st.altair_chart(c, use_container_width=True)

    c = alt.Chart(df).mark_bar().encode(
        x='IME',
        y='MJESECNA_RATA_APN',
        color = "IME:N",
        tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']
    )

    st.altair_chart(c, use_container_width=True)

    c = alt.Chart(df).mark_bar().encode(
        x='IME',
        y='MJESECNA_RATA',
        color = "IME:N",
        tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']
    )

    st.altair_chart(c, use_container_width=True)

    #d = alt.Chart(df).transform_fold(
    #    ['MJESECNA_RATA', 'MJESECNA_RATA_APN']
    #    ).mark_bar().encode(
    #    x=alt.X('key:N', axis=alt.Axis(title='')),
    #    y=alt.Y('value:Q', axis=alt.Axis(title='Rata u €')),
    #    color=alt.Color('key:N',title="",legend=None),
    #    column = alt.Column("IME:N", title='Krediti'),
    #    tooltip = ['VRSTA_KREDITA', 'CIJENA', 'TRAJANJE', 'GODINA_POTPORE', 'MJESECNA_RATA', 'MJESECNA_RATA_APN', 'UKUPNI_IZNOS_POTPORE', 'UKUPNA_CIJENA_NEKRETNINE']
#
    #    ).properties(
    #        width=100
    #    )
    #
    #st.altair_chart(d, use_container_width=True)

st.write("---")
reset = st.button("Reset")
if reset:
    st.session_state.states = []
    st.info('Uspješan reset!')

