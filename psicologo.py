import mysql.connector
import streamlit as st 
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

class Psicologo:
    def __init__(self):      
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
            port = int(os.getenv('DB_PORT'))

        )
        self.cursor = self.connection.cursor(dictionary=True)