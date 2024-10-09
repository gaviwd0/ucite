import mysql.connector
import streamlit as st
import dotenv as load_dotenv
import os

load_dotenv


class Psicologouser:
    def __init__(self) -> None:
        self.connection = mysql.connector.connet(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
            port = int(os.getenv('DB_PORT'))
        )
        self.cursor = self.connection.cursor(dictionary=True)