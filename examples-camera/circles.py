import cv2 as cv
import numpy as np

img_path = '/home/pi/LAB/rt-opto/rtiist/images/img-3.jpg'
img = cv.imread(img_path)
gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

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
    X,Y = gray.shape
    r = np.uint16(np.mean(circles[0][:,2])+7)
    thresh2 = np.zeros((X,Y))
    vals = []
    for c in circles[0,:]:
        cv.circle(gray,(c[0],c[1]),r,(255,255,255),1)

        mask = np.zeros((X,Y))
        for x in range(c[0]-r*2,c[0]+r*2):
            for y in range(c[1]-r*2,c[1]+r*2):

                if 0 <= (x-c[0])**2 + (y-c[1])**2 <= r*5:
                    mask[y,x] = 1

                # if 4.5 <= (x-c[0])**2 + (y-c[1])**2 <= r*5:
                #     mask[y,x] = 0.5

        thresh2 = thresh2 + mask
        val = np.round(np.mean((gray*mask)[(gray*mask)>0]),2)
        vals.append(val)
        cv.putText(gray, str(val), (c[0] + r+ 5, c[1] + r+5),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))

print(np.std(vals))
cv.imshow('detected circles',thresh)
cv.imshow('detected circles2',thresh2)

cv.imshow('mean circles',gray)
cv.waitKey(0)
cv.destroyAllWindows()