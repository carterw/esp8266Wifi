import ujson
import os
import utime

class AccessPoints:
    '''
    Reads/writes a parameters file in JSON format
    '''
    rtParams = {}
    rtParamsFilename = ''
    apIndex = 0

    def __init__(self, filename):
        self.rtParamsFilename = filename

    def readParamsFile(self):
        fileName = self.rtParamsFilename
        fileList = os.listdir()
        if fileName in fileList:
            f = open(self.rtParamsFilename)
            data = f.read()
            f.close()
            # print(data)
            self.rtParams = ujson.loads(data)
        else:
            self.rtParams['accessPoints'] = {}
            # self.setSection('accessPoints', {})
            self.writeParamsFile()

    def getSection(self, sectionName):
        self.readParamsFile()        
        if sectionName in self.rtParams:
            section = self.rtParams[sectionName]
            rtParams = {}
            return section
        else:
            print('getSection', sectionName, ' not found')
            return None # should raise exception
    
    def setSection(self, sectionName, sectionData):
        self.readParamsFile()
        self.rtParams[sectionName] = sectionData
        self.writeParamsFile()
        rtParams = {}

    def getAccessPointData(self, ssid):
        accessPoints = self.getSection('accessPoints')
        if ssid in accessPoints:
            return accessPoints[ssid]
        else:
            # print(ssid, ' password not found')
            return {}

    def setAccessPointData(self, ssid, point):
        accessPoints = self.getSection('accessPoints')
        accessPoints[ssid] = point
        self.setSection('accessPoints', accessPoints)

    def getNextAccessPoint(self):
        # should check to make sure this element is present
        accessPoints = self.getSection('accessPoints')
        if self.apIndex == len(accessPoints):
            self.apIndex = 0
        ap = accessPoints[self.apIndex]
        self.apIndex += 1
        return ap     

    def writeParamsFile(self):
        f = open(self.rtParamsFilename, 'w')
        jsonData = ujson.dumps(self.rtParams)
        f.write(jsonData)
        f.close()

    def doScan(self, wlan):
        points = []

        wlan.active(True)

        accessPoints = wlan.scan()

        for i, point in enumerate(accessPoints):
            # print(point)
            ssid = point[0]
            ssid = str(ssid, "utf-8")
            rssi = point[3]
            authmode = point[4]
            hidden = point[5]

            if authmode == 0:
                authmode = 'open'
            else:
                authmode = 'pw'

            if hidden == 0:
                hidden = 'visible'
            else:
                hidden = 'hidden'

            pobj = {"ssid": ssid, "rssi": str(rssi), "authmode": authmode, "hidden": hidden}
            points.append(pobj)
        wlan.active(False)
        return points

    def checkLoop(self, wlan, totalMS):
        '''
        Look to see if we have a network connection periodically. If/when
        we do, return True immediately. If we haven't seen one within
        totalMS we return False
        '''
        checkInterval = 500
        timeElapsed = 0

        while timeElapsed < totalMS:
            status = wlan.isconnected()
            if status:
                return True
            utime.sleep_ms(checkInterval)
            timeElapsed += checkInterval
        return False