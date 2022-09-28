class TerminalColors():
    purple  = '\033[95m'
    blue    = '\033[94m'
    cyan    = '\033[96m'
    green   = '\033[92m'
    red     = '\033[93m'
    endColor    = '\033[0m'
    bold        = '\033[1m'
    underline   = '\033[4m'
    face        = '\u001b[31;1m'
    debug       = '\u001b[30;1m'
    file        = '\033[95m'
    
    pure_red = "\033[0;31m"
    dark_green = "\033[0;32m"
    orange = "\033[0;33m"
    dark_blue = "\033[0;34m"
    bright_purple = "\033[0;35m"
    dark_cyan = "\033[0;36m"
    dull_white = "\033[0;37m"
    pure_black = "\033[0;30m"
    bright_red = "\033[0;91m"
    light_green = "\033[0;92m"
    yellow = "\033[0;93m"
    bright_blue = "\033[0;94m"
    magenta = "\033[0;95m"
    light_cyan = "\033[0;96m"
    bright_black = "\033[0;90m"
    bright_white = "\033[0;97m"
    cyan_back = "\033[0;46m"
    purple_back = "\033[0;45m"
    white_back = "\033[0;47m"
    blue_back = "\033[0;44m"
    orange_back = "\033[0;43m"
    green_back = "\033[0;42m"
    pink_back = "\033[0;41m"
    grey_back = "\033[0;40m"
    grey = '\033[38;4;236m'
    bold = "\033[1m"
    underline = "\033[4m"
    italic = "\033[3m"
    darken = "\033[2m"
    invisible = '\033[08m'
    reverse_colour = '\033[07m'
    
    
    def getString(self, string, color, newLine = False):
        if hasattr(self, color):
            colorVar = getattr(self, color)
            return str(colorVar+string+self.endColor+("\n" if newLine == True else ''))
        else:
            return string+("\n" if newLine == True else '')
