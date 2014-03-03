#include <Python.h>
#include <math.h>

#define PI 3.14159265

static PyObject *fourier_an(PyObject *self, PyObject *args) {
    int n;
    int x;
    int i;

    if (!PyArg_ParseTuple(args, "iii", &x,  &n, &i)) {
        return NULL;
    }
    
    return Py_BuildValue("i", x * cos( (2*PI*n*i) ));
}

static PyObject *fourier_bn(PyObject *self, PyObject *args) {
    int n;
    int x;
    int i;

    if (!PyArg_ParseTuple(args, "iii", &x,  &n, &i)) {
        return NULL;
    }
    
    return Py_BuildValue("i", x * sin( (2*PI*n*i) ));
}

static PyMethodDef fourier_funcs[] = {
    {"an", (PyCFunction)fourier_an, 
        METH_VARARGS, NULL},
    {"bn", (PyCFunction)fourier_bn, 
        METH_VARARGS, NULL},
    {NULL}
};

void initfouriertransform(void)
{
    Py_InitModule3("fouriertransform", fourier_funcs,"");

}
