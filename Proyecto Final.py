import network, time, urequests
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from MAX6675 import MAX6675

#Conexion de pantalla
ancho = 128
alto = 64
i2c = I2C( 0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto,i2c)

#Conexion de termocupla
so = Pin(12, Pin.IN)
sck = Pin(14, Pin.OUT)
cs = Pin(16, Pin.OUT)
max = MAX6675(sck, cs , so)

#Conexion a wifi
def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi ("FAMILIA LUNA", "Spike1998@"):
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    url = "https://api.thingspeak.com/update?api_key=T8SZFO2CZSN66UN1&field1=0"


print(i2c.scan())
while True:

    time.sleep(1)
    temp= max.read()
    print(temp)
    respuesta = urequests.get(url+"&field1="+str(temp)) 
    respuesta.close ()
    oled.fill(0)
    oled.text("Temperatura C", 0,20)
    oled.text(str(temp), 0,40)
    oled.show()

else:
    print ("Imposible conectar")
    miRed.active (False)  
