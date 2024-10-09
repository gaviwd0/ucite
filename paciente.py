import mysql.connector
import streamlit as st 
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

#clase paciente 
class Paciente:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
            port = int(os.getenv('DB_PORT'))

        )
        self.cursor = self.connection.cursor(dictionary=True)
    #CRUD de manejo de paciente
    def agregar_paciente(self,id_paciente,nombre,apellido,direccion,telefono,email):
        self.cursor.execute('INSERT INTO pacientes (id_paciente = %s,nombre = %s, apellido = %s, direccion = %s, telefono = %s, email = %s',  (id_paciente,nombre,apellido,direccion,telefono,email))
        self.connection.commit()

    #obtiene todos los pacientes 
    def obtener_pacientes(self):
        self.cursor.execute("SELECT * FROM pacientes")
        pacientes_obtenidos = self.cursor.fetchall()
        return pacientes_obtenidos
    
    #modofica el paciente por su id
    def modificar_paciente(self,id_paciente,nombre,apellido,direccion,telefono,email):
        self.cursor.execute(  'UPDATE pacientes SET nombre = %s, apellido = %s, direccion = %s, telefono = %s, email = %s, WHERE id_paciente = %s',  (nombre,apellido,direccion,telefono,email,id_paciente))
        self.connection.commit()
    #elimina un paciente por su id

    def eliminar_paciente(self,id):
        self.cursor.execute('DELETE FROM pacientes WHERE id_paciente = %s', (id,))
        self.connection.commit()

#interfaz del CRUD 
class ManagerPaciente:
    def __init__(self) -> None:
        self.db_paciente = Paciente()
    @st.dialog('Modificar o Eliminar Paciente')
    def interfaz_modify_paciente(self,id_paciente,nombre,apellido,direccion,telefono,email):
        nombre_categoria = st.text_input('Ingrese la Categoría', value=nombre)
        lista = ['Ingreso','Egreso']
        tipo_categoria = st.selectbox('Ingrese el tipo de categoría', options=lista,index=lista.index(tipo))
        col_a,col_b, col_c =  st.columns([3,2,2])
        with col_b:
            if st.button('Modificar', use_container_width=True):
                self.db_paciente.modificar_paciente(id_paciente,nombre,apellido,direccion,telefono,email)
                st.rerun()
        with col_c:    
            if st.button('Eliminar', use_container_width=True):
                self.db_paciente.eliminar_categoria(id_paciente)
                st.rerun()
        
    def interfaz_display_categoria(self):
        data_categoria = self.db_paciente.obtener_categoria()
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
                self.db_paciente.agregar_categoria(nombre_categoría, tipo_categoría)
    
def fun_categoria():
    objeto_transaccion = DataManagerTransaccion()
    col_I, col_II = st.columns(2)
    with col_I:
        objeto_transaccion.interfaz_add_categoria()
    with col_II:
        objeto_transaccion.interfaz_display_categoria()
        
fun_categoria()







