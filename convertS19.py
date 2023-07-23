import bincopy

f = bincopy.BinFile("./source/log.bin")

img = f.as_ti_txt()
print(img.split()[1:-1])
