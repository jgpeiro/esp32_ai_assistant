import time
import lvgl as lv

class Display_Driver:
    def __init__( self, lcd, tsc ):
        self.lcd = lcd
        self.tsc = tsc
        
        self.fb1 = None
        self.fb2 = None
        
        self.disp_draw_buf = None
        self.disp_drv = None
        self.indev_drv = None
        
        self.is_fb1 = True
    
        self.x_bck = 0
        self.y_bck = 0
        self.p_bck = 0
        
        self.initialize()
        self.last_tick = time.ticks_ms()
    
    def initialize( self ):
        FB_HEIGHT = self.lcd.HEIGHT//8       
        self.fb1 = bytearray( self.lcd.WIDTH*FB_HEIGHT*lv.color_t.__SIZE__ )
        self.fb2 = bytearray( self.lcd.WIDTH*FB_HEIGHT*lv.color_t.__SIZE__ )
    
        self.disp_draw_buf = lv.disp_draw_buf_t()
        self.disp_draw_buf.init( self.fb1, self.fb2, len( self.fb1 )//lv.color_t.__SIZE__ )

        self.disp_drv = lv.disp_drv_t()
        self.disp_drv.init()
        self.disp_drv.draw_buf = self.disp_draw_buf
        self.disp_drv.flush_cb = self.disp_drv_flush_cb
        self.disp_drv.hor_res = self.lcd.WIDTH
        self.disp_drv.ver_res = self.lcd.HEIGHT
        self.disp_drv.color_format = lv.COLOR_FORMAT.NATIVE_REVERSE
        self.disp_drv.register()
        
        self.indev_drv = lv.indev_drv_t()
        self.indev_drv.init()
        self.indev_drv.type = lv.INDEV_TYPE.POINTER
        self.indev_drv.read_cb = self.indev_drv_read_cb
        self.indev_drv.register()

    def disp_drv_flush_cb( self, disp_drv, area, color ):
        if( self.is_fb1 ):
            fb = memoryview( self.fb1 )
        else:
            fb = memoryview( self.fb2 )
        self.is_fb1 = not self.is_fb1
        x = area.x1
        y = area.y1
        w = area.x2 - area.x1 + 1
        h = area.y2 - area.y1 + 1
        self.lcd.draw( x, y, w, h, fb[0:w*h*lv.color_t.__SIZE__] )
        self.disp_drv.flush_ready()

    def indev_drv_read_cb( self, indev_drv, data ):
        p, x, y = self.tsc.read()
        if( p ):
            self.x_bck = x
            self.y_bck = y
        self.s_bck = p
        
        data.point.x = int( self.x_bck )
        data.point.y = int( self.y_bck )
        data.state = int( self.s_bck )
        return False
    
    def process( self ):
        tick = time.ticks_ms()
        lv.tick_inc( tick - self.last_tick )
        lv.task_handler()
        self.last_tick = tick
