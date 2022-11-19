import machine
import st7796s
import ft6x36

# LEDs
led_green = machine.Pin( 27, machine.Pin.OUT, value=0 )
led_red = machine.Pin( 12, machine.Pin.OUT, value=0 )

# Buttons
btn_left = machine.Pin( 2, machine.Pin.IN, machine.Pin.PULL_UP )
btn_right = machine.Pin( 4, machine.Pin.IN, machine.Pin.PULL_UP )

# LCD Init
LCD_SPI = 2
LCD_SPI_BAUDRATE = 20_000_000

lcd_rst= machine.Pin( 22, machine.Pin.OUT, value=0 )
lcd_cs = machine.Pin( 15, machine.Pin.OUT, value=1 )
lcd_dc = machine.Pin( 21, machine.Pin.OUT, value=0 )
lcd_bl = machine.Pin( 23, machine.Pin.OUT, value=0 )
lcd_sck  = machine.Pin( 14, machine.Pin.OUT )
lcd_mosi = machine.Pin( 13, machine.Pin.OUT )
lcd_miso = None

lcd_spi = machine.SPI(
    LCD_SPI,
    LCD_SPI_BAUDRATE,
    polarity=0,
    phase=0,
    sck=lcd_sck,
    mosi=lcd_mosi,
    miso=lcd_miso,
)
lcd = st7796s.St7796s( lcd_spi, lcd_rst, lcd_cs, lcd_dc, lcd_bl )

# TSC Init
TSC_I2C_ID = 1
TSC_I2C_BAUDRATE = 400_000
tsc_sda = machine.Pin( 18 )
tsc_scl = machine.Pin( 19 )
tsc_i2c = machine.I2C(
    TSC_I2C_ID,
    freq=TSC_I2C_BAUDRATE,
    sda=tsc_sda,
    scl=tsc_scl
)

TSC_CALIB_AX, TSC_CALIB_BX =-1.000, 480.0
TSC_CALIB_AY, TSC_CALIB_BY = 0.956, 6.533
tsc = ft6x36.Ft6x36(
    tsc_i2c,
    ax=TSC_CALIB_AX,
    bx=TSC_CALIB_BX,
    ay=TSC_CALIB_AY,
    by=TSC_CALIB_BY,
    swap_xy=True
)


# I2S init
I2S_ID = 0
I2S_BAUDRATE = 8000
I2S_BUF_SIZE = 8192
I2S_BITS = 16
i2s_sck = machine.Pin(0)
i2s_ws  = machine.Pin(5)
i2s_sd  = machine.Pin(35)
i2s_lr  = machine.Pin(25, machine.Pin.OUT, value=0 )

mic = machine.I2S(
    I2S_ID,
    sck=i2s_sck,
    ws=i2s_ws,
    sd=i2s_sd,
    mode=machine.I2S.RX,
    bits=I2S_BITS,
    format=machine.I2S.MONO,
    rate=I2S_BAUDRATE,
    ibuf=I2S_BUF_SIZE,
)

#print( "hal done" )