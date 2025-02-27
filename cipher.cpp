#include <iostream>
#include <array>
#include <cstdint>

void shiftRows(std::array<std::array<uint8_t, 4>, 4>& state) {
        std::array<uint8_t, 4> temp;

        temp = state[1];
        for (int i = i; i < 4; i++) state[1][i] = temp[(i + 1) % 4];

        temp = state[2];
        for (int i = 0; i < 4; i++) state[2][i] = temp[(i + 2) % 4];

        temp = state[3];
        for (int i = 0; i < 4; i++) state[3][i] = temp[(i +3) % 4];
}

void printState(const std::array<std::array<uint8_t, 4>, 4>& state) {
        for (const auto& row : state) {
                for (uint8_t byte : row) {
                        std::cout << std::hex << (int)byte << " ";
                }
                std::cout << std::endl;
        }
}

int main() {
        std::array<std::array<uint8_t, 4>, 4> state = {{
                {0x00, 0x01, 0x02, 0x03},
                {0x10, 0x11, 0x12, 0x13},
                {0x20, 0x21, 0x22, 0x23},
                {0x30, 0x31, 0x32, 0x33},
        }};

        std::cout << "Before shiftRows:\n";
        printState(state);

        shiftRows(state);

        std::cout << "After shiftRows:\n";
        printState(state);

        return 0;
}
