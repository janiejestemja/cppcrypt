#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <array>
#include <cstdint>

namespace py = pybind11;

#include "aes.h"


// Convert Python bytes/bytearray/list to std::array<uint8_t, 16>
std::array<uint8_t, 16> bytes_to_key(py::object key_obj) {
        std::array<uint8_t, 16> key;

        // Handling various Python types
        if (py::isinstance<py::bytes>(key_obj) || py::isinstance<py::bytearray>(key_obj)) {
                py::bytes key_bytes = key_obj.cast<py::bytes>();

                if (py::len(key_bytes) != 16) {
                        throw py::value_error("Key must be 16 bytes");
                }

                std::string key_str = key_bytes;
                for (size_t i = 0; i < 16; i++) {
                        key[i] = static_cast<uint8_t>(key_str[i]);
                }
        }
        else if (py::isinstance<py::list>(key_obj)) {
                py::list key_list = key_obj.cast<py::list>();
                
                if (py::len(key_list) != 16) {
                        throw py::value_error("Key list must have 16 elements");
                }

                for (size_t i = 0; i < 16; i++) {
                        key[i] = key_list[i].cast<uint8_t>();
                }
        }
        else {
                throw py::type_error("Key must be bytes, bytearray, or list of integers");
        }

        return key;
}

// Convert Python 2D list/array to state matrix
std::array<std::array<uint8_t, 4>, 4> py_to_state(py::object state_obj) {
        std::array<std::array<uint8_t, 4>, 4> state;

        // Handle numpy
        if (py::isinstance<py::array>(state_obj)) {
                py::array_t<uint8_t, 4> np_array = state_obj.cast<py::array_t<uint8_t>>();

                auto r = np_array.unchecked<2>();

                if (r.shape(0) != 4 || r.shape(1) != 4) {
                        throw py::value_error("State must be 4x4");
                }

                for (py::ssize_t i = 0; i < 4; i++) {
                        for (py::ssize_t j = 0; j< 4; j++) {
                                state[i][j] = r(i, j);
                        }
                }
        }
        // Handle Python list of lists
        else if (py::isinstance<py::list>(state_obj)) {
                py::list outer_list = state_obj.cast<py::list>();

                if (py::len(outer_list) != 4) {
                        throw py::value_error("State must be 4x4");
                }

                for (py::ssize_t i = 0; i < 4; i++) {
                        py::list inner_list = outer_list[i].cast<py::list>();

                        if (py::len(inner_list) != 4) {
                                throw py::value_error("Each row of state must have 4 elements");
                        }

                        for (py::ssize_t j = 0; j < 4; j++) {
                                state[i][j] = inner_list[j].cast<uint8_t>();
                        }
                }
        }
        else {
                throw py::type_error("State must be numpy array or list of lists");
        }

        return state;
}

// Conversion of state matrix to Python list
py::list state_to_py(const std::array<std::array<uint8_t, 4>, 4>& state) {
        py::list result;
        for (int i = 0; i < 4; i++) {
                py::list row;
                for (int j = 0; j < 4; j++) {
                        row.append(state[i][j]);
                }
                result.append(row);
        }
        return result;
}

// Wrapper for key expansion
py::array_t<uint8_t> py_key_expansion(py::object key_obj) {
        // Convert py obj to key
        std::array<uint8_t, 16> key = bytes_to_key(key_obj);

        // Initialize round keys
        std::array<uint32_t, 44> roundKeys;

        keyExpansion(key, roundKeys);

        auto result = py::array_t<uint32_t>(44);
        auto result_ptr = result.mutable_data();

        for (size_t i = 0; i < 44; i++) {
                result_ptr[i] = roundKeys[i];
        }

        return result;
}

// Wrapper for encryption
py::list py_aes_encrypt(py::object state_obj, py::array_t<uint8_t> roundKeys_obj) {
        // Convert Python state to C++ state
        std::array<std::array<uint8_t, 4>, 4> state = py_to_state(state_obj);

        // Convert Python round keys to C++ round keys
        std::array<uint32_t, 44> roundKeys;
        auto roundKeys_ptr = roundKeys_obj.data();
        if (roundKeys_obj.size() != 44) {
                throw py::value_error("Round keys must have 44 elements");
        }

        for (size_t i = 0; i< 44; i++) {
                roundKeys[i] = roundKeys_ptr[i];
        }

        // Encrypt
        aesEncrypt(state, roundKeys);

        // Convert result to Python
        return state_to_py(state);
}

// Wrapper for decryption
py::list py_aes_decrypt(py::object state_obj, py::array_t<uint32_t> roundKeys_obj) {
        // Convert Python state to C++ state
        std::array<std::array<uint8_t, 4>, 4> state = py_to_state(state_obj);

        // Convert Python round keys to C++ round keys
        std::array<uint32_t, 44> roundKeys;
        auto roundKeys_ptr = roundKeys_obj.data();
        if (roundKeys_obj.size() != 44) {
                throw py::value_error("Round keys must have 44 elements");
        }

        for (size_t i = 0; i < 44; i++) {
                roundKeys[i] = roundKeys_ptr[i];
        }

        aesDecrypt(state, roundKeys);

        return state_to_py(state);
}

PYBIND11_MODULE(pyaes, m) {
        m.doc() = "Python wrapper for C++ AES implementation";

        m.def("key_expansion", &py_key_expansion, "Expand 16-byte key into round keys", py::arg("key"));

        m.def("aes_encrypt", &py_aes_encrypt, "Encrypt a 4x4 state matrix using round keys", py::arg("state"), py::arg("round_keys"));
        m.def("aes_decrypt", &py_aes_decrypt, "Decrypt a 4x4 state matrix using round keys", py::arg("state"), py::arg("round_keys"));
}
