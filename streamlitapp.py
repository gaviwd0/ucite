import streamlit as st
import pandas as pd

def main():
    #redirije a la vista inicio
    if 'page' not in st.session_state:
        st.session_state.page = 'Inicio'
    
    st.sidebar.title('Menu de Opciones')
    #boton inicio en la sidebar
    if st.sidebar.button('Inicio'):
        st.session_state.page = 'Inicio'
    #boton "panel de control" en la sidebar
    if st.sidebar.button('Panel de Control'):
        st.session_state.page= 'Panel de Control'


def ir_home():
    st.session_state.page='inicio'

if __name__ == "__main__":
    main()