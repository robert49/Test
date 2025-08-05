import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # La ligne qui causait problème

st.title("Test d'Importation de Plotly")
st.success("Si vous voyez ce message, c'est que `streamlit`, `pandas`, `plotly.express` et `plotly.graph_objects` ont été importés avec succès !")
