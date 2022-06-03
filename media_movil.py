import numpy as np


def media_movil_ayudantia(media_calculada, a):
    media_calculada = np.array(media_calculada)
    array = np.array([])
    m = len(media_calculada)
    for i in range(1, m+1):
        if i <= a:
            s = -(i-1)
            top = i-1
            slice = media_calculada[i+s-1:i+top]
            Y_i = np.sum(slice/(2*i-1))
            array = np.append(array, [Y_i])
        elif a+1 <= i <= m-a:
            s = -a
            top = a
            slice = media_calculada[i+s-1:i+top]
            den = 2*a + 1
            Y_i = np.sum(slice)/den
            array = np.append(array, [Y_i])
        elif m - a < i <= m+1:
            top = i-1
            s = -(m-i)
            slice = media_calculada[i+s-1:i+top]
            Y_i = np.mean(slice)
            array = np.append(array, [Y_i])
    return array
