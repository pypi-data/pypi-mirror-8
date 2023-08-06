/*
   Copyright 2011 Torsten Landschoff

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

/*
   extension.cpp --- Python extension module for open-vcdiff
*/

#include <Python.h>
#include <google/vcencoder.h>
#include <google/vcdecoder.h>
#include <string>
#include <cassert>

using open_vcdiff::VCDiffEncoder;
using open_vcdiff::VCDiffStreamingEncoder;
using open_vcdiff::VCDiffDecoder;
using open_vcdiff::HashedDictionary;

struct hasheddictionary {
    PyObject_HEAD
    HashedDictionary imp;
};

inline PyTypeObject *getHashedDictionaryType();

// Get start address of Py_buffer as const char pointer (Python uses void*).
inline const char *start(const Py_buffer &buffer)
{
    return reinterpret_cast<const char*>(buffer.buf);
}

// For consistency of access, this gives the length of a Py_buffer.
inline std::size_t len(const Py_buffer &buffer)
{
    return buffer.len;
}

static PyObject *
simple_encode(Py_buffer &dictionary, Py_buffer &target)
{
    std::string delta;

    Py_BEGIN_ALLOW_THREADS
    VCDiffEncoder encoder(start(dictionary), len(dictionary));
    encoder.Encode(start(target), len(target), &delta);
    Py_END_ALLOW_THREADS

    PyBuffer_Release(&target);
    PyBuffer_Release(&dictionary);

    return PyString_FromStringAndSize(delta.data(), delta.size());
}

static PyObject *
hashdict_encode(hasheddictionary *hashdict, Py_buffer &target)
{
    HashedDictionary &hd = hashdict->imp;
    std::string delta;

    Py_BEGIN_ALLOW_THREADS
    VCDiffStreamingEncoder v(&hd, open_vcdiff::VCD_STANDARD_FORMAT, false);
    if (!v.StartEncoding(&delta)) {
        assert(0);
    }

    if (!v.EncodeChunk(start(target), len(target), &delta)) {
        assert(0);
    }

    if (!v.FinishEncoding(&delta)) {
        assert(0);
    }
    Py_END_ALLOW_THREADS

    PyBuffer_Release(&target);
    Py_DECREF((PyObject*) hashdict);
    return PyString_FromStringAndSize(delta.data(), delta.size());
}

static PyObject *
openvcdiff_encode(PyObject *self, PyObject *args, PyObject *kwargs)
{
    Py_buffer target;
    PyObject *dictionary;

    static const char *keywords[] = { "target", "dictionary", NULL };

    /* The s* format actually enforces a continuous buffer, which is not
       mentioned in the Python documentation. */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s*O:encode",
            const_cast<char**>(keywords), &target, &dictionary)) {
        return NULL;
    }

    Py_INCREF(dictionary);
    if (PyObject_CheckBuffer(dictionary)) {
        Py_buffer dict_buffer;
        if (PyObject_GetBuffer(dictionary, &dict_buffer, PyBUF_SIMPLE)) {
            Py_DECREF(dictionary);
            PyBuffer_Release(&target);
            return NULL;
        }
        Py_DECREF(dictionary);      // now held via dict_buffer
        return simple_encode(dict_buffer, target);
    }

    if (Py_TYPE(dictionary) != getHashedDictionaryType()) {
        PyBuffer_Release(&target);
        Py_DECREF(dictionary);
        return PyErr_Format(PyExc_TypeError,
                "encode() argument 2 must be string, buffer or HashedDictionary");
    }

    return hashdict_encode((hasheddictionary*) dictionary, target);
}

static PyObject *
openvcdiff_decode(PyObject *self, PyObject *args, PyObject *kwargs)
{
    Py_buffer delta, dictionary;

    static const char *keywords[] = { "delta", "dictionary", NULL };

    /* The s* format actually enforces a continuous buffer, which is not
       mentioned in the Python documentation. */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s*s*:decode",
            const_cast<char**>(keywords), &delta, &dictionary)) {
        return NULL;
    }

    std::string target;

    Py_BEGIN_ALLOW_THREADS

    // Too bad, this is one more unneeded copy: The simple interface wants
    // a string object for the input data...
    std::string delta_string(start(delta), len(delta));

    VCDiffDecoder decoder;
    decoder.Decode(start(dictionary), len(dictionary), delta_string, &target);

    Py_END_ALLOW_THREADS

    PyBuffer_Release(&delta);
    PyBuffer_Release(&dictionary);

    return PyString_FromStringAndSize(target.data(), target.size());
}

static PyMethodDef OpenVcdiffMethods[] = {
    {"encode", (PyCFunction) openvcdiff_encode, METH_VARARGS | METH_KEYWORDS,
     "encode(target, dictionary)\n"
     "Encodes *target* using the data in *dictionary*. Both can be byte "
     "strings or memory views. Returns a memory view with the delta."},
    {"decode", (PyCFunction) openvcdiff_decode, METH_VARARGS | METH_KEYWORDS,
     "decode(delta, dictionary)\n"
     "Applies the given *delta* to the *dictionary* data. Again, both "
     "can be byte strings or memory views. Returns a memory view with the "
     "reconstructed target."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyObject *hasheddictionary_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds)
{
    Py_buffer dictionary;
    bool init_okay;

    if (!PyArg_ParseTuple(args, "s*:HashedDictionary", &dictionary))
        return NULL;

    hasheddictionary *self = (hasheddictionary*) PyType_GenericNew(subtype, args, kwds);
    Py_BEGIN_ALLOW_THREADS
    HashedDictionary *pimp = new (&self->imp) HashedDictionary(start(dictionary), len(dictionary));
    assert(pimp == &self->imp);
    init_okay = pimp->Init();
    Py_END_ALLOW_THREADS
    if (!init_okay) {
        self->imp.~HashedDictionary();
        return PyErr_Format(PyExc_RuntimeError, "HashedDictionary::Init failed.");
    }
    return (PyObject *) self;
}

static void hasheddictionary_dealloc(PyObject *self)
{
    hasheddictionary *hdself = (hasheddictionary*) self;
    hdself->imp.~HashedDictionary();
    Py_TYPE(self)->tp_free(self);
}


static PyTypeObject HashedDictionaryType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "openvcdiff.HashedDictionary", /*tp_name*/
    sizeof(hasheddictionary),  /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    hasheddictionary_dealloc,  /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    /* tp_doc */
    "HashedDictionary for creating multiple datas from the same dictionary data.",
    0,                         /*tp_traverse*/
    0,                         /*tp_clear*/
    0,                         /*tp_richcompare*/
    0,                         /*tp_weaklistoffset*/
    0,                         /*tp_iter*/
    0,                         /*tp_iternext*/

    /* Attribute descriptor and subclassing stuff */
    0,                         /*tp_methods*/
    0,                         /*tp_members*/
    0,                         /*tp_getset*/
    0,                         /*tp_base*/
    0,                         /*tp_dict*/
    0,                         /*tp_descr_get*/
    0,                         /*tp_descr_set*/
    0,                         /*tp_dictoffset*/
    0,                         /*tp_init*/
    0,                         /*tp_alloc*/
    hasheddictionary_new,      /*tp_new*/
};

inline PyTypeObject *getHashedDictionaryType()
{
    return &HashedDictionaryType;
}


PyMODINIT_FUNC
initopenvcdiff(void)
{
    PyObject *module;

    if (PyType_Ready(&HashedDictionaryType) < 0)
        return;

    module = Py_InitModule("openvcdiff", OpenVcdiffMethods);
    if (module) {
        Py_INCREF(&HashedDictionaryType);
        PyModule_AddObject(module, "HashedDictionary", (PyObject *) &HashedDictionaryType);
    }
}
