# --- APPLICATION WEB INTERACTIVE DES SOLDES SECTORIELS (Version sans Plotly) ---

import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(layout="wide", page_title="Carte des Modèles Économiques")

# --- 1. CHARGEMENT ET PRÉPARATION DES DONNÉES ---
@st.cache_data
def load_data():
    excel_file = "donnees_macro_1980-2029_filtrees.xlsx"
    try:
        df = pd.read_excel(excel_file)
        df.columns = df.columns.str.strip()
        df.rename(columns={'Année': 'Year', 'Pays': 'Country', 'SoldeCourant': 'CurrentAccountBalance', 'SoldeBudgétaire': 'BudgetBalance'}, inplace=True)
        for col in ['CurrentAccountBalance', 'BudgetBalance', 'PIB/habitant']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=['CurrentAccountBalance', 'BudgetBalance', 'Country', 'Year'], inplace=True)
        df['Year'] = df['Year'].astype(int)
        return df
    except FileNotFoundError:
        st.error(f"ERREUR : Le fichier de données '{excel_file}' est introuvable.")
        return pd.DataFrame()

df_all = load_data()

# --- 2. PANNEAU DE CONTRÔLE DANS LA BARRE LATÉRALE ---
st.sidebar.title("Panneau de Contrôle")
annees_disponibles = sorted(df_all['Year'].unique())

# On utilise un slider simple pour sélectionner UNE SEULE année (pas d'animation)
annee_choisie = st.sidebar.slider(
    'Sélectionnez une année :',
    min_value=min(annees_disponibles),
    max_value=max(annees_disponibles),
    value=max(annees_disponibles)
)

groupes_de_pays = {
    "Monde Entier": sorted(df_all['Country'].unique()),
    "G7": ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States'],
}
groupe_choisi = st.sidebar.selectbox("Choisir un groupe de pays :", options=list(groupes_de_pays.keys()))
pays_selectionnes = st.sidebar.multiselect("Choisir un ou plusieurs pays :", options=groupes_de_pays[groupe_choisi], default=groupes_de_pays[groupe_choisi])

# --- 3. FILTRAGE FINAL DES DONNÉES ---
df_display = df_all[
    (df_all['Year'] == annee_choisie) &
    (df_all['Country'].isin(pays_selectionnes))
].copy()

# --- 4. AFFICHAGE DE L'APPLICATION ---
st.title("Carte Statique des Modèles Économiques Mondiaux")
st.markdown(f"Visualisation de **{len(pays_selectionnes)} pays** pour l'année **{annee_choisie}**.")

if df_display.empty:
    st.warning("Aucune donnée disponible pour la sélection et l'année choisies.")
else:
    # On prépare les données pour le graphique de Streamlit
    df_chart = df_display.set_index('Country')[['CurrentAccountBalance', 'BudgetBalance']]
    
    st.scatter_chart(
        df_chart,
        x='CurrentAccountBalance',
        y='BudgetBalance',
        size=100, # Taille fixe pour les points
        height=600
    )
    
    st.info("Ce graphique montre la position des pays pour l'année sélectionnée.")