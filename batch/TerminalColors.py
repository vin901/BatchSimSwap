class TerminalColors():
    purple  = '\033[95m'
    blue    = '\033[94m'
    cyan    = '\033[96m'
    green   = '\033[92m'
    red     = '\033[93m'
    yellow  = '\033[91m'
    endColor    = '\033[0m'
    bold        = '\033[1m'
    underline   = '\033[4m'
    face        = '\u001b[31;1m'
    debug       = '\u001b[30;1m'
    file        = '\033[95m'
    
    def getString(self, string, color, newLine = False):
        if hasattr(self, color):
            colorVar = getattr(self, color)
            return str(colorVar+string+self.endColor+("\n" if newLine == True else ''))
        else:
            return string+("\n" if newLine == True else '')
