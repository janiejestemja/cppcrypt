import bigint

def basic_operations():
    a = bigint.BigInteger("98765432109876543210987654321098765432109876543210")
    b = bigint.BigInteger("12345678901234567890123456789012345678901234567890")

    print("Arithmetic...")

    print("a")
    print(a.to_string())
    print("b")
    print(b.to_string())
    print("a + b")
    print((a + b).to_string())
    print("a - b")
    print((a - b).to_string())

    print("a * b")
    print((a * b).to_string())
    print("a / b")
    print((a / b).to_string())
    print("a % b")
    print((a % b).to_string())

    print("a & b")
    print((a & b).to_string())
    print("a | b")
    print((a | b).to_string())
    print("a ^ b")
    print((a ^ b).to_string())

    print("a << 10")
    print((a << 10).to_string())
    print("a >> 10")
    print((a >> 10).to_string())

    print("a == b")
    print(a == b)
    print("a != b")
    print(a != b)
    print("a < b")
    print(a < b)
    print("a <= b")
    print(a <= b)
    print("a > b")
    print(a > b)
    print("a >= b")
    print(a >= b)

    p = bigint.BigInteger("1234567890123456789012345678901234567890123456789013")
    q = bigint.BigInteger("9876543210987654321098765432109876543210987654321097")


if __name__ == "__main__":
    basic_operations()
