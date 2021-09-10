# https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/
import pyasn1
e = 0x010001

n = 0x00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffffffffffffffffffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
p = pow(2,521)-1
q = pow(2,607)-1


phi = (p -1)*(q-1)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


print (modinv(e,phi))
print ("==============================================================")
print (hex(modinv(e,phi)))
print( "==============================================================")


d = modinv(e,phi)
dp = modinv(e,(p-1))
dq = modinv(e,(q-1))
qi = modinv(q,p)

import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

def pempriv(n, e, d, p, q, dP, dQ, qInv):
    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()
    for x in [0, n, e, d, p, q, dP, dQ, qInv]:
        seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodestring(der).decode('ascii'))

print(pempriv(n,e,d,p,q,dp,dq,qi))