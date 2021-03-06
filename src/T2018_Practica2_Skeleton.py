#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

MODE_CIPHER = 0
MODE_DECIPHER = 1

# --- IMPLEMENTATION GOES HERE ---------------------------------------------
#  Student helpers (functions, constants, etc.) can be defined here, if needed
import binascii

def stringToBinary(str):
    result = ''
    for ch in str:
        result = "{}{}".format(result, bin(ord(ch))[2:].zfill(8))
    return result


# --------------------------------------------------------------------------


def uoc_lfsr_sequence(polynomial, initial_state, output_bits):
    """
    Returns the output sequence of output_bits bits of an LFSR with a given initial state and connection polynomial.

    :param polynomial: list of integers, with the coefficients of the connection polynomial that define the LFSR.
    :param initial_state: list of integers with the initial state of the LFSR
    :param output_bits: integer, number of bits of the output sequence
    :return: a list of output_bits bits
    """
    result = None

    # --- IMPLEMENTATION GOES HERE ---
    result = []
    l = len(polynomial)

    for i in range(output_bits):
        start = initial_state[0]
        # go around the polynomial
        for j in range(l):
            # do the xor operation if it is not the first position and there is a xor door
            if(polynomial[j] == 1 and j != 0):
                start = start ^ initial_state[j]
        # append the first element of inital_state to the result
        result.append(initial_state[0])
        #rotate the initial_state list and pushing in the new value
        for z in range(l-1):
            initial_state[z] = initial_state[z+1]
        initial_state[len(initial_state)-1] = start

    # --------------------------------

    return result

def uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, clocking_bits, output_bits):
    """
    Implements extended A5's pseudorandom generator.
    :param params_pol_0: two-element list describing the first LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param params_pol_1: two-element list describing the second LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param params_pol_2: two-element list describing the third LFSR: the first element contains a list with the
    coefficients of the connection polynomial, the second element contains a list with the initial state of the LFSR.
    :param clocking_bits: three-element list, with the clocking bits of each LFSR
    :param output_bits: integer, number of bits of the output sequence
    :return: list of output_bits elements with the pseudo random sequence
    """

    sequence = []

    # --- IMPLEMENTATION GOES HERE ---

    l0 = len(params_pol_0[0])
    l1 = len(params_pol_1[0])
    l2 = len(params_pol_2[0])

    if clocking_bits[0] > l0 or clocking_bits[1] > l1 or clocking_bits[2] > l2:
        raise ValueError("Clocking bits are not correct")

    for i in range(output_bits):
        start0 = params_pol_0[1][0]
        start1 = params_pol_1[1][0]
        start2 = params_pol_2[1][0]
        # go around the polynomial
        for j in range(l0):
            # do the xor operation if it is not the first position and there is a xor door
            if(params_pol_0[0][j] == 1 and j != 0):
                start0 = start0 ^ params_pol_0[1][j]

        for j in range(l1):
            # do the xor operation if it is not the first position and there is a xor door
            if(params_pol_1[0][j] == 1 and j != 0):
                start1 = start1 ^ params_pol_1[1][j]

        for j in range(l2):
            # do the xor operation if it is not the first position and there is a xor door
            if(params_pol_2[0][j] == 1 and j != 0):
                start2 = start2 ^ params_pol_2[1][j]

        sequence.append((params_pol_0[1][0] ^ params_pol_1[1][0]) ^ params_pol_2[1][0])

        n1 = 0
        if (params_pol_0[1][l0-clocking_bits[0]-1] == 1):
            n1 += 1
        if (params_pol_1[1][l1-clocking_bits[1]-1] == 1):
            n1 += 1
        if (params_pol_2[1][l2-clocking_bits[2]-1] == 1):
            n1 += 1
        winner = int(n1 > 1)

        if(params_pol_0[1][l0-clocking_bits[0]-1] == winner):
            for z in range(l0-1):
                params_pol_0[1][z] = params_pol_0[1][z+1]
            params_pol_0[1][len(params_pol_0[1])-1] = start0

        if (params_pol_1[1][l1 - clocking_bits[1]-1] == winner):
            for z in range(l1-1):
                params_pol_1[1][z] = params_pol_1[1][z+1]
            params_pol_1[1][len(params_pol_1[1])-1] = start1

        if (params_pol_2[1][l2 - clocking_bits[2]-1] == winner):
            for z in range(l2-1):
                params_pol_2[1][z] = params_pol_2[1][z+1]
            params_pol_2[1][len(params_pol_2[1])-1] = start2


    # --------------------------------

    return sequence


def uoc_a5_cipher(initial_state_0, initial_state_1, initial_state_2, message, mode):
    """
    Implements ciphering/deciphering with the A5 pseudo random generator.

    :param initial_state_0: list, initial state of the first LFSR
    :param initial_state_1: list, initial state of the second LFSR
    :param initial_state_2: list, initial state of the third LFSR
    :param message: string, plaintext to cipher (mode=MODE_CIPHER) or ciphertext to decipher (mode=MODE_DECIPHER)
    :param mode: MODE_CIPHER or MODE_DECIPHER, whether to cipher or decipher
    :return: string, ciphertext (mode=MODE_CIPHER) or plaintext (mode=MODE_DECIPHER)
    """

    output = ""

    # --- IMPLEMENTATION GOES HERE ---

    params_pol_0 = [[1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], initial_state_0]
    params_pol_1 = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], initial_state_1]
    params_pol_2 = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], initial_state_2]

    if mode == MODE_CIPHER:

        binary = stringToBinary(message)
        l = len(binary)

        sequence = uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, [8, 10, 10], l)

        for i in range(len(binary)):
            output = "{}{}".format(output, (int(binary[i]) ^ sequence[i]))

    if mode == MODE_DECIPHER:
        l = len(message)

        sequence = uoc_ext_a5_pseudo_random_gen(params_pol_0, params_pol_1, params_pol_2, [8, 10, 10], l)
        for i in range(len(message)):
            output = "{}{}".format(output, (int(message[i]) ^ sequence[i]))

        output = binascii.unhexlify('%x' % int(output,2)).decode("utf-8")

    # --------------------------------
    return output


def uoc_aes(message, key):
    """
    Implements 1 block AES enciphering using a 256-bit key.

    :param message: string of 1 and 0s with the binary representation of the messsage, 128 char. long
    :param key: string of 1 and 0s with the binary representation of the key, 256 char. long
    :return: string of 1 and 0s with the binary representation of the ciphered message, 128 char. long
    """

    cipher_text = ""

    # --- IMPLEMENTATION GOES HERE ---


    # --------------------------------

    return cipher_text


def uoc_g(message):
    """
    Implements the g function.

    :param message: string of 1 and 0s with the binary representation of the messsage, 128 char. long
    :return: string of 1 and 0s, 256 char. long
    """

    output = ""

    # --- IMPLEMENTATION GOES HERE ---


    # --------------------------------

    return output


def uoc_naive_padding(message, block_len):
    """
    Implements a naive padding scheme. As many 0 are appended at the end of the message
    until the desired block length is reached.

    :param message: string with the message
    :param block_len: integer, block length
    :return: string of 1 and 0s with the padded message
    """

    output = ""

    # --- IMPLEMENTATION GOES HERE ---



    # --------------------------------

    return output


def uoc_mmo_hash(message):
    """
    Implements the hash function.

    :param message: a char. string with the message
    :return: string of 1 and 0s with the hash of the message
    """

    h_i = ""

    # --- IMPLEMENTATION GOES HERE ---




    # --------------------------------

    return h_i


def uoc_collision(prefix):
    """
    Generates collisions for uoc_mmo_hash, with messages having a given prefix.

    :param prefix: string, prefix for the messages
    :return: 2-element tuple, with the two strings that start with prefix and have the same hash.
    """

    collision = ("", "")

    # --- IMPLEMENTATION GOES HERE ---



    # --------------------------------

    return collision
