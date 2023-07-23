with open("./source/log.bin", "rb") as f_bin:
    byte_data = f_bin.read()  # .bin 파일을 바이트 데이터로 읽어옴

# 각 바이트 값을 16진수 문자열로 변환하고 앞에 '0x'를 추가합니다.
hex_list = [hex(byte) for byte in byte_data]

# '0x' 부분을 제거하고 문자열을 리스트에 저장합니다.
result_list = [hex_value[2:].zfill(2) for hex_value in hex_list]

print(len(result_list))
print(result_list)
