"""
mk-rc Corr Test

Rasgele 1000 adet mk alir ve her bir bitini tek tek değiştirip round çiktilarini hesaplar.
Genel beklenti rc'deki her bit bitin 450-550 arasında değişmesidir.
Buna göre convert_2d_list fonksiyonunda 255 beyaz 0 siyah olacak şekilde piksellere renk atar.
Çikti olarak verdiği resimde sol taraf mk bitleri üst raraf rc bitleri.


"""

from PIL import Image
import utils
import Alg as cipher
import time


# takes 2d list and converts it to 1d list
# Gives values btw 0-255 for drawing the image. 255 -> white, 0 -> black
def convert_2d_list(input_list):
    def convert_value(value):
        if 0 <= value < 300:
            return 0
        elif 300 <= value < 350:
            return 50
        elif 350 <= value < 400:
            return 100
        elif 400 <= value < 450:
            return 150
        elif 450 <= value < 550:
            return 255
        elif 550 <= value < 600:
            return 210
        elif 600 <= value < 700:
            return 150
        elif 700 <= value < 800:
            return 100
        elif 800 <= value < 900:
            return 50
        elif 900 <= value <= 1000:
            return 0
        else:
            raise ValueError(f"Value {value} is out of range 0-1000.")

    return [convert_value(value) for row in input_list for value in row]

if __name__ == "__main__":

    a=time.time()
    # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
    img = Image.new( 'L', (cipher.ciphertext_size*8*cipher.num_rounds,cipher.mkey_size*8), "black") # create a new black image
    pixels = img.load() # create the pixel map

    # for each bit in mk
    for i in range(0,cipher.mkey_size*8):
    
        # Define empty list to store result
        result = [[0 for _ in range(cipher.ciphertext_size * 8)] for _ in range(cipher.num_rounds)]

        # Generate 1000 unique keys
        for k in range(1000):
        
            # Convert the counter `k` to a hexadecimal string with zero-padding
            hex_value = ''.join(f"{(k + j) % 256:02x}" for j in range(cipher.mkey_size))
            unique_key = f"0x{hex_value}"
    
            mkey = utils.str_to_int_array(unique_key)

            mkey_bits=utils.int_list_to_bit_list(mkey)

            plaintext = utils.str_to_int_array("0x00112233445566778899aabbccddeeff")

            ciphertext=cipher.return_rc(plaintext,mkey) # round ciphertexts

            ciphertext_bits = utils.convert_to_2d_bit_list(ciphertext)

            for m in range(len(ciphertext_bits)):
                for n in range(len(ciphertext_bits[0])):
                    if ciphertext_bits[m][n] == mkey_bits[i]:
                        result[m][n] += 1
        
        draw_list = convert_2d_list(result)
        
        for j in range(img.size[0]):    # For every row
               pixels[j,i] = (draw_list[j]) # set the colour accordingly
        

    img.save("corr_mk-rc.png")
    b=time.time()
    print("Time of corr mk-rc: ",(b-a)/60," minutes")

    

    