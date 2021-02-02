import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D #Importation des librairies nécessaires
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import warnings
from sklearn.utils import shuffle
import coremltools

warnings.filterwarnings('ignore')#Ignore les messages d'erreur
sns.set()

dataset = pd.read_csv("A_Z Handwritten_Data.csv").astype('float32')#Lecture du data set contenant les données
dataset.rename(columns={'0': 'label'}, inplace=True)#Renomme l'identifiant de la ligne du fichier en tant que "label"

X = dataset.drop('label', axis=1) #Identifiant de lettre
y = dataset['label'] #Les données à prédire

X_shuffle = shuffle(X) #Mélange les données aléatoirement

alphabets_mapper = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
                    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W',
                    23: 'X', 24: 'Y', 25: 'Z'} #Liste des possibilités de sorties
dataset_alphabets = dataset.copy() #Copie de la liste d'au dessus
dataset['label'] = dataset['label'].map(alphabets_mapper) #Les données à prédire appartiennent au dictionnaire map (alphabets_mapper)

label_size = dataset.groupby('label').size() #Classement au sein du data set en fonction de la taille (de 0 à 25)
label_size.plot.barh(figsize=(10, 10)) #Affichage optimale

X_train, X_test, y_train, y_test = train_test_split(X, y) #Séparation des données en sous ensemble pour pouvoir tester le modèle entrainé

standard_scaler = MinMaxScaler()#Mise à l'echelle
standard_scaler.fit(X_train)

X_train = standard_scaler.transform(X_train) #Definir longeur de X_train
X_test = standard_scaler.transform(X_test) #Definir longeur de X_test

X_shuffle = shuffle(X_train) #Mélange de la liste
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')#Recadrage des images en 28*28px
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')#Recadrage des images en 28*28px

y_train = np_utils.to_categorical(y_train)#Conversion en matrice
y_test = np_utils.to_categorical(y_test)#Conversion en matrice

# Construction du modèle  avec implémentation des couches
cls = Sequential()
cls.add(Conv2D(32, (5, 5), input_shape=(28, 28, 1), activation='relu'))
cls.add(MaxPooling2D(pool_size=(2, 2)))
cls.add(Dropout(0.3))
cls.add(Flatten())
cls.add(Dense(128, activation='relu'))
cls.add(Dense(len(y.unique()), activation='softmax'))

cls.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])#Variables du modèle
#Parcours des données (X_train / Y_train)
history = cls.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=1, batch_size=200, verbose=2)
#Comparaison des données test et train

scores = cls.evaluate(X_test, y_test, verbose=0)#Calcul de la précision
print("Précision du modèle :", scores[1])#Affichage précision obtenu avec les tests


#Création matrice permettant de connaitre la précision pour chaque lettre
cm=confusion_matrix(y_test.argmax(axis=1),cls.predict(X_test).argmax(axis=1))
df_cm = pd.DataFrame(cm, range(26),
                  range(26))
plt.figure(figsize = (20,15))
sns.set(font_scale=1.4)
sns.heatmap(df_cm, annot=True,annot_kws={"size": 16})

cls.save('modele_ecriture.model')#Sauvegarde du modele

output_labels = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] #Liste des sorties du modele
core_ml=coremltools.converters.keras.convert('modele_ecriture.model', input_names=['image'], output_names=['output'],
    class_labels=output_labels,image_scale=1/255.0, is_bgr = False, image_input_names = "image")
#Transformation du modele