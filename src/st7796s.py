import time
import machine

class St7796s:
    WIDTH = 480
    HEIGHT = 320

    CASET = 0x2A
    RASET = 0x2B
    RAMWR = 0x2C 

    X_OFFSET = 0
    Y_OFFSET = 0
    
    def __init__( self, spi, rst, cs, dc, bl ):
        self.spi = spi
        self.rst = rst
        self.cs = cs
        self.dc = dc
        self.bl = bl
        self.buf1 = bytearray(1)
        self.buf4 = bytearray(4)
        self.reset()
        self.config()
        self.clear()
        self.bl.value(1)
    
    def reset( self ):
        self.rst.value(0)
        self.cs.value(1)
        self.dc.value(0)
        self.bl.value(0)
        time.sleep_ms( 10 )
        
        self.rst.value(1)
        time.sleep_ms( 100 )
    
    def write_reg( self, cmd, buf ):
        self.buf1[0] = cmd
        
        self.dc(0)
        self.cs(0)
        self.spi.write( self.buf1 )
        if( buf ):
            self.dc(1)
            self.spi.write( buf )
        self.cs(1)
        self.dc(0)
    
    def config( self ):
        self.write_reg( 0x01, b"\x01" )
        time.sleep_ms( 100 )
        self.write_reg( 0x11, b"" )
        time.sleep_ms( 10 )
        self.write_reg( 0x36, b"\xF8" ) # b"\xF0" ) #b"\x70" )
        self.write_reg( 0x3A, b"\x05" )
        self.write_reg( 0xB2, b"\x0C\x0C\x00\x33\x33"  )
        self.write_reg( 0xB7, b"\x35" )
        self.write_reg( 0xBB, b"\x19" )
        self.write_reg( 0xC0, b"\x2C" )
        self.write_reg( 0xC2, b"\x01" )
        self.write_reg( 0xC3, b"\x12" )
        self.write_reg( 0xC4, b"\x20" )
        self.write_reg( 0xC6, b"\x0F" )
        self.write_reg( 0xD0, b"\xA4\xA1" )
        self.write_reg( 0xE0, b"\xD0\x04\x0D\x11\x13\x2B\x3F\x54\x4C\x18\x0D\x0B\x1F\x23" )
        self.write_reg( 0xE1, b"\xD0\x04\x0C\x11\x13\x2C\x3F\x44\x51\x2F\x1F\x1F\x20\x23" )
        #self.write_reg( 0x21, b"" ) # Display Inversion On
        self.write_reg( 0x11, b"" )
        self.write_reg( 0x29, b"" )
        time.sleep_ms( 100 )
    
    def set_window( self, x, y, w, h ):
        x0 = x + self.X_OFFSET
        y0 = y + self.Y_OFFSET
        x1 = x0 + w - 1
        y1 = y0 + h - 1
        
        self.buf4[0] = x0>>8
        self.buf4[1] = x0&0xFF
        self.buf4[2] = x1>>8
        self.buf4[3] = x1&0xFF
        self.write_reg( self.CASET, self.buf4 )
        
        self.buf4[0] = y0>>8
        self.buf4[1] = y0&0xFF
        self.buf4[2] = y1>>8
        self.buf4[3] = y1&0xFF
        self.write_reg( self.RASET, self.buf4 )

    def draw( self, x, y, w, h, buf ):
        self.set_window( x, y, w, h )
        self.write_reg( self.RAMWR, buf )

    def clear( self ):
        buf = bytearray( [0xFF, 0xFF]*self.WIDTH )
        for i in range( self.HEIGHT ):
            self.draw( 0, i, self.WIDTH, 1, buf )
