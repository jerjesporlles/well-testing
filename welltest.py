# Librerias
import streamlit as st

# Librerias internas
import buildup
import drawdown

st.title('Well Testing App')
st.sidebar.title('Parámetros')

modulo = st.sidebar.selectbox("Escoja un Módulo",['Select an option', 'Buildup', 'Drawdown'], format_func=lambda x: 'Select an option' if x == '' else x)
if modulo == 'Buildup':
	buildup.Buildup_Test_Sequence()
elif modulo == 'Drawdown':
	drawdown.Drawdown_Test_Sequence()
else:
	st.warning("Bienvenido a Well Testing") #Amarillo
