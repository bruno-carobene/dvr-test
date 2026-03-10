import streamlit as st
from document_generator import genera_dvr
from datetime import datetime
import os

# === CONFIGURAZIONE CODICI MONOUSO ===
import os

# Incolla qui i tuoi 100 codici. Se il codice è in questa lista, può entrare.
# === CONFIGURAZIONE CODICI MONOUSO ===
CODICI_VALIDI = [
    "EW-72A1-9XB", "EW-15K2-4ML", "EW-88P3-7RT", "EW-24V4-1NQ", "EW-63S5-8DP",
    "EW-41G6-2WY", "EW-90J7-5KH", "EW-37B8-9CV", "EW-52M9-1XZ", "EW-19R0-4BF",
    "EW-81T1-6NQ", "EW-27H2-8PL", "EW-66D3-3KJ", "EW-45F4-7HG", "EW-93G5-1VX",
    "EW-32S6-4TR", "EW-74K7-9NM", "EW-11L8-2DB", "EW-58P9-5CX", "EW-22V0-8RQ",
    "EW-85M1-3YF", "EW-39T2-7KG", "EW-61B3-1PH", "EW-48D4-4SJ", "EW-95H5-9WL",
    "EW-26G6-2VX", "EW-77J7-5RT", "EW-14K8-8NM", "EW-53S9-1DP", "EW-89P0-4KJ",
    "EW-31L1-7TR", "EW-64V2-9BQ", "EW-42F3-2HG", "EW-91D4-5SJ", "EW-35M5-8YF",
    "EW-70T6-1KG", "EW-18B7-4PH", "EW-55H8-7WL", "EW-82G9-9VX", "EW-29K0-2NM",
    "EW-67S1-5DP", "EW-46P2-8KJ", "EW-94L3-1TR", "EW-33V4-4BQ", "EW-71F5-7HG",
    "EW-12D6-9SJ", "EW-59M7-2YF", "EW-23T8-5KG", "EW-86B9-8PH", "EW-40H0-1WL",
    "EW-62G1-4VX", "EW-49K2-7NM", "EW-96S3-9DP", "EW-25P4-2KJ", "EW-78L5-5TR",
    "EW-13V6-8BQ", "EW-54F7-1HG", "EW-87D8-4SJ", "EW-36M9-7YF", "EW-92T0-9KG",
    "EW-30B1-2PH", "EW-65H2-5WL", "EW-43G3-8VX", "EW-97K4-1NM", "EW-28S5-4DP",
    "EW-73P6-7KJ", "EW-16L7-9TR", "EW-51V8-2BQ", "EW-84F9-5HG", "EW-38D0-8SJ",
    "EW-60M1-1YF", "EW-47T2-4KG", "EW-99B3-7PH", "EW-21H4-9WL", "EW-75G5-2VX",
    "EW-10K6-5NM", "EW-57S7-8DP", "EW-20P8-1KJ", "EW-83L9-4TR", "EW-44V0-7BQ",
    "EW-68F1-9HG", "EW-34D2-2SJ", "EW-79M3-5YF", "EW-17T4-8KG", "EW-56B5-1PH",
    "EW-80H6-4WL", "EW-24G7-7VX", "EW-69K8-9NM", "EW-41S9-2DP", "EW-90P0-5KJ",
    "EW-37L1-8TR", "EW-72V2-1BQ", "EW-15F3-4HG", "EW-52D4-7SJ", "EW-88M5-9YF",
    "EW-31T6-2KG", "EW-64B7-5PH", "EW-42H8-8WL", "EW-91G9-1VX", "EW-35K0-4NM"
]

FILE_USATI = "codici_usati.txt"

def leggi_codici_usati():
    if not os.path.exists(FILE_USATI):
        return set()
    with open(FILE_USATI, "r") as f:
        return set(line.strip() for line in f)

def salva_codice_usato(codice):
    with open(FILE_USATI, "a") as f:
        f.write(f"{codice}\n")
# CONTROLLO PASSWORD
def check_password():
    """Verifica il codice monouso e gestisce il login"""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔐 Accesso Monouso")
        st.image("https://raw.githubusercontent.com/bruno-carobene/dvr-generator/main/assets/logo-easywork.png", use_column_width=True)
        st.markdown("### Generatore DVR")
        st.info("Inserisci il tuo codice univoco. Una volta usato, il codice scadrà.")
        
        codice_inserito = st.text_input("Codice di Accesso", type="default", key="password_input")
        
        if st.button("Accedi", use_container_width=True):
            usati = leggi_codici_usati()
            
            if codice_inserito in usati:
                st.error("❌ Questo codice è già stato utilizzato.")
            elif codice_inserito in CODICI_VALIDI:
                salva_codice_usato(codice_inserito)
                st.session_state.password_correct = True
                st.success("✅ Codice valido! Accesso in corso...")
                st.rerun()
            else:
                st.error("❌ Codice non valido. Riprova.")
        
        st.caption("© Easywork - Servizio Generazione DVR")
    return False

# === VERIFICA ACCESSO ===
if not check_password():
    st.stop()  # Blocca esecuzione se non loggato

# === INIZIO APP (dopo login) ===
st.set_page_config(
    page_title="Generatore DVR",
    page_icon="📋",
    layout="wide"
)

# Logo in header (più piccolo)
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("https://raw.githubusercontent.com/bruno-carobene/dvr-generator/main/assets/logo-easywork.png", 
             width=400)

# Titolo centrato
st.markdown("""
    <h1 style='text-align: center;'>
        Generatore Documento di Valutazione Rischi (DVR)<br>
        Un progetto Easywork Italia S.r.l.
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center;'>
        Compila il modulo per generare il documento di valutazione rischi personalizzato.
    </p>
""", unsafe_allow_html=True)

# Pulsante logout (opzionale, in sidebar)
with st.sidebar:
    # RESTRINGI sidebar al minimo
    st.markdown("""
        <style>
        /* Sidebar chiusa (mobile) */
        [data-testid="stSidebar"][aria-expanded="false"] {
            width: 0 !important;
            min-width: 0 !important;
        }
        
        /* Sidebar aperta (desktop) - REGOLA QUESTO VALORE */
        [data-testid="stSidebar"][aria-expanded="true"] {
            width: 150px !important;
            min-width: 150px !important;
            max-width: 150px !important;
        }
        
        /* Contenuto interno sidebar */
        [data-testid="stSidebar"][aria-expanded="true"] > div {
            width: 150px !important;
        }
        
        /* Rimuovi padding eccessivo */
        .css-1d391kg, .css-1lcbmhc {
            padding: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.password_correct = False
        st.rerun()
    st.markdown("---")

# Inizializza session state per i dati
if 'azienda_data' not in st.session_state:
    st.session_state.azienda_data = {}

# === SEZIONE 1: ANAGRAFICA AZIENDA ===
st.header("🏢 Anagrafica Aziendale")

# Caricamento Logo
st.subheader("🖼️ Logo Aziendale")
logo_caricato = st.file_uploader("Se lo desideri, carica il logo della tua azienda", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome dell'azienda *", key="nome")
    tipologia = st.text_input("Tipologia di azienda", key="tipologia")
    ateco = st.text_input("Codice ATECO", key="ateco")
    datore = st.text_input("Datore di lavoro *", key="datore")
    rspp = st.text_input("RSPP", key="rspp")
    rls = st.text_input("RLS", key="rls")
    
with col2:
    piva = st.text_input("Partita IVA", key="piva")
    cf = st.text_input("Codice Fiscale", key="cf")
    medico = st.text_input("Medico competente", key="medico")
    antincendio = st.text_input("Incaricato antincendio", key="antincendio")
    primo_soccorso = st.text_input("Incaricato primo soccorso", key="primo_soccorso")
    orario = st.text_input("Orario di lavoro", key="orario")

# Indirizzi
st.subheader("📍 Sedi")
col3, col4 = st.columns(2)
with col3:
    st.markdown("**Sede Legale**")
    ind_legale = st.text_input("Via e numero civico", key="ind_legale")
    citta_legale = st.text_input("Comune", key="citta_legale")
    prov_legale = st.text_input("Provincia", key="prov_legale")

with col4:
    st.markdown("**Sede Operativa**")
    ind_op = st.text_input("Via e numero civico ", key="ind_op")
    citta_op = st.text_input("Comune ", key="citta_op")
    prov_op = st.text_input("Provincia ", key="prov_op")

# Descrizione attività
st.subheader("📝 Descrizione Attività")
attivita_desc = st.text_area("Descrivi brevemente il settore di attività della tua azienda", key="attivita")
locali = st.text_area("Struttura dei locali", key="locali")
terzi = st.text_input("Specifica se vi sono attività affidate a terzi", key="terzi")
terzi_svolte = st.text_input("Specifica se vi sono attività svolte presso terzi", key="terzi_svolte")

# === SEZIONE 2: AMBIENTI ===
st.header("🏭 Ambienti Aziendali")

st.markdown("Seleziona gli ambienti utilizzati per la tua attività:")

col_amb1, col_amb2, col_amb3 = st.columns(3)

with col_amb1:
    ufficio = st.checkbox("Ufficio")
    magazzino = st.checkbox("Magazzino")
    palestre = st.checkbox("Palestre e locali annessi")
    sala_attivita = st.checkbox("Sala attività associazione")

with col_amb2:
    dehors = st.checkbox("Dehors esterno - tensostruttura")
    area_bar = st.checkbox("Area bar e ristoro")
    locale_quadri = st.checkbox("Locale quadri elettrici")
    locali_spogliatoio = st.checkbox("Locali spogliatoio")

with col_amb3:
    tribuna = st.checkbox("Tribuna")
    locali_caldaia = st.checkbox("Locali caldaia")
    altro_amb = st.text_input("Altro (specificare)")

# === AGGIUNTA DOPO LA SEZIONE 2: AMBIENTI (app.py) ===
st.header("📸 Foto Ambienti di Lavoro (Opzionale)")
st.info("Puoi caricare file esistenti, o scattare foto se sei su mobile, per mostrare gli ambienti di lavoro della tua azienda.")

foto_ambienti = []
file_caricati = st.file_uploader("Carica o scatta foto degli ambienti", 
                                  type=["png", "jpg", "jpeg"], 
                                  accept_multiple_files=True)

if file_caricati:
    for i, file in enumerate(file_caricati):
        col_img, col_txt = st.columns([1, 2])
        with col_img:
            st.image(file, width=150)
        with col_txt:
            didascalia = st.text_input(f"Didascalia per la foto {i+1}", 
                                       placeholder="Es: Uffici Amministrativi", 
                                       key=f"cap_{i}")
            foto_ambienti.append({"file": file, "caption": didascalia})

# === SEZIONE 3: ATTREZZATURE ===
st.header("🔧 Attrezzature Impiegate")

st.markdown("**Cucina e Ristorazione**")
col_att1, col_att2, col_att3 = st.columns(3)
with col_att1:
    att_cucina = st.checkbox("Attrezzature cucina")
    att_cucina_man = st.checkbox("Attrezzi manuali cucina")
    forno_micro = st.checkbox("Forno microonde")
with col_att2:
    forno_elettr = st.checkbox("Forno elettrico")
    frigorifero = st.checkbox("Frigorifero")
    macchina_caffe = st.checkbox("Macchina caffè bar")
with col_att3:
    macchina_ghiaccio = st.checkbox("Macchina ghiaccio")
    piastra_toast = st.checkbox("Piastra toast/panini")

st.markdown("**Ufficio e Tecnologia**")
col_att4, col_att5, col_att6 = st.columns(3)
with col_att4:
    registratore = st.checkbox("Registratore cassa")
    videoterm = st.checkbox("Videoterminali")
    att_ufficio = st.checkbox("Attrezzi manuali ufficio")
with col_att5:
    stampante_laser = st.checkbox("Stampante laser")
    stampante_ink = st.checkbox("Stampante getto inchiostro")
    telefono = st.checkbox("Telefono/Cellulare")
with col_att6:
    pc = st.checkbox("PC fisso/portatile")
    tablet = st.checkbox("Tablet")

st.markdown("**Logistica, Sport e Pulizia**")
col_att7, col_att8 = st.columns(2)
with col_att7:
    scaffali = st.checkbox("Scaffali metallici")
    att_sport = st.checkbox("Attrezzi sportivi")
    att_pulizia = st.checkbox("Attrezzi pulizia")
with col_att8:
    autoveicoli = st.checkbox("Autoveicoli")
    motoveicoli = st.checkbox("Motoveicoli")
    scala = st.checkbox("Scala portatile doppia")

altro_att = st.text_input("Altre attrezzature (specificare)")

# === SEZIONE 4: MANSIONI ===
st.header("👷 Mansioni Presenti")

st.markdown("**Ristorazione e Accoglienza**")
col_man1, col_man2 = st.columns(2)
with col_man1:
    addetto_bar = st.checkbox("Addetto bar")
    aiuto_cuoco = st.checkbox("Addetto cucina/aiutocuoco")
    resp_sala = st.checkbox("Responsabile sala")
with col_man2:
    reception = st.checkbox("Addetto reception")
    customer = st.checkbox("Addetto customer service")

st.markdown("**Amministrazione e Dirigenza**")
col_man3, col_man4 = st.columns(2)
with col_man3:
    dirigente = st.checkbox("Dirigente")
    imp_admin = st.checkbox("Impiegato amministrativo")
with col_man4:
    impiegato = st.checkbox("Impiegato")
    segretario = st.checkbox("Segretario/a")

st.markdown("**Sport e Benessere**")
col_man5, col_man6 = st.columns(2)
with col_man5:
    istruttore = st.checkbox("Istruttore/allenatore/preparatore")
    bagnino = st.checkbox("Bagnino")
with col_man6:
    estetista = st.checkbox("Estetista")
    parrucchiere = st.checkbox("Parrucchiere")

st.markdown("**Servizi e Manutenzione**")
col_man7, col_man8 = st.columns(2)
with col_man7:
    add_servizi = st.checkbox("Addetto ai servizi")
    add_pulizia = st.checkbox("Addetto pulizia base")
    minuta_man = st.checkbox("Addetto minuta manutenzione")
with col_man8:
    manutenzione = st.checkbox("Addetto manutenzione/tuttofare")
    magazzino = st.checkbox("Addetto magazzino")
    operaio = st.checkbox("Operaio generico")

altra_mansione = st.text_input("Altra mansione (specificare)")

# === SEZIONE 5: AGENTI CHIMICI ===
st.header("🧪 Agenti Chimici")

st.markdown("**Pulizia, Igiene e Ristorazione**")
col_ch1, col_ch2, col_ch3 = st.columns(3)
with col_ch1:
    acidi = st.checkbox("Acidi per laboratori didattici")
    alcool = st.checkbox("Alcool etilico")
    ammoniaca = st.checkbox("Ammoniaca")
with col_ch2:
    candeggina = st.checkbox("Candeggina")
    det_forni = st.checkbox("Detergente disincrostante forni")
    det_stov = st.checkbox("Detergente stoviglie")
with col_ch3:
    det_lavast = st.checkbox("Detergente lavastoviglie")
    det_pav = st.checkbox("Detergente pavimenti")
    det_wc = st.checkbox("Detergente WC")

st.markdown("**Officina, Manutenzione e Gas**")
col_ch4, col_ch5 = st.columns(2)
with col_ch4:
    anticorrosivo = st.checkbox("Anticorrosivo")
    antiruggine = st.checkbox("Antiruggine")
    argon = st.checkbox("Argon")
    azoto = st.checkbox("Azoto")
with col_ch5:
    fumi_sald = st.checkbox("Fumi di saldatura")
    grasso_lub = st.checkbox("Grasso lubrificante")
    lubr_spray = st.checkbox("Lubrificanti spray")
    polveri = st.checkbox("Polveri da molatura")

st.markdown("**Verniciatura e Carrozzeria**")
col_ch6, col_ch7 = st.columns(2)
with col_ch6:
    acquaragia = st.checkbox("Acquaragia")
    catalizzatore = st.checkbox("Catalizzatore vernici")
    det_carrozz = st.checkbox("Detergente carrozzerie")
with col_ch7:
    fondo_vern = st.checkbox("Fondo verniciatura")
    primer = st.checkbox("Primer verniciatura")
    vernice_spray = st.checkbox("Vernice spray")

st.markdown("**Carburanti e Altro**")
col_ch8, col_ch9 = st.columns(2)
with col_ch8:
    benzina = st.checkbox("Benzina")
    gasolio = st.checkbox("Gasolio")
with col_ch9:
    toner = st.checkbox("Toner")
    tinta = st.checkbox("Tinta per capelli")

# === PULSANTE GENERAZIONE ===
st.divider()
st.header("🚀 Generazione Documento")

if st.button("Genera DVR", type="primary", use_container_width=True):
    
    # Verifica campi obbligatori
    if not nome or not datore:
        st.error("❌ Compila i campi obbligatori (Nome azienda e Datore di lavoro)")
    else:
        with st.spinner("Generazione documento in corso..."):
            
            # Prepara dizionario azienda
            azienda_data = {
                "nome": nome,
                "tipologia": tipologia,
                "ateco": ateco,
                "Datore_di_lavoro": datore,
                "RSPP": rspp,
                "RLS": rls,
                "indirizzo_legale": ind_legale,
                "citta_legale": citta_legale,
                "provincia_legale": prov_legale,
                "indirizzo_operativo": ind_op,
                "citta_operativa": citta_op,
                "provincia_operativa": prov_op,
                "Incaricato_antincendio": antincendio,
                "Indirizzo_sede": ind_op or ind_legale,
                "Attivita": attivita_desc,
                "Partita_Iva": piva,
                "Codice_fiscale": cf,
                "Orario": orario,
                "Medico": medico,
                "Incaricato_primo_soccorso": primo_soccorso,
                "locali": locali,
                "terzi": terzi,
                "terzi_svolte": terzi_svolte
            }
            
            # Prepara liste
            ambienti = []
            if ufficio: ambienti.append("ufficio")
            if magazzino: ambienti.append("magazzino")
            if palestre: ambienti.append("palestre_locali_annessi")
            if sala_attivita: ambienti.append("sala_attivita_associazione")
            if dehors: ambienti.append("dehors_esterno")
            if area_bar: ambienti.append("area_bar_ristoro")
            if locale_quadri: ambienti.append("locale_quadri_elettrici")
            if locali_spogliatoio: ambienti.append("locali_spogliatoio")
            if tribuna: ambienti.append("tribuna")
            if locali_caldaia: ambienti.append("locali_caldaia")
            if altro_amb: ambienti.append(altro_amb.lower().replace(" ", "_"))
            
            attrezzature = []
            if att_cucina: attrezzature.append("attrezzature_cucina")
            if att_cucina_man: attrezzature.append("attrezzi_manuali_cucina")
            if forno_micro: attrezzature.append("forno_microonde")
            if forno_elettr: attrezzature.append("forno_elettrico")
            if frigorifero: attrezzature.append("frigorifero")
            if macchina_caffe: attrezzature.append("macchina_caffe_bar")
            if macchina_ghiaccio: attrezzature.append("macchina_ghiaccio")
            if piastra_toast: attrezzature.append("piastra_toast_panini")
            if registratore: attrezzature.append("registratore_cassa")
            if videoterm: attrezzature.append("videoterminali")
            if att_ufficio: attrezzature.append("attrezzi_manuali_ufficio")
            if stampante_laser: attrezzature.append("stampante_laser")
            if stampante_ink: attrezzature.append("stampante_getto_inchiostro")
            if telefono: attrezzature.append("telefono_cellulare")
            if pc: attrezzature.append("pc_fisso_portatile")
            if tablet: attrezzature.append("tablet")
            if scaffali: attrezzature.append("scaffali_metallici")
            if att_sport: attrezzature.append("attrezzi_sportivi")
            if att_pulizia: attrezzature.append("attrezzi_pulizia")
            if autoveicoli: attrezzature.append("autoveicoli")
            if motoveicoli: attrezzature.append("motoveicoli")
            if scala: attrezzature.append("scala_portatile_doppia")
            if altro_att: attrezzature.append(altro_att.upper())
            
            mansioni = []
            if addetto_bar: mansioni.append("addetto_bar")
            if aiuto_cuoco: mansioni.append("addetto_cucina_aiutocuoco")
            if resp_sala: mansioni.append("responsabile_sala")
            if reception: mansioni.append("addetto_reception")
            if customer: mansioni.append("addetto_customer_service")
            if dirigente: mansioni.append("dirigente")
            if imp_admin: mansioni.append("impiegato_amministrativo")
            if impiegato: mansioni.append("impiegato")
            if segretario: mansioni.append("segretario_a")
            if istruttore: mansioni.append("istruttore_allenatore_preparatore")
            if bagnino: mansioni.append("bagnino")
            if estetista: mansioni.append("estetista")
            if parrucchiere: mansioni.append("parrucchiere")
            if add_servizi: mansioni.append("addetto_ai_servizi")
            if add_pulizia: mansioni.append("addetto_pulizia_base")
            if minuta_man: mansioni.append("addetto_minuta_manutenzione")
            if manutenzione: mansioni.append("addetto_manutenzione_tuttofare_officina")
            if magazzino: mansioni.append("addetto_magazzino")
            if operaio: mansioni.append("operaio_generico")
            if altra_mansione: mansioni.append(altra_mansione.upper())
            
            # Mappatura agenti chimici
            m_chem = {
                "acidi": "Acidi per laboratori didattici",
                "alcool": "Alcool etilico",
                "ammoniaca": "Ammoniaca",
                "candeggina": "Candeggina",
                "det_forni": "Detergente disincrostante forni",
                "det_stov": "Detergente stoviglie a mano",
                "det_lavast": "Detergente lavastoviglie",
                "det_pav": "Detergente per pavimenti",
                "det_wc": "Detergente per WC",
                "anticorrosivo": "Anticorrosivo",
                "antiruggine": "Antiruggine",
                "argon": "Argon",
                "azoto": "Azoto",
                "fumi_sald": "Fumi di saldatura",
                "grasso_lub": "Grasso lubrificante",
                "lubr_spray": "Lubrificanti spray (Svitol/Grasso)",
                "polveri": "Polveri da molatura",
                "acquaragia": "Acquaragia",
                "catalizzatore": "Catalizzatore vernici veicoli",
                "det_carrozz": "Detergente lucidatura carrozzerie",
                "fondo_vern": "Fondo verniciatura veicoli",
                "primer": "Primer verniciatura veicoli",
                "vernice_spray": "Vernice spray",
                "benzina": "Benzina",
                "gasolio": "Gasolio",
                "toner": "Toner",
                "tinta": "Tinta per capelli"
            }
            
            agenti_chimici = []
            for var, name in m_chem.items():
                if locals().get(var):
                    agenti_chimici.append(name)
            
            try:
                # Genera documento
                templates_dir = "templates"
                doc_buffer = genera_dvr(
                    azienda_data, 
                    ambienti, 
                    attrezzature, 
                    mansioni, 
                    agenti_chimici,
                    templates_dir,
                    logo_file=logo_caricato,       # Nuovo
                    foto_ambienti=foto_ambienti    # Nuovo
                )
                
                # Nome file
                filename = f"DVR_{nome.replace(' ', '_')}_{datetime.now().strftime('%d-%m-%Y')}.docx"
                
                st.success("✅ Documento generato con successo!")
                
                # Download button
                st.download_button(
                    label="📥 Scarica Documento DVR",
                    data=doc_buffer,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
                # Istruzioni sommario
                st.info("""
                📋 **Il vostro documento:**  
                Puoi ora scaricare il file docx che è stato generato.
                1. Leggilo con attenzione
                2. E' un file editabile e può essere corretto in ogni sua parte
                3. Il documento deve essere stampato e firmato dai referenti.
                """)
                
                # Riepilogo
                with st.expander("📋 Riepilogo selezioni"):
                    st.write(f"**Ambienti:** {len(ambienti)} selezionati")
                    st.write(f"**Attrezzature:** {len(attrezzature)} selezionate")  
                    st.write(f"**Mansioni:** {len(mansioni)} selezionate")
                    st.write(f"**Agenti chimici:** {len(agenti_chimici)} selezionati")
                    
            except Exception as e:
                st.error(f"❌ Errore durante la generazione: {str(e)}")
                st.exception(e)

















