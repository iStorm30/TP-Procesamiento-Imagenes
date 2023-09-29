import cv2
import pickle
import numpy as np

pasillo = []
with open('espacios.pkl', 'rb') as file:
    pasillo = pickle.load(file)

video = cv2.VideoCapture('video2.mp4')

b = []
cc = 0
veces = 0

while True:
    cc += 1
    check, img = video.read()
    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgTH, 5)
    kernel = np.ones((5,5), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel)

    for x, y, w, h in pasillo:
        espacio = imgDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)
        cv2.putText(img, str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        if count < 1800:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)        
        else:
            b.append(cc)
            if len(b)>1:
                if b[-1] != (b[-2]+1):
                    veces += 1


    texto = f'Recuadro Ocupado: {veces}'
    cv2.putText(img, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('video2', img)
    cv2.waitKey(10)
