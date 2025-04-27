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
from functions.data_item_functions.data_item_28 import data_item_28
from functions.data_item_functions.data_item_1Corrected import data_item_1
from functions.data_item_functions.data_item_2Corrected import data_item_2
from functions.data_item_functions.data_item_3Corrected import data_item_3
from functions.data_item_functions.data_item_4Corrected import data_item_4
from functions.data_item_functions.data_item_5Corrected import data_item_5
from functions.data_item_functions.data_item_6Corrected import data_item_6
from functions.data_item_functions.data_item_7 import data_item_7
from functions.data_item_functions.data_item_8Corrected import data_item_8
from functions.data_item_functions.data_item_9Corrected import data_item_9
#from functions.data_item_functions.data_item_10 import data_item_10
from functions.data_item_functions.data_item_11Corrected import data_item_11
from functions.data_item_functions.data_item_12Corrected import data_item_12
from functions.data_item_functions.data_item_13Corrected import data_item_13
from functions.data_item_functions.data_item_14Corrected import data_item_14
# from functions.data_item_functions.data_item_200 import data_item_200
# from functions.data_item_functions.data_item_170 import data_item_170
from functions.Posiciones import process_aircraft_packet



def single_test(func: callable, hexnumber: str):
    print(f"Prueba de {func.__name__} con el número hexadecimal: {hexnumber}")
    sigma = func(hexnumber)
    if sigma is None:
        print(f"falla la prueba de {func.__name__}")
    else:
        print(sigma)
    print("--------------------\n")


def run_all_tests():

    single_test(data_item_1, "A1D2")
    single_test(data_item_2, "A2D3")
    single_test(data_item_3, "210F")
    single_test(data_item_4, "01000000")
    single_test(data_item_5, "0080FF80")
    single_test(data_item_6, "600F")
    single_test(data_item_7, "0000")
    single_test(data_item_8, "ABCDEF")
    single_test(data_item_9, "3452ABC61192")
   # single_test(data_item_10, "600F")
    single_test(data_item_11, "0000")
    single_test(data_item_12, "8E23")
    single_test(data_item_13, "A512345678")
    single_test(data_item_14, "123456")
    single_test(data_item_15, "11111111")
    single_test(data_item_16, "11011213")
    single_test(data_item_17, "1111")
    single_test(data_item_19, "1111")
    single_test(data_item_21, "1111")
    single_test(data_item_22, "11111111111111")
    single_test(data_item_23, "11")
    single_test(data_item_24, "1111")
    single_test(data_item_25, "11")
    single_test(data_item_26, "1111")
    single_test(data_item_28, "0000")

if __name__ == "__main__":
    run_all_tests()
    # comment to run some individual test like:
    # single_test(data_item_1, "A1D2")

