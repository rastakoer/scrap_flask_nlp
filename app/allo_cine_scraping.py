from flask import render_template, request, redirect, url_for
from app import app
from .db import get_db_config, db_connect
import mysql.connector
from bs4 import BeautifulSoup
import requests
import joblib
from sklearn.linear_model import LogisticRegression

from nltk.corpus import stopwords
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

vector = joblib.load('brief_nlp_joblib.joblib')['vector']
LReg = joblib.load('brief_nlp_joblib.joblib')['model']

path = "/home/kevin/workspace/py-sql/flask/app_mega_tutorail/app_ensemble/config.json"
config = get_db_config(path)

myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()

class  Allo_Cine :
    """ Pour scrapper et afficher les commentaires
        du film avatar
    """

    @staticmethod
    def scrape():
        for i in range(1,668):
                url = f"https://www.allocine.fr/film/fichefilm-61282/critiques/spectateurs/?page={i}"
                reponse=requests.get(url)
                soup = BeautifulSoup(reponse.text,"html.parser")
                donnees=soup.find_all("div", {"class":"hred review-card cf"})

                for comment in donnees:
                    id_com = comment.get("id").split("_")[1]
                    note= comment.find("span",{"class":"stareval-note"}).text.replace(",",".")
                    commentaire = comment.find("div",{"class":"content-txt review-card-content"}).text.replace("'"," ").replace("\n","")
                    query =f"""INSERT INTO avatar(id_comment, commentaire, note) """
                    query += f"""VALUES ('{id_com}','{commentaire}',{note})"""
                    query += f"""ON DUPLICATE KEY UPDATE id_comment='{id_com}' """
                    cursor.execute(query)
                myDB.commit()
        return 

    @staticmethod
    def affich():
        query="""
            SELECT * FROM allo_cine;
        """
        cursor.execute(query)
        result_select = cursor.fetchall()
        return result_select

    def standardize_phrase(donnees):
        donnees = donnees.replace(r"http\S+", "")
        donnees = donnees.replace(r"http", "")
        donnees = donnees.replace(r"@\S+", "")
        donnees = donnees.replace(r"[0-9(),;!:?@<>.=\'\`\"\-\_\n]", " ")
        donnees = donnees.replace(r"@", "at")
        donnees = donnees.replace("é", "e")
        donnees = donnees.replace("è", "e")
        donnees = donnees.lower()
        
        lemmatizer = FrenchLefffLemmatizer()
        corpus = []
        message = donnees.split()
        message =[word for word in message if word not in stopwords.words('french')]
        message = [lemmatizer.lemmatize(word) for word in message]
        message = ' '.join(message)
        corpus.append(message)
        
        return corpus
    
    def predict(corpus_phrase):
        vectorisation=vector.transform(corpus_phrase)
        prediction = LReg.predict(vectorisation)
        return prediction