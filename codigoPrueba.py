import mysql.connector
import streamlit as st 
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

class CategoriaTransaccion:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
        
    def obtener_categoria(self):
        self.cursor.execute('SELECT * FROM categoria_transaccion')
        result = self.cursor.fetchall()
        return result
    
    def agregar_categoria(self,nombre,tipo):
        self.cursor.execute('INSERT INTO categoria_transaccion (nombre_categoria, tipo_categoria) VALUES (%s, %s)',(nombre,tipo))
        self.connection.commit()
    
    def actualizar_categoria(self, id, nombre, tipo):
        self.cursor.execute('UPDATE categoria_transaccion SET nombre_categoria = %s, tipo_categoria = %s WHERE id_categoria = %s',(nombre, tipo, id))
        self.connection.commit()

    def eliminar_categoria(self, id):
        self.cursor.execute('DELETE FROM categoria_transaccion WHERE id_categoria = %s',(id,))
        self.connection.commit()

class DataManagerTransaccion:
    def __init__(self) -> None:
        self.db_categoria = CategoriaTransaccion()
        
    @st.dialog('Modificar o Eliminar Categoría')
    def interfaz_modify_categoria(self, id, nombre, tipo):
        nombre_categoria = st.text_input('Ingrese la Categoría', value=nombre)
        lista = ['Ingreso','Egreso']
        tipo_categoria = st.selectbox('Ingrese el tipo de categoría', options=lista,index=lista.index(tipo))
        col_a,col_b, col_c =  st.columns([3,2,2])
        with col_b:
            if st.button('Modificar', use_container_width=True):
                self.db_categoria.actualizar_categoria(id, nombre_categoria, tipo_categoria)
                st.rerun()
        with col_c:    
            if st.button('Eliminar', use_container_width=True):
                self.db_categoria.eliminar_categoria(id)
                st.rerun()
        
    def interfaz_display_categoria(self):
        data_categoria = self.db_categoria.obtener_categoria()
        dataframe_categoria = pd.DataFrame(data_categoria)
        dataframe_categoria = dataframe_categoria.rename(columns={'id_categoria':'ID', 'nombre_categoria':'NOMBRE', 'tipo_categoria':'TIPO'})
        evento = st.dataframe(dataframe_categoria,
                    height=332,
                    use_container_width=True,
                    hide_index=True, 
                    selection_mode="single-row",
                    on_select="rerun")
        if evento['selection']['rows']:
            filtrado = dataframe_categoria[dataframe_categoria.index.isin(evento.selection['rows'])]
            
            valor_id = int(filtrado.iloc[0,0])
            valor_nombre = str(filtrado.iloc[0,1])
            valor_tipo = str(filtrado.iloc[0,2])
            self.interfaz_modify_categoria(valor_id, valor_nombre, valor_tipo)
    
    def interfaz_add_categoria(self):
        cont_add_categoria = st.container(border=True)
        with cont_add_categoria:
            st.subheader('Agregar Nueva Categoría')
            nombre_categoría = st.text_input('Ingresar Categoría: ')
            lista_tipo_categoría = ['Ingreso','Egreso']
            tipo_categoría = st.selectbox('Tipo de Categoría',options=lista_tipo_categoría,index=0)
            if st.button('Guardar Categoria'):
                self.db_categoria.agregar_categoria(nombre_categoría, tipo_categoría)
    
def fun_categoria():
    objeto_transaccion = DataManagerTransaccion()
    col_I, col_II = st.columns(2)
    with col_I:
        objeto_transaccion.interfaz_add_categoria()
    with col_II:
        objeto_transaccion.interfaz_display_categoria()
        
fun_categoria()