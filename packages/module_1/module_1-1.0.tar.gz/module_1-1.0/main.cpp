#include <Python/Python.h>

static PyObject* test(PyObject* self, PyObject* args)
{
    return Py_BuildValue("s", "you are a madebi");
}

static PyMethodDef methods[] = {
    {"test", (PyCFunction)test,
     METH_VARARGS, NULL},
    {NULL}
};

PyMODINIT_FUNC
initmadebi(void)
{
  printf("hello world!!");
  (void) Py_InitModule("madebi", methods);
}


 