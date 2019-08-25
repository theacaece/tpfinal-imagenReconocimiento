import cv2
import train, detect, config, imutils, argparse

# Funcion que reconoce imagen pasada por parametro
def RecognizeFace(image, faceCascade, eyeCascade, faceSize, threshold):
    found_faces = []
    recognizer = train.trainRecognizer("train", faceSize, showFaces=True)
    gray, faces = detect.detectFaces(image, faceCascade, eyeCascade, returnGray=1)
    for ((x, y, w, h), eyedim)  in faces:
        label, confidence = recognizer.predict(cv2.resize(detect.levelFace(gray, ((x, y, w, h), eyedim)), faceSize))
        if confidence < threshold:
            found_faces.append((label, confidence, (x, y, w, h)))

    return found_faces

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
    help = "Ruta de la imagen para reconocer")
    args = vars(ap.parse_args())

    faceCascade = cv2.CascadeClassifier('cascades/face.xml')
    eyeCascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')
    faceSize = config.DEFAULT_FACE_SIZE
    threshold = 500
    recognizer = train.trainRecognizer('train', faceSize, showFaces=True)

    # Crea la ventana con el nombre 'Reconocimiento Facial' y la imagen a reconocer
    cv2.namedWindow("Reconocimiento Facial", 1)
    capture = cv2.imread(args["image"])

    # Inicia bucle
    while True:
        img = imutils.resize(capture, height=500)
        # Busca el nombre de la persona del rostro que esta en la imagen
        for (label, confidence, (x, y, w, h)) in RecognizeFace(img, faceCascade, eyeCascade, faceSize, threshold):
            font = cv2.FONT_HERSHEY_DUPLEX
            # Coloca rectangulo en el rostro encontrado y reconocido
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Coloca el nombre de la persona reconocida
            cv2.putText(img, "{}".format(recognizer.getLabelInfo(label)), (x, y-5), font, 1, (0,255,0), 1, cv2.LINE_AA)

        # Indica el nombre de la persona reconocida en la imagen pasada por parametro
        print("Rostro Reconocido: %s" % (recognizer.getLabelInfo(label)))
        # Crea la ventana con el nombre 'Reconocimiento Facial' y la imagen a reconocer
        cv2.imshow("Reconocimiento Facial", img)

        # Comprueba si se ha pulsado la tecla 'Esc' para salir del bucle
        ch = cv2.waitKey(0)
        if ch == 27:
            break
        
    # Si se ha salido del bucle, destruye la ventana y finaliza el programa
    cv.destroyAllWindows()
