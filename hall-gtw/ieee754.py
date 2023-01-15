def convertToInt(mantissa_str):
    power_count = -1
    mantissa_int = 0
    for i in mantissa_str:
        mantissa_int += (int(i) * pow(2, power_count))
        power_count -= 1
    return (mantissa_int + 1)

def reorder(hexstr):
    newstr=''
    for i in range(len(hexstr)-1,-1,-2):
        newstr+=hexstr[i-1]+hexstr[i]
    return newstr

def ieee754toreal(x):
    x=reorder(x)
    binx=bin(int(x,16))
    numstr = '0'*(34-len(binx))+binx[2:]
    sign_bit = int(numstr[0])
    exponent_bias = int(numstr[1 : 9], 2)
    exponent_unbias = exponent_bias - 127
    mantissa_str = numstr[9:]
    mantissa_int = convertToInt(mantissa_str)
    real = pow(-1, sign_bit) * mantissa_int * pow(2, exponent_unbias)
    return real