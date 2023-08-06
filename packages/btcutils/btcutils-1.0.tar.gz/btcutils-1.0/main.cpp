#include <iostream>
#include "utilstrencodings.h"
#include "uint256.h"
#include "hash.h"
#include <Python.h>

uint256 CheckMerkleBranch(uint256 hash, const std::vector<uint256>& vMerkleBranch, int nIndex)
{
    if (nIndex == -1)
        return 0;
    for (std::vector<uint256>::const_iterator it(vMerkleBranch.begin()); it != vMerkleBranch.end(); ++it)
    {
        if (nIndex & 1)
            hash = Hash(BEGIN(*it), END(*it), BEGIN(hash), END(hash));
        else
            hash = Hash(BEGIN(hash), END(hash), BEGIN(*it), END(*it));
        nIndex >>= 1;
    }
    return hash;
}

static PyObject* btcutils(PyObject* self, PyObject* args)
{
    const char *hash;
    PyObject* listobj;
    int index;

    if (!PyArg_ParseTuple(args, "sOi", &hash, &listobj, &index))
        return NULL;

    //printf(hash);

    PyObject* seq;
    PyObject* item;
    int i, len;

    std::vector<uint256> v;
    seq = PySequence_Fast(listobj, "expected a sequence");
    len = PySequence_Size(listobj);
    for (i = 0; i < len; i++) {
        item = PySequence_Fast_GET_ITEM(seq, i);
        //PyObject* objectsRepresentation = PyObject_Repr(item);
        //printf(PyString_AsString(objectsRepresentation));
        const char *item_cstr;
        std::string item_str(PyString_AsString(item));
        uint256 item_uint(item_str);
        v.push_back(item_uint);
    }
    Py_DECREF(seq);

    std::string hash_str(hash);
    uint256 hash_uint(hash_str);

    uint256 res;
    res = CheckMerkleBranch(hash_uint, v, index);

    std::string res_str = res.ToString();

    //todo: convert res to PyString and return it

    return Py_BuildValue("s", res_str.c_str());
}

static PyMethodDef methods[] = {
    {"check_merkle_branch", (PyCFunction)btcutils,
     METH_VARARGS, NULL},
    {NULL}
};

PyMODINIT_FUNC
initbtcutils(void)
{
  (void) Py_InitModule("btcutils", methods);
}

