from flask import render_template, request, redirect, url_for
from app import app
from .db import get_db_config, db_connect
import mysql.connector
from bs4 import BeautifulSoup
import requests
from .allo_cine_scraping import Allo_Cine
from flask_paginate import Pagination, get_page_parameter

# Afficher les valeurs utilisateurs dans le tableau puis db
# Mettre le cemin absolu de votre config.json
path = "/home/kevin/workspace/py-sql/flask/app_mega_tutorail/app_ensemble/config.json"
config = get_db_config(path)

myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()


#----------------------------------------------------------------
# Base
#----------------------------------------------------------------
@app.route('/')


#----------------------------------------------------------------
# Index
#----------------------------------------------------------------
@app.route('/index', methods=["GET", "POST"])   # == @app.route('/index')
def index():

    if request.method == "GET":

        try:
            query="""
                SELECT * FROM `Utilisateur`;
            """
            cursor.execute(query)
            result_select = cursor.fetchall()

            return render_template('index.html',configHTML=config, dbOK__=dbOK, HTML_Result=result_select)
        

        except mysql.connector.Error as e:
            return render_template('index.html', configHTML=config, error=e)

        # inserer des valeurs utilisateurs dans le tableau puis db

    if request.method == "POST":

        try:
            prenom = request.form["prenom"]
            nom = request.form["nom"]
            adresse_mail = request.form["adresse_mail"]

            query=f"""
                INSERT INTO Utilisateur (nom, prenom, adresse_email) VALUES ("{nom}", "{prenom}", "{adresse_mail}");
            """
            cursor.execute(query)
            myDB.commit()
            
            return redirect(url_for("index"))

        except mysql.connector.Error as e:
            return redirect(url_for("index"), error=e)

#----------------------------------------------------------------
# TEST
#----------------------------------------------------------------
@app.route('/test', methods=['GET', 'POST'])   # == @app.route('/index')
def test():
    if request.method == "GET":
        longueur_phrase=0
        return render_template('test.html',longueur_phrase=longueur_phrase)

    if request.method == 'POST':
        phrase=request.form.get('phrase')
        longueur_phrase = len(phrase)
        standard = Allo_Cine.standardize_phrase(phrase)
        predict = Allo_Cine.predict(standard)
        return render_template('test.html', predict=predict, phrase=phrase, longueur_phrase=longueur_phrase)

        

    
#----------------------------------------------------------------
# COMMENTAIRE D'AVATAR
#----------------------------------------------------------------    
@app.route('/avis', methods=['GET', 'POST'])  
def avis():

    if request.method == "GET":
        try:
            query ="SELECT COUNT(*) FROM allo_cine"
            cursor.execute(query)
            for i in cursor:
                print(i)
                nb_comment=i[0]
            print(nb_comment)
            result_select = Allo_Cine.affich()
            return render_template('avis.html', commentaires=result_select,nb_comment=nb_comment)
    
        except mysql.connector.Error as e:
            return render_template('avis.html')


#----------------------------------------------------------------
# SCRAPPING
#----------------------------------------------------------------         
@app.route('/scrapping', methods=["GET", "POST"])   # == @app.route('/index')
def scrapping():  
    if request.method == "GET": 
        requete=0
        return render_template('scrapping.html',requete=requete)

    if request.method == 'POST':
        requete=1
        name=request.form.get('film')
        info = Allo_Cine.scrape_film(name)
        
        return render_template('scrapping.html', info=info, name=name, requete=requete)



    


    


        
   