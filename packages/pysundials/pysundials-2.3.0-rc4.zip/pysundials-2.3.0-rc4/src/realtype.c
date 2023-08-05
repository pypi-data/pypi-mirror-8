#include <Python.h>
#include <stdio.h>
#include "sundials/sundials_types.h"

static PyObject *realtype_getsizeofrealtype(PyObject *self, PyObject *args) {
	if (!PyArg_ParseTuple(args, "")) return NULL;
	return Py_BuildValue("i", sizeof(realtype));
}

static PyMethodDef RealtypeMethods[] = {
	{"getsizeofrealtype",  realtype_getsizeofrealtype, METH_VARARGS, "Return the size of SUNDIALS' realtype."},
	{NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initrealtype(void) {
	(void) Py_InitModule("realtype", RealtypeMethods);
}
