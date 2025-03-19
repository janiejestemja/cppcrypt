#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gmp.h>
#include <string>
#include <stdexcept>
#include <vector>

namespace py = pybind11;

// Wrapper class for GMP's mpz_t type
class BigInteger {
private:
    mpz_t value;
public:
    // Constructors
    BigInteger() {
        mpz_init(value);
    }
    // Constructor from string
    BigInteger(const std::string& str, int base = 10) {
        mpz_init(value);
        if (mpz_set_str(value, str.c_str(), base) != 0) {
            mpz_clear(value);
            throw std::invalid_argument("Invalid number format");
        }
    }

    // Copy constructor
    BigInteger(const BigInteger& other) {
        mpz_init(value);
        mpz_set(value, other.value);
    }

    // Constructor from unsigned long
    BigInteger(unsigned long num) {
        mpz_init_set_ui(value, num);
    }

    // Destructor
    ~BigInteger() {
        mpz_clear(value);
    }

    // Assignment operator
    BigInteger& operator=(const BigInteger& other) {
        if (this != &other) {
            mpz_set(value, other.value);
        }
        return *this;
    }

    // Addition
    BigInteger operator+(const BigInteger& other) const {
        BigInteger result;
        mpz_add(result.value, value, other.value);
        return result;
    }

    // Subtraction
    BigInteger operator-(const BigInteger& other) const {
        BigInteger result;
        mpz_sub(result.value, value, other.value);
        return result;
    }

    // Multiplication
    BigInteger operator*(const BigInteger& other) const {
        BigInteger result;
        mpz_mul(result.value, value, other.value);
        return result;
    }

    // Integer Division
    BigInteger operator/(const BigInteger& other) const {
        if (mpz_sgn(other.value) == 0) {
            throw std::invalid_argument("Division by zero");
        }
        BigInteger result;
        mpz_tdiv_q(result.value, value, other.value);
        return result;
    }

    // Modulo
    BigInteger operator%(const BigInteger& other) const {
        if (mpz_sgn(other.value) == 0) {
            throw std::invalid_argument("Modulo by zero");
        }
        BigInteger result;
        mpz_tdiv_r(result.value, value, other.value);
        return result;
    }

    // AND
    BigInteger operator&(const BigInteger& other) const {
        BigInteger result;
        mpz_and(result.value, value, other.value);
        return result;
    }

    // OR
    BigInteger operator|(const BigInteger& other) const {
        BigInteger result;
        mpz_ior(result.value, value, other.value);
        return result;
    }

    // XOR
    BigInteger operator^(const BigInteger& other) const {
        BigInteger result;
        mpz_xor(result.value, value, other.value);
        return result;
    }

    // Left shift
    BigInteger operator<<(unsigned long bits) const {
        BigInteger result;
        mpz_mul_2exp(result.value, value, bits);
        return result;
    }

    // Right shift
    BigInteger operator>>(unsigned long bits) const {
        BigInteger result;
        mpz_tdiv_q_2exp(result.value, value, bits);
        return result;
    }

    // Comparison operators
    bool operator==(const BigInteger& other) const {
        return mpz_cmp(value, other.value) == 0;
    }
    bool operator!=(const BigInteger& other) const {
        return mpz_cmp(value, other.value) != 0;
    }
    bool operator<(const BigInteger& other) const {
        return mpz_cmp(value, other.value) < 0;
    }
    bool operator<=(const BigInteger& other) const {
        return mpz_cmp(value, other.value) <= 0;
    }
    bool operator>(const BigInteger& other) const {
        return mpz_cmp(value, other.value) > 0;
    }
    bool operator>=(const BigInteger& other) const {
        return mpz_cmp(value, other.value) >= 0;
    }

    // Conversion to string
    std::string toString(int base = 10) const {
        char* str = mpz_get_str(nullptr, base, value);
        std::string result(str);
        free(str);
        return result;
    }

    // Get bits as vector
    std::vector<bool> getBits() const {
        std::vector<bool> bits;
        size_t numBits = mpz_sizeinbase(value, 2);
        bits.reserve(numBits);

        for (size_t i = 0; i < numBits; i++) {
            bits.push_back(mpz_tstbit(value, i) == 1);
        }

        return bits;
    }

    // Set from bytes
    void setFromBytes(const std::vector<unsigned char>& bytes) {
        mpz_import(value, bytes.size(), 1, sizeof(unsigned char), 0, 0, bytes.data());
    }

    // Get bytes 
    std::vector<unsigned char> getBytes() const {
        size_t count;
        std::vector<unsigned char> bytes(mpz_sizeinbase(value, 256) + 1);
        mpz_export(bytes.data(), &count, 1, sizeof(unsigned char), 0, 0, value);
        bytes.resize(count);
        return bytes;
    }

    // Modular exponentation (a^b mod m)
    static BigInteger powMod(const BigInteger& base, const BigInteger& exp, const BigInteger& mod) {
        BigInteger result;
        mpz_powm(result.value, base.value, exp.value, mod.value);
        return result;
    }

    // Generate random big integer in range [0, n-1]
    static BigInteger random(const BigInteger& n) {
        BigInteger result;
        gmp_randstate_t state;
        gmp_randinit_default(state);
        gmp_randseed_ui(state, time(NULL));
        mpz_urandomm(result.value, state, n.value);
        gmp_randclear(state);
        return result;
    }
};

PYBIND11_MODULE(bigint, m) {
    m.doc() = "Big integer module using GMP";

    py::class_<BigInteger>(m, "BigInteger")
        .def(py::init<>())
        .def(py::init<const std::string&, int>(), py::arg("str"), py::arg("base") = 10)
        .def(py::init<unsigned long>())

        .def("__str__", &BigInteger::toString)
        .def("__repr__", [](const BigInteger& self) {
            return "BigInteger(\"" + self.toString() + "\")";
        })
        .def("__add__", &BigInteger::operator+)
        .def("__sub__", &BigInteger::operator-)
        .def("__mul__", &BigInteger::operator*)
        .def("__truediv__", &BigInteger::operator/)
        .def("__mod__", &BigInteger::operator%)
        .def("__and__", &BigInteger::operator&)
        .def("__or__", &BigInteger::operator|)
        .def("__xor__", &BigInteger::operator^)
        .def("__lshift__", &BigInteger::operator<<)
        .def("__rshift__", &BigInteger::operator>>)
        .def("__eq__", &BigInteger::operator==)
        .def("__ne__", &BigInteger::operator!=)
        .def("__lt__", &BigInteger::operator<)
        .def("__le__", &BigInteger::operator<=)
        .def("__gt__", &BigInteger::operator>)
        .def("__ge__", &BigInteger::operator>=)
        .def("to_string", &BigInteger::toString, py::arg("base") = 10)
        .def("set_from_bytes", &BigInteger::setFromBytes)
        .def("get_bytes", &BigInteger::getBytes)
        .def_static("pow_mod", &BigInteger::powMod)
        .def_static("random", &BigInteger::random);
}
