#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <algorithm>

// Calculate greatest common divisor
int gcd(int a, int b) {
        while (b) {
                int temp = b;
                b = a % b;
                a = temp;
        }
        return a;
}

// Check if prime
bool is_prime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;

        for (int i = 5; i * i <= n; i += 6) {
                if (n % i == 0 || n % (i +2) == 0) {
                        return false;
                }
        }
        return true;
}

// Find prime factors
std::set<int> find_prime_factors(int n) {
        std::set<int> factors;

        // Handle divisibility by 2
        while (n % 2 == 0) {
                factors.insert(2);
                n /= 2;
        }

        // Check odd divisiors
        for (int i = 3; i * i <= n; i += 2) {
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
int power_mod(int base, int exponent, int modulus) {
        int result = 1;
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
bool is_primitive_root(int g, int p) {
        if (gcd(g, p) != 1) {
                return false;
        }

        // Find prime factors of p-1
        int phi = p - 1;
        std::set<int> prime_factors = find_prime_factors(phi);

        // Test conditions
        for (int q : prime_factors) {
                if (power_mod(g, phi / q, p) == 1) {
                        return false;
                }
        }

        return true;
}

// Find all primitive roots modulo p
std::vector<int> find_primitive_roots(int p) {
        if (!is_prime(p)) {
                std::cerr << p << " is not a prime number" << std::endl;
                return {};
        }

        std::vector<int> primitive_roots;

        for (int g = 2; g < p; ++g) {
                if (is_primitive_root(g, p)) {
                        primitive_roots.push_back(g);
                }
        }

        return primitive_roots;
}

// Verify primitve root
bool verify_primitive_root(int g, int p) {
        std::vector<int> residues;

        for (int k = 1; k < p; ++k) {
                residues.push_back(power_mod(g, k, p));
        }

        std::sort(residues.begin(), residues.end());

        for (int i = 0; i < p - 1; ++i) {
                if (residues[i] != i + 1) {
                        return false;
                }
        }

        return true;
}

int main() {
        int p = 13;

        std::vector<int> roots = find_primitive_roots(p);

        std::cout << "Primitive roots modulo " << p << ": ";
        for (int root : roots) {
                std::cout << root << " ";
        }
        std::cout << std::endl;

        // Verify first primitive root
        if (!roots.empty()) {
                int g = roots[0];
                bool verified = verify_primitive_root(g, p);

                if (verified) {
                        std::cout << "Verification: " << g << " generates all residues modulo " << p << std::endl;
                } else {
                        std::cout << "Verification failed." << std::endl;
                }
        }
        return 0;
}
