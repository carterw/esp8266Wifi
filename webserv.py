# Begin configuration
TITLE    = "ESP8266 WiFi Configurator"
GPIO_NUM = 2
# End configuration

import network
import machine
import usocket

import accessPoints as ap
accessPointsFile = 'accessPoints.json'
aPoints = ap.AccessPoints(accessPointsFile)

# do a little test
point = aPoints.getAccessPointData('testSSID')
point['password'] = 'testPW'
aPoints.setAccessPointData('testSSID', point)

import cssStash as cssStash
css = cssStash.CSS()
cssString = css.getCSS()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
ap_if = network.WLAN(network.AP_IF) # create access-point interface
ap_if.active(True)         # activate it
try:
    # this doesn't work on some devices?
    ap_if.config(essid='ESP-AP') # set the ESSID of the access point
except OSError as ose:
    print(ose)
ifc = ap_if.ifconfig()
print('server at IP', ifc[0])

pin = machine.Pin(GPIO_NUM)

pin.init(pin.OUT)
try:
    pin.low()
except AttributeError:
    pin.off()


pwform = ''' 
<h3>Set access point password</h3>
<form method='GET' action='/setpw'>
    _SSID: verified = _VER<br><br>
    Password: <input type="text" class="text" name="password" value="_PW"><br>
    Name: <input type="text" class="text" name="apName" value="_NAME" placeholder="optional"><br>
    <span>
    <input type="submit" name="testpw" value="Test">
    <input type="submit" name="savepw" value="Save">
    </span>
    <input type="hidden" name="ssid" value="_SSID">
</form> 
'''

def makeActionButton(action, query, value):
    buttonStr = "<form method='POST' action='" + action + "?" + query.decode() + "'>"
    buttonStr += "<input type='submit' value='" + value + "'>"
    # <input type="hidden" name="query" value="something">
    buttonStr += "</form>"
    # print(buttonStr)
    return buttonStr

def makeRadio(name, value, mode):
    radioStr = "<input onChange='this.form.submit();' type='radio' name='" + name + "' value='" + value + "'/>"
    # print(radioStr)
    return radioStr

def makeAPtable(points):
    pointsStr = '<h2>Visible access points</h2>'
    pointsStr += '<form action="/getpw"" method="GET">'
    pointsStr += '<table><th>SSID</th><th>Open</th><th>Str</th><th>Known</th><th>Set</th></tr>'

    for i, point in enumerate(points):
        # print(point)
        aPoint = aPoints.getAccessPointData(point["ssid"])
        if 'verified' in aPoint and aPoint['verified'] == 1:
            point['verified'] = 'Y'
        else:
            point['verified'] = 'N'
        radioStr = makeRadio('radioSet', point["ssid"], point["authmode"])
        pointsStr += '<tr><td>' + point["ssid"] + '</td><td>' + point["authmode"] + '</td><td>' + point["rssi"] + '</td><td>' + point["verified"] + '</td><td>' + radioStr + '</td></tr>'
    pointsStr += '</table>'
    pointsStr += '</form><br>'
    return pointsStr

def emitScanTable(socket):
    points = aPoints.doScan(sta_if)
    apTable = makeAPtable(points)
    socket.write(apTable)

def emitPWform(socket, rawQuery):
    asString = str(rawQuery, "utf-8")
    # print('emitPWform>>> ', asString)
    parsedQuery = queryParse(asString)
    # print('emitPWform>>> ', parsedQuery)
    ssid = parsedQuery['radioSet']
    point = aPoints.getAccessPointData(ssid)

    actionButton = "<input type='submit' value='Submit'>"
    pwf = pwform
    # there's probably a more clever way to do the following...
    pwf = pwf.replace('_SSID', ssid)
    if 'password' in point:
        pwf = pwf.replace('_PW', point['password'])
    else:
        pwf = pwf.replace('_PW', '')
    if 'apName' in point:
        pwf = pwf.replace('_NAME', point['apName'])
    else:
        pwf = pwf.replace('_NAME', '')
    if 'verified' in point and point['verified'] == 1:
        pwf = pwf.replace('_VER', 'yes')
    else:
        pwf = pwf.replace('_VER', 'no')
    # print(pwf)
    socket.write(pwf)

reps = {'%20':' ', '%2B':' ', '+':' ', '%27':"'", '%23': '#'}
def unescape(text):
    for i, j in reps.items():
        text = text.replace(i, j)
    return text

def queryParse(queryString):
      result = {}
      pairs = queryString.split('&')
      for i, pair in enumerate(pairs):
          if '=' not in pair:
              continue
          key, value = pair.split('=')
          value = unescape(value)
        #   print('queryParse: ', key, value)
          result[key] = value
      return result

# may have hit the save button or the test button (test and then save)
def handleSetPW(rawQuery):
    asString = str(rawQuery, "utf-8")
    parsedQuery = queryParse(asString)
    # print('>>> ', parsedQuery)

    ssid = parsedQuery['ssid']
    point = aPoints.getAccessPointData(ssid)
    point['password'] = parsedQuery['password']
    point['apName'] = parsedQuery['apName']
    # print(point)

    if 'testpw' in parsedQuery:
        sta_if.active(True)
        sta_if.connect(ssid, point['password'])
        success = aPoints.checkLoop(sta_if, 10000)
        print('checkLoop result:', success)
        if success:
            point['verified'] = 1
        else:
            point['verified'] = 0
        sta_if.active(False)

    aPoints.setAccessPointData(ssid, point)

# this is where we construct the response
def respond(socket, path, query):
    global sta_if
    global aPoints

    print('accessed!')

    socket.write("HTTP/1.1 OK\r\n\r\n")
    socket.write(css.getHeader())
    socket.write(css.getCSS())
    socket.write("<title>"+TITLE+"</title>")
    socket.write("<body>")

    if path == b"/scan":
        emitScanTable(socket)
    elif path == b"/getpw":
        emitPWform(socket, query)
    elif path == b"/setpw":
        emitScanTable(socket)
    else:
        socket.write("<h2>ESP8266 WiFi Configurator</h2>")

    socket.write( makeActionButton('/scan', query, 'Scan') )

    socket.write("<br><br>")
    socket.write(" pin " + str(GPIO_NUM) + " status: ")
    if pin.value():
        socket.write("<span style='color:green'>OFF</span>")
    else:
        socket.write("<span style='color:red'>ON</span>")
    socket.write("<br>")
    if pin.value():
        socket.write( makeActionButton('/off', query, 'turn ON') )
    else:
        socket.write( makeActionButton('/on', query, 'turn OFF') )

    socket.write(css.getFooter())

def err(socket, code, message):
    socket.write("HTTP/1.1 "+code+" "+message+"\r\n\r\n")
    socket.write("<h1>"+message+"</h1>")

# HTTP requests come in here
def handleQuery(socket):
    try:
        (method, url, version) = socket.readline().split(b" ")
    except ValueError:
        print('invalid query')
        return

    if b"?" in url:
        (path, query) = url.split(b"?", 2)
    else:
        (path, query) = (url, b"")
    while True:
        header = socket.readline()
        if header == b"":
            return
        if header == b"\r\n":
            break

    print('path: ', path, 'query:', query)
    if version != b"HTTP/1.0\r\n" and version != b"HTTP/1.1\r\n":
        err(socket, "505", "Version Not Supported")
    elif method == b"GET":
        # print('GET', path, query)
        if path == b"/":
            respond(socket, path, query)
        elif path == b"/getpw":
            # print('received getpw')
            respond(socket, path, query)
        elif path == b"/setpw":
            # print('received setpw')
            # we go ahead and send response so browser doesn't time out
            path = b"/"
            respond(socket, path, query)
            handleSetPW(query)
        else:
            err(socket, "404", "Not Found")
    elif method == b"POST":
        if path == b"/on":
            # print('received ON')
            try:
                pin.high()
            except AttributeError:
                pin.on()
            respond(socket, path, query)
        elif path == b"/off":
            # print('received OFF')
            try:
                pin.low()
            except AttributeError:
                pin.off()
            respond(socket, path, query)
        elif path == b"/scan":
            # print('received scan')
            respond(socket, path, query)
        else:
            err(socket, "404", "Not Found")
    else:
        err(socket, "501", "Not Implemented")

server = usocket.socket()

def mainLoop():
    server.bind(('0.0.0.0', 80))
    server.listen(1)
    while True:
        try:
            (socket, sockaddr) = server.accept()
            handleQuery(socket)
        except OSError as ose:
            print(ose)
            code = ose.args[0]
            if code == 104 or code == 103 or code == 103: 
                print('OSError:', code)
                # ECONNRESET or ECONNABORTED or EALREADY
                return code
            socket.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
            socket.write("<h1>Internal Server Error</h1>")
        socket.close()

while True:
    mainLoop()