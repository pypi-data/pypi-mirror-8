#include <Python.h>

#include "gost89.h"
#include "gosthash.h"
#include "sbox.h"

static gost_subst_block default_unpacked_sbox;

/* Docstrings */
static char module_docstring[] =
    "Gost89 crypto and hashsum";

static PyObject *pgosthash(PyObject *self, PyObject *args)
{
    int err = -1;
    byte hash[32];
    int inp_len;
    unsigned char *inp;
    gost_hash_ctx hash_ctx;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "s#", &inp, &inp_len))
        return NULL;

    memset(&hash_ctx, 0, sizeof(hash_ctx));
    err = init_gost_hash_ctx(&hash_ctx, &default_unpacked_sbox);
    if(err != 1) {
        goto err1;
    }

    err = hash_block(&hash_ctx, inp, inp_len);
    if(err != 1) {
        goto err;
    }

    err = finish_hash(&hash_ctx, hash);
    if(err != 1) {
        goto err;
    }

    done_gost_hash_ctx(&hash_ctx);

    /* Build the output tuple */
    PyObject *ret = Py_BuildValue("s#", hash, 32);
    return ret;
err:
    done_gost_hash_ctx(&hash_ctx);
err1:
    PyErr_SetString(PyExc_RuntimeError, "Internal error in gosthash");
    return NULL;

}
/* Module specification */
static PyMethodDef module_methods[] = {
    {"hash", pgosthash, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

/* Initialize the module */
PyMODINIT_FUNC init_gost89(void)
{
    PyObject *m = Py_InitModule3("_gost89", module_methods, module_docstring);
    if (m == NULL)
        return;

    unpack_sbox(default_sbox, &default_unpacked_sbox);
}

