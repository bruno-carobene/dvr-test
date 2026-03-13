import streamlit as st
from document_generator import genera_dvr
from supabase import create_client, Client
from datetime import datetime
import os

# === CONFIGURAZIONE SUPABASE ===
URL_SUPABASE = os.getenv("SUPABASE_URL")
KEY_SUPABASE = os.getenv("SUPABASE_KEY")

if not URL_SUPABASE or not KEY_SUPABASE:
    st.error("Errore: Variabili d'ambiente SUPABASE_URL o SUPABASE_KEY non trovate su Render!")
else:
    supabase: Client = create_client(URL_SUPABASE, KEY_SUPABASE)

# === LISTA 100 CODICI MONOUSO ===
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

# === FUNZIONI DATABASE ===
def verifica_codice_nel_db(codice):
    risposta = supabase.table("codici_usati").select("codice").eq("codice", codice).execute()
    return len(risposta.data) > 0

def registra_codice_usato(codice):
    supabase.table("codici_usati").insert({"codice": codice}).execute()

def log_dati_generazione(codice, azienda_data, ambienti, attrezzature, mansioni, chimici):
    try:
        data_to_save = {
            "codice_usato": codice,
            "nome_azienda": azienda_data.get("nome"),
            "partita_iva": azienda_data.get("Partita_Iva"),
            "codice_ateco": azienda_data.get("ateco"),
            "tipologia_azienda": azienda_data.get("tipologia"),
            "datore_lavoro": azienda_data.get("Datore_di_lavoro"),
            "via_sede_legale": azienda_data.get("indirizzo_legale"),      
            "comune_sede_legale": azienda_data.get("citta_legale"),      
            "provincia_sede_legale": azienda_data.get("provincia_legale"), 
            "ambienti_selezionati": ", ".join(ambienti),
            "attrezzature_selezionate": ", ".join(attrezzature),
            "mansioni_selezionate": ", ".join(mansioni),
            "agenti_chimici_selezionati": ", ".join(chimici),
            "tutti_i_dati_json": azienda_data 
        }
        supabase.table("log_generazioni").insert(data_to_save).execute()
    except Exception as e:
        st.error(f"Errore tecnico durante il salvataggio dei log: {e}")

# === FUNZIONE CONTROLLO ACCESSO ===
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    
    if st.session_state.password_correct:
        return True
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/logo-easywork.png", use_container_width=True)
        st.markdown("## 🔐 DVR Generator: accesso con password")
        st.markdown("##### Un progetto Easywork Italia Srl.")
        st.divider() 
        
        codice_inserito = st.text_input("Inserisci il tuo codice univoco", key="password_input")
   
        if st.button("Verifica ed Entra"):
            if codice_inserito not in CODICI_VALIDI:
                st.error("❌ Codice non valido.")
            else:
                if verifica_codice_nel_db(codice_inserito):
                    st.error("❌ Questo codice è già stato riscattato in precedenza.")
                else:
                    registra_codice_usato(codice_inserito)
                    st.session_state.password_correct = True
                    st.session_state.codice_usato = codice_inserito
                    st.success("✅ Codice accettato!")
                    st.rerun()
    return False

# Blocca l'app se non autenticato
if not check_password():
    st.stop()

# === CONFIGURAZIONE PAGINA ===
st.set_page_config(page_title="Generatore DVR", page_icon="📋", layout="wide")

# Header
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("assets/logo-easywork.png", width=400)

st.markdown("<h1 style='text-align: center;'>Generatore Documento di Valutazione Rischi (DVR)<br>Un progetto Easywork Italia S.r.l.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Compila il modulo per generare il documento di valutazione rischi personalizzato.</p>", unsafe_allow_html=True)

# Sidebar Logout
with st.sidebar:
    st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"] {width: 150px !important; min-width: 150px !important;}</style>""", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.password_correct = False
        st.rerun()
    st.markdown("---")

# Inizializzazione dati
if 'azienda_data' not in st.session_state:
    st.session_state.azienda_data = {}

# === SEZIONE 1: ANAGRAFICA ===
st.header("🏢 Anagrafica Aziendale")
st.subheader("🖼️ Logo Aziendale")
logo_caricato = st.file_uploader("Carica il logo della tua azienda", type=["png", "jpg", "jpeg"])

col_a, col_b = st.columns(2)
with col_a:
    nome = st.text_input("Nome dell'azienda *", key="nome")
    tipologia = st.text_input("Tipologia di azienda", key="tipologia")
    ateco = st.text_input("Codice ATECO", key="ateco")
    datore = st.text_input("Datore di lavoro *", key="datore")
    rspp = st.text_input("RSPP", key="rspp")
    rls = st.text_input("RLS", key="rls")
with col_b:
    piva = st.text_input("Partita IVA", key="piva")
    cf = st.text_input("Codice Fiscale", key="cf")
    medico = st.text_input("Medico competente", key="medico")
    antincendio = st.text_input("Incaricato antincendio", key="antincendio")
    primo_soccorso = st.text_input("Incaricato primo soccorso", key="primo_soccorso")
    orario = st.text_input("Orario di lavoro", key="orario")

st.subheader("📍 Sedi")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Sede Legale**")
    ind_legale = st.text_input("Via e numero civico", key="ind_legale")
    citta_legale = st.text_input("Comune", key="citta_legale")
    prov_legale = st.text_input("Provincia", key="prov_legale")
with c2:
    st.markdown("**Sede Operativa**")
    ind_op = st.text_input("Via e numero civico ", key="ind_op")
    citta_op = st.text_input("Comune ", key="citta_op")
    prov_op = st.text_input("Provincia ", key="prov_op")

attivita_desc = st.text_area("Descrizione attività", key="attivita")
locali = st.text_area("Struttura dei locali", key="locali")
terzi = st.text_input("Attività affidate a terzi", key="terzi")
terzi_svolte = st.text_input("Attività svolte presso terzi", key="terzi_svolte")

# === SEZIONE 2: AMBIENTI ===
st.header("🏭 Ambienti Aziendali")
ca1, ca2, ca3 = st.columns(3)
with ca1:
    ufficio = st.checkbox("Ufficio")
    magazzino = st.checkbox("Magazzino")
    palestre = st.checkbox("Palestre e locali annessi")
    sala_attivita = st.checkbox("Sala attività associazione")
with ca2:
    dehors = st.checkbox("Dehors esterno - tensostruttura")
    area_bar = st.checkbox("Area bar e ristoro")
    locale_quadri = st.checkbox("Locale quadri elettrici")
    locali_spogliatoio = st.checkbox("Locali spogliatoio")
with ca3:
    tribuna = st.checkbox("Tribuna")
    locali_caldaia = st.checkbox("Locali caldaia")
    altro_amb = st.text_input("Altro (specificare)")

st.header("📸 Foto Ambienti (Opzionale)")
foto_ambienti = []
file_caricati = st.file_uploader("Carica foto", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
if file_caricati:
    for i, file in enumerate(file_caricati):
        col_img, col_txt = st.columns([1, 2])
        with col_img: st.image(file, width=150)
        with col_txt:
            didascalia = st.text_input(f"Didascalia foto {i+1}", key=f"cap_{i}")
            foto_ambienti.append({"file": file, "caption": didascalia})

# === SEZIONE 3: ATTREZZATURE ===
st.header("🔧 Attrezzature Impiegate")
# (Cucina)
st.markdown("**Cucina e Ristorazione**")
ct1, ct2, ct3 = st.columns(3)
with ct1:
    att_cucina = st.checkbox("Attrezzature cucina")
    att_cucina_man = st.checkbox("Attrezzi manuali cucina")
    forno_micro = st.checkbox("Forno microonde")
with ct2:
    forno_elettr = st.checkbox("Forno elettrico")
    frigorifero = st.checkbox("Frigorifero")
    macchina_caffe = st.checkbox("Macchina caffè bar")
with ct3:
    macchina_ghiaccio = st.checkbox("Macchina ghiaccio")
    piastra_toast = st.checkbox("Piastra toast/panini")

# (Ufficio)
st.markdown("**Ufficio e Tecnologia**")
ct4, ct5, ct6 = st.columns(3)
with ct4:
    registratore = st.checkbox("Registratore cassa")
    videoterm = st.checkbox("Videoterminali")
    att_ufficio = st.checkbox("Attrezzi manuali ufficio")
with ct5:
    stampante_laser = st.checkbox("Stampante laser")
    stampante_ink = st.checkbox("Stampante getto inchiostro")
    telefono = st.checkbox("Telefono/Cellulare")
with ct6:
    pc = st.checkbox("PC fisso/portatile")
    tablet = st.checkbox("Tablet")

# (Logistica/Sport)
st.markdown("**Logistica, Sport e Pulizia**")
ct7, ct8 = st.columns(2)
with ct7:
    scaffali = st.checkbox("Scaffali metallici")
    att_sport = st.checkbox("Attrezzi sportivi")
    att_pulizia = st.checkbox("Attrezzi pulizia")
with ct8:
    autoveicoli = st.checkbox("Autoveicoli")
    motoveicoli = st.checkbox("Motoveicoli")
    scala = st.checkbox("Scala portatile doppia")
altro_att = st.text_input("Altre attrezzature")

# === SEZIONE 4: MANSIONI ===
st.header("👷 Mansioni Presenti")
cm1, cm2 = st.columns(2)
with cm1:
    addetto_bar = st.checkbox("Addetto bar")
    aiuto_cuoco = st.checkbox("Addetto cucina/aiutocuoco")
    resp_sala = st.checkbox("Responsabile sala")
    reception = st.checkbox("Addetto reception")
    customer = st.checkbox("Addetto customer service")
with cm2:
    dirigente = st.checkbox("Dirigente")
    imp_admin = st.checkbox("Impiegato amministrativo")
    impiegato = st.checkbox("Impiegato")
    segretario = st.checkbox("Segretario/a")

cm3, cm4 = st.columns(2)
with cm3:
    istruttore = st.checkbox("Istruttore/allenatore")
    bagnino = st.checkbox("Bagnino")
    estetista = st.checkbox("Estetista")
    parrucchiere = st.checkbox("Parrucchiere")
with cm4:
    add_servizi = st.checkbox("Addetto ai servizi")
    add_pulizia = st.checkbox("Addetto pulizia base")
    minuta_man = st.checkbox("Addetto minuta manutenzione")
    manutenzione = st.checkbox("Addetto manutenzione tuttofare")
    magazzino_man = st.checkbox("Addetto magazzino")
    operaio = st.checkbox("Operaio generico")
altra_mansione = st.text_input("Altra mansione")

# === SEZIONE 5: AGENTI CHIMICI ===
st.header("🧪 Agenti Chimici")
cc1, cc2, cc3 = st.columns(3)
with cc1:
    acidi = st.checkbox("Acidi")
    alcool = st.checkbox("Alcool")
    ammoniaca = st.checkbox("Ammoniaca")
    candeggina = st.checkbox("Candeggina")
with cc2:
    det_forni = st.checkbox("Detergente forni")
    det_stov = st.checkbox("Detergente stoviglie")
    det_lavast = st.checkbox("Detergente lavastoviglie")
    det_pav = st.checkbox("Detergente pavimenti")
with cc3:
    det_wc = st.checkbox("Detergente WC")
    grasso_lub = st.checkbox("Grasso lubrificante")
    toner = st.checkbox("Toner")
    tinta = st.checkbox("Tinta capelli")

# Altri chimici mappatura rapida
anticorrosivo = st.checkbox("Anticorrosivo")
antiruggine = st.checkbox("Antiruggine")
argon = st.checkbox("Argon")
azoto = st.checkbox("Azoto")
fumi_sald = st.checkbox("Fumi saldatura")
lubr_spray = st.checkbox("Lubrificanti spray")
polveri = st.checkbox("Polveri molatura")
acquaragia = st.checkbox("Acquaragia")
catalizzatore = st.checkbox("Catalizzatore")
det_carrozz = st.checkbox("Detergente carrozzeria")
fondo_vern = st.checkbox("Fondo vernice")
primer = st.checkbox("Primer")
vernice_spray = st.checkbox("Vernice spray")
benzina = st.checkbox("Benzina")
gasolio = st.checkbox("Gasolio")

# === GENERAZIONE ===
st.divider()
if st.button("Genera DVR", type="primary", use_container_width=True):
    if not nome or not datore:
        st.error("❌ Nome azienda e Datore di lavoro obbligatori!")
    else:
        with st.spinner("Generazione in corso..."):
            azienda_data = {
                "nome": nome, "tipologia": tipologia, "ateco": ateco,
                "Datore_di_lavoro": datore, "RSPP": rspp, "RLS": rls,
                "Partita_Iva": piva, "Codice_fiscale": cf, "Medico": medico,
                "Incaricato_antincendio": antincendio, "Incaricato_primo_soccorso": primo_soccorso,
                "Orario": orario, "indirizzo_legale": ind_legale, "citta_legale": citta_legale,
                "provincia_legale": prov_legale, "indirizzo_operativo": ind_op,
                "citta_operativa": citta_op, "provincia_operativa": prov_op,
                "Attivita": attivita_desc, "locali": locali, "terzi": terzi, "terzi_svolte": terzi_svolte
            }
            
            ambienti = [k for k,v in {"ufficio":ufficio, "magazzino":magazzino, "palestre":palestre, "sala_attivita":sala_attivita, "dehors":dehors, "area_bar":area_bar, "locale_quadri":locale_quadri, "spogliatoi":locali_spogliatoio, "tribuna":tribuna, "caldaia":locali_caldaia}.items() if v]
            if altro_amb: ambienti.append(altro_amb)
            
            attrezzature = [k for k,v in {"cucina":att_cucina, "cucina_man":att_cucina_man, "microonde":forno_micro, "forno_el":forno_elettr, "frigo":frigorifero, "caffe":macchina_caffe, "ghiaccio":macchina_ghiaccio, "piastra":piastra_toast, "cassa":registratore, "vdt":videoterm, "ufficio_man":att_ufficio, "laser":stampante_laser, "inkjet":stampante_ink, "tel":telefono, "pc":pc, "tablet":tablet, "scaffali":scaffali, "sport":att_sport, "pulizia":att_pulizia, "auto":autoveicoli, "moto":motoveicoli, "scala":scala}.items() if v]
            if altro_att: attrezzature.append(altro_att)
            
            mansioni = [k for k,v in {"bar":addetto_bar, "cucina":aiuto_cuoco, "sala":resp_sala, "reception":reception, "customer":customer, "dirigente":dirigente, "admin":imp_admin, "impiegato":impiegato, "segretario":segretario, "istruttore":istruttore, "bagnino":bagnino, "estetista":estetista, "parrucchiere":parrucchiere, "servizi":add_servizi, "pulizia":add_pulizia, "minuta_man":minuta_man, "manutenzione":manutenzione, "magazzino":magazzino_man, "operaio":operaio}.items() if v]
            if altra_mansione: mansioni.append(altra_mansione)

            agenti_chimici = [v for k,v in {"acidi":"Acidi","alcool":"Alcool","ammoniaca":"Ammoniaca","candeggina":"Candeggina","det_forni":"Detergente forni","det_stov":"Detergente stoviglie","det_lavast":"Detergente lavastoviglie","det_pav":"Detergente pavimenti","det_wc":"Detergente WC","anticorrosivo":"Anticorrosivo","antiruggine":"Antiruggine","argon":"Argon","azoto":"Azoto","fumi_sald":"Fumi saldatura","grasso_lub":"Grasso lubrificante","lubr_spray":"Lubrificanti spray","polveri":"Polveri molatura","acquaragia":"Acquaragia","catalizzatore":"Catalizzatore","det_carrozz":"Detergente carrozzeria","fondo_vern":"Fondo vernice","primer":"Primer","vernice_spray":"Vernice spray","benzina":"Benzina","gasolio":"Gasolio","toner":"Toner","tinta":"Tinta capelli"}.items() if locals().get(k)]

            # SALVATAGGIO LOG SU SUPABASE
            log_dati_generazione(st.session_state.codice_usato, azienda_data, ambienti, attrezzature, mansioni, agenti_chimici)
            
            try:
                doc_buffer = genera_dvr(azienda_data, ambienti, attrezzature, mansioni, agenti_chimici, "templates", logo_file=logo_caricato, foto_ambienti=foto_ambienti)
                filename = f"DVR_{nome.replace(' ', '_')}_{datetime.now().strftime('%d-%m-%Y')}.docx"
                st.success("✅ Generato!")
                st.download_button("📥 Scarica DVR", data=doc_buffer, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            except Exception as e:
                st.error(f"❌ Errore: {e}")




