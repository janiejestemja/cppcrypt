#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <algorithm>

// Calculate greatest common divisor
long int gcd(long int a,long int b) {
        while (b) {
                long int temp = b;
                b = a % b;
                a = temp;
        }
        return a;
}

// Check if prime
bool is_prime(long int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;

        for (long int i = 5; i * i <= n; i += 6) {
                if (n % i == 0 || n % (i +2) == 0) {
                        return false;
                }
        }
        return true;
}

// Find prime factors
std::set<long int> find_prime_factors(long int n) {
        std::set<long int> factors;

        // Handle divisibility by 2
        while (n % 2 == 0) {
                factors.insert(2);
                n /= 2;
        }

        // Check odd divisiors
        for (long int i = 3; i * i <= n; i += 2) {
                while (n % i == 0) {
                        factors.insert(i);
                        n /= i;
                }
        }

        // If n is prime greater than 2
        if (n > 2) {
                factors.insert(n);
        }

        return factors;
}

// Calculate (base^exponent) % modulus
long int power_mod(long int base, long int exponent, long int modulus) {
        long int result = 1;
        base = base % modulus;

        while (exponent > 0) {
                if (exponent % 2 == 1) {
                        result = (1LL * result * base) % modulus;
                }
                exponent = exponent >> 1;
                base = (1LL * base * base) % modulus;
        }

        return result;
}

// Check if g is primitive root modulo p
bool is_primitive_root(long int g, long int p) {
        if (gcd(g, p) != 1) {
                return false;
        }

        // Find prime factors of p-1
        long int phi = p - 1;
        std::set<long int> prime_factors = find_prime_factors(phi);

        // Test conditions
        for (long int q : prime_factors) {
                if (power_mod(g, phi / q, p) == 1) {
                        return false;
                }
        }

        return true;
}

// Find all primitive roots modulo p
std::vector<long int> find_primitive_roots(long int p) {
        if (!is_prime(p)) {
                std::cerr << p << " is not a prime number" << std::endl;
                return {};
        }

        std::vector<long int> primitive_roots;

        for (long int g = 2; g < p; ++g) {
                if (is_primitive_root(g, p)) {
                        primitive_roots.push_back(g);
                }
        }

        return primitive_roots;
}

// Verify primitve root
bool verify_primitive_root(long int g, long int p) {
        std::vector<long int> residues;

        for (long int k = 1; k < p; ++k) {
                residues.push_back(power_mod(g, k, p));
        }

        std::sort(residues.begin(), residues.end());

        for (long int i = 0; i < p - 1; ++i) {
                if (residues[i] != i + 1) {
                        return false;
                }
        }

        return true;
}

namespace py = pybind11;

PYBIND11_MODULE(primitive_roots, m) {
        m.doc() = "Primitive Roots Calculation Module";

        m.def("gcd", &gcd, "Calculate the greatest common divisor of two numbers", py::arg("a"), py::arg("b"));

        m.def("is_prime", &is_prime, "Check if a number is prime", py::arg("n"));

        m.def("find_prime_factors", &find_prime_factors, "Find prime factors of a number", py::arg("n"));

        m.def("power_mod", &power_mod, "Calculate (base^exponent) % modulus", py::arg("base"), py::arg("exponent"), py::arg("modulus"));

        // Main primitive root functions
        m.def("is_primitive_root", &is_primitive_root, "Check if g is a primitive root modulo p", py::arg("g"), py::arg("p"));

        m.def("find_primitive_roots", &find_primitive_roots, "Find all primitive roots modulo p", py::arg("p"));

        m.def("verify_primitive_root", &verify_primitive_root, "Verify a primitive root by generating all residues", py::arg("g"), py::arg("p"));

}
