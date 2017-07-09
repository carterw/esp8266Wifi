import ujson
import os
import utime

class AccessPoints:
    '''
    Reads/writes a parameters file in JSON format
    '''
    apParams = {}
    accessPointsFilename = ''
    apIndex = 0

    def __init__(self, filename):
        self.accessPointsFilename = filename

    def readApFile(self):
        fileName = self.accessPointsFilename
        fileList = os.listdir()
        if fileName in fileList:
            f = open(self.accessPointsFilename)
            data = f.read()
            f.close()
            # print(data)
            self.apParams = ujson.loads(data)
        else:
            self.apParams['accessPoints'] = {}
            # self.setSection('accessPoints', {})
            self.writeApFile()

    def getSection(self, sectionName):
        self.readApFile()        
        if sectionName in self.apParams:
            section = self.apParams[sectionName]
            apParams = {}
            return section
        else:
            print('getSection', sectionName, ' not found')
            return None # should raise exception
    
    def setSection(self, sectionName, sectionData):
        self.readApFile()
        self.apParams[sectionName] = sectionData
        self.writeApFile()
        apParams = {}

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
        accessPoints = self.getSection('accessPoints')
        apLength = len(accessPoints)
        if self.apIndex == apLength:
            self.apIndex = 0
        ap = next( v for i, v in enumerate(accessPoints.values()) if i == self.apIndex )
        self.apIndex += 1
        return ap    

    def checkAccessPointIgnore(self, point):
        if 'verified' in point:
            if point['verified'] == 2:
                return True
        return False

    def getAccessPointPassword(self, ssid):
        accessPoints = self.getSection('accessPoints')
        password = ''
        if ssid in accessPoints:
            point = accessPoints[ssid]
            # print('password found!!!', point['password'])
            return point['password']
        return password

    def writeApFile(self):
        f = open(self.accessPointsFilename, 'w')
        jsonData = ujson.dumps(self.apParams)
        f.write(jsonData)
        f.close()

class NetScan:

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