import altair as alt
import numpy_financial as npf
import pandas as pd
import streamlit as st

# st.set_option("server.runOnSave", True)

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


# Load Data
skupine = [
    [
        0.51,
        [
            "Babina Greda",
            "Berek",
            "Biskupija",
            "Brinje",
            "Cetingrad",
            "CistaProvo",
            "Civljane",
            "Crnac",
            "Čađavica",
            "Dežanovac",
            "Donja Motičina",
            "Donja Voća",
            "Donji Kukuruzari",
            "Donji Lapac",
            "Draž",
            "Drenovci",
            "Drenje",
            "Dvor",
            "Đulovac",
            "Ervenik",
            "Glina",
            "Gornji Bogićevci",
            "Gračac",
            "Gradina",
            "Gunja",
            "Gvozd",
            "HrvatskaDubica",
            "Jagodnjak",
            "Jasenovac",
            "Kapela",
            "Kijevo",
            "Kistanje",
            "Krnjak",
            "Lećevica",
            "Levanjska Varoš",
            "Lokvičići",
            "Lovreć",
            "Lukač",
            "Majur",
            "Markušica",
            "Mikleuš",
            "Negoslavci",
            "Nova Bukovica",
            "Nova Rača",
            "Okučani",
            "Petlovac",
            "Plaški",
            "Podgorač",
            "Podravska Moslavina",
            "Popovac",
            "Proložac",
            "Saborsko",
            "Severin",
            "Sopje",
            "Stara Gradiška",
            "Staro Petrovo Selo",
            "Suhopolje",
            "Sunja",
            "Šodolovci",
            "Špišić Bukovica",
            "Štitar",
            "Tompojevci",
            "Trnava",
            "Trpinja",
            "Udbina",
            "Unešić",
            "VelikaPisanica",
            "Viljevo",
            "Voćin",
            "Vojnić",
            "Vrbje",
            "Vrhovine",
            "Zagvozd",
            "Zažablje",
            "Zrinski Topolovac",
            "Žumberak",
        ],
    ],
    [
        0.48,
        [
            "Bebrina",
            "Bogdanovci",
            "Borovo",
            "Bošnjaci",
            "Brestovac",
            "Cernik",
            "Čačinci",
            "Čaglin",
            "Darda",
            "Davor",
            "Desinić",
            "Dragalić",
            "Đurđenovac",
            "Erdut",
            "Farkaševac",
            "Ferdinandovac",
            "Generalski Stol",
            "Gola",
            "Gorjani",
            "Gornja Rijeka",
            "Gradište",
            "Grubišno Polje",
            "Gundinci",
            "Hrvatska Kostajnica",
            "Ivanska",
            "Kaptol",
            "Kloštar Podravski",
            "Kneževi Vinogradi",
            "Končanica",
            "Koška",
            "Legrad",
            "Lišane Ostrovičke",
            "Magadenovac",
            "Marijanci",
            "Martijanec",
            "Martinska Ves",
            "Nijemci",
            "Nova Kapela",
            "Novo Virje",
            "Otok (Vukovarsko-srijemska županija)",
            "Perušić",
            "Podbablje",
            "Pojezerje",
            "Preseka",
            "Prgomet",
            "Privlaka (Vukovarsko-srijemska županija)",
            "Punitovci",
            "Rešetari",
            "Ribnik",
            "Rovišće",
            "Runovići",
            "Ružić",
            "Satnica Đakovačka",
            "Semeljci",
            "Sikirevci",
            "Sirač",
            "Skradin",
            "Slavonski Šamac",
            "Slunj",
            "Sokolovac",
            "Stari Jankovci",
            "Strizivojna",
            "Sveti Petar Orehovec",
            "Šandrovac",
            "Šestanovac",
            "Štefanje",
            "Topusko",
            "Tounj",
            "Velika Kopanica",
            "Velika Trnovitica",
            "Veliki Grđevac",
            "Veliko Trojstvo",
            "Viškovci",
            "Vladislavci",
            "Vrbanja",
            "Zdenci",
        ],
    ],
    [
        0.45,
        [
            "Andrijaševci",
            "Bednja",
            "Beli Manastir",
            "Bizovac",
            "BrodskiStupnik",
            "Cerna",
            "Cestica",
            "Čeminac",
            "Domašinec",
            "Donja Dubrava",
            "Donji Andrijevci",
            "Donji Vidovec",
            "Dubrava",
            "Feričanci",
            "Garčin",
            "Garešnica",
            "Gornja Vrba",
            "Hercegovac",
            "Hlebine",
            "Hrvace",
            "Ilok",
            "Ivankovo",
            "Janjina",
            "Jarmina",
            "Kalnik",
            "Knin",
            "Koprivnički Bregi",
            "Krašić",
            "Kula Norinska",
            "Kutjevo",
            "Lanišće",
            "Lasinja",
            "Lipik",
            "Lovas",
            "Lovinac",
            "Mala Subotica",
            "MaliBukovec",
            "Muć",
            "Netretić",
            "Oprisavci",
            "Orehovica",
            "Oriovac",
            "Orle",
            "Otok (Splitsko-dalmatinska županija)",
            "Peteranec",
            "Petrijevci",
            "Pitomača",
            "Pleternica",
            "Podcrkavlje",
            "Podravske Sesvete",
            "Podturen",
            "Pokupsko",
            "Primorski Dolac",
            "Promina",
            "Rakovec",
            "Rasinja",
            "Selnica",
            "Sibinj",
            "Slivno",
            "Stari Mikanovci",
            "Sućuraj",
            "Sveti Đurđ",
            "Sveti Ivan Žabno",
            "Štrigova",
            "Tordinci",
            "Trilj",
            "Velika",
            "Virje",
            "Visoko",
            "Vođinci",
            "Vrlika",
            "Vrpolje",
            "Vuka",
            "Zagorska Sela",
            "Zmijavci",
            "Žakanje",
        ],
    ],
    [
        0.42,
        [
            "Barilović",
            "Bedenica",
            "Belica",
            "Belišće",
            "Benkovac",
            "Bilje",
            "Bosiljevo",
            "Brckovljani",
            "Breznica",
            "Breznički Hum",
            "Brod Moravice",
            "Budinščina",
            "Bukovlje",
            "Čazma",
            "Čepin",
            "Dekanovec",
            "Dicmo",
            "Donji Miholjac",
            "Draganić",
            "Drnje",
            "Dubravica",
            "Đakovo",
            "Đelekovec",
            "Ernestinovo",
            "Galovac",
            "Goričan",
            "GornjaStubica",
            "Gornji Mihaljevec",
            "Gradec",
            "Hrašćina",
            "Imotski",
            "Jakšić",
            "Jalžabet",
            "Josipdol",
            "Kamanje",
            "Klakar",
            "Klenovnik",
            "Koprivnički Ivanec",
            "Kotoriba",
            "Kraljevec na Sutli",
            "Kumrovec",
            "Lekenik",
            "Lepoglava",
            "Lipovljani",
            "Lobor",
            "Mače",
            "Maruševec",
            "Mihovljan",
            "Molve",
            "Mrkopalj",
            "Nova Gradiška",
            "Novigrad Podravski",
            "Novska",
            "Nuštar",
            "Obrovac",
            "Otočac",
            "Pakrac",
            "Petrijanec",
            "Petrinja",
            "Petrovsko",
            "Polača",
            "Popovača",
            "Skrad",
            "Slatina",
            "Stankovci",
            "Sveti Martin na Muri",
            "Tovarnik",
            "Tuhelj",
            "Valpovo",
            "Velika Ludina",
            "Vinica",
            "Vratišinec",
            "Vrbovsko",
            "Vrgorac",
            "Vukovar",
            "Županja",
        ],
    ],
    [
        0.39,
        [
            "Antunovac",
            "Bedekovčina",
            "Beretinec",
            "Cerovlje",
            "Čabar",
            "Daruvar",
            "Donji Kraljevec",
            "Drniš",
            "Đurđevac",
            "Đurmanec",
            "Jakovlje",
            "Jesenje",
            "Kalinovac",
            "Karlobag",
            "Klanjec",
            "KloštarIvanić",
            "Komiža",
            "Kravarsko",
            "Križ",
            "Lokve",
            "Ljubešćica",
            "Marija Bistrica",
            "Marina",
            "Metković",
            "Mursko Središće",
            "Našice",
            "Nedelišće",
            "Novi Golubovec",
            "Novi Marof",
            "Novigrad (Zadarska županija)",
            "Ogulin",
            "Oprtalj – Portole",
            "Opuzen",
            "Orahovica",
            "Ozalj",
            "Pisarovina",
            "Plitvička jezera",
            "Poličnik",
            "Posedarje",
            "Pregrada",
            "Preko",
            "Pribislavec",
            "Radoboj",
            "Rakovica",
            "Ravna Gora",
            "Ražanac",
            "Rugvica",
            "Selca",
            "Senj",
            "Sinj",
            "Smokvica",
            "Sračinec",
            "Sveta Marija",
            "Sveti Juraj na Bregu",
            "Sveti Križ Začretje",
            "Škabrnja",
            "Vela Luka",
            "Veliko Trgovišće",
            "Vidovec",
            "Vrsi",
            "Zadvarje",
            "Zemunik Donji",
            "Zlatar",
        ],
    ],
    [
        0.36,
        [
            "Bibinje",
            "Bilice",
            "Bjelovar",
            "Blato",
            "Delnice",
            "Donja Stubica",
            "Dubrovačko primorje",
            "Duga Resa",
            "Fužine",
            "Gornji Kneginec",
            "Gospić",
            "Gradac",
            "Grožnjan – Grisignana",
            "Hum na Sutli",
            "Ivanec",
            "Ivanić-Grad",
            "Karojba",
            "Klana",
            "Klinča Sela",
            "Klis",
            "Konjščina",
            "Krapinske Toplice",
            "Križevci",
            "Kutina",
            "Luka",
            "Lumbarda",
            "Lupoglav",
            "Marija Gorica",
            "Mljet",
            "Motovun – Montona",
            "Nerežišća",
            "Omiš",
            "Orebić",
            "Pakoštane",
            "Pašman",
            "Pirovac",
            "Ploče",
            "Povljana",
            "Požega",
            "Prelog",
            "Pučišća",
            "Sali",
            "Seget",
            "Sisak",
            "Slavonski Brod",
            "Starigrad",
            "Ston",
            "Strahoninec",
            "Sukošan",
            "Sveti Filip i Jakov",
            "Sveti Ilija",
            "Sveti Ivan Zelina",
            "Šolta",
            "Tribunj",
            "Trnovec Bartolovečki",
            "Trpanj",
            "VaraždinskeToplice",
            "Veliki Bukovec",
            "Vinkovci",
            "Vinodolska općina",
            "Virovitica",
            "Vrbovec",
            "Zlatar Bistrica",
        ],
    ],
    [
        0.33,
        [
            "Barban",
            "Bistra",
            "Brdovec",
            "Brtonigla – Verteneglio",
            "Buje – Buie",
            "Čavle",
            "Dugi Rat",
            "Dugo Selo",
            "Dugopolje",
            "Gračišće",
            "Jasenice",
            "Jastrebarsko",
            "Jelenje",
            "Jelsa",
            "Kali",
            "Karlovac",
            "Kaštela",
            "Korčula",
            "Kraljevica",
            "Krapina",
            "Kršan",
            "Kukljica",
            "Lastovo",
            "Lopar",
            "Lovran",
            "Ludbreg",
            "Milna",
            "Moščenička Draga",
            "Murter – Kornati",
            "Nin",
            "Novi Vinodolski",
            "Okrug",
            "Oroslavje",
            "Osijek",
            "Pag",
            "Pićan",
            "Podgora",
            "Postira",
            "Primošten",
            "Privlaka (Zadarska županija)",
            "Pušća",
            "Rab",
            "Raša",
            "Rogoznica",
            "Solin",
            "Stari Grad",
            "Stubičke Toplice",
            "Sveta Nedelja(Istarska županija)",
            "Sveti Lovreč",
            "Sveti Petar u Šumi",
            "Svetvinčenat",
            "Šenkovec",
            "Šibenik",
            "Tinjan",
            "Tisno",
            "Tkon",
            "Trogir",
            "Tučepi",
            "Vis",
            "Višnjan – Visignano",
            "Vižinada – Visinada",
            "Vodice",
            "Žminj",
        ],
    ],
    [
        0.30,
        [
            "Bakar",
            "Bale – Valle",
            "Baška",
            "Baška Voda",
            "Biograd na Moru",
            "Bol",
            "Brela",
            "Buzet",
            "Cres",
            "Crikvenica",
            "Čakovec",
            "Dobrinj",
            "Dubrovnik",
            "Fažana – Fasana",
            "Funtana – Fontane",
            "Hvar",
            "Kanfanar",
            "Kastav",
            "Kaštelir-Labinci – Castelliere-S. Domenica",
            "Kolan",
            "Konavle",
            "Koprivnica",
            "Kostrena",
            "Krk",
            "Labin",
            "Ližnjan – Lisignano",
            "Makarska",
            "Mali Lošinj",
            "Malinska – Dubašnica",
            "Marčana",
            "Matulji",
            "Medulin",
            "Novalja",
            "Novigrad – Cittanova",
            "Omišalj",
            "Opatija",
            "Pazin",
            "Podstrana",
            "Poreč – Parenzo",
            "Pula – Pola",
            "Punat",
            "Rijeka",
            "Rovinj –Rovigno",
            "Samobor",
            "Split",
            "Stupnik",
            "Supetar",
            "Sutivan",
            "Sveta Nedelja (Zagrebačka županija)",
            "Tar Vabriga-TorreAbrega",
            "Umag – Umago",
            "Varaždin",
            "Velika Gorica",
            "Vir",
            "Viškovo",
            "Vodnjan – Dignano",
            "Vrbnik",
            "Vrsar – Orsera",
            "Zabok",
            "Zadar",
            "Zagreb",
            "Zaprešić",
            "Župa dubrovačka",
        ],
    ],
]
naselja = {grad: posto for posto, x in skupine for grad in x}

# Giving Choices

if "states" not in st.session_state:
    st.session_state.states = []

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
    MJESECNA_POTPORA = MJESECNA_RATA - MJESECNA_RATA_APN
    UKUPNI_IZNOS_POTPORE = round(MJESECNA_POTPORA * GODINA_POTPORE * 12, 2)

UKUPNI_KREDIT = round(MJESECNA_RATA * TRAJANJE * 12, 2)
UKUPNE_KAMATE = round(UKUPNI_KREDIT - IZNOS_KREDITA, 2)
UKUPNO_PLACENO = round(UKUPNI_KREDIT - UKUPNI_IZNOS_POTPORE, 2)
UKUPNA_CIJENA_NEKRETNINE = UKUPNO_PLACENO + UKUPNI_TROSKOVI

KREDIT_SUMMARY = {
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

st.write("""# Izračun""")
st.metric("""Anuitet u eurima""", value=str(round(MJESECNA_RATA, 2)) + " €")
st.metric(
    "Ukupna cijena nekretnine:",
    value=str(UKUPNA_CIJENA_NEKRETNINE) + " €",
    delta=str(round(UKUPNA_CIJENA_NEKRETNINE - CIJENA, 2)) + " €",
    delta_color="inverse",
)

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


def save_state():
    print()


increment = st.button("Save")
if increment:
    st.session_state.states.append(KREDIT_SUMMARY)

reset = st.button("Reset")
if reset:
    st.session_state.states = []
st.write(st.session_state.states)

