import lvgl as lv

class User_Interface:
    def __init__( self, cb_button_record, cb_button_codex, cb_button_run ):
        self.cb_button_record = cb_button_record
        self.cb_button_codex = cb_button_codex
        self.cb_button_run = cb_button_run
        
        self.label_terminal = None
        self.panel_terminal = None
        
        self.button_whisper = None
        self.button_codex = None
        self.button_run = None
        
        self.build_ui()
    
    def set_terminal( self, text ):
        self.label_terminal.set_text( text )
        self.panel_terminal.scroll_to_y( lv.COORD.MAX , lv.ANIM.OFF )
        self.panel_terminal.update_layout()
    
    def build_ui( self ):
        scr = lv.scr_act()
        
        style = lv.style_t()
        style.init()
        style.set_pad_all( 2 )
        style.set_pad_gap( 2 ) 
        style.set_radius( 2 )
        style.set_border_width( 0 )
        style.set_bg_color( lv.palette_lighten( lv.PALETTE.GREY, 3 ) )

        col = lv.obj( scr )
        col.add_style( style, 0 )
        col.set_flex_flow( lv.FLEX_FLOW.COLUMN )
        col.set_size( lv.pct(100), lv.pct(100) )
        col.clear_flag( lv.obj.FLAG.SCROLLABLE )

        self.panel_terminal = lv.obj( col )
        self.panel_terminal.set_size( lv.pct(98), lv.pct(80) )
        self.panel_terminal.clear_flag( lv.obj.FLAG.SCROLL_MOMENTUM )
        
        self.label_terminal = lv.label( self.panel_terminal )
        self.label_terminal.set_recolor( True)  
        
        row = lv.obj( col )
        row.add_style( style, 0 )
        row.set_flex_flow( lv.FLEX_FLOW.ROW )
        row.set_size(lv.pct(100), lv.pct(100) )

        self.button_record = lv.btn( row )
        self.button_record.add_flag( lv.obj.FLAG.CHECKABLE )
        self.button_record.set_size( lv.pct(33), lv.pct(18) )
        self.button_record.add_event_cb( self.cb_button_record, lv.EVENT.VALUE_CHANGED, None )
        label = lv.label( self.button_record )
        label.set_text( "Record" )
        label.center()

        self.button_codex = lv.btn( row )
        self.button_codex.set_size( lv.pct(33), lv.pct(18) )
        self.button_codex.add_event_cb( self.cb_button_codex, lv.EVENT.CLICKED, None )
        label = lv.label( self.button_codex )
        label.set_text( "Codex" )
        label.center()

        self.button_run = lv.btn( row )
        self.button_run.set_size( lv.pct(33), lv.pct(18) )
        self.button_run.add_event_cb( self.cb_button_run, lv.EVENT.CLICKED, None )
        label = lv.label( self.button_run )
        label.set_text( "Run" )
        label.center()
        
        self.button_record.clear_state( lv.STATE.DISABLED )
        self.button_codex.add_state( lv.STATE.DISABLED )
        self.button_run.add_state( lv.STATE.DISABLED )
        
