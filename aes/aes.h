#ifndef AES_H
#define AES_H

#include <array>
#include <cstdint>

uint8_t aes_sbox(uint8_t byte);
uint8_t aes_inv_sbox(uint8_t byte);

uint8_t gmul(uint8_t a, uint8_t b);

void shiftRows(std::array<std::array<uint8_t, 4>, 4>& state);
void invShiftRows(std::array<std::array<uint8_t, 4>, 4>& state);

void mixColumns(std::array<std::array<uint8_t, 4>, 4>& state);
void invMixColumns(std::array<std::array<uint8_t, 4>, 4>& state);

void keyExpansion(const std::array<uint8_t, 16>& key, std::array<uint32_t, 44>& roundKeys);

void addRoundKey(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 4>& roundKey);

void subBytes(std::array<std::array<uint8_t, 4>, 4>& state);
void invSubBytes(std::array<std::array<uint8_t, 4>, 4>& state);

void aesEncrypt(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 44>& roundKeys);
void aesDecrypt(std::array<std::array<uint8_t, 4>, 4>& state, const std::array<uint32_t, 44>& roundKeys);

#endif // AES_H
