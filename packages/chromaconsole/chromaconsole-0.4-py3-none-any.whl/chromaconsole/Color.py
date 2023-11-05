from Style import enabled

class Color:
    @staticmethod
    def text(*args): #38;2;r;g;bm
        '''
        changes the color of the text\n
        Color.text(r, g, b)\n
        Color.text("#rrggbb")
        '''
        if enabled:
            if len(args) == 1:
                color = args[0].lstrip("#")
                if len(color) == 3:
                    r, g, b = (int(c * 2, 16) for c in color)
                elif len(color) == 6:
                    r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
                else:
                    raise ValueError("Invalid color format")
            elif len(args) == 3:
                r, g, b = args
            else:
                raise ValueError("Invalid number of arguments")

            return f"\033[38;2;{r};{g};{b}m"
        else:
            return ""
        
    @staticmethod
    def default_text(): #39m
        '''
        Default foreground color\n
        Implementation defined (according to standard)
        '''
        if enabled:
            return "\033[39m"
        else:
            return ""
    
    @staticmethod
    def background(*args): #48;2;r;g;bm
        '''
        changes the color of the text background\n
        Color.background(r, g, b)\n
        Color.background("#rrggbb")
        '''
        if enabled:
            if len(args) == 1:
                color = args[0].lstrip("#")
                if len(color) == 3:
                    r, g, b = (int(c * 2, 16) for c in color)
                elif len(color) == 6:
                    r, g, b = (int(color[i:i+2], 16) for i in range(0, 6, 2))
                else:
                    raise ValueError("Invalid color format")
            elif len(args) == 3:
                r, g, b = args
            else:
                raise ValueError("Invalid number of arguments")

            return f"\033[48;2;{r};{g};{b}m"
        else:
            return ""
    
    @staticmethod
    def default_background(): #49m
        '''
        Default background color\n
        Implementation defined (according to standard)
        '''
        if enabled:
            return "\033[49m"
        else:
            return ""
    
    @staticmethod
    def text_black():
        if enabled:
            return "\033[30m"
        else:
            return ""
        
    @staticmethod
    def text_red():
        if enabled:
            return "\033[31m"
        else:
            return ""
        
    @staticmethod
    def text_green():
        if enabled:
            return "\033[32m"
        else:
            return ""
        
    @staticmethod
    def text_yellow():
        if enabled:
            return "\033[33m"
        else:
            return ""
        
    @staticmethod
    def text_blue():
        if enabled:
            return "\033[34m"
        else:
            return ""
        
    @staticmethod
    def text_magenta():
        if enabled:
            return "\033[35m"
        else:
            return ""
        
    @staticmethod
    def text_cyan():
        if enabled:
            return "\033[36m"
        else:
            return ""
    
    @staticmethod
    def text_white():
        if enabled:
            return "\033[37m"
        else:
            return ""
        
    @staticmethod
    def bg_black():
        if enabled:
            return "\033[40m"
        else:
            return ""
        
    @staticmethod
    def bg_red():
        if enabled:
            return "\033[41m"
        else:
            return ""
        
    @staticmethod
    def bg_green():
        if enabled:
            return "\033[42m"
        else:
            return ""
        
    @staticmethod
    def bg_yellow():
        if enabled:
            return "\033[43m"
        else:
            return ""
        
    @staticmethod
    def bg_blue():
        if enabled:
            return "\033[44m"
        else:
            return ""
        
    @staticmethod
    def bg_magenta():
        if enabled:
            return "\033[45m"
        else:
            return ""
        
    @staticmethod
    def bg_cyan():
        if enabled:
            return "\033[46m"
        else:
            return ""
    
    @staticmethod
    def bg_white():
        if enabled:
            return "\033[47m"
        else:
            return ""
