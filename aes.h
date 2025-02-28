#ifndef AES_H
#define AES_H

#include <array>
#include <cstdint>

// AES uses a 4x4 state matrix
using AESState = std::array<std::array<uint8_t, 4>, 4>;

uint8_t aes_sbox(uint8_t byte);
uint8_t aes_inv_sbox(uint8_t byte);

uint8_t gmul(uint8_t a, uint8_t b);

void shiftRows(AESState& state);
void invShiftRows(AESState& state);

void mixColumns(AESState& state);
void invMixColumns(AESState& state);

void keyExpansion(const uint8_t* key, std::array<uint32_t, 44>& roundKeys);

void addRoundKey(AESState& state, const std::array<uint32_t, 4>& roundKey);

void subBytes(AESState& state);
void invSubBytes(AESState& state);

void aesEncrypt(AESState& state, const std::array<uint32_t, 44>& roundKeys);
void aesDecrypt(AESState& state, const std::array<uint32_t, 44>& roundKeys);

#endif // AES_H
