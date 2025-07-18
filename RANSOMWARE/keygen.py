def generate_key_iv():
    key = bytes.fromhex("00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff")
    iv  = bytes.fromhex("0102030405060708090a0b0c0d0e0f10")
    return key, iv