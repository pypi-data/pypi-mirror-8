
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
   typedef unsigned char _Bool;
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ?   /* unsigned */                                   \
        (sizeof(type) < sizeof(long) ? PyInt_FromLong(x) :               \
         sizeof(type) == sizeof(long) ? PyLong_FromUnsignedLong(x) :     \
                                        PyLong_FromUnsignedLongLong(x))  \
      : (sizeof(type) <= sizeof(long) ? PyInt_FromLong(x) :              \
                                        PyLong_FromLongLong(x)))

#define _cffi_to_c_int(o, type)                                          \
    (sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), 0))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/



    #include "turbojpeg.h"
    

static void _cffi_check__tjregion(tjregion *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->x) << 1);
  (void)((p->y) << 1);
  (void)((p->w) << 1);
  (void)((p->h) << 1);
}
static PyObject *
_cffi_layout__tjregion(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; tjregion y; };
  static Py_ssize_t nums[] = {
    sizeof(tjregion),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(tjregion, x),
    sizeof(((tjregion *)0)->x),
    offsetof(tjregion, y),
    sizeof(((tjregion *)0)->y),
    offsetof(tjregion, w),
    sizeof(((tjregion *)0)->w),
    offsetof(tjregion, h),
    sizeof(((tjregion *)0)->h),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__tjregion(0);
}

static int _cffi_e_enum_TJXOP(PyObject *lib)
{
  if ((TJXOP_NONE) < 0 || (unsigned long)(TJXOP_NONE) != 0UL) {
    char buf[64];
    if ((TJXOP_NONE) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_NONE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_NONE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_NONE", buf, "0");
    return -1;
  }
  if ((TJXOP_HFLIP) < 0 || (unsigned long)(TJXOP_HFLIP) != 1UL) {
    char buf[64];
    if ((TJXOP_HFLIP) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_HFLIP));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_HFLIP));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_HFLIP", buf, "1");
    return -1;
  }
  if ((TJXOP_VFLIP) < 0 || (unsigned long)(TJXOP_VFLIP) != 2UL) {
    char buf[64];
    if ((TJXOP_VFLIP) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_VFLIP));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_VFLIP));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_VFLIP", buf, "2");
    return -1;
  }
  if ((TJXOP_TRANSPOSE) < 0 || (unsigned long)(TJXOP_TRANSPOSE) != 3UL) {
    char buf[64];
    if ((TJXOP_TRANSPOSE) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_TRANSPOSE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_TRANSPOSE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_TRANSPOSE", buf, "3");
    return -1;
  }
  if ((TJXOP_TRANSVERSE) < 0 || (unsigned long)(TJXOP_TRANSVERSE) != 4UL) {
    char buf[64];
    if ((TJXOP_TRANSVERSE) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_TRANSVERSE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_TRANSVERSE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_TRANSVERSE", buf, "4");
    return -1;
  }
  if ((TJXOP_ROT90) < 0 || (unsigned long)(TJXOP_ROT90) != 5UL) {
    char buf[64];
    if ((TJXOP_ROT90) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_ROT90));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_ROT90));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_ROT90", buf, "5");
    return -1;
  }
  if ((TJXOP_ROT180) < 0 || (unsigned long)(TJXOP_ROT180) != 6UL) {
    char buf[64];
    if ((TJXOP_ROT180) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_ROT180));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_ROT180));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_ROT180", buf, "6");
    return -1;
  }
  if ((TJXOP_ROT270) < 0 || (unsigned long)(TJXOP_ROT270) != 7UL) {
    char buf[64];
    if ((TJXOP_ROT270) < 0)
        snprintf(buf, 63, "%ld", (long)(TJXOP_ROT270));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(TJXOP_ROT270));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "TJXOP", "TJXOP_ROT270", buf, "7");
    return -1;
  }
  return 0;
}

static PyObject *
_cffi_f_tjDecompressHeader2(PyObject *self, PyObject *args)
{
  void * x0;
  unsigned char * x1;
  unsigned long x2;
  int * x3;
  int * x4;
  int * x5;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:tjDecompressHeader2", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(1), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, unsigned long);
  if (x2 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(2), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(2), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca(datasize);
    memset((void *)x5, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(2), arg5) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = tjDecompressHeader2(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_tjDestroy(PyObject *self, PyObject *arg0)
{
  void * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = tjDestroy(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_tjFree(PyObject *self, PyObject *arg0)
{
  unsigned char * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(1), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { tjFree(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_tjGetErrorStr(PyObject *self, PyObject *no_arg)
{
  char * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = tjGetErrorStr(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(4));
}

static PyObject *
_cffi_f_tjInitTransform(PyObject *self, PyObject *no_arg)
{
  void * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = tjInitTransform(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(0));
}

static PyObject *
_cffi_f_tjTransform(PyObject *self, PyObject *args)
{
  void * x0;
  unsigned char * x1;
  unsigned long x2;
  int x3;
  unsigned char * * x4;
  unsigned long * x5;
  tjtransform * x6;
  int x7;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;
  PyObject *arg6;
  PyObject *arg7;

  if (!PyArg_ParseTuple(args, "OOOOOOOO:tjTransform", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5, &arg6, &arg7))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(0), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(1), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, unsigned long);
  if (x2 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(5), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca(datasize);
    memset((void *)x5, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(6), arg5) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg6, (char **)&x6);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x6 = alloca(datasize);
    memset((void *)x6, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x6, _cffi_type(7), arg6) < 0)
      return NULL;
  }

  x7 = _cffi_to_c_int(arg7, int);
  if (x7 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = tjTransform(x0, x1, x2, x3, x4, x5, x6, x7); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static int _cffi_const_TJXOPT_CROP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(TJXOPT_CROP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "TJXOPT_CROP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_e_enum_TJXOP(lib);
}

static int _cffi_const_TJXOPT_GRAY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(TJXOPT_GRAY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "TJXOPT_GRAY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_TJXOPT_CROP(lib);
}

static int _cffi_const_TJXOPT_PERFECT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(TJXOPT_PERFECT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "TJXOPT_PERFECT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_TJXOPT_GRAY(lib);
}

static int _cffi_const_TJXOPT_TRIM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(TJXOPT_TRIM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "TJXOPT_TRIM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_TJXOPT_PERFECT(lib);
}

static void _cffi_check_struct_tjtransform(struct tjtransform *p)
{
  /* only to generate compile-time warnings or errors */
  { tjregion *tmp = &p->r; (void)tmp; }
  (void)((p->op) << 1);
  (void)((p->options) << 1);
}
static PyObject *
_cffi_layout_struct_tjtransform(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct tjtransform y; };
  static Py_ssize_t nums[] = {
    sizeof(struct tjtransform),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct tjtransform, r),
    sizeof(((struct tjtransform *)0)->r),
    offsetof(struct tjtransform, op),
    sizeof(((struct tjtransform *)0)->op),
    offsetof(struct tjtransform, options),
    sizeof(((struct tjtransform *)0)->options),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_tjtransform(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_TJXOPT_TRIM(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__tjregion", _cffi_layout__tjregion, METH_NOARGS, NULL},
  {"tjDecompressHeader2", _cffi_f_tjDecompressHeader2, METH_VARARGS, NULL},
  {"tjDestroy", _cffi_f_tjDestroy, METH_O, NULL},
  {"tjFree", _cffi_f_tjFree, METH_O, NULL},
  {"tjGetErrorStr", _cffi_f_tjGetErrorStr, METH_NOARGS, NULL},
  {"tjInitTransform", _cffi_f_tjInitTransform, METH_NOARGS, NULL},
  {"tjTransform", _cffi_f_tjTransform, METH_VARARGS, NULL},
  {"_cffi_layout_struct_tjtransform", _cffi_layout_struct_tjtransform, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__xb366312fxf3ca0677",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__xb366312fxf3ca0677(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (0 < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__xb366312fxf3ca0677(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__xb366312fxf3ca0677", _cffi_methods);
  if (lib == NULL)
    return;
  if (0 < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
