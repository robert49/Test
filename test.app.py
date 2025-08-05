import streamlit as st
import pandas as pd

st.title("Bonjour, Streamlit !")
st.write("Si vous voyez ce mess, c'est que le déploiement a fonctionné.")

st.header("Test avec un DataFrame Pandas")
df = pd.DataFrame({
    'colonne 1': [1, 2, 3],
    'colonne 2': [10, 20, 30]
})
st.write(df)

