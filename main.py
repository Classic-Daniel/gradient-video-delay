import numpy as np
import cv2

BUFFER_SIZE = 30

class imageGenerator:
    def __init__(self, img):
        self.imgBuffer = [img] * BUFFER_SIZE
        self.currentIndex = 0
        print(f"Image type: {type(img)}")
        print(f"buffer shape: {self.imgBuffer[0].shape}")

    def addNewImage(self, img):
        self.imgBuffer[self.currentIndex] = img
        self.currentIndex = (self.currentIndex + 1) % BUFFER_SIZE

    def getProcessedImage(self):
        generatedImg = np.copy(self.imgBuffer[self.currentIndex])
        height = self.imgBuffer[self.currentIndex].shape[1]
        heightStep = round(height / BUFFER_SIZE)

        for i in range(1, BUFFER_SIZE):
            generatedImg[:, heightStep * i : heightStep * (i + 1)] = self.imgBuffer[(self.currentIndex + i) % BUFFER_SIZE][:, heightStep * i : heightStep * (i + 1)]

        return generatedImg

def initCameraStream():    
    cap = cv2.VideoCapture(cv2.CAP_V4L2)
    generator = None
    # The device number might be 0 or 1 depending on the device and the webcam
    # cap.open(0, cv2.CAP_DSHOW)
    while(True):
        ret, frame = cap.read()
        if(ret and frame.shape[0] > 0):
            if generator == None:
                generator = imageGenerator(frame)

            generator.addNewImage(frame)
            cv2.imshow('frame', generator.getProcessedImage())
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def main():
    initCameraStream()

if __name__ == "__main__":
    main()
