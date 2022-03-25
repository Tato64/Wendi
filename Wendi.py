import json
import requests
from requests_html import HTMLSession
from datetime import datetime

#####################################################################
#        .{{}}}}}}.                                                 #
#       {{{{{}}}}}}}.       __          __            _ _           #        
#      {{{{  }}}}}}}}}      \ \        / /           | (_)          #
#     }}}}} _   _ {{{{{      \ \  /\  / /__ _ __   __| |_           #
#     }}}}  U   U  {{{{       \ \/  \/ / _ \ '_ \ / _` | |          #
#    {{{{{    ^    }}}}}       \  /\  /  __/ | | | (_| | |          #
#   {{{{{{\  ._.  /}}}}}}       \/  \/ \___|_| |_|\__,_|_|          #
#   {{{{{{{;.___.;}}}}}}}                                           #
#                                                                   #
#   Wendi ("Wen dia") es un programa creado para entregar           #
#   algunos datos utiles al inicio del dia (Preferentemente,        #
#   porque reconoce la hora actual para saludar de la forma         #
#   correcta) y tambien mi primer proyecto de web scraping.         # 
#####################################################################

url_dia = "https://www.google.com/search?q=fecha+de+hoy"    # Para el dia y
url_clima = "https://www.google.com/search?q=clima"         # la fecha se utiliza Google.
url_dolar = "https://api.bluelytics.com.ar/v2/latest"       # Para el dolar, un API publico.
url_bitcoin = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"           # Y para el bitcoin, un API que requiere key.

r1 = HTMLSession().get(url_dia, headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
r2 = HTMLSession().get(url_clima, headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"})
r3 = requests.get(url_dolar)
#"r4" Esta mas abajo, ya que esa informacion sale de un API que requiere clave.

headers_bitcoin = {
    "Accepts":"application/json",
    "X-CMC_PRO_API_KEY":"3a4bbe89-1cc2-4521-a218-363bc03b69db" #Dejo la clave asi porque la cuenta asociada no importa, y para que otros puedan usar el programa sin tener que obtener una key y editar el codigo.
}
r4 = requests.get(url_bitcoin, params = {"slug":"bitcoin","convert":"USD"}, headers = headers_bitcoin)

#Clima
hora = int(datetime.now().strftime("%H")) #Para la hora no hace web scraping, utiliza la hora del sistema.
fecha = r1.html.find("div.vk_bk.dDoNo.FzvWSb", first = True).text
temp = r2.html.find("span#wob_tm", first = True).text
unit = r2.html.find("div.vk_bk.wob-unit span.wob_t", first = True).text
rain = r2.html.find("span#wob_pp",first = True).text
#Economia
dolar = json.loads(r3.text)["blue"]["value_sell"]
bitcoin = json.loads(r4.text)["data"]["1"]["quote"]["USD"]["price"]


temp_int = int(temp)                    # Estos dos transforman los valores de temperatura y % de precipitaciones
rain_int = int(rain.replace("%",""))    # en un int, para calcular las sugerencias de abrigo y lluvia.

rain_text = ""
temp_text = ""
saludo = ""

#Texto sobre la temperatura. La sugerencia de abrigo esta ajustada a mi preferencia, y soy todo lo contrario a friolento.
if temp_int > 20:
    temp_text = "No hace falta un abrigo, la temperatura es de "
elif temp_int > 16:
    temp_text = "Un buzo seria buena idea porque la temperatura es de "
elif temp_int <= 16 :
    temp_text = "Vas a necesitar una campera porque la temperatura es de "

#Texto sobre la lluvia
if rain_int > 70:
    rain_text = "Cuidado, va a llover fuertemente."
elif rain_int > 50:
    rain_text = "Hay lluvias considerables."
elif rain_int > 20:
    rain_text = "Cae agua del cielo."
elif rain_int >= 10:
    rain_text = "Hay ligeras lluvias."
elif rain_int < 10:
    rain_text = "Poco riesgo de lluvias."
else:
    raint_text = "No hay riesgo de lluvias."

#Buenos dias? Buenas tardes? Buenas noches?
if hora >= 20:
    saludo = "Buenas noches!"
elif hora >= 14:
    saludo = "Buenas tardes!"
elif hora >= 6:
    saludo = "Buen dia!"
else:
    saludo = "Buenas madrugadas!"


#Prints
print("#_______________________________________________________________#")
print("| " + saludo + " Hoy es " + fecha + ".")
print("| " + temp_text + temp + " " + unit)
print("| " + rain_text)
print("#_______________________________________________________________#")
print("| $$$ Divisas $$$")
print("| \tDolar Blue: \t$" + str(int(dolar)) + " ARS")
print("| \tBitcoin: \t$" + str(int(bitcoin)) + " USD")
print("#_______________________________________________________________#")
print("| Estado del transporte publico:")
print("| [ACA IRIA INFORMACION SOBRE EL ESTADO DE TRENES Y SUBTES\n| SI EL REGISTRO DEL API DE TRANSPORTE PUBLICO FUNCIONARA]")
print("#_______________________________________________________________#")
print("| Pasala lindo y tomá agua, toca ENTER para salir.")
print("#_______________________________________________________________#")

a = input()
if a:
    quit()