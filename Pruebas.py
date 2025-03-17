from functions.data_item_functions.data_item_15 import data_item_15
from functions.data_item_functions.data_item_16 import data_item_16
from functions.data_item_functions.data_item_17 import data_item_17
from functions.data_item_functions.data_item_19 import data_item_19
from functions.data_item_functions.data_item_21 import data_item_21
from functions.data_item_functions.data_item_22 import data_item_22
from functions.data_item_functions.data_item_23 import data_item_23
from functions.data_item_functions.data_item_24 import data_item_24
from functions.data_item_functions.data_item_25 import data_item_25
from functions.data_item_functions.data_item_26 import data_item_26

hexnumber_15 = str(11111111)
print("Prueba_15")
sigma = data_item_15(hexnumber_15)
for entry in sigma:
    print(entry)
print("\n")  

hexnumber_16 = str(11011213)
print("Prueba_16")
mensajes = data_item_16(hexnumber_16)
for entry in mensajes:
    print(entry)
print("\n") 

# PREGUNTAR EL 17 SI HAY QUE ESPECIFICAR LOS CODIGOS
hexnumber_17 = "1111"
print("Prueba_17")
code_mode3A = data_item_17(hexnumber_17)
for entry in code_mode3A:
    print(entry)
print (code_mode3A)
print("\n") 

# PREGUNTAR EL 18 SI HAY QUE ESPECIFICAR LOS CODIGOS Y INTENTAR ENTENDER LA ESTRUCTURA


hexnumber_19 = "1111"
print("Prueba_19")
height_3D = data_item_19(hexnumber_19)
print (height_3D)
print("\n") 

# PREGUNTAR EL 20 PARA QUE SIRVE EL FX DEL PRIMER OCTECT, ES DECIR, PARA QUE QUERRIAS ALARGAR ESTE FIELD?

hexnumber_21 = "1111"
print("Prueba_21")
messages = data_item_21(hexnumber_21)
for entry in messages:
    print(entry)
print (messages)
print("\n") 

hexnumber_22 = "11111111111111"
print("Prueba_22")
ACASRA = data_item_22(hexnumber_22)
print (ACASRA)
print("\n") 

hexnumber_23 = "11"
print("Prueba_23")
messages = data_item_23(hexnumber_23)
for entry in messages:
    print(entry)
print (messages)
print("\n") 

hexnumber_24 = "1111"
print("Prueba_24")
messages = data_item_24(hexnumber_24)
for entry in messages:
    print(entry)
print (messages)
print("\n") 

hexnumber_25 = "11"
print("Prueba_25")
messages = data_item_25(hexnumber_25)
for entry in messages:
    print(entry)
print (messages)
print("\n") 

hexnumber_26 = "1111"
print("Prueba_26")
messages = data_item_26(hexnumber_26)
for entry in messages:
    print(entry)
print (messages)
print("\n") 