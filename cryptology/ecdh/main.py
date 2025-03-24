import elliptic_curves as ec

curve = ec.EllipticCurve(2, 3, 97)

P = ec.ECPoint(curve, 3, 6)
Q = ec.ECPoint(curve, 80, 10)

print(P + Q)
print(P.double())
print(P.multiply(5))
