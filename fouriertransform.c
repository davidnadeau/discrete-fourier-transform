#include <Python.h>
#include <math.h>

#define PI 3.14159265

static PyObject *fourier_getcoefficients(PyObject *self, PyObject *args) {
    int n;
    PyObject *x;
    PyObject *samplechannels;
    PyObject *sample;
    int T;
    int channel;
    int i;
    double an = 0;
    double bn = 0;
    char *samp;
    double samplevalue;
    
    if (!PyArg_ParseTuple(args, "Oiii", &x,  &n, &T, &channel)) {
        return NULL;
    }
    
    for (i = 1; i < T; ++i) { 
        samplechannels = PySequence_GetItem(x,i);
        sample = PySequence_GetItem(samplechannels, channel);
        PyArg_Parse(sample, "s", &samp);
        samplevalue = atoi(samp);
        an += samplevalue * cos( (2.0*PI*n*i) );
        bn += samplevalue * sin( (2.0*PI*n*i) );
    }
    return Py_BuildValue("dd", an * (2.0/T), bn *(2.0/T));
}

static PyObject *fourier_a0(PyObject *self, PyObject *args) {
    int n;
    PyObject *x;
    PyObject *samplechannels;
    PyObject *sample;
    int T;
    int channel;
    int i;
    double a0 = 0;
    char *samp;

    if (!PyArg_ParseTuple(args, "Oii", &x, &T, &channel)) {
        return NULL;
    }
    for (i = 0; i < T; ++i) { 
        samplechannels = PySequence_GetItem(x,i);
        sample = PySequence_GetItem(samplechannels, channel);
        PyArg_Parse(sample, "s", &samp);
        a0 += atoi (samp);
    }

    return Py_BuildValue("d", a0 / T);
}

static PyMethodDef fourier_funcs[] = {
    {"coefficients", (PyCFunction)fourier_getcoefficients, 
        METH_VARARGS, NULL},
    {"a0", (PyCFunction)fourier_a0, 
        METH_VARARGS, NULL},
    {NULL}
};

void initfouriertransform(void)
{
    Py_InitModule3("fouriertransform", fourier_funcs,"");

}
