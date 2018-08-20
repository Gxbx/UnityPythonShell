import cv2, numpy as np
from math import sqrt
import numpy as np
from matplotlib import pyplot as plt

class DetectDarkZones:

    def __init__(self, zones):
        self._zones   = zones
        self._step    = 0
        self._centers = []
        self._histogs = []
        self._brightness = np.arange(256)/256

    def __init__(self, zones, width, height):
        self._zones   = zones
        self._width   = width
        self._height  = height
        self._centers = []
        self._histogs = []
        self._brightness = np.arange(256)/256
        N = self._width * self._height
        self._step = int(sqrt(N/self._zones))

    def getModel(self, frame, midStep = 0):
        '''
        Get the histogram model.
        Input:
            frame:
            midStep: Half of the step.
        '''
        x_center = int(self._step/2)
        while x_center < self._width:
            y_center = int(self._step/2)
            while y_center < self._height:
                self._histogs.append(self.detectHistogram(frame[y_center - midStep : y_center + midStep, x_center - midStep : x_center + midStep]))
                self._centers.append((x_center, y_center))
                y_center = y_center + self._step
            x_center = x_center + self._step

    def detectZones(self, frame):
        '''
        Detect the light by zones.
        Input:
             frame: Image ro process.
        '''
        self._centers = []
        self._histogs = []
        midStep = int(self._step/2)
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.getModel(grayFrame, midStep)

    def drawRectangle(self, frame, color = (255,255,255), thickness = 1):
        '''
        Draw in the principal image the porcentage of each area.
        Input:
            frame: Image to be painted
            color:
            thickness:
        Output:
            frame: Image painted with rectangles of each area.
        '''
        midStep = int(self._step/2)
        for center in self._centers:
            cv2.rectangle(frame, (center[0] - midStep, center[1] - midStep), (center[0] + midStep, center[1] + midStep), color, thickness, cv2.LINE_AA)
        return frame

    def drawPercentage(self, frame, color = (255,255,255), thickness = 1):
        '''
        Draw in the principal image the porcentage of each area.
        Input:
              frame: image to be painted.
              color:
              thickness:
        Output:
              frame: Image painted with text of each area.
        '''
        midStep = int(self._step/2)
        for center, perce in zip(self._centers, self._histogs):
            cv2.putText(frame, str(int(perce)) + '%', (center[0] - midStep, center[1]), cv2.FONT_HERSHEY_PLAIN , 1, color, thickness, cv2.LINE_AA)
        return frame

    def detectHistogram(self, Frame):
        '''
        Get Histogram model for each area
        Input:
             Frame: roi area in gray scale
        Ouput:
             frame: percentage of light in the input area.
        '''
        x, y = Frame.shape
        totalPixels = x * y
        percentage = 0
        histogram = cv2.calcHist([Frame], [0], None, [256], [0,256])
        for numPixels, bright in zip(histogram, self._brightness):
            percentage = percentage + ((numPixels/totalPixels) * bright)
        return percentage * 100

    def setWidthAndHeight(self, width=0, height=0):
        '''
        Set width and height of an image
        Input:
              width:
              height:
        '''
        self._width  = _width
        self._height = _height
        N = self._width * self._height;
        self._step = sqrt(N/self._zones)

    def getDarkestZone(self):
        '''
        Get vector of the darknest zone.
        Output:
              pos: Contain the position x and y. (x, y)
        '''
        min = self._histogs[0]
        pos = self._centers[0]
        var = 0
        for value in self._histogs:
            if value < min:
                min = value
                pos = self._centers[var]
            var = var + 1
        return pos

    def getLightestZone(self):
        '''
        Get vector of the Lightest zone.
        output:
              pos: Contain the position x and y. exm: (x, y)
        '''
        max = self._histogs[0]
        pos = self._centers[0]
        var = 0
        for value in self._histogs:
            if value > max:
                max = value
                pos = self._centers[var]
            var = var + 1
        return pos

    def getDarknestAndLightestZone(self):
            '''
            Get vector of the darknest and Lightest zone.
            output:
                  pos: Contain the position x and y. exm: [(dx, dy), (lx,ly)]
            '''
            min = self._histogs[0]
            max = self._histogs[0]
            posMin = self._centers[0]
            posMax = self._centers[0]
            var = 0
            for value in self._histogs:
                if value < min:
                    min = value
                    posMin = self._centers[var]
                if value > max:
                    max = value
                    posMax = self._centers[var]
                var = var + 1
            return [posMin, posMax]

    def getDarkZones(self, amount = -1):
        '''
        get the amount defined by "amount"
        Input:
             amount: number of dark areas.
        Output:
             hisMin: Contain the position x and y for tha amount dark areas. exm: amount = 3 [(x1, y1), (x2, y2), (x3, y3)]
        '''
        if amount < 0 or amount >= len(self._centers):
            return self._histogs
        if amount > 0:
            histogs  = self._histogs
            hisMin   = []
            pos      = 0
            min      = self._histogs[0]
            counter  = 0
            position = 0
            while counter < amount:
                for percentage in histogs:
                    if percentage < min:
                        min = percentage
                        pos = position
                    position = position + 1
                hisMin.append(self._centers[pos])
                histogs[pos] = 100;
                position = 0
                min = histogs[pos]
                pos = 0
                counter = counter + 1
            return hisMin
