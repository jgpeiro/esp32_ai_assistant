import time
import array
import wave

class Recorder:
    STATE_IDLE   = 0
    STATE_START  = 1
    STATE_RECORD = 2
    STATE_STOP   = 3
    
    def __init__( self, i2s, fl_name, buf_len=800 ):
        self.i2s = i2s
        self.state = self.STATE_IDLE
        self.buf = array.array( "h", [0]*buf_len )
        self.buf_mv = memoryview( self.buf )
        self.wave = wave.Wave( fl_name )
        self.t0 = 0
        self.t1 = 0
    
    def start( self ):
        self.state = self.STATE_START
        self.process( None ) # Start the fsm. This will continue via i2s interrupts
    
    def stop( self ):
        self.state = self.STATE_STOP
        while( self.state != self.STATE_IDLE ):
            time.sleep_ms( 100 )
    
    def process( self, arg ):
        if( self.state == self.STATE_IDLE ):
            pass
        
        elif( self.state == self.STATE_START ):
            self.wave.open()
            self.i2s.irq( self.process )
            self.i2s.readinto( self.buf_mv )
            self.state = self.STATE_RECORD
        
        elif( self.state == self.STATE_RECORD ):
            self.wave.write( self.buf_mv )
            self.i2s.readinto( self.buf_mv )
        
        elif( self.state == self.STATE_STOP ):
            self.wave.write( self.buf )
            self.i2s.irq( None )
            self.wave.close()
            self.state = self.STATE_IDLE