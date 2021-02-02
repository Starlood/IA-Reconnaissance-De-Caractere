import flask
from tensorflow import keras
import numpy as np
import cv2
from cv2 import cv2 #Chargement des modules nécessaires
import base64
import string
import sys
import logging

app = flask.Flask(__name__, template_folder='progprincipale')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

model = keras.models.load_model('modele') #Chargement du modele
labels = list(string.ascii_uppercase) #Liste contenant les lettres de l'alphabet

@app.route('/')
def home():
	return flask.render_template('draw.html',  prediction = None) #Renvoi du résultat du test


@app.route('/', methods=['POST'])
def predict():
	draw = flask.request.form['url']  #Recuperation du dessin
	draw = draw[22:] 
	draw_decoded = base64.b64decode(draw) #Décodage des donnés reçus
	
	image = np.asarray(bytearray(draw_decoded)) #Transformationde de draw_decode en un tableau d'octet
	image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE) #Retouche de l'image en nuance de gris
	resized = cv2.resize(image, (28,28), interpolation=cv2.INTER_AREA)#Redimensionnement de l'image en 28*28 px
	
	vect = np.asarray(resized, dtype="uint8") #Conversion de la matrice en img
	vect = vect.reshape(1, 28, 28, 1).astype('float32') #Redimensionnement
	vect = vect/255.0

	#Test si c'est vide
	if(vect.sum() == 0):
		return flask.render_template('draw.html',  prediction = None)
	
	pred = model.predict(vect) #Test de prediction
	index_pred = np.argmax(pred) #Choix de l'index en se basant sur argument max
	
	return flask.render_template('draw.html', prediction = labels[index_pred]) #Renvoi du résultat du test

if __name__ == '__main__':
	app.run()