#include <Python.h>
#include <array>
#include <vector>
#include "aes.h"

// Conversion of Python bytes to a C++ AES state array
std::array<std::array<uint8_t, 4>, 4> bytesToState(PyObject* pyBytes) {
        std::array<std::array<uint8_t, 4>, 4> state{};
        const char* data = PyBytes_AsString(pyBytes);

        for (int i = 0; i < 16; i ++) {
                state[i / 4][i % 4] = static_cast<uint8_t>(data[i]);
        }

        return state;
}

// Conversion of AES state array to Python bytes
PyObject* stateToBytes(const std::array<std::array<uint8_t, 4>, 4>& state) {
        char output[16];

        for (int i = 0; i < 16; i++) {
                output[i] = static_cast<char>(state[i / 4][i % 4]);
        }

        return PyBytes_FromStringAndSize(output, 16);
}

// Wrapping aesEncrypt
static PyObject* py_aes_encrypt(PyObject* self, PyObject* args) {
        PyObject* pyPlaintext;
        PyObject* pyKey;

        if (!PyArg_ParseTuple(args, "Y#Y#", &pyPlaintext, &pyKey)) {
                return nullptr;
        }

        std::array<std::array<uint8_t, 4>, 4> state = bytesToState(pyPlaintext);
        std::array<uint32_t, 44> roundKeys;

        keyExpansion(reinterpret_cast<uint8_t*>(PyBytes_AsString(pyKey)), roundKeys);

        aesEncrypt(state, roundKeys);

        return stateToBytes(state);
}

// Wrapping aesDecrypt
static PyObject* py_aes_decrypt(PyObject* self, PyObject* args) {
        PyObject* pyCiphertext;
        PyObject* pyKey;

        if (!PyArg_ParseTuple(args, "Y#Y#", &pyCiphertext, &pyKey)) {
                return nullptr;
        }

        std::array<std::array<uint8_t, 4>, 4> state = bytesToState(pyCiphertext);
        std::array<uint32_t, 44> roundKeys;

        keyExpansion(reinterpret_cast<uint8_t*>(PyBytes_AsString(pyKey)), roundKeys);

        aesDecrypt(state, roundKeys);
        return stateToBytes(state);
}

// Define module methods
static PyMethodDef AESMethods[] = {
        {"encrypt", py_aes_encrypt, METH_VARARGS, "Encrypt 16 bytes with AES."},
        {"decrypt", py_aes_decrypt, METH_VARARGS, "Decrypt 16 bytes with AES."},
        {nullptr, nullptr, 0, nullptr} // Sentinel
};

// Define module
static struct PyModuleDef aesModule = {
        PyModuleDef_HEAD_INIT, "aes", nullptr, -1, AESMethods
};

// Initialize module
PyMODINIT_FUNC PyInit_aes(void) {
        return PyModule_Create(&aesModule);
}
