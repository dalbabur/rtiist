import cv2 as cv
import numpy as np

class DefaultImgProcessor:
    def __init__(self) -> None:
        self.masks = []
        pass

    def make_mask(self, img):
        if len(self.masks) > 0: 
            print('mask already created')
            return

        gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        self._mask_img = gray

        thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)[1]
        # apply morphology open and close and dilate
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11,11))
        thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (55,55))
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
        thresh = cv.morphologyEx(thresh, cv.MORPH_DILATE, kernel)

        circles = cv.HoughCircles(thresh, cv.HOUGH_GRADIENT, 1, 30, param1=100, param2=1, minRadius=5, maxRadius=15)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            self._detected_roi = circles

            X,Y = gray.shape
            r = np.uint16(np.mean(circles[0][:,2])+7)
            
            for c in circles[0,:]:

                mask = np.zeros((X,Y))
                for x in range(c[0]-r*2,c[0]+r*2):
                    for y in range(c[1]-r*2,c[1]+r*2):
                        if 0 <= (x-c[0])**2 + (y-c[1])**2 <= r*5:
                            mask[y,x] = 1

                self.masks.append(mask)

    def show_mask(self):
        if not(len(self.masks) > 0): 
            print('no mask created')
            return

        r = np.uint16(np.mean(self._detected_roi[0][:,2])+7)
        thresh = np.zeros((self._mask_img.shape))
        img = np.copy(self._mask_img)

        vals = self.extract_values(img)

        for c,m,v in zip(self._detected_roi[0,:], self.masks, vals):
            cv.circle(img,(c[0],c[1]),r,(255,255,255),1)
            thresh = thresh + m
            cv.putText(img, str(np.round(v,2)), (c[0] + r+ 5, c[1] + r+5),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
        
        cv.imshow('detected circles',thresh) 
        cv.imshow('mean circles',img)
        cv.waitKey(0)
        
    def extract_values(self, img):
        vals = []
        for m in self.masks:
            vals.append(np.mean((img*m)[(img*m)>0]))
        
        return vals
    
    def process(self, raw_data):
        img = cv.cvtColor(raw_data, cv.COLOR_RGB2GRAY)
        return self.extract_values(img)
