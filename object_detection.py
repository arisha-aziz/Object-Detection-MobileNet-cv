# importing the packages
import numpy as np
import argparse
import cv2
import os

class MobileNetSSD:

    def __init__(self, args, verbose=False):
        self.image = args.image
        self.prototxt = args.prototxt
        self.model = args.model
        self.confidence = args.confidence
        self.query = args.query
        self.verbose = verbose

    def main(self):

        # all CLASSES for which MobileNetSSD was originally pretrained
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        	"sofa", "train", "tvmonitor"]

        # storing random colors for bounding boxes ,
        # since image is colored , so all RGB colors assigned
        COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
        # loading model
        print("loading model...")
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        # read image

        image = cv2.imread(self.image)
        # finding height, weight
        h, w = image.shape[0], image.shape[1]
        # perform preprocessing like mean subtraction and scaling
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        print("Passing the image to the model...")
        net.setInput(blob)
        detections = net.forward()
        detected = 0
        detected_items = set()
        # now constructing bounding boxes for every object detected
        for i in range(0, detections.shape[2]):
            # for every image detected extract the confidence
            confidence = detections[0, 0, i, 2]
            # only draw bounding box if it is greater than threshold confidence
            if confidence > float(self.confidence):
                # extracting the index of the label
                idx = int(detections[0, 0, i, 1])
                detected_items.add(CLASSES[idx])
                if self.query == CLASSES[idx]:
                    # extracting the four offset values for bounding boxes
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    # setting the four core coordinates to draw the rectangle
                    (startX, startY, endX, endY) = box.astype("int")
                    label = f"{CLASSES[idx]} : {confidence*100}"
                    # increment every time it is detected
                    detected += 1
                    cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

        if not detected:
            print(f"NO {self.query} detected in the given image !")
        else:
            print(f"{self.query} detected {detected} !")
        cv2.imshow("Output", image)
        cv2.waitKey(0)
        if self.verbose:
            print(f"All objects detected in the image : {detected_items}")


# main driver function
if __name__ == '__main__':
    print("WELCOME TO Object DETECTION")
    parser = argparse.ArgumentParser(description='Automating RoI extraction', epilog='Happy detection :)')
    parser.add_argument('image', type=str, help='Image path')
    parser.add_argument('prototxt', type=str, help='info about model')
    parser.add_argument('model', type=str, help='model file of caffemodel type')
    parser.add_argument('confidence', type=str, help='threshold confidence %')
    parser.add_argument('query', type=str, help='Query string to search for')
    parser.add_argument('-v', type=str, help='debug output to print all items detected')
    args = parser.parse_args()
    m = MobileNetSSD(args, args.v)
    m.main()
