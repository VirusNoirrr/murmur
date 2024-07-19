# ngl u need to star this repo for this
def x64Add(t, r):
    t = [(t[0] >> 16) & 0xffff, t[0] & 0xffff, (t[1] >> 16) & 0xffff, t[1] & 0xffff]
    r = [(r[0] >> 16) & 0xffff, r[0] & 0xffff, (r[1] >> 16) & 0xffff, r[1] & 0xffff]
    e = [0, 0, 0, 0]
    e[3] += t[3] + r[3]
    e[2] += (e[3] >> 16) & 0xffff
    e[3] &= 0xffff
    e[2] += t[2] + r[2]
    e[1] += (e[2] >> 16) & 0xffff
    e[2] &= 0xffff
    e[1] += t[1] + r[1]
    e[0] += (e[1] >> 16) & 0xffff
    e[1] &= 0xffff
    e[0] += t[0] + r[0]
    e[0] &= 0xffff
    return [(e[0] << 16) | e[1], (e[2] << 16) | e[3]]
def x64Multiply(t, r):
    t = [(t[0] >> 16) & 0xffff, t[0] & 0xffff, (t[1] >> 16) & 0xffff, t[1] & 0xffff]
    r = [(r[0] >> 16) & 0xffff, r[0] & 0xffff, (r[1] >> 16) & 0xffff, r[1] & 0xffff]
    e = [0, 0, 0, 0]
    e[3] += t[3] * r[3]
    e[2] += (e[3] >> 16) & 0xffff
    e[3] &= 0xffff
    e[2] += t[2] * r[3]
    e[1] += (e[2] >> 16) & 0xffff
    e[2] &= 0xffff
    e[2] += t[3] * r[2]
    e[1] += (e[2] >> 16) & 0xffff
    e[2] &= 0xffff
    e[1] += t[1] * r[3]
    e[0] += (e[1] >> 16) & 0xffff
    e[1] &= 0xffff
    e[1] += t[2] * r[2]
    e[0] += (e[1] >> 16) & 0xffff
    e[1] &= 0xffff
    e[1] += t[3] * r[1]
    e[0] += (e[1] >> 16) & 0xffff
    e[1] &= 0xffff
    e[0] += t[0] * r[3] + t[1] * r[2] + t[2] * r[1] + t[3] * r[0]
    e[0] &= 0xffff
    return [(e[0] << 16) | e[1], (e[2] << 16) | e[3]]
def x64Rotl(t, r):
    r %= 64
    
    if r == 32:
        return [t[1], t[0]]
    elif r < 32:
        return [
            ((t[0] << r) & 0xffffffffffffffff) | ((t[1] >> (32 - r)) & 0xffffffffffffffff),
            ((t[1] << r) & 0xffffffffffffffff) | ((t[0] >> (32 - r)) & 0xffffffffffffffff)
        ]
    else:
        r -= 32
        return [
            ((t[1] << r) & 0xffffffffffffffff) | ((t[0] >> (32 - r)) & 0xffffffffffffffff),
            ((t[0] << r) & 0xffffffffffffffff) | ((t[1] >> (32 - r)) & 0xffffffffffffffff)
        ]
def x64LeftShift(t, r):
    r %= 64
    
    if r == 0:
        return t
    elif r < 32:
        return [
            ((t[0] << r) & 0xffffffffffffffff) | ((t[1] >> (32 - r)) & 0xffffffffffffffff),
            (t[1] << r) & 0xffffffffffffffff
        ]
    else:
        return [
            (t[1] << (r - 32)) & 0xffffffffffffffff,
            0
        ]
def x64Xor(t, r):
    return [t[0] ^ r[0], t[1] ^ r[1]]
def x64Fmix(t):
    t = x64Xor(t, [0, t[0] >> 1])
    t = x64Multiply(t, [4283543511, 3981806797])
    t = x64Xor(t, [0, t[0] >> 1])
    t = x64Multiply(t, [3301882366, 444984403])
    t = x64Xor(t, [0, t[0] >> 1])
    return t
def x64hash128(t, r=0):
    r = r or 0
    e = len(t) % 16
    o = len(t) - e
    x = [0, r]
    c = [0, r]
    h = [0, 0]
    a = [0, 0]
    d = [2277735313, 289559509]
    i = [1291169091, 658871167]

    for l in range(0, o, 16):
        h = [
            (ord(t[l + 4]) & 0xFF) | ((ord(t[l + 5]) & 0xFF) << 8) | ((ord(t[l + 6]) & 0xFF) << 16) | ((ord(t[l + 7]) & 0xFF) << 24),
            (ord(t[l]) & 0xFF) | ((ord(t[l + 1]) & 0xFF) << 8) | ((ord(t[l + 2]) & 0xFF) << 16) | ((ord(t[l + 3]) & 0xFF) << 24)
        ]
        a = [
            (ord(t[l + 12]) & 0xFF) | ((ord(t[l + 13]) & 0xFF) << 8) | ((ord(t[l + 14]) & 0xFF) << 16) | ((ord(t[l + 15]) & 0xFF) << 24),
            (ord(t[l + 8]) & 0xFF) | ((ord(t[l + 9]) & 0xFF) << 8) | ((ord(t[l + 10]) & 0xFF) << 16) | ((ord(t[l + 11]) & 0xFF) << 24)
        ]
        h = x64Multiply(h, d)
        h = x64Rotl(h, 31)
        h = x64Multiply(h, i)
        x = x64Xor(x, h)
        x = x64Rotl(x, 27)
        x = x64Add(x, c)
        x = x64Add(x64Multiply(x, [0, 5]), [0, 1390208809])
        a = x64Multiply(a, i)
        a = x64Rotl(a, 33)
        a = x64Multiply(a, d)
        c = x64Xor(c, a)
        c = x64Rotl(c, 31)
        c = x64Add(c, x)
        c = x64Add(x64Multiply(c, [0, 5]), [0, 944331445])

    h = [0, 0]
    a = [0, 0]
    if e:
        if e >= 15:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 14])], 48))
        if e >= 14:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 13])], 40))
        if e >= 13:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 12])], 32))
        if e >= 12:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 11])], 24))
        if e >= 11:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 10])], 16))
        if e >= 10:
            a = x64Xor(a, x64LeftShift([0, ord(t[o + 9])], 8))
        if e >= 9:
            a = x64Xor(a, [0, ord(t[o + 8])])
            a = x64Multiply(a, i)
            a = x64Rotl(a, 33)
            a = x64Multiply(a, d)
            c = x64Xor(c, a)
        if e >= 8:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 7])], 56))
        if e >= 7:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 6])], 48))
        if e >= 6:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 5])], 40))
        if e >= 5:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 4])], 32))
        if e >= 4:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 3])], 24))
        if e >= 3:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 2])], 16))
        if e >= 2:
            h = x64Xor(h, x64LeftShift([0, ord(t[o + 1])], 8))
        if e >= 1:
            h = x64Xor(h, [0, ord(t[o])])
            h = x64Multiply(h, d)
            h = x64Rotl(h, 31)
            h = x64Multiply(h, i)
            x = x64Xor(x, h)

    x = x64Xor(x, [0, len(t)])
    c = x64Xor(c, [0, len(t)])
    x = x64Add(x, c)
    c = x64Add(c, x)
    x = x64Fmix(x)
    c = x64Fmix(c)
    x = x64Add(x, c)
    c = x64Add(c, x)
    return (("00000000" + format(x[0] & 0xFFFFFFFF, "x"))[-8:] + ("00000000" + format(x[1] & 0xFFFFFFFF, "x"))[-8:] + ("00000000" + format(c[0] & 0xFFFFFFFF, "x"))[-8:] + ("00000000" + format(c[1] & 0xFFFFFFFF, "x"))[-8:])
