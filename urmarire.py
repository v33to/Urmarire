import cv2
import numpy as np
from detectare import detectare
import math

alegere = int(input("Ce camera vreti sa folositi? \n 1 - San Francisco \n 2 - Pascani  \n 3 - Bucuresti\n 4 - Neamt\n"))
oras = ["san_francisco.mp4", "pascani.mp4", "bucuresti.mp4", "neamt.mp4"]

captura = cv2.VideoCapture(oras[alegere - 1])
tasta = cv2.waitKey(1)

centreAnterior = []
numarObiecte = {}
contor = 0
nr = 0

#initializare
detectare = detectare()

#incarcare video
while tasta != 27:
    ret, fereastra = captura.read()
    nr = nr + 1
    centreCurent = []

    #detectare
    (numar, verdict, incadrare) = detectare.detect(fereastra)
    for i in incadrare:
        (x, y, L, l) = i
        #calculare centru
        xCentru = int((x + x + L) / 2)
        yCentru = int((y + y + l) / 2)
        centreCurent.append((xCentru, yCentru))
        #incadrare
        cv2.rectangle(fereastra, (x, y), (x + L, y + l), (255, 0, 0), 3)

    #comparatie intre cadre
    if nr <= 2:
        for i in centreCurent:
            for j in centreAnterior:
                distantaCentre = math.hypot(j[0] - i[0], j[1] - i[1])
                if distantaCentre < 35:
                    numarObiecte[contor] = i
                    contor = contor + 1
    else:
        aux = numarObiecte.copy()
        aux2 = centreCurent.copy()
        for j, k in aux.items():
            prezentaObiect = 0
            for i in aux2:
                distantaCentre = math.hypot(k[0] - i[0], k[1] - i[1])
                
                #pozitie obiect
                if distantaCentre < 35:
                    numarObiecte[j] = i
                    prezentaObiect = 1
                    if i in centreCurent:
                        centreCurent.remove(i)
                    continue
            if not prezentaObiect:
                numarObiecte.pop(j)
        for i in centreCurent:
            numarObiecte[contor] = i 
            contor = contor + 1
    
    for i, j in numarObiecte.items():
        cv2.circle(fereastra, j, 10, (0, 255, 0), -1)
        cv2.putText(fereastra, str(i), (j[0], j[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Obiecte detectate: ")
    print(numarObiecte)

    centreAnterior = centreCurent.copy()

    cv2.imshow("Fereastra", fereastra)
    tasta = cv2.waitKey(1)

captura.release()
cv2.destroyAllWindows()
