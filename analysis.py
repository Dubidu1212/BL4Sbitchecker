from enum import Enum



#Block location
block_path = "./blocks/"

class l_lev:
    Verbose  = 3
    Medium = 2
    Silent = 1

log_level = l_lev.Medium


#generates a block with a sequence of bytes
def write_block(block_nr, block_type, write_bytes):
    
    file = open(block_path + str(block_nr)+ block_type, "wb")
    try:
        for byte in write_bytes:
            file.write(byte.to_bytes(1,byteorder="big"))
        if(log_level >= l_lev.Verbose):
            print("wrote file: " + str(block_nr) + block_type + " sucessfully!")
    except BaseException as error:
        #log error
        print(error)
    finally:
        file.close()


#creates null blocks, one blocks, random blocks and alternating Blocks of size <size> in bytes
def create_blocks(nB, oB, rB, aB, size):
    for i in range(nB):
        write_block(i, "nB", [0 for i in range(size)])
    
    for i in range(oB):
        write_block(i, "oB", [255 for i in range(size)])

    #TODO: Random block

    for i in range(aB):
        #alternates 0 and 1 blocks
        write_block(i, "aB", [(255 if (i%2 == 0) else 0)  for i in range(size)])



def count_errors(byte, reference):
    on_flips = 0
    off_flips = 0
    for i in range(8):
        #if the byte is set to one but should be set to zero. increase on_flips
        if((byte & 1) and (not (reference & 1))):
            on_flips +=1
        if((not (byte & 1)) and (reference & 1)):
            off_flips += 1
        
        #shift one to the right
        byte = byte >> 1
        reference = reference >> 1
    return (on_flips, off_flips)

#Checks a specific block
def check_block(block_nr, block_type):
    
    file = open(block_path + str(block_nr)+ block_type, "rb")
    try:
        on_flips = 0
        off_flips = 0 
        bitnr = 0
        #itterates over every byte in the file
        while (byte := file.read(1)):
            #converts the byte to a workable format
            byte = int.from_bytes(byte, byteorder="big")

            #creates the difference between the should value and the actual value
            reference = 0
            if block_type == "nB":
                reference = 0 
            if block_type == "oB":
                reference = 255 
            if block_type == "aB":
                if(bitnr%2 == 0):
                    reference = 255
                else: 
                    reference = 0
            #counts the number of differences
            res = count_errors(byte,reference)
            on_flips += res[0]
            off_flips += res[1]

            bitnr += 1
        if log_level >= l_lev.Verbose:    
            print("read file: " + str(block_nr) + block_type + " sucessfully!")
        if(on_flips + off_flips == 0):
            if(log_level >= l_lev.Verbose):
                print("no errors found")
        else:
            if(log_level >= l_lev.Medium):
                print(on_flips,"bits flipped on and", off_flips, "bits flipped off in ", str(block_nr) + block_type)
    except BaseException as error:
        #log error
        print(error)
    finally:
        file.close()


if __name__ == "__main__":

    #create new blocks
    #print(create_blocks(3,3,0,3,8))

    #check blocks for integrity
    for i in range(3):
        check_block(i,"nB")
    for i in range(3):
        check_block(i,"oB")
    for i in range(3):
        check_block(i,"aB")
