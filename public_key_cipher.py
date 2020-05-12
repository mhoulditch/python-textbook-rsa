import sys, math

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
DEFAULT_BLOCK_SIZE = 128
#TODO, write a unit test for readfromfileanddecrypt and encryptandwritetofile

# helper functions
def get_blocks_from_text(message, block_size=DEFAULT_BLOCK_SIZE):
    ''' inputs: string message, outputs: a list of block integers. '''
    for character in message:
        if character not in SYMBOLS:
            print(' the symbol set does not have the character {}'.format(character))
            sys.exit()

    # calculate block integer for this block of text
    block_ints = []
    for block_start in range(0, len(message), block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(message))):
            block_int += (SYMBOLS.index(message[i])) * (len(SYMBOLS) ** (i % block_size))
        block_ints.append(block_int)
    return block_ints

def get_text_from_blocks(block_ints, message_length, block_size=DEFAULT_BLOCK_SIZE):
    ''' inputs: a list of block integers outputs: the original message string '''
    message = []
    for block_int in block_ints:
        block_message = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                char_index = block_int // (len(SYMBOLS) ** i)
                block_int = block_int % (len(SYMBOLS) ** i)
                block_message.insert(0, SYMBOLS[char_index])
        message.extend(block_message)
    return ''.join(message)

def encrypt_message(message, key, block_size):
    ''' use the get_blocks_from_text function to convert the msg string into a list of  \
        block ints, then encrypt each block integer using n and e '''
    encrypted_blocks = []
    n, e = key

    for block in get_blocks_from_text(message, block_size):
        # ciphertext = plaintext ^ e mod n
        encrypted_blocks.append(pow(block, e, n))
    return encrypted_blocks

def decrypt_message(encryptedBlocks, message_length, key, block_size=DEFAULT_BLOCK_SIZE):
    ''' decrypt a list of encrypted block ints into the original msg string. \
        we must know the length to properly decrypt the last block'''
    decrypted_blocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decrypted_blocks.append(pow(block, d, n))
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)

def read_key_file(key_filename):
    ''' inputs: string of public or private key filename \
        outputs: tuple of key as (n,e) or (n,d) '''
    with open(key_filename) as file:
        content = file.read()
    key_size, n, e_or_d = content.split(',')
    return (int(key_size), int(n), int(e_or_d))

# main functions
# i.e. encrypt_and_write_to_file('foo_encrypted.txt', 'foo_pubkey.txt', 'hello world')
def encrypt_and_write_to_file(message_filename, key_filename, message, block_size=DEFAULT_BLOCK_SIZE):
    keySize, n, e = read_key_file(key_filename)

    if keySize < block_size * 8:
        sys.exit(' blocksize is {} bits and key size is {} bits.  \
                blocksize should be = to or less than key'.format(block_size * 8, keySize))
    # encrypt the message
    encrypted_blocks = encrypt_message(message, (n, e), block_size)

    #convert the large int vals to one string val
    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(encrypted_blocks[i])
    encrypted_content = ','.join(encrypted_blocks)

    #write the encrypted string to the output file
    encrypted_content = '{}_{}_{}'.format(len(message), block_size, \
            encrypted_content)
    with open(message_filename, 'w') as file:
        file.write(encrypted_content)

    print('wrote the encrypted content to a file')
    return encrypted_content

# i.e. read_from_file_and_decrypt('foo_encrypted.txt', foo_privkey.txt')
def read_from_file_and_decrypt(message_filename, key_filename):


    # get everything we need from the key file and the encrypted message file
    keySize, n, d = read_key_file(key_filename)

    with open(message_filename) as file:
        content = file.read()

    message_length, block_size, encrypted_message = content.split('_')
    message_length = int(message_length)
    block_size = int(block_size)

    if keySize < block_size * 8:
        sys.exit(' blocksize is {} bits and key size is {} bits. \
                blocksize should be = to or less than key'.format(block_size * 8, keySize))

    # convert encrypted msg into large int vals
    encrypted_blocks = []
    for block in encrypted_message.split(','):
        encrypted_blocks.append(int(block))

    # decrypt these large int vals
    return decrypt_message(encrypted_blocks, message_length, (n, d), block_size)
