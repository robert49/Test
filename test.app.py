# --- APPLICATION WEB INTERACTIVE DES SOLDES SECTORIELS (Version Statique et Fiable) ---

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
        # On ne garde que les colonnes nécessaires
        cols_to_keep = ['Year', 'Country', 'CurrentAccountBalance', 'BudgetBalance', 'PIB/habitant']
        df = df[cols_to_keep]
        for col in ['CurrentAccountBalance', 'BudgetBalance', 'PIB/habitant']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(subset=['CurrentAccountBalance', 'BudgetBalance', 'Country', 'Year'], inplace=True)
        df['Year'] = df['Year'].astype(int)
        return df
    except FileNotFoundError:
        st.error(f"ERREUR : Le fichier de données '{excel_file}' est introuvable.")
        return pd.DataFrame()

def classifier_revenu(pib_par_habitant):
    if pd.isna(pib_par_habitant): return 'Inconnu'
    if pib_par_habitant <= 1135: return 'Revenu faible'
    elif pib_par_habitant <= 4465: return 'Revenu intermédiaire inférieur'
    elif pib_par_habitant <= 13845: return 'Revenu intermédiaire supérieur'
    else: return 'Revenu élevé'

df_all = load_data()
if not df_all.empty:
    df_latest_pib = df_all.sort_values('Year').drop_duplicates('Country', keep='last')
    country_to_income = df_latest_pib.set_index('Country')['PIB/habitant'].apply(classifier_revenu).to_dict()
    df_all['Niveau_Revenu'] = df_all['Country'].map(country_to_income)

# --- 2. PANNEAU DE CONTRÔLE DANS LA BARRE LATÉRALE ---
st.sidebar.title("Panneau de Contrôle")
annees_disponibles = sorted(df_all['Year'].unique())

# On utilise un slider simple pour sélectionner UNE SEULE année
annee_choisie = st.sidebar.slider(
    'Sélectionnez une année :',
    min_value=int(min(annees_disponibles)),
    max_value=int(max(annees_disponibles)),
    value=int(max(annees_disponibles))
)

groupes_de_pays = {
    "Monde Entier": sorted(df_all['Country'].unique()),
    "G7": ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States'],
    # Ajoutez d'autres groupes si vous le souhaitez
}
groupe_choisi = st.sidebar.selectbox("Choisir un groupe de pays :", options=list(groupes_de_pays.keys()))
pays_selectionnes = st.sidebar.multiselect("Choisir un ou plusieurs pays :", options=groupes_de_pays[groupe_choisi], default=groupes_de_pays[groupe_choisi])

# --- 3. FILTRAGE FINAL DES DONNÉES ---
df_display = df_all[
    (df_all['Year'] == annee_choisie) &
    (df_all['Country'].isin(pays_selectionnes))
].copy()

# Ajout de la colonne couleur pour le graphique natif de Streamlit
color_map = {'Revenu élevé': '#00008B', 'Revenu intermédiaire supérieur': '#008000',
             'Revenu intermédiaire inférieur': '#FFA500', 'Revenu faible': '#A52A2A', 'Inconnu': '#808080'}
df_display['Couleur'] = df_display['Niveau_Revenu'].map(color_map)

# --- 4. AFFICHAGE DE L'APPLICATION ---
st.title(f"Carte Statique des Modèles Économiques Mondiaux ({annee_choisie})")
st.markdown(f"Visualisation de **{len(df_display)} pays** pour l'année sélectionnée.")

if df_display.empty:
    st.warning("Aucune donnée disponible pour la sélection et l'année choisies.")
else:
    st.scatter_chart(
        df_display,
        x='CurrentAccountBalance',
        y='BudgetBalance',
        color='Couleur', # On utilise la colonne de couleur hexadécimale
        size=100
    )
    
    st.info("Ce graphique montre la position des pays pour l'année sélectionnée. Utilisez le curseur dans la barre latérale pour changer d'année.")
    
    # On peut afficher le tableau de données en dessous pour plus de détails
    st.dataframe(df_display[['Country', 'Niveau_Revenu', 'CurrentAccountBalance', 'BudgetBalance']].set_index('Country'))```

