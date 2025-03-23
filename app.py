import streamlit as st
import zipfile
import os
import shutil
import uuid
import datetime
from logic.convert import convert_zip_to_pdf_and_word

st.set_page_config(page_title="Notion ➜ PDF/Word Converter", page_icon="📄")

st.image("static/logo.png", width=100)
st.title("Notion ➜ PDF/Word Converter")
st.markdown("Glissez votre **export Notion (.zip)** ici, personnalisez la couverture, choisissez les pages, et obtenez un PDF + Word 📄📝")

uploaded_file = st.file_uploader("Déposez votre fichier .zip", type="zip")

title = st.text_input("Titre du document", f"Export Notion – {datetime.date.today().isoformat()}")
author = st.text_input("Auteur", "Laurent Lefebvre")
custom_date = st.text_input("Date", datetime.date.today().strftime("%d/%m/%Y"))

if uploaded_file:
    with st.spinner("Analyse du fichier..."):
        session_id = str(uuid.uuid4())
        work_dir = f"temp/{session_id}"
        os.makedirs(work_dir, exist_ok=True)
        zip_path = os.path.join(work_dir, "notion.zip")

        with open(zip_path, "wb") as f:
            f.write(uploaded_file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(f"{work_dir}/extracted")

        md_files = [f for f in os.listdir(f"{work_dir}/extracted") if f.endswith(".md")]
        page_selection = st.multiselect("Sélectionnez les pages à inclure :", md_files, default=md_files)

        if st.button("📄 Générer le PDF & Word"):
            pdf_path, docx_path = convert_zip_to_pdf_and_word(
                f"{work_dir}/extracted", page_selection, title, author, custom_date, work_dir
            )

            with open(pdf_path, "rb") as f_pdf:
                st.download_button("📥 Télécharger le PDF", f_pdf, "Notion_Document.pdf")

            with open(docx_path, "rb") as f_docx:
                st.download_button("📝 Télécharger le Word", f_docx, "Notion_Document.docx")

            shutil.rmtree(work_dir)