
class CSS:
    '''
    contains all the css styling text we use, plus header and footer
    '''

    cssText = ''' <style> 
        body {
        position:relative; 
        left:20px;
        padding: 50px;
        font: 40px "Lucida Grande", Helvetica, Arial, sans-serif;
        background-color:cornsilk;
        } 
        input[type="text"] {
            font: 40px "Lucida Grande", Helvetica, Arial, sans-serif;
            width: 10em;
            height: 2em;
        }
        input[type="radio"] {
            width: 30px;
            height: 30px;
        }
        input[type="submit"] {
            width: 5em;  
            height: 2em;
            font-size: 40px;
            margin:15px 15px 15px 15px;
        }
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        } 
        th, td {
            padding: 15px;
        }
    </style>'''

    header = '''
        <!DOCTYPE html>
        <html>
        <head> 
    '''

    footer = '''
        </body>
        </head>
        </html>
    '''

    def __init__(self):
        self.apIndex = 0

    def getCSS(self):
        return self.cssText

    def getHeader(self):
        return self.header

    def getFooter(self):
        return self.footer