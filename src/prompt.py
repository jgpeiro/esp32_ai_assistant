
class Prompt:
    NEW_LINE = "\r\n" # Be sure it matches your text editor
    NEW_LINE_LVGL = "\n"
    
    HUMAN_TURN = "# Human: " # Note all ends with space. This is not mandatory.
    CODEX_TURN = "# Esp32: "
    REPL_SIGNS = ">>> "
    REPL_DOTS = "... "
    
    START_COLOR_CMD = "$"
    END_COLOR_CMD = "$"
    
    HUMAN_COLOR   = "7F0000" # RED"
    REPL_COLOR    = "444444" # GREY
    CODEX_COLOR   = "00007F" # BLUE
    DEFAULT_COLOR = "000000" # BLACK
    
    COLON = ":"
    
    def __init__( self, text ):
        self.text = text
        
        self.text_human = text  # Use two temporal prompts allows kind of "retry" operation without duplicate last text.
        self.text_codex = text
        self.text_codex_last = ""
        
    def add_human( self, text ):
        self.text = self.text_codex
        self.text_human = self.text + text + self.NEW_LINE + self.CODEX_TURN
    
    def add_codex( self, text ):
        if( text[-1] == "\n" ):
            text = text[:-1]
        if( text[-1] == "\r" ):
            text = text[:-1]
        self.text_codex_last = text + self.NEW_LINE
        self.text = self.text_human
        self.text_codex = self.text + text + self.NEW_LINE + self.HUMAN_TURN
    
    def run( self, is_first=False ):
        if( is_first ):
            text = self.text.split( self.NEW_LINE )
        else:
            text = self.text_codex_last.split( self.NEW_LINE )
        try:
            lines = []
            for line in text:
                line = line.strip()
                
                if( line.startswith( self.REPL_SIGNS ) ):
                    if( len( lines ) ):
                        code = self.NEW_LINE.join( lines )
                        exec( code )
                        lines = []
                    
                    if( line.endswith( self.COLON ) ):
                        lines.append( line.replace( self.REPL_SIGNS , "" ) )
                    else:
                        code = line.replace( self.REPL_SIGNS, "" )
                        if( code == self.REPL_SIGNS[:-1] ):
                            continue
                        exec( code )
                
                elif( line.startswith( self.REPL_DOTS ) ):
                    lines.append( line.replace( self.REPL_DOTS, "" ) )
            
            if( len( lines ) ):
                code = self.NEW_LINE.join( lines )
                exec( code )
                lines = []
        except Exception as e:
            print( "run failed", e )
    
    def colorize_line( self, line, color ):
        # The space after the color is needed by LVGL
        return self.START_COLOR_CMD + color + " " + line + self.END_COLOR_CMD
    
    def colorize( self, is_human ):
        if( is_human ):
            text = self.text_human.split( self.NEW_LINE )
        else:
            text = self.text_codex.split( self.NEW_LINE )
        
        text_color = ""
        for line in text:
            if line.startswith( self.HUMAN_TURN ):
                text_color += self.colorize_line( line, self.HUMAN_COLOR )
            
            elif line.startswith( self.REPL_SIGNS ) or line.startswith( self.REPL_DOTS ) :
                text_color += self.colorize_line( line, self.REPL_COLOR )
            
            elif line.startswith( self.CODEX_TURN ):
                text_color += self.colorize_line( line, self.CODEX_COLOR )
            
            else:
                text_color += self.colorize_line( line, self.DEFAULT_COLOR )
            
            text_color += self.NEW_LINE_LVGL
        
        return text_color
