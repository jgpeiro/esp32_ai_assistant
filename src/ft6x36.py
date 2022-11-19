import time
import machine

class Ft6x36:
    SLAVE_ADDR = 0x38
    
    STATUS_REG = 0x02
    P1_XH_REG  = 0x03
    
    def __init__( self, i2c, ax=1, bx=0, ay=1, by=0, swap_xy=False ):
        self.i2c = i2c
        self.ax = ax
        self.bx = bx
        self.ay = ay
        self.by = by
        self.swap_xy = swap_xy
        self.read_buffer1 = bytearray(1)
        self.read_buffer4 = bytearray(4)
    
    def read( self ):
        self.i2c.readfrom_mem_into( self.SLAVE_ADDR, self.STATUS_REG, self.read_buffer1 )
        points = self.read_buffer1[0] & 0x0F
        if( points == 1 ):
            time.sleep_ms(1)
            # Read again to avoid glitches
            self.i2c.readfrom_mem_into( self.SLAVE_ADDR, self.STATUS_REG, self.read_buffer1 )
            points = self.read_buffer1[0] & 0x0F
            if( points == 1 ):
                self.i2c.readfrom_mem_into( self.SLAVE_ADDR, self.P1_XH_REG, self.read_buffer4 )
                x = (self.read_buffer4[0] << 8 | self.read_buffer4[1]) & 0x0FFF
                y = (self.read_buffer4[2] << 8 | self.read_buffer4[3]) & 0x0FFF
                
                if( self.swap_xy ):
                    tmp = x
                    x = y
                    y = tmp
                
                x = self.ax*x + self.bx
                y = self.ay*y + self.by
                return 1, x, y
            else:
                return 0, 0, 0
        else:
            return 0, 0, 0