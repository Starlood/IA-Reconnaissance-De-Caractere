import csv
import os

from PIL import Image
import numpy as np
import string

#Initialisation variable
csv_File_Path = "A_Z_Handwritten_Data.csv"
count = 1
last_digit_Name = None
image_Folder_Path = "..\..\..\LETTRES"
Alphabet_Mapping_List = list(string.ascii_uppercase)

#Pour chaque lettre on créer un dossier avec le nom de la lettre
for alphabet in Alphabet_Mapping_List:
    path = image_Folder_Path + '\\' + alphabet
    if not os.path.exists(path): #Si le dossier n'existe pas on le créer
        os.makedirs(path)


with open(csv_File_Path, newline='') as csvfile: #Se deplacer dans le fichier de la lettre actuelle
    reader = csv.reader(csvfile, delimiter=',', quotechar='|') # On lit une ligne définit par les delimiter
    count = 0
    for row in reader:
        digit_Name = row.pop(0) #Obtenir l'identifiant de l'image, la lettre à laquelle il correspond
        image_array = np.asarray(row) #la matrice de l'image
        image_array = image_array.reshape(28, 28) #On redéfinit sa taille en 28x28
        new_image = Image.fromarray(image_array.astype('uint8')) #On récupère la matrice en tant qu'image

        if last_digit_Name != str(Alphabet_Mapping_List[(int)(digit_Name)]): #Si on change de lettre
            last_digit_Name = str(Alphabet_Mapping_List[(int)(digit_Name)]) #On actualise la nouvelle lettre
            count = 0
            print("")
            print("Prcessing Alphabet - " + str(last_digit_Name))

        image_Path = image_Folder_Path + '\\' + last_digit_Name + '\\' + str(last_digit_Name) + '-' + str(
            count) + '.png' #chemin de sauvegarde de l'image
        new_image.save(image_Path) #On sauvegarde l'image au chemin précédent
        count = count + 1

        if count % 1000 == 0: #Comptez toutes les 1000 images faites
            print("Images processed: " + str(count))
