import numpy as np
import cv2 as cv
import frameedge as fe

class FrameEdgeFilter(fe.FrameEdge):
    def __init__(self, cap):
        super().__init__(cap)

    def shader(self):
        flag, self.frame = self.cap.read()
        if not flag:
            print("Frame error")
            return False
        self.frame = cv.flip(self.frame, 1)
        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (5, 5), 1.5)
        gray = cv.medianBlur(gray, 5) 
        self.edge = cv.Canny(gray, self.threshold[0], self.threshold[1])
        kernel = np.ones((3, 3), np.uint8)
        self.edge = cv.morphologyEx(self.edge, cv.MORPH_CLOSE, kernel)
        self.edge = cv.GaussianBlur(self.edge, (3, 3), 1.0)
        self.application = self.frame
        return True
