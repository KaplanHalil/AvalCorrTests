import utils

# AES S-Box
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# AES Rcon values
RCON = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 
    0x6C, 0xD8, 0xAB, 0x4D
]

# Substitute bytes using the AES S-box
def sub_bytes(state):
    return [SBOX[byte] for byte in state]

# Rotate rows in the state matrix
def shift_rows(state):
    return [
        state[0], state[5], state[10], state[15],
        state[4], state[9], state[14], state[3],
        state[8], state[13], state[2], state[7],
        state[12], state[1], state[6], state[11]
    ]

# MixColumns operation 
def mix_columns(state): 
    new_state = [0] * 16 
    for i in range(4): # Process each column 
        col = state[i*4:(i+1)*4] # Extract the column 
        new_state[i*4 + 0] = utils.gmul(col[0], 2) ^ utils.gmul(col[1], 3) ^ col[2] ^ col[3] 
        new_state[i*4 + 1] = col[0] ^ utils.gmul(col[1], 2) ^ utils.gmul(col[2], 3) ^ col[3] 
        new_state[i*4 + 2] = col[0] ^ col[1] ^ utils.gmul(col[2], 2) ^ utils.gmul(col[3], 3) 
        new_state[i*4 + 3] = utils.gmul(col[0], 3) ^ col[1] ^ col[2] ^ utils.gmul(col[3], 2) 
    return new_state

# Add round key operation
def add_round_key(state, round_key):
    return [state[i] ^ round_key[i] for i in range(len(state))]

# AES-256 Key Expansion
def key_expansion(key):
    # The AES-256 key size is 32 bytes (256 bits), and we need 60 32-bit words (15 rounds, plus the initial key)
    expanded_keys = list(key)
    
    # AES-256 has 14 rounds, so we need a total of 60 words (4 words per round + the initial key)
    for i in range(8, 60):
        temp = expanded_keys[-4:]
        if i % 8 == 0:
            temp = temp[1:] + temp[:1]  # Rotate word
            temp = [SBOX[b] for b in temp]  # Apply S-box
            temp[0] ^= RCON[(i // 8) - 1]  # XOR with the round constant
        elif i % 8 == 4:
            temp = [SBOX[b] for b in temp]  # Apply S-box to the word

        expanded_keys.extend([expanded_keys[-32 + j] ^ temp[j] for j in range(4)])
    
    return [expanded_keys[i:i + 16] for i in range(0, len(expanded_keys), 16)]


# AES encryption
def encrypt(block, key):
    round_keys = key_expansion(key)
    state = add_round_key(block, round_keys[0])

    for round in range(1, 14):
        
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round])
            
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[14])

    return state

# AES decryption

if __name__ == "__main__":

    # AES-256 Test vectors
    plaintext = utils.str_to_int_array("0x00112233445566778899aabbccddeeff")
    key = utils.str_to_int_array("0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    
    print("plaintext:",utils.int_to_hex(plaintext))
    print("key:",utils.int_to_hex(key))

    ciphertext = encrypt(plaintext, key)
    
    print("Ciphertext:", utils.int_to_hex(ciphertext))

    print(key_expansion(key))
