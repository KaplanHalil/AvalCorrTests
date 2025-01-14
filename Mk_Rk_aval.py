import utils
import AES_256 as cipher

mkey_size= 32 #bytes
round_key_size = 16 #bytes
round_key = 15 # number of subkeys

result = [[0]*(round_key_size*8)]*round_key

if __name__ == "__main__":

    mkey = utils.str_to_int_array("0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")

    mkey_bits=utils.int_list_to_bit_list(mkey)

    rkeys=cipher.key_expansion(mkey)

    rkeys_bits = utils.convert_to_2d_bit_list(rkeys)



    # for each bit in mk
    for i in range(0,mkey_size*8):

        mkey_bits=utils.int_list_to_bit_list(mkey)

        # change value of bit
        mkey_bits[i] = mkey_bits[i]^1
        # Compute new mk and rk
        new_mkey = utils.bit_list_to_int_list(mkey_bits)
        new_rkeys=cipher.key_expansion(new_mkey)
        new_rkeys_bits = utils.convert_to_2d_bit_list(new_rkeys)
        # xor new and old rk to find different bits
        fark=utils.xor_2d_lists(rkeys_bits,new_rkeys_bits)
        # accumilate different bits
        result=utils.sum_2d_lists(result,fark)


    print(result)

    