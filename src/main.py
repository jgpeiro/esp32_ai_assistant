import time
import machine
import hal

import lvgl as lv
import display_driver
import user_interface
import prompt

import secrets
import wifi
import google
import whisper
import codex

import wave
import recorder


use_whisper = False

class Application:
    FL_WAV_NAME = "record.wav"
    FL_PROMPT_NAME = "prompt.txt"
    
    def __init__( self ):
        lv.init()
        self.display_driver = display_driver.Display_Driver( hal.lcd, hal.tsc )
        self.ui = user_interface.User_Interface( self.cb_record, self.cb_codex, self.cb_run )
        with open( self.FL_PROMPT_NAME ) as fl:
            self.prompt = prompt.Prompt( fl.read() )
        self.ui.set_terminal( self.prompt.colorize(True) )
        self.prompt.run(True)
        self.recorder = recorder.Recorder( hal.mic, self.FL_WAV_NAME )
        self.wifi = wifi.Wifi()
    
    def cb_record( self, evt ):
        print("cb_record")
        if( self.ui.button_record.get_state() & lv.STATE.CHECKED ):
            self.recorder.start()
            
            self.ui.button_record.clear_state( lv.STATE.DISABLED )
            self.ui.button_codex.add_state( lv.STATE.DISABLED )
            self.ui.button_run.add_state( lv.STATE.DISABLED )
        else:
            self.recorder.stop()

            try:
                if( use_whisper ):
                    t0 = time.ticks_ms()
                    with open( self.FL_WAV_NAME, "rb" ) as fl:
                        buf = fl.read()
                    text = whisper.transcribe( buf=buf )
                    t1 = time.ticks_ms()
                    print( "transcribed", t1-t0, text )
                else:
                    # Option 2. Google AI
                    t0 = time.ticks_ms()
                    text = google.recognize( secrets.GOOGLE_KEY, self.FL_WAV_NAME )
                    t1 = time.ticks_ms()
                    print( "recognized", t1-t0, text )
                    if( not text ):
                        return
                    
                    t0 = time.ticks_ms()
                    text = google.translate( secrets.GOOGLE_KEY, text )
                    t1 = time.ticks_ms()
                    print( "translated", t1-t0, text )
                    if( not text ):
                        return
            except Exception as e:
                print("except", e )
                return
            self.prompt.add_human( text )
            self.ui.set_terminal( self.prompt.colorize(True) )
            
            self.ui.button_record.clear_state( lv.STATE.DISABLED )
            self.ui.button_codex.clear_state( lv.STATE.DISABLED )
            self.ui.button_run.add_state( lv.STATE.DISABLED )
    
    def cb_codex( self, evt ):
        print("cb_codex")
        # OpenAI Codex AI
        t0 = time.ticks_ms()
        status, text = codex.complete( secrets.OPENAI_KEY, self.prompt.text, 1000, [self.prompt.HUMAN_TURN] )
        t1 = time.ticks_ms()
        print( "codex", t1-t0, text )
        self.prompt.add_codex( text )
        self.ui.set_terminal( self.prompt.colorize(False) )
        
        self.ui.button_record.add_state( lv.STATE.DISABLED )
        self.ui.button_codex.clear_state( lv.STATE.DISABLED )
        self.ui.button_run.clear_state( lv.STATE.DISABLED )
    
    def cb_run( self, evt ):
        print("cb_run")
        self.prompt.run()
        
        self.ui.button_record.clear_state( lv.STATE.DISABLED )
        self.ui.button_codex.add_state( lv.STATE.DISABLED )
        self.ui.button_run.clear_state( lv.STATE.DISABLED )
    
    def run( self ):
        self.wifi.connect( secrets.WIFI_SSID, secrets.WIFI_PSWD )
        try:
            while( True ):
                self.display_driver.process()
                time.sleep_ms(10)
        except Exception as e:
            print( "except", e )
            self.wifi.disconnect()
            machine.reset()

app = Application()
app.run()

print("done")