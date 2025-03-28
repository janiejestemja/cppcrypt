#include <iostream>
#include <array>
#include <cstdint>

// Rijndaels forward s-box
const std::array<uint8_t, 256> SBox = {
  0x63 ,0x7c ,0x77 ,0x7b ,0xf2 ,0x6b ,0x6f ,0xc5 ,0x30 ,0x01 ,0x67 ,0x2b ,0xfe ,0xd7 ,0xab ,0x76
 ,0xca ,0x82 ,0xc9 ,0x7d ,0xfa ,0x59 ,0x47 ,0xf0 ,0xad ,0xd4 ,0xa2 ,0xaf ,0x9c ,0xa4 ,0x72 ,0xc0
 ,0xb7 ,0xfd ,0x93 ,0x26 ,0x36 ,0x3f ,0xf7 ,0xcc ,0x34 ,0xa5 ,0xe5 ,0xf1 ,0x71 ,0xd8 ,0x31 ,0x15
 ,0x04 ,0xc7 ,0x23 ,0xc3 ,0x18 ,0x96 ,0x05 ,0x9a ,0x07 ,0x12 ,0x80 ,0xe2 ,0xeb ,0x27 ,0xb2 ,0x75
 ,0x09 ,0x83 ,0x2c ,0x1a ,0x1b ,0x6e ,0x5a ,0xa0 ,0x52 ,0x3b ,0xd6 ,0xb3 ,0x29 ,0xe3 ,0x2f ,0x84
 ,0x53 ,0xd1 ,0x00 ,0xed ,0x20 ,0xfc ,0xb1 ,0x5b ,0x6a ,0xcb ,0xbe ,0x39 ,0x4a ,0x4c ,0x58 ,0xcf
 ,0xd0 ,0xef ,0xaa ,0xfb ,0x43 ,0x4d ,0x33 ,0x85 ,0x45 ,0xf9 ,0x02 ,0x7f ,0x50 ,0x3c ,0x9f ,0xa8
 ,0x51 ,0xa3 ,0x40 ,0x8f ,0x92 ,0x9d ,0x38 ,0xf5 ,0xbc ,0xb6 ,0xda ,0x21 ,0x10 ,0xff ,0xf3 ,0xd2
 ,0xcd ,0x0c ,0x13 ,0xec ,0x5f ,0x97 ,0x44 ,0x17 ,0xc4 ,0xa7 ,0x7e ,0x3d ,0x64 ,0x5d ,0x19 ,0x73
 ,0x60 ,0x81 ,0x4f ,0xdc ,0x22 ,0x2a ,0x90 ,0x88 ,0x46 ,0xee ,0xb8 ,0x14 ,0xde ,0x5e ,0x0b ,0xdb
 ,0xe0 ,0x32 ,0x3a ,0x0a ,0x49 ,0x06 ,0x24 ,0x5c ,0xc2 ,0xd3 ,0xac ,0x62 ,0x91 ,0x95 ,0xe4 ,0x79
 ,0xe7 ,0xc8 ,0x37 ,0x6d ,0x8d ,0xd5 ,0x4e ,0xa9 ,0x6c ,0x56 ,0xf4 ,0xea ,0x65 ,0x7a ,0xae ,0x08
 ,0xba ,0x78 ,0x25 ,0x2e ,0x1c ,0xa6 ,0xb4 ,0xc6 ,0xe8 ,0xdd ,0x74 ,0x1f ,0x4b ,0xbd ,0x8b ,0x8a
 ,0x70 ,0x3e ,0xb5 ,0x66 ,0x48 ,0x03 ,0xf6 ,0x0e ,0x61 ,0x35 ,0x57 ,0xb9 ,0x86 ,0xc1 ,0x1d ,0x9e
 ,0xe1 ,0xf8 ,0x98 ,0x11 ,0x69 ,0xd9 ,0x8e ,0x94 ,0x9b ,0x1e ,0x87 ,0xe9 ,0xce ,0x55 ,0x28 ,0xdf
 ,0x8c ,0xa1 ,0x89 ,0x0d ,0xbf ,0xe6 ,0x42 ,0x68 ,0x41 ,0x99 ,0x2d ,0x0f ,0xb0 ,0x54 ,0xbb ,0x16
};

uint8_t aes_sbox(uint8_t byte) {
        return SBox[byte];
}

// Rijndaels inverse s-box
uint8_t aes_inv_sbox(uint8_t byte) {
        static const std::array<uint8_t, 256> InvSBox = {
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
};
return InvSBox[byte]; 
}

// Shift rows 
void shiftRows(std::array<std::array<uint8_t, 4>, 4>& state) {
        std::array<uint8_t, 4> temp;

        temp = state[1];
        for (int i = 0; i < 4; i++) state[1][i] = temp[(i + 1) % 4];

        temp = state[2];
        for (int i = 0; i < 4; i++) state[2][i] = temp[(i + 2) % 4];

        temp = state[3];
        for (int i = 0; i < 4; i++) state[3][i] = temp[(i + 3) % 4];
}

// inverse shift rows
void invShiftRows(std::array<std::array<uint8_t, 4>, 4>& state) {
        std::array<uint8_t, 4> temp;

        temp = state[1];
        for (int i = 0; i < 4; i++) state[1][i] = temp[(i - 1 + 4) % 4];

        temp = state[2];
        for (int i = 0; i < 4; i++) state[2][i] = temp[(i - 2 + 4) % 4];

        temp = state[3];
        for (int i = 0; i < 4; i++) state[3][i] = temp[(i - 3 + 4) % 4];
}

void printState(const std::array<std::array<uint8_t, 4>, 4>& state) {
        for (const auto& row : state) {
                for (uint8_t byte : row) {
                        std::cout << std::hex << (int)byte << " ";
                }
                std::cout << std::endl;
        }
}

// MixColumns 
// Multiplication in Galois Field (2^8)
uint8_t gmul(uint8_t a, uint8_t b) {
        uint8_t p = 0;
        for (int i = 0; i < 8; i++) {
                if (b & 1) p ^= a; // XOR if LSB of b is 1
                bool hiBitSet = a & 0x80;
                a <<= 1;
                if (hiBitSet) a^= 0x1B;
                b >>= 1;
        }
        return p;
}

// Apply MixColumns
void mixColumns(std::array<std::array<uint8_t, 4>, 4>& state) {
        std::array<uint8_t, 4> temp;
        for (int c = 0; c < 4; c++) {
                temp[0] = gmul(2, state[0][c]) ^ gmul(3, state[1][c]) ^ state[2][c] ^ state[3][c];
                temp[1] = state[0][c] ^ gmul(2, state[1][c]) ^ gmul(3, state[2][c]) ^ state[3][c];
                temp[2] = state[0][c] ^ state[1][c] ^ gmul(2, state[2][c]) ^ gmul(3, state[3][c]);
                temp[3] = gmul(3, state[0][c]) ^ state[1][c] ^ state[2][c] ^ gmul(2, state[3][c]);

                for (int i = 0; i < 4; i++) state[i][c] = temp[i];
        }
}

// Apply inverse MixColumns
void invMixColumns(std::array<std::array<uint8_t, 4>, 4>& state) {
        std::array<uint8_t, 4> temp;
        for (int c = 0; c < 4; c++) {
                temp[0] = gmul(14, state[0][c]) ^ gmul(11, state[1][c]) ^ gmul(13, state[2][c]) ^ gmul(9, state[3][c]);
                temp[1] = gmul(9, state[0][c]) ^ gmul(14, state[1][c]) ^ gmul(11, state[2][c]) ^ gmul(13, state[3][c]);
                temp[2] = gmul(13, state[0][c]) ^ gmul(9, state[1][c]) ^ gmul(14, state[2][c]) ^ gmul(11, state[3][c]);
                temp[3] = gmul(11, state[0][c]) ^ gmul(13, state[1][c]) ^ gmul(9, state[2][c]) ^ gmul(14, state[3][c]);

                for (int i = 0; i < 4; i++) state[i][c] = temp[i];
        }
}

// Expand Key

// Round constant (Rcon)
const uint8_t Rcon[11] = {0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36};

// Shift bytes left
uint32_t rotWord(uint32_t word) {
        return (word << 8 ) | (word >> 24);
}

// Apply s-box
uint32_t subWord(uint32_t word) {
        return (aes_sbox((word >> 24) & 0xFF) << 24) | 
                (aes_sbox((word >> 16) & 0xFF) << 16) |
                (aes_sbox((word >> 8) & 0xFF) << 8) | 
                (aes_sbox(word & 0xFF));
}

// Key expansion
void keyExpansion(const std::array<uint8_t, 16>& key, std::array<uint32_t, 44>& roundKeys) {
        for (int i = 0; i < 4; i++) {
                roundKeys[i] = (key[4 * i] << 24) | (key[4 * i + 1] << 16) | (key[4 * i +2] << 8) | key[4 * i + 3];
        }
        for (int i = 4; i < 44; i++) {
                uint32_t temp = roundKeys[i - 1];

                if (i % 4 == 0) {
                        temp = subWord(rotWord(temp)) ^ (Rcon[i / 4] << 24);
                }

                roundKeys[i] = roundKeys[i - 4] ^ temp;
        }
}

// XOR each byte of state with a round key
void addRoundKey(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 4>& roundKey) {
        for (int c = 0; c < 4; c++) {
                state[0][c] ^= (roundKey[c] >> 24) & 0xFF;
                state[1][c] ^= (roundKey[c] >> 16) & 0xFF;
                state[2][c] ^= (roundKey[c] >> 8) & 0xFF;
                state[3][c] ^= roundKey[c] & 0xFF;
        }
}

// subBytes
void subBytes(std::array<std::array<uint8_t, 4>, 4>& state) {
        for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j ++) {
                        state[i][j] = aes_sbox(state[i][j]);
                }
        }
}

// inverse subBytes
void invSubBytes(std::array<std::array<uint8_t, 4>, 4>& state) {
        for (int i = 0; i < 4; i++) {
                for (int j = 0; j < 4; j++) {
                        state[i][j] = aes_inv_sbox(state[i][j]);
                }
        }
}

// AES encryption
void aesEncrypt(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 44>& roundKeys) {
        // initial round
        addRoundKey(state, {roundKeys[0], roundKeys[1], roundKeys[2], roundKeys[3]});

        // Nine rounds of SubBytes, ShiftRows, MixColumns, AddRoundKey
        for (int round = 1; round < 10; round++) {
                subBytes(state);
                shiftRows(state);
                mixColumns(state);
                addRoundKey(state, {roundKeys[round * 4], roundKeys[round * 4 + 1], roundKeys[round * 4 + 2], roundKeys[round * 4 + 3]});
        }

        // Final round (no MixColumns)
        subBytes(state);
        shiftRows(state);
        addRoundKey(state, {roundKeys[40], roundKeys[41], roundKeys[42], roundKeys[43]});
}

// AES decryption
void aesDecrypt(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 44>& roundKeys) {
        addRoundKey(state, {roundKeys[40], roundKeys[41], roundKeys[42], roundKeys[43]});

        for (int round = 9; round > 0; round--) {
                invShiftRows(state);
                invSubBytes(state);
                addRoundKey(state, {roundKeys[round * 4], roundKeys[round * 4 + 1], roundKeys[round * 4 + 2], roundKeys[round * 4 + 3]});
                invMixColumns(state);
        }
        
        // Final round (no invMixColumns
        invShiftRows(state);
        invSubBytes(state);
        addRoundKey(state, {roundKeys[0], roundKeys[1], roundKeys[2], roundKeys[3]});
}

int main() {
        uint8_t input = 0x53;
        std::cout << "S-Box[" << std::hex << (int)input << "] = " << std::hex << (int)aes_sbox(input) << std::endl;
        std::cout << "Inverse S-Box[" << std::hex << (int)aes_sbox(input) << "] = " << std::hex << (int)aes_inv_sbox(aes_sbox(input)) << std::endl;
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

        invShiftRows(state);

        std::cout << "After invShiftRows:\n";
        printState(state);

        mixColumns(state);

        std::cout << "After mixColumns:\n";
        printState(state);

        invMixColumns(state);

        std::cout << "After invMixColumns:\n";
        printState(state);

        std::array<std::array<uint8_t, 4>, 4> plaintext = {{
        {0x32, 0x88, 0x31, 0xE0},
        {0x43, 0x5A, 0x31, 0x37},
        {0xF6, 0x30, 0x98, 0x07},
        {0xA8, 0x8D, 0xA2, 0x34}
        }};

        std::array<uint8_t, 16> key = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x3e, 0x1d, 0x4c, 0x9c, 0x8a, 0xe0};

        std::array<uint32_t, 44> roundKeys;

        keyExpansion(key, roundKeys);

        std::cout << std::endl;

        printState(plaintext);

        std::cout << std::endl;

        std::array<std::array<uint8_t, 4>, 4> ciphertext = plaintext;
        aesEncrypt(ciphertext, roundKeys);
        printState(ciphertext);

        std::cout << std::endl;

        std::array<std::array<uint8_t, 4>, 4> uncipheredText = ciphertext;
        aesDecrypt(uncipheredText, roundKeys);
        printState(uncipheredText);

        std::cout << std::endl;

        // Check if decryption was successful
        if (uncipheredText == plaintext) {
                std::cout << "Decryption successful! 🎉" << std::endl;
        } else {
                std::cout << "Decryption failed! 😢" << std::endl;
        }

        return 0;
}
