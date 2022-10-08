#!/usr/bin/python

print("<= Format String Output to String =>")
text = input("Entrez la chaine : ")

if text[8] in ["-", ",", "|", "_", "/"]:
    sep = text[8]
else:
    sep = input("Entrez le separateur : ")

array = text.split(sep)
for i in range(len(array)):
    if len(array[i]) > 8:
        print("[Error] invalid format must be output of format string !\n with format %04x-%04x-%04x where - is a separator")
        print("like : 7b425448-5f796877-5f643164-34735f31-745f3376-665f3368-5f67346c-745f6e30-355f3368-6b633474-007d213f-73b8d500")
    elif len(array[i]) < 8:
        array[i] = "0"*(8-len(array[i])) + array[i]

output = ""

for k in array:
    for y in range(0, 7, 2):
        i = 6-y
        output += (k[i] + k[i+1])


for i in range(0, len(output)-1, 2):
    char = output[i] + output[i+1]
    print(chr(int(char, 16)), end="")
print("")
