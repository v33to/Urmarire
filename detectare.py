import cv2
import numpy as np


class detectare:
    def __init__(a, weights = "dnn_model/yolov4.weights", cfg = "dnn_model/yolov4.cfg"):
        a.nmsThreshold = 0.4
        a.certitudine = 0.5
        a.marime = 608

        #Incarcare retea
        retea = cv2.dnn.readNet(weights, cfg)
        retea.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        retea.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        a.model = cv2.dnn_DetectionModel(retea)
        a.clase = []
        a.load_class_names()
        a.culori = np.random.uniform(0, 255, size = (80, 3))
        a.model.setInputParams(size = (a.marime, a.marime), scale = 1 / 255)

    def load_class_names(a, clase = "dnn_model/classes.txt"):
        with open(clase, "r") as obiect:
            for i in obiect.readlines():
                i = i.strip()
                a.clase.append(i)
        a.colors = np.random.uniform(0, 255, size = (80, 3))
        return a.clase

    def detect(a, fereastra):
        return a.model.detect(fereastra, nmsThreshold = a.nmsThreshold, confThreshold = a.certitudine)

