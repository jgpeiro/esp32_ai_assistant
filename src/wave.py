import struct

class Wave:
    HEADER_FMT = "<4sI4s4sIHHIIHH4sI"
    FORMAT_PCM = 1
    
    def __init__( self, fl_name, freq=8000, bits=16, channels=1 ):
        self.fl_name = fl_name
        self.freq = freq
        self.bits = bits
        self.channels = channels
        
        self.fl = None
        self.size = 0
    
    def build_header( self ):
        header = struct.pack( self.HEADER_FMT,
            b'RIFF',
            self.size + struct.calcsize( self.HEADER_FMT ) - 8,
            b'WAVE',
            b'fmt ',
            self.bits,
            self.FORMAT_PCM,
            self.channels,
            self.freq, 
            (self.freq*self.channels*self.bits)//8,
            (self.channels * self.bits)//8,
            self.bits,
            b'data',
            self.size
        )
        return header
    
    def open( self ):
        self.fl = open( self.fl_name, "wb" )
        self.fl.write( self.build_header() )
    
    def write( self, buf ):
        self.size += self.fl.write( buf )
    
    def close( self ):
        # Update header with the written data
        self.fl.seek( 0 )
        self.fl.write( self.build_header() )
        self.fl.close()

