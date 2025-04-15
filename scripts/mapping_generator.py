#! /usr/bim/env python3

#turn a list of numbers into a list of functions

#[1,2,4,5] -> [None,_1,_2,None,_4,_5]

inputs = [5,6,7,8,9,10,11,12,
 16,23,24,25,26,27,28,29,30,31,
 32,33,34,37,
 48,
 64,65,
 66,67,68,69,72]

results = [None]*256
for i in inputs:
    results[i] = f"_{i}"

# print like 16x16

print ("[")
for i in range(0,256,16):
    print("  ", end="")
    for j in range(16):
        if results[i+j] is None:
            print("None,", end="")
        else:
            print(f"{results[i+j]},", end="")
    print()
print("]")

