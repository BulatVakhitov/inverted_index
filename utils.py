""" Some useful functions """

def encode_delta_single(N):
    """ Source link: https://en.wikipedia.org/wiki/Elias_delta_coding """
    L = bin(N)[2:] # 10 -> 0b1010, that's why I delete first 2 symbols
    L_bin = bin(len(L))[2:]
    M = len(L_bin)

    result = '0' * (M - 1) + '1'
    result += L_bin[1:]
    result += L[1:]
    return result

def decode_delta_single(encoded):
    if len(encoded) == 1: # TODO: fix this hardcode
        return 1
    M = 0
    for symbol in encoded:
        if symbol == '0':
            M += 1
        else:
            break

    result = 2 ** (len(encoded) - 2 * M - 1) + int(encoded[2*M + 1:], 2)
    return result

def encode_gamma_single(N):
    """ Source link: https://en.wikipedia.org/wiki/Elias_gamma_coding """
    N_bin = bin(N)[2:]
    result = '0' * (len(N_bin) - 1) + N_bin
    return result

def decode_gamma_single(encoded):
    M = 0
    for symbol in encoded:
        if symbol == '0':
            M += 1
        else:
            break
    return int(encoded[M:], 2)