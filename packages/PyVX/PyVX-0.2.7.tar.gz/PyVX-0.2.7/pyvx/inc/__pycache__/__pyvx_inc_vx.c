
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


#include "VX/vx.h"

enum vx_additional_df_image_e {
    VX_DF_IMAGE_S8   = VX_DF_IMAGE('S','0','0','8'),
    VX_DF_IMAGE_U64  = VX_DF_IMAGE('U','0','6','4'),
    VX_DF_IMAGE_S64  = VX_DF_IMAGE('S','0','6','4'),
    VX_DF_IMAGE_F32  = VX_DF_IMAGE('F','0','3','2'),
    VX_DF_IMAGE_F64  = VX_DF_IMAGE('F','0','6','4'),
    VX_DF_IMAGE_F128 = VX_DF_IMAGE('F','1','2','8'),
};


static int _cffi_const_vx_false_e(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(vx_false_e);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "vx_false_e", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return 0;
}

static int _cffi_const_vx_true_e(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(vx_true_e);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "vx_true_e", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_vx_false_e(lib);
}

static int _cffi_const_VX_READ_ONLY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_READ_ONLY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_READ_ONLY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_vx_true_e(lib);
}

static int _cffi_const_VX_WRITE_ONLY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_WRITE_ONLY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_WRITE_ONLY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_READ_ONLY(lib);
}

static int _cffi_const_VX_READ_AND_WRITE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_READ_AND_WRITE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_READ_AND_WRITE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_WRITE_ONLY(lib);
}

static int _cffi_const_VX_ACTION_CONTINUE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ACTION_CONTINUE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ACTION_CONTINUE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_READ_AND_WRITE(lib);
}

static int _cffi_const_VX_ACTION_RESTART(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ACTION_RESTART);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ACTION_RESTART", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ACTION_CONTINUE(lib);
}

static int _cffi_const_VX_ACTION_ABANDON(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ACTION_ABANDON);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ACTION_ABANDON", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ACTION_RESTART(lib);
}

static int _cffi_const_VX_DF_IMAGE_S8(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_S8);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_S8", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ACTION_ABANDON(lib);
}

static int _cffi_const_VX_DF_IMAGE_U64(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_U64);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_U64", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_S8(lib);
}

static int _cffi_const_VX_DF_IMAGE_S64(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_S64);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_S64", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_U64(lib);
}

static int _cffi_const_VX_DF_IMAGE_F32(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_F32);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_F32", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_S64(lib);
}

static int _cffi_const_VX_DF_IMAGE_F64(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_F64);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_F64", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_F32(lib);
}

static int _cffi_const_VX_DF_IMAGE_F128(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_F128);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_F128", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_F64(lib);
}

static int _cffi_const_VX_ARRAY_ATTRIBUTE_ITEMTYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ARRAY_ATTRIBUTE_ITEMTYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ARRAY_ATTRIBUTE_ITEMTYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_F128(lib);
}

static int _cffi_const_VX_ARRAY_ATTRIBUTE_NUMITEMS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ARRAY_ATTRIBUTE_NUMITEMS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ARRAY_ATTRIBUTE_NUMITEMS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ARRAY_ATTRIBUTE_ITEMTYPE(lib);
}

static int _cffi_const_VX_ARRAY_ATTRIBUTE_CAPACITY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ARRAY_ATTRIBUTE_CAPACITY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ARRAY_ATTRIBUTE_CAPACITY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ARRAY_ATTRIBUTE_NUMITEMS(lib);
}

static int _cffi_const_VX_ARRAY_ATTRIBUTE_ITEMSIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ARRAY_ATTRIBUTE_ITEMSIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ARRAY_ATTRIBUTE_ITEMSIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ARRAY_ATTRIBUTE_CAPACITY(lib);
}

static int _cffi_const_VX_BORDER_MODE_UNDEFINED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_BORDER_MODE_UNDEFINED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_BORDER_MODE_UNDEFINED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ARRAY_ATTRIBUTE_ITEMSIZE(lib);
}

static int _cffi_const_VX_BORDER_MODE_CONSTANT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_BORDER_MODE_CONSTANT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_BORDER_MODE_CONSTANT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_BORDER_MODE_UNDEFINED(lib);
}

static int _cffi_const_VX_BORDER_MODE_REPLICATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_BORDER_MODE_REPLICATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_BORDER_MODE_REPLICATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_BORDER_MODE_CONSTANT(lib);
}

static int _cffi_const_VX_CHANNEL_0(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_0);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_0", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_BORDER_MODE_REPLICATE(lib);
}

static int _cffi_const_VX_CHANNEL_1(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_1);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_1", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_0(lib);
}

static int _cffi_const_VX_CHANNEL_2(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_2);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_2", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_1(lib);
}

static int _cffi_const_VX_CHANNEL_3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_2(lib);
}

static int _cffi_const_VX_CHANNEL_R(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_R);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_R", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_3(lib);
}

static int _cffi_const_VX_CHANNEL_G(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_G);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_G", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_R(lib);
}

static int _cffi_const_VX_CHANNEL_B(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_B);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_B", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_G(lib);
}

static int _cffi_const_VX_CHANNEL_A(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_A);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_A", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_B(lib);
}

static int _cffi_const_VX_CHANNEL_Y(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_Y);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_Y", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_A(lib);
}

static int _cffi_const_VX_CHANNEL_U(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_U);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_U", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_Y(lib);
}

static int _cffi_const_VX_CHANNEL_V(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_V);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_V", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_U(lib);
}

static int _cffi_const_VX_CHANNEL_RANGE_FULL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_RANGE_FULL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_RANGE_FULL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_V(lib);
}

static int _cffi_const_VX_CHANNEL_RANGE_RESTRICTED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CHANNEL_RANGE_RESTRICTED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CHANNEL_RANGE_RESTRICTED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_RANGE_FULL(lib);
}

static int _cffi_const_VX_COLOR_SPACE_NONE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_COLOR_SPACE_NONE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_COLOR_SPACE_NONE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CHANNEL_RANGE_RESTRICTED(lib);
}

static int _cffi_const_VX_COLOR_SPACE_BT601_525(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_COLOR_SPACE_BT601_525);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_COLOR_SPACE_BT601_525", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_COLOR_SPACE_NONE(lib);
}

static int _cffi_const_VX_COLOR_SPACE_BT601_625(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_COLOR_SPACE_BT601_625);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_COLOR_SPACE_BT601_625", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_COLOR_SPACE_BT601_525(lib);
}

static int _cffi_const_VX_COLOR_SPACE_BT709(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_COLOR_SPACE_BT709);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_COLOR_SPACE_BT709", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_COLOR_SPACE_BT601_625(lib);
}

static int _cffi_const_VX_COLOR_SPACE_DEFAULT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_COLOR_SPACE_DEFAULT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_COLOR_SPACE_DEFAULT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_COLOR_SPACE_BT709(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_VENDOR_ID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_VENDOR_ID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_VENDOR_ID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_COLOR_SPACE_DEFAULT(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_VERSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_VERSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_VERSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_VENDOR_ID(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_VERSION(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_MODULES(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_MODULES);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_MODULES", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNELS(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_REFERENCES(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_REFERENCES);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_REFERENCES", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_MODULES(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_REFERENCES(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_IMPLEMENTATION(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_EXTENSIONS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_EXTENSIONS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_EXTENSIONS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_EXTENSIONS_SIZE(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_EXTENSIONS(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_CONVOLUTION_MAXIMUM_DIMENSION(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_OPTICAL_FLOW_WINDOW_MAXIMUM_DIMENSION(lib);
}

static int _cffi_const_VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_IMMEDIATE_BORDER_MODE(lib);
}

static int _cffi_const_VX_CONVERT_POLICY_WRAP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVERT_POLICY_WRAP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVERT_POLICY_WRAP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONTEXT_ATTRIBUTE_UNIQUE_KERNEL_TABLE(lib);
}

static int _cffi_const_VX_CONVERT_POLICY_SATURATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVERT_POLICY_SATURATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVERT_POLICY_SATURATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVERT_POLICY_WRAP(lib);
}

static int _cffi_const_VX_CONVOLUTION_ATTRIBUTE_ROWS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVOLUTION_ATTRIBUTE_ROWS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVOLUTION_ATTRIBUTE_ROWS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVERT_POLICY_SATURATE(lib);
}

static int _cffi_const_VX_CONVOLUTION_ATTRIBUTE_COLUMNS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVOLUTION_ATTRIBUTE_COLUMNS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVOLUTION_ATTRIBUTE_COLUMNS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVOLUTION_ATTRIBUTE_ROWS(lib);
}

static int _cffi_const_VX_CONVOLUTION_ATTRIBUTE_SCALE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVOLUTION_ATTRIBUTE_SCALE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVOLUTION_ATTRIBUTE_SCALE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVOLUTION_ATTRIBUTE_COLUMNS(lib);
}

static int _cffi_const_VX_CONVOLUTION_ATTRIBUTE_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_CONVOLUTION_ATTRIBUTE_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_CONVOLUTION_ATTRIBUTE_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVOLUTION_ATTRIBUTE_SCALE(lib);
}

static int _cffi_const_VX_DELAY_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DELAY_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DELAY_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_CONVOLUTION_ATTRIBUTE_SIZE(lib);
}

static int _cffi_const_VX_DELAY_ATTRIBUTE_COUNT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DELAY_ATTRIBUTE_COUNT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DELAY_ATTRIBUTE_COUNT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DELAY_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_DF_IMAGE_VIRT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_VIRT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_VIRT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DELAY_ATTRIBUTE_COUNT(lib);
}

static int _cffi_const_VX_DF_IMAGE_RGB(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_RGB);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_RGB", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_VIRT(lib);
}

static int _cffi_const_VX_DF_IMAGE_RGBX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_RGBX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_RGBX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_RGB(lib);
}

static int _cffi_const_VX_DF_IMAGE_NV12(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_NV12);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_NV12", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_RGBX(lib);
}

static int _cffi_const_VX_DF_IMAGE_NV21(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_NV21);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_NV21", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_NV12(lib);
}

static int _cffi_const_VX_DF_IMAGE_UYVY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_UYVY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_UYVY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_NV21(lib);
}

static int _cffi_const_VX_DF_IMAGE_YUYV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_YUYV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_YUYV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_UYVY(lib);
}

static int _cffi_const_VX_DF_IMAGE_IYUV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_IYUV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_IYUV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_YUYV(lib);
}

static int _cffi_const_VX_DF_IMAGE_YUV4(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_YUV4);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_YUV4", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_IYUV(lib);
}

static int _cffi_const_VX_DF_IMAGE_U8(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_U8);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_U8", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_YUV4(lib);
}

static int _cffi_const_VX_DF_IMAGE_U16(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_U16);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_U16", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_U8(lib);
}

static int _cffi_const_VX_DF_IMAGE_S16(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_S16);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_S16", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_U16(lib);
}

static int _cffi_const_VX_DF_IMAGE_U32(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_U32);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_U32", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_S16(lib);
}

static int _cffi_const_VX_DF_IMAGE_S32(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DF_IMAGE_S32);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DF_IMAGE_S32", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_U32(lib);
}

static int _cffi_const_VX_INPUT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_INPUT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_INPUT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DF_IMAGE_S32(lib);
}

static int _cffi_const_VX_OUTPUT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_OUTPUT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_OUTPUT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_INPUT(lib);
}

static int _cffi_const_VX_BIDIRECTIONAL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_BIDIRECTIONAL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_BIDIRECTIONAL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_OUTPUT(lib);
}

static int _cffi_const_VX_DIRECTIVE_DISABLE_LOGGING(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DIRECTIVE_DISABLE_LOGGING);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DIRECTIVE_DISABLE_LOGGING", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_BIDIRECTIONAL(lib);
}

static int _cffi_const_VX_DIRECTIVE_ENABLE_LOGGING(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DIRECTIVE_ENABLE_LOGGING);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DIRECTIVE_ENABLE_LOGGING", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DIRECTIVE_DISABLE_LOGGING(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DIRECTIVE_ENABLE_LOGGING(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_OFFSET(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_OFFSET);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_OFFSET", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_DIMENSIONS(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_RANGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_RANGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_RANGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_OFFSET(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_BINS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_BINS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_BINS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_RANGE(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_WINDOW(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_WINDOW);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_WINDOW", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_BINS(lib);
}

static int _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_DISTRIBUTION_ATTRIBUTE_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_DISTRIBUTION_ATTRIBUTE_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_WINDOW(lib);
}

static int _cffi_e_enum_vx_enum_e(PyObject *lib)
{
  if ((VX_ENUM_DIRECTION) < 0 || (unsigned long)(VX_ENUM_DIRECTION) != 0UL) {
    char buf[64];
    if ((VX_ENUM_DIRECTION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_DIRECTION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_DIRECTION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_DIRECTION", buf, "0");
    return -1;
  }
  if ((VX_ENUM_ACTION) < 0 || (unsigned long)(VX_ENUM_ACTION) != 1UL) {
    char buf[64];
    if ((VX_ENUM_ACTION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_ACTION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_ACTION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_ACTION", buf, "1");
    return -1;
  }
  if ((VX_ENUM_HINT) < 0 || (unsigned long)(VX_ENUM_HINT) != 2UL) {
    char buf[64];
    if ((VX_ENUM_HINT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_HINT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_HINT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_HINT", buf, "2");
    return -1;
  }
  if ((VX_ENUM_DIRECTIVE) < 0 || (unsigned long)(VX_ENUM_DIRECTIVE) != 3UL) {
    char buf[64];
    if ((VX_ENUM_DIRECTIVE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_DIRECTIVE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_DIRECTIVE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_DIRECTIVE", buf, "3");
    return -1;
  }
  if ((VX_ENUM_INTERPOLATION) < 0 || (unsigned long)(VX_ENUM_INTERPOLATION) != 4UL) {
    char buf[64];
    if ((VX_ENUM_INTERPOLATION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_INTERPOLATION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_INTERPOLATION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_INTERPOLATION", buf, "4");
    return -1;
  }
  if ((VX_ENUM_OVERFLOW) < 0 || (unsigned long)(VX_ENUM_OVERFLOW) != 5UL) {
    char buf[64];
    if ((VX_ENUM_OVERFLOW) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_OVERFLOW));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_OVERFLOW));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_OVERFLOW", buf, "5");
    return -1;
  }
  if ((VX_ENUM_COLOR_SPACE) < 0 || (unsigned long)(VX_ENUM_COLOR_SPACE) != 6UL) {
    char buf[64];
    if ((VX_ENUM_COLOR_SPACE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_COLOR_SPACE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_COLOR_SPACE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_COLOR_SPACE", buf, "6");
    return -1;
  }
  if ((VX_ENUM_COLOR_RANGE) < 0 || (unsigned long)(VX_ENUM_COLOR_RANGE) != 7UL) {
    char buf[64];
    if ((VX_ENUM_COLOR_RANGE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_COLOR_RANGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_COLOR_RANGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_COLOR_RANGE", buf, "7");
    return -1;
  }
  if ((VX_ENUM_PARAMETER_STATE) < 0 || (unsigned long)(VX_ENUM_PARAMETER_STATE) != 8UL) {
    char buf[64];
    if ((VX_ENUM_PARAMETER_STATE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_PARAMETER_STATE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_PARAMETER_STATE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_PARAMETER_STATE", buf, "8");
    return -1;
  }
  if ((VX_ENUM_CHANNEL) < 0 || (unsigned long)(VX_ENUM_CHANNEL) != 9UL) {
    char buf[64];
    if ((VX_ENUM_CHANNEL) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_CHANNEL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_CHANNEL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_CHANNEL", buf, "9");
    return -1;
  }
  if ((VX_ENUM_CONVERT_POLICY) < 0 || (unsigned long)(VX_ENUM_CONVERT_POLICY) != 10UL) {
    char buf[64];
    if ((VX_ENUM_CONVERT_POLICY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_CONVERT_POLICY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_CONVERT_POLICY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_CONVERT_POLICY", buf, "10");
    return -1;
  }
  if ((VX_ENUM_THRESHOLD_TYPE) < 0 || (unsigned long)(VX_ENUM_THRESHOLD_TYPE) != 11UL) {
    char buf[64];
    if ((VX_ENUM_THRESHOLD_TYPE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_THRESHOLD_TYPE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_THRESHOLD_TYPE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_THRESHOLD_TYPE", buf, "11");
    return -1;
  }
  if ((VX_ENUM_BORDER_MODE) < 0 || (unsigned long)(VX_ENUM_BORDER_MODE) != 12UL) {
    char buf[64];
    if ((VX_ENUM_BORDER_MODE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_BORDER_MODE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_BORDER_MODE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_BORDER_MODE", buf, "12");
    return -1;
  }
  if ((VX_ENUM_COMPARISON) < 0 || (unsigned long)(VX_ENUM_COMPARISON) != 13UL) {
    char buf[64];
    if ((VX_ENUM_COMPARISON) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_COMPARISON));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_COMPARISON));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_COMPARISON", buf, "13");
    return -1;
  }
  if ((VX_ENUM_IMPORT_MEM) < 0 || (unsigned long)(VX_ENUM_IMPORT_MEM) != 14UL) {
    char buf[64];
    if ((VX_ENUM_IMPORT_MEM) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_IMPORT_MEM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_IMPORT_MEM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_IMPORT_MEM", buf, "14");
    return -1;
  }
  if ((VX_ENUM_TERM_CRITERIA) < 0 || (unsigned long)(VX_ENUM_TERM_CRITERIA) != 15UL) {
    char buf[64];
    if ((VX_ENUM_TERM_CRITERIA) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_TERM_CRITERIA));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_TERM_CRITERIA));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_TERM_CRITERIA", buf, "15");
    return -1;
  }
  if ((VX_ENUM_NORM_TYPE) < 0 || (unsigned long)(VX_ENUM_NORM_TYPE) != 16UL) {
    char buf[64];
    if ((VX_ENUM_NORM_TYPE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_NORM_TYPE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_NORM_TYPE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_NORM_TYPE", buf, "16");
    return -1;
  }
  if ((VX_ENUM_ACCESSOR) < 0 || (unsigned long)(VX_ENUM_ACCESSOR) != 17UL) {
    char buf[64];
    if ((VX_ENUM_ACCESSOR) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_ACCESSOR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_ACCESSOR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_ACCESSOR", buf, "17");
    return -1;
  }
  if ((VX_ENUM_ROUND_POLICY) < 0 || (unsigned long)(VX_ENUM_ROUND_POLICY) != 18UL) {
    char buf[64];
    if ((VX_ENUM_ROUND_POLICY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ENUM_ROUND_POLICY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ENUM_ROUND_POLICY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_enum_e", "VX_ENUM_ROUND_POLICY", buf, "18");
    return -1;
  }
  return 0;
}

static int _cffi_const_VX_GRAPH_ATTRIBUTE_NUMNODES(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_GRAPH_ATTRIBUTE_NUMNODES);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_GRAPH_ATTRIBUTE_NUMNODES", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_DISTRIBUTION_ATTRIBUTE_SIZE(lib);
}

static int _cffi_const_VX_GRAPH_ATTRIBUTE_STATUS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_GRAPH_ATTRIBUTE_STATUS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_GRAPH_ATTRIBUTE_STATUS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_GRAPH_ATTRIBUTE_NUMNODES(lib);
}

static int _cffi_const_VX_GRAPH_ATTRIBUTE_PERFORMANCE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_GRAPH_ATTRIBUTE_PERFORMANCE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_GRAPH_ATTRIBUTE_PERFORMANCE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_GRAPH_ATTRIBUTE_STATUS(lib);
}

static int _cffi_const_VX_GRAPH_ATTRIBUTE_NUMPARAMETERS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_GRAPH_ATTRIBUTE_NUMPARAMETERS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_GRAPH_ATTRIBUTE_NUMPARAMETERS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_GRAPH_ATTRIBUTE_PERFORMANCE(lib);
}

static int _cffi_const_VX_HINT_SERIALIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_HINT_SERIALIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_HINT_SERIALIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_GRAPH_ATTRIBUTE_NUMPARAMETERS(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_WIDTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_WIDTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_WIDTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_HINT_SERIALIZE(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_HEIGHT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_HEIGHT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_HEIGHT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_WIDTH(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_FORMAT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_FORMAT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_FORMAT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_HEIGHT(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_PLANES(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_PLANES);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_PLANES", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_FORMAT(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_SPACE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_SPACE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_SPACE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_PLANES(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_RANGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_RANGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_RANGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_SPACE(lib);
}

static int _cffi_const_VX_IMAGE_ATTRIBUTE_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMAGE_ATTRIBUTE_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMAGE_ATTRIBUTE_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_RANGE(lib);
}

static int _cffi_const_VX_IMPORT_TYPE_NONE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMPORT_TYPE_NONE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMPORT_TYPE_NONE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMAGE_ATTRIBUTE_SIZE(lib);
}

static int _cffi_const_VX_IMPORT_TYPE_HOST(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_IMPORT_TYPE_HOST);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_IMPORT_TYPE_HOST", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMPORT_TYPE_NONE(lib);
}

static int _cffi_const_VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_IMPORT_TYPE_HOST(lib);
}

static int _cffi_const_VX_INTERPOLATION_TYPE_BILINEAR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_INTERPOLATION_TYPE_BILINEAR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_INTERPOLATION_TYPE_BILINEAR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_INTERPOLATION_TYPE_NEAREST_NEIGHBOR(lib);
}

static int _cffi_const_VX_INTERPOLATION_TYPE_AREA(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_INTERPOLATION_TYPE_AREA);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_INTERPOLATION_TYPE_AREA", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_INTERPOLATION_TYPE_BILINEAR(lib);
}

static int _cffi_const_VX_KERNEL_ATTRIBUTE_PARAMETERS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ATTRIBUTE_PARAMETERS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ATTRIBUTE_PARAMETERS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_INTERPOLATION_TYPE_AREA(lib);
}

static int _cffi_const_VX_KERNEL_ATTRIBUTE_NAME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ATTRIBUTE_NAME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ATTRIBUTE_NAME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ATTRIBUTE_PARAMETERS(lib);
}

static int _cffi_const_VX_KERNEL_ATTRIBUTE_ENUM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ATTRIBUTE_ENUM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ATTRIBUTE_ENUM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ATTRIBUTE_NAME(lib);
}

static int _cffi_const_VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ATTRIBUTE_ENUM(lib);
}

static int _cffi_const_VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ATTRIBUTE_LOCAL_DATA_SIZE(lib);
}

static int _cffi_const_VX_KERNEL_INVALID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_INVALID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_INVALID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ATTRIBUTE_LOCAL_DATA_PTR(lib);
}

static int _cffi_const_VX_KERNEL_COLOR_CONVERT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_COLOR_CONVERT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_COLOR_CONVERT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_INVALID(lib);
}

static int _cffi_const_VX_KERNEL_CHANNEL_EXTRACT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_CHANNEL_EXTRACT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_CHANNEL_EXTRACT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_COLOR_CONVERT(lib);
}

static int _cffi_const_VX_KERNEL_CHANNEL_COMBINE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_CHANNEL_COMBINE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_CHANNEL_COMBINE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_CHANNEL_EXTRACT(lib);
}

static int _cffi_const_VX_KERNEL_SOBEL_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_SOBEL_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_SOBEL_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_CHANNEL_COMBINE(lib);
}

static int _cffi_const_VX_KERNEL_MAGNITUDE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MAGNITUDE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MAGNITUDE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_SOBEL_3x3(lib);
}

static int _cffi_const_VX_KERNEL_PHASE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_PHASE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_PHASE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MAGNITUDE(lib);
}

static int _cffi_const_VX_KERNEL_SCALE_IMAGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_SCALE_IMAGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_SCALE_IMAGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_PHASE(lib);
}

static int _cffi_const_VX_KERNEL_TABLE_LOOKUP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_TABLE_LOOKUP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_TABLE_LOOKUP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_SCALE_IMAGE(lib);
}

static int _cffi_const_VX_KERNEL_HISTOGRAM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_HISTOGRAM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_HISTOGRAM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_TABLE_LOOKUP(lib);
}

static int _cffi_const_VX_KERNEL_EQUALIZE_HISTOGRAM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_EQUALIZE_HISTOGRAM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_EQUALIZE_HISTOGRAM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_HISTOGRAM(lib);
}

static int _cffi_const_VX_KERNEL_ABSDIFF(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ABSDIFF);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ABSDIFF", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_EQUALIZE_HISTOGRAM(lib);
}

static int _cffi_const_VX_KERNEL_MEAN_STDDEV(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MEAN_STDDEV);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MEAN_STDDEV", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ABSDIFF(lib);
}

static int _cffi_const_VX_KERNEL_THRESHOLD(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_THRESHOLD);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_THRESHOLD", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MEAN_STDDEV(lib);
}

static int _cffi_const_VX_KERNEL_INTEGRAL_IMAGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_INTEGRAL_IMAGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_INTEGRAL_IMAGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_THRESHOLD(lib);
}

static int _cffi_const_VX_KERNEL_DILATE_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_DILATE_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_DILATE_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_INTEGRAL_IMAGE(lib);
}

static int _cffi_const_VX_KERNEL_ERODE_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ERODE_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ERODE_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_DILATE_3x3(lib);
}

static int _cffi_const_VX_KERNEL_MEDIAN_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MEDIAN_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MEDIAN_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ERODE_3x3(lib);
}

static int _cffi_const_VX_KERNEL_BOX_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_BOX_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_BOX_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MEDIAN_3x3(lib);
}

static int _cffi_const_VX_KERNEL_GAUSSIAN_3x3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_GAUSSIAN_3x3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_GAUSSIAN_3x3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_BOX_3x3(lib);
}

static int _cffi_const_VX_KERNEL_CUSTOM_CONVOLUTION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_CUSTOM_CONVOLUTION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_CUSTOM_CONVOLUTION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_GAUSSIAN_3x3(lib);
}

static int _cffi_const_VX_KERNEL_GAUSSIAN_PYRAMID(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_GAUSSIAN_PYRAMID);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_GAUSSIAN_PYRAMID", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_CUSTOM_CONVOLUTION(lib);
}

static int _cffi_const_VX_KERNEL_ACCUMULATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ACCUMULATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ACCUMULATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_GAUSSIAN_PYRAMID(lib);
}

static int _cffi_const_VX_KERNEL_ACCUMULATE_WEIGHTED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ACCUMULATE_WEIGHTED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ACCUMULATE_WEIGHTED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ACCUMULATE(lib);
}

static int _cffi_const_VX_KERNEL_ACCUMULATE_SQUARE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ACCUMULATE_SQUARE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ACCUMULATE_SQUARE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ACCUMULATE_WEIGHTED(lib);
}

static int _cffi_const_VX_KERNEL_MINMAXLOC(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MINMAXLOC);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MINMAXLOC", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ACCUMULATE_SQUARE(lib);
}

static int _cffi_const_VX_KERNEL_CONVERTDEPTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_CONVERTDEPTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_CONVERTDEPTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MINMAXLOC(lib);
}

static int _cffi_const_VX_KERNEL_CANNY_EDGE_DETECTOR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_CANNY_EDGE_DETECTOR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_CANNY_EDGE_DETECTOR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_CONVERTDEPTH(lib);
}

static int _cffi_const_VX_KERNEL_AND(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_AND);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_AND", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_CANNY_EDGE_DETECTOR(lib);
}

static int _cffi_const_VX_KERNEL_OR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_OR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_OR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_AND(lib);
}

static int _cffi_const_VX_KERNEL_XOR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_XOR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_XOR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_OR(lib);
}

static int _cffi_const_VX_KERNEL_NOT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_NOT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_NOT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_XOR(lib);
}

static int _cffi_const_VX_KERNEL_MULTIPLY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MULTIPLY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MULTIPLY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_NOT(lib);
}

static int _cffi_const_VX_KERNEL_ADD(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_ADD);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_ADD", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MULTIPLY(lib);
}

static int _cffi_const_VX_KERNEL_SUBTRACT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_SUBTRACT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_SUBTRACT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_ADD(lib);
}

static int _cffi_const_VX_KERNEL_WARP_AFFINE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_WARP_AFFINE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_WARP_AFFINE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_SUBTRACT(lib);
}

static int _cffi_const_VX_KERNEL_WARP_PERSPECTIVE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_WARP_PERSPECTIVE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_WARP_PERSPECTIVE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_WARP_AFFINE(lib);
}

static int _cffi_const_VX_KERNEL_HARRIS_CORNERS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_HARRIS_CORNERS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_HARRIS_CORNERS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_WARP_PERSPECTIVE(lib);
}

static int _cffi_const_VX_KERNEL_FAST_CORNERS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_FAST_CORNERS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_FAST_CORNERS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_HARRIS_CORNERS(lib);
}

static int _cffi_const_VX_KERNEL_OPTICAL_FLOW_PYR_LK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_OPTICAL_FLOW_PYR_LK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_OPTICAL_FLOW_PYR_LK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_FAST_CORNERS(lib);
}

static int _cffi_const_VX_KERNEL_REMAP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_REMAP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_REMAP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_OPTICAL_FLOW_PYR_LK(lib);
}

static int _cffi_const_VX_KERNEL_HALFSCALE_GAUSSIAN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_HALFSCALE_GAUSSIAN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_HALFSCALE_GAUSSIAN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_REMAP(lib);
}

static int _cffi_const_VX_KERNEL_MAX_1_0(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_KERNEL_MAX_1_0);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_KERNEL_MAX_1_0", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_HALFSCALE_GAUSSIAN(lib);
}

static int _cffi_e_enum_vx_library_e(PyObject *lib)
{
  if ((VX_LIBRARY_KHR_BASE) < 0 || (unsigned long)(VX_LIBRARY_KHR_BASE) != 0UL) {
    char buf[64];
    if ((VX_LIBRARY_KHR_BASE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_LIBRARY_KHR_BASE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_LIBRARY_KHR_BASE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_library_e", "VX_LIBRARY_KHR_BASE", buf, "0");
    return -1;
  }
  return _cffi_e_enum_vx_enum_e(lib);
}

static int _cffi_const_VX_LUT_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_LUT_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_LUT_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_KERNEL_MAX_1_0(lib);
}

static int _cffi_const_VX_LUT_ATTRIBUTE_COUNT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_LUT_ATTRIBUTE_COUNT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_LUT_ATTRIBUTE_COUNT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_LUT_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_LUT_ATTRIBUTE_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_LUT_ATTRIBUTE_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_LUT_ATTRIBUTE_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_LUT_ATTRIBUTE_COUNT(lib);
}

static int _cffi_const_VX_MATRIX_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MATRIX_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MATRIX_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_LUT_ATTRIBUTE_SIZE(lib);
}

static int _cffi_const_VX_MATRIX_ATTRIBUTE_ROWS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MATRIX_ATTRIBUTE_ROWS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MATRIX_ATTRIBUTE_ROWS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MATRIX_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_MATRIX_ATTRIBUTE_COLUMNS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MATRIX_ATTRIBUTE_COLUMNS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MATRIX_ATTRIBUTE_COLUMNS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MATRIX_ATTRIBUTE_ROWS(lib);
}

static int _cffi_const_VX_MATRIX_ATTRIBUTE_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MATRIX_ATTRIBUTE_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MATRIX_ATTRIBUTE_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MATRIX_ATTRIBUTE_COLUMNS(lib);
}

static int _cffi_const_VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MATRIX_ATTRIBUTE_SIZE(lib);
}

static int _cffi_const_VX_NODE_ATTRIBUTE_STATUS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NODE_ATTRIBUTE_STATUS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NODE_ATTRIBUTE_STATUS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_META_FORMAT_ATTRIBUTE_DELTA_RECTANGLE(lib);
}

static int _cffi_const_VX_NODE_ATTRIBUTE_PERFORMANCE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NODE_ATTRIBUTE_PERFORMANCE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NODE_ATTRIBUTE_PERFORMANCE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NODE_ATTRIBUTE_STATUS(lib);
}

static int _cffi_const_VX_NODE_ATTRIBUTE_BORDER_MODE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NODE_ATTRIBUTE_BORDER_MODE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NODE_ATTRIBUTE_BORDER_MODE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NODE_ATTRIBUTE_PERFORMANCE(lib);
}

static int _cffi_const_VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NODE_ATTRIBUTE_BORDER_MODE(lib);
}

static int _cffi_const_VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NODE_ATTRIBUTE_LOCAL_DATA_SIZE(lib);
}

static int _cffi_const_VX_NORM_L1(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NORM_L1);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NORM_L1", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NODE_ATTRIBUTE_LOCAL_DATA_PTR(lib);
}

static int _cffi_const_VX_NORM_L2(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_NORM_L2);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_NORM_L2", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NORM_L1(lib);
}

static int _cffi_const_VX_PARAMETER_ATTRIBUTE_INDEX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_ATTRIBUTE_INDEX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_ATTRIBUTE_INDEX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_NORM_L2(lib);
}

static int _cffi_const_VX_PARAMETER_ATTRIBUTE_DIRECTION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_ATTRIBUTE_DIRECTION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_ATTRIBUTE_DIRECTION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_ATTRIBUTE_INDEX(lib);
}

static int _cffi_const_VX_PARAMETER_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_ATTRIBUTE_DIRECTION(lib);
}

static int _cffi_const_VX_PARAMETER_ATTRIBUTE_STATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_ATTRIBUTE_STATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_ATTRIBUTE_STATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_PARAMETER_ATTRIBUTE_REF(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_ATTRIBUTE_REF);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_ATTRIBUTE_REF", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_ATTRIBUTE_STATE(lib);
}

static int _cffi_const_VX_PARAMETER_STATE_REQUIRED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_STATE_REQUIRED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_STATE_REQUIRED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_ATTRIBUTE_REF(lib);
}

static int _cffi_const_VX_PARAMETER_STATE_OPTIONAL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PARAMETER_STATE_OPTIONAL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PARAMETER_STATE_OPTIONAL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_STATE_REQUIRED(lib);
}

static int _cffi_const_VX_PYRAMID_ATTRIBUTE_LEVELS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PYRAMID_ATTRIBUTE_LEVELS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PYRAMID_ATTRIBUTE_LEVELS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PARAMETER_STATE_OPTIONAL(lib);
}

static int _cffi_const_VX_PYRAMID_ATTRIBUTE_SCALE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PYRAMID_ATTRIBUTE_SCALE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PYRAMID_ATTRIBUTE_SCALE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PYRAMID_ATTRIBUTE_LEVELS(lib);
}

static int _cffi_const_VX_PYRAMID_ATTRIBUTE_WIDTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PYRAMID_ATTRIBUTE_WIDTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PYRAMID_ATTRIBUTE_WIDTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PYRAMID_ATTRIBUTE_SCALE(lib);
}

static int _cffi_const_VX_PYRAMID_ATTRIBUTE_HEIGHT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PYRAMID_ATTRIBUTE_HEIGHT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PYRAMID_ATTRIBUTE_HEIGHT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PYRAMID_ATTRIBUTE_WIDTH(lib);
}

static int _cffi_const_VX_PYRAMID_ATTRIBUTE_FORMAT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_PYRAMID_ATTRIBUTE_FORMAT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_PYRAMID_ATTRIBUTE_FORMAT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PYRAMID_ATTRIBUTE_HEIGHT(lib);
}

static int _cffi_const_VX_REF_ATTRIBUTE_COUNT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REF_ATTRIBUTE_COUNT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REF_ATTRIBUTE_COUNT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_PYRAMID_ATTRIBUTE_FORMAT(lib);
}

static int _cffi_const_VX_REF_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REF_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REF_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REF_ATTRIBUTE_COUNT(lib);
}

static int _cffi_const_VX_REMAP_ATTRIBUTE_SOURCE_WIDTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REMAP_ATTRIBUTE_SOURCE_WIDTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REMAP_ATTRIBUTE_SOURCE_WIDTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REF_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REMAP_ATTRIBUTE_SOURCE_WIDTH(lib);
}

static int _cffi_const_VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REMAP_ATTRIBUTE_SOURCE_HEIGHT(lib);
}

static int _cffi_const_VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REMAP_ATTRIBUTE_DESTINATION_WIDTH(lib);
}

static int _cffi_const_VX_ROUND_POLICY_TO_ZERO(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ROUND_POLICY_TO_ZERO);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ROUND_POLICY_TO_ZERO", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_REMAP_ATTRIBUTE_DESTINATION_HEIGHT(lib);
}

static int _cffi_const_VX_ROUND_POLICY_TO_NEAREST_EVEN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_ROUND_POLICY_TO_NEAREST_EVEN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_ROUND_POLICY_TO_NEAREST_EVEN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ROUND_POLICY_TO_ZERO(lib);
}

static int _cffi_const_VX_SCALAR_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_SCALAR_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_SCALAR_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_ROUND_POLICY_TO_NEAREST_EVEN(lib);
}

static int _cffi_e_enum_vx_status_e(PyObject *lib)
{
  if ((VX_STATUS_MIN) >= 0 || (long)(VX_STATUS_MIN) != -25L) {
    char buf[64];
    if ((VX_STATUS_MIN) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_STATUS_MIN));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_STATUS_MIN));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_STATUS_MIN", buf, "-25");
    return -1;
  }
  if ((VX_ERROR_REFERENCE_NONZERO) >= 0 || (long)(VX_ERROR_REFERENCE_NONZERO) != -24L) {
    char buf[64];
    if ((VX_ERROR_REFERENCE_NONZERO) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_REFERENCE_NONZERO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_REFERENCE_NONZERO));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_REFERENCE_NONZERO", buf, "-24");
    return -1;
  }
  if ((VX_ERROR_MULTIPLE_WRITERS) >= 0 || (long)(VX_ERROR_MULTIPLE_WRITERS) != -23L) {
    char buf[64];
    if ((VX_ERROR_MULTIPLE_WRITERS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_MULTIPLE_WRITERS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_MULTIPLE_WRITERS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_MULTIPLE_WRITERS", buf, "-23");
    return -1;
  }
  if ((VX_ERROR_GRAPH_ABANDONED) >= 0 || (long)(VX_ERROR_GRAPH_ABANDONED) != -22L) {
    char buf[64];
    if ((VX_ERROR_GRAPH_ABANDONED) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_GRAPH_ABANDONED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_GRAPH_ABANDONED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_GRAPH_ABANDONED", buf, "-22");
    return -1;
  }
  if ((VX_ERROR_GRAPH_SCHEDULED) >= 0 || (long)(VX_ERROR_GRAPH_SCHEDULED) != -21L) {
    char buf[64];
    if ((VX_ERROR_GRAPH_SCHEDULED) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_GRAPH_SCHEDULED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_GRAPH_SCHEDULED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_GRAPH_SCHEDULED", buf, "-21");
    return -1;
  }
  if ((VX_ERROR_INVALID_SCOPE) >= 0 || (long)(VX_ERROR_INVALID_SCOPE) != -20L) {
    char buf[64];
    if ((VX_ERROR_INVALID_SCOPE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_SCOPE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_SCOPE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_SCOPE", buf, "-20");
    return -1;
  }
  if ((VX_ERROR_INVALID_NODE) >= 0 || (long)(VX_ERROR_INVALID_NODE) != -19L) {
    char buf[64];
    if ((VX_ERROR_INVALID_NODE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_NODE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_NODE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_NODE", buf, "-19");
    return -1;
  }
  if ((VX_ERROR_INVALID_GRAPH) >= 0 || (long)(VX_ERROR_INVALID_GRAPH) != -18L) {
    char buf[64];
    if ((VX_ERROR_INVALID_GRAPH) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_GRAPH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_GRAPH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_GRAPH", buf, "-18");
    return -1;
  }
  if ((VX_ERROR_INVALID_TYPE) >= 0 || (long)(VX_ERROR_INVALID_TYPE) != -17L) {
    char buf[64];
    if ((VX_ERROR_INVALID_TYPE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_TYPE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_TYPE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_TYPE", buf, "-17");
    return -1;
  }
  if ((VX_ERROR_INVALID_VALUE) >= 0 || (long)(VX_ERROR_INVALID_VALUE) != -16L) {
    char buf[64];
    if ((VX_ERROR_INVALID_VALUE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_VALUE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_VALUE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_VALUE", buf, "-16");
    return -1;
  }
  if ((VX_ERROR_INVALID_DIMENSION) >= 0 || (long)(VX_ERROR_INVALID_DIMENSION) != -15L) {
    char buf[64];
    if ((VX_ERROR_INVALID_DIMENSION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_DIMENSION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_DIMENSION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_DIMENSION", buf, "-15");
    return -1;
  }
  if ((VX_ERROR_INVALID_FORMAT) >= 0 || (long)(VX_ERROR_INVALID_FORMAT) != -14L) {
    char buf[64];
    if ((VX_ERROR_INVALID_FORMAT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_FORMAT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_FORMAT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_FORMAT", buf, "-14");
    return -1;
  }
  if ((VX_ERROR_INVALID_LINK) >= 0 || (long)(VX_ERROR_INVALID_LINK) != -13L) {
    char buf[64];
    if ((VX_ERROR_INVALID_LINK) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_LINK));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_LINK));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_LINK", buf, "-13");
    return -1;
  }
  if ((VX_ERROR_INVALID_REFERENCE) >= 0 || (long)(VX_ERROR_INVALID_REFERENCE) != -12L) {
    char buf[64];
    if ((VX_ERROR_INVALID_REFERENCE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_REFERENCE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_REFERENCE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_REFERENCE", buf, "-12");
    return -1;
  }
  if ((VX_ERROR_INVALID_MODULE) >= 0 || (long)(VX_ERROR_INVALID_MODULE) != -11L) {
    char buf[64];
    if ((VX_ERROR_INVALID_MODULE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_MODULE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_MODULE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_MODULE", buf, "-11");
    return -1;
  }
  if ((VX_ERROR_INVALID_PARAMETERS) >= 0 || (long)(VX_ERROR_INVALID_PARAMETERS) != -10L) {
    char buf[64];
    if ((VX_ERROR_INVALID_PARAMETERS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_INVALID_PARAMETERS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_INVALID_PARAMETERS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_INVALID_PARAMETERS", buf, "-10");
    return -1;
  }
  if ((VX_ERROR_OPTIMIZED_AWAY) >= 0 || (long)(VX_ERROR_OPTIMIZED_AWAY) != -9L) {
    char buf[64];
    if ((VX_ERROR_OPTIMIZED_AWAY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_OPTIMIZED_AWAY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_OPTIMIZED_AWAY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_OPTIMIZED_AWAY", buf, "-9");
    return -1;
  }
  if ((VX_ERROR_NO_MEMORY) >= 0 || (long)(VX_ERROR_NO_MEMORY) != -8L) {
    char buf[64];
    if ((VX_ERROR_NO_MEMORY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NO_MEMORY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NO_MEMORY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NO_MEMORY", buf, "-8");
    return -1;
  }
  if ((VX_ERROR_NO_RESOURCES) >= 0 || (long)(VX_ERROR_NO_RESOURCES) != -7L) {
    char buf[64];
    if ((VX_ERROR_NO_RESOURCES) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NO_RESOURCES));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NO_RESOURCES));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NO_RESOURCES", buf, "-7");
    return -1;
  }
  if ((VX_ERROR_NOT_COMPATIBLE) >= 0 || (long)(VX_ERROR_NOT_COMPATIBLE) != -6L) {
    char buf[64];
    if ((VX_ERROR_NOT_COMPATIBLE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NOT_COMPATIBLE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NOT_COMPATIBLE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NOT_COMPATIBLE", buf, "-6");
    return -1;
  }
  if ((VX_ERROR_NOT_ALLOCATED) >= 0 || (long)(VX_ERROR_NOT_ALLOCATED) != -5L) {
    char buf[64];
    if ((VX_ERROR_NOT_ALLOCATED) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NOT_ALLOCATED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NOT_ALLOCATED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NOT_ALLOCATED", buf, "-5");
    return -1;
  }
  if ((VX_ERROR_NOT_SUFFICIENT) >= 0 || (long)(VX_ERROR_NOT_SUFFICIENT) != -4L) {
    char buf[64];
    if ((VX_ERROR_NOT_SUFFICIENT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NOT_SUFFICIENT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NOT_SUFFICIENT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NOT_SUFFICIENT", buf, "-4");
    return -1;
  }
  if ((VX_ERROR_NOT_SUPPORTED) >= 0 || (long)(VX_ERROR_NOT_SUPPORTED) != -3L) {
    char buf[64];
    if ((VX_ERROR_NOT_SUPPORTED) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NOT_SUPPORTED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NOT_SUPPORTED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NOT_SUPPORTED", buf, "-3");
    return -1;
  }
  if ((VX_ERROR_NOT_IMPLEMENTED) >= 0 || (long)(VX_ERROR_NOT_IMPLEMENTED) != -2L) {
    char buf[64];
    if ((VX_ERROR_NOT_IMPLEMENTED) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ERROR_NOT_IMPLEMENTED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ERROR_NOT_IMPLEMENTED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_ERROR_NOT_IMPLEMENTED", buf, "-2");
    return -1;
  }
  if ((VX_FAILURE) >= 0 || (long)(VX_FAILURE) != -1L) {
    char buf[64];
    if ((VX_FAILURE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_FAILURE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_FAILURE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_FAILURE", buf, "-1");
    return -1;
  }
  if ((VX_SUCCESS) < 0 || (unsigned long)(VX_SUCCESS) != 0UL) {
    char buf[64];
    if ((VX_SUCCESS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_SUCCESS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_SUCCESS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_status_e", "VX_SUCCESS", buf, "0");
    return -1;
  }
  return _cffi_e_enum_vx_library_e(lib);
}

static int _cffi_const_VX_TERM_CRITERIA_ITERATIONS(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_TERM_CRITERIA_ITERATIONS);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_TERM_CRITERIA_ITERATIONS", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_SCALAR_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_TERM_CRITERIA_EPSILON(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_TERM_CRITERIA_EPSILON);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_TERM_CRITERIA_EPSILON", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_TERM_CRITERIA_ITERATIONS(lib);
}

static int _cffi_const_VX_TERM_CRITERIA_BOTH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_TERM_CRITERIA_BOTH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_TERM_CRITERIA_BOTH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_TERM_CRITERIA_EPSILON(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_TYPE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_TYPE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_TYPE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_TERM_CRITERIA_BOTH(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_TYPE(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_VALUE(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_LOWER(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_THRESHOLD_UPPER(lib);
}

static int _cffi_const_VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_TRUE_VALUE(lib);
}

static int _cffi_const_VX_THRESHOLD_TYPE_BINARY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_TYPE_BINARY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_TYPE_BINARY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_ATTRIBUTE_FALSE_VALUE(lib);
}

static int _cffi_const_VX_THRESHOLD_TYPE_RANGE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_THRESHOLD_TYPE_RANGE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_THRESHOLD_TYPE_RANGE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_THRESHOLD_TYPE_BINARY(lib);
}

static int _cffi_e_enum_vx_type_e(PyObject *lib)
{
  if ((VX_TYPE_INVALID) < 0 || (unsigned long)(VX_TYPE_INVALID) != 0UL) {
    char buf[64];
    if ((VX_TYPE_INVALID) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_INVALID));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_INVALID));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_INVALID", buf, "0");
    return -1;
  }
  if ((VX_TYPE_CHAR) < 0 || (unsigned long)(VX_TYPE_CHAR) != 1UL) {
    char buf[64];
    if ((VX_TYPE_CHAR) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_CHAR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_CHAR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_CHAR", buf, "1");
    return -1;
  }
  if ((VX_TYPE_INT8) < 0 || (unsigned long)(VX_TYPE_INT8) != 2UL) {
    char buf[64];
    if ((VX_TYPE_INT8) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_INT8));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_INT8));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_INT8", buf, "2");
    return -1;
  }
  if ((VX_TYPE_UINT8) < 0 || (unsigned long)(VX_TYPE_UINT8) != 3UL) {
    char buf[64];
    if ((VX_TYPE_UINT8) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_UINT8));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_UINT8));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_UINT8", buf, "3");
    return -1;
  }
  if ((VX_TYPE_INT16) < 0 || (unsigned long)(VX_TYPE_INT16) != 4UL) {
    char buf[64];
    if ((VX_TYPE_INT16) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_INT16));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_INT16));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_INT16", buf, "4");
    return -1;
  }
  if ((VX_TYPE_UINT16) < 0 || (unsigned long)(VX_TYPE_UINT16) != 5UL) {
    char buf[64];
    if ((VX_TYPE_UINT16) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_UINT16));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_UINT16));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_UINT16", buf, "5");
    return -1;
  }
  if ((VX_TYPE_INT32) < 0 || (unsigned long)(VX_TYPE_INT32) != 6UL) {
    char buf[64];
    if ((VX_TYPE_INT32) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_INT32));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_INT32));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_INT32", buf, "6");
    return -1;
  }
  if ((VX_TYPE_UINT32) < 0 || (unsigned long)(VX_TYPE_UINT32) != 7UL) {
    char buf[64];
    if ((VX_TYPE_UINT32) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_UINT32));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_UINT32));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_UINT32", buf, "7");
    return -1;
  }
  if ((VX_TYPE_INT64) < 0 || (unsigned long)(VX_TYPE_INT64) != 8UL) {
    char buf[64];
    if ((VX_TYPE_INT64) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_INT64));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_INT64));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_INT64", buf, "8");
    return -1;
  }
  if ((VX_TYPE_UINT64) < 0 || (unsigned long)(VX_TYPE_UINT64) != 9UL) {
    char buf[64];
    if ((VX_TYPE_UINT64) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_UINT64));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_UINT64));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_UINT64", buf, "9");
    return -1;
  }
  if ((VX_TYPE_FLOAT32) < 0 || (unsigned long)(VX_TYPE_FLOAT32) != 10UL) {
    char buf[64];
    if ((VX_TYPE_FLOAT32) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_FLOAT32));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_FLOAT32));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_FLOAT32", buf, "10");
    return -1;
  }
  if ((VX_TYPE_FLOAT64) < 0 || (unsigned long)(VX_TYPE_FLOAT64) != 11UL) {
    char buf[64];
    if ((VX_TYPE_FLOAT64) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_FLOAT64));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_FLOAT64));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_FLOAT64", buf, "11");
    return -1;
  }
  if ((VX_TYPE_ENUM) < 0 || (unsigned long)(VX_TYPE_ENUM) != 12UL) {
    char buf[64];
    if ((VX_TYPE_ENUM) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_ENUM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_ENUM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_ENUM", buf, "12");
    return -1;
  }
  if ((VX_TYPE_SIZE) < 0 || (unsigned long)(VX_TYPE_SIZE) != 13UL) {
    char buf[64];
    if ((VX_TYPE_SIZE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_SIZE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_SIZE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_SIZE", buf, "13");
    return -1;
  }
  if ((VX_TYPE_DF_IMAGE) < 0 || (unsigned long)(VX_TYPE_DF_IMAGE) != 14UL) {
    char buf[64];
    if ((VX_TYPE_DF_IMAGE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_DF_IMAGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_DF_IMAGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_DF_IMAGE", buf, "14");
    return -1;
  }
  if ((VX_TYPE_BOOL) < 0 || (unsigned long)(VX_TYPE_BOOL) != 16UL) {
    char buf[64];
    if ((VX_TYPE_BOOL) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_BOOL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_BOOL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_BOOL", buf, "16");
    return -1;
  }
  if ((VX_TYPE_SCALAR_MAX) < 0 || (unsigned long)(VX_TYPE_SCALAR_MAX) != 17UL) {
    char buf[64];
    if ((VX_TYPE_SCALAR_MAX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_SCALAR_MAX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_SCALAR_MAX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_SCALAR_MAX", buf, "17");
    return -1;
  }
  if ((VX_TYPE_RECTANGLE) < 0 || (unsigned long)(VX_TYPE_RECTANGLE) != 32UL) {
    char buf[64];
    if ((VX_TYPE_RECTANGLE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_RECTANGLE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_RECTANGLE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_RECTANGLE", buf, "32");
    return -1;
  }
  if ((VX_TYPE_KEYPOINT) < 0 || (unsigned long)(VX_TYPE_KEYPOINT) != 33UL) {
    char buf[64];
    if ((VX_TYPE_KEYPOINT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_KEYPOINT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_KEYPOINT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_KEYPOINT", buf, "33");
    return -1;
  }
  if ((VX_TYPE_COORDINATES2D) < 0 || (unsigned long)(VX_TYPE_COORDINATES2D) != 34UL) {
    char buf[64];
    if ((VX_TYPE_COORDINATES2D) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_COORDINATES2D));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_COORDINATES2D));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_COORDINATES2D", buf, "34");
    return -1;
  }
  if ((VX_TYPE_COORDINATES3D) < 0 || (unsigned long)(VX_TYPE_COORDINATES3D) != 35UL) {
    char buf[64];
    if ((VX_TYPE_COORDINATES3D) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_COORDINATES3D));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_COORDINATES3D));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_COORDINATES3D", buf, "35");
    return -1;
  }
  if ((VX_TYPE_STRUCT_MAX) < 0 || (unsigned long)(VX_TYPE_STRUCT_MAX) != 36UL) {
    char buf[64];
    if ((VX_TYPE_STRUCT_MAX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_STRUCT_MAX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_STRUCT_MAX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_STRUCT_MAX", buf, "36");
    return -1;
  }
  if ((VX_TYPE_USER_STRUCT_START) < 0 || (unsigned long)(VX_TYPE_USER_STRUCT_START) != 256UL) {
    char buf[64];
    if ((VX_TYPE_USER_STRUCT_START) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_USER_STRUCT_START));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_USER_STRUCT_START));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_USER_STRUCT_START", buf, "256");
    return -1;
  }
  if ((VX_TYPE_REFERENCE) < 0 || (unsigned long)(VX_TYPE_REFERENCE) != 2048UL) {
    char buf[64];
    if ((VX_TYPE_REFERENCE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_REFERENCE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_REFERENCE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_REFERENCE", buf, "2048");
    return -1;
  }
  if ((VX_TYPE_CONTEXT) < 0 || (unsigned long)(VX_TYPE_CONTEXT) != 2049UL) {
    char buf[64];
    if ((VX_TYPE_CONTEXT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_CONTEXT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_CONTEXT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_CONTEXT", buf, "2049");
    return -1;
  }
  if ((VX_TYPE_GRAPH) < 0 || (unsigned long)(VX_TYPE_GRAPH) != 2050UL) {
    char buf[64];
    if ((VX_TYPE_GRAPH) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_GRAPH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_GRAPH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_GRAPH", buf, "2050");
    return -1;
  }
  if ((VX_TYPE_NODE) < 0 || (unsigned long)(VX_TYPE_NODE) != 2051UL) {
    char buf[64];
    if ((VX_TYPE_NODE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_NODE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_NODE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_NODE", buf, "2051");
    return -1;
  }
  if ((VX_TYPE_KERNEL) < 0 || (unsigned long)(VX_TYPE_KERNEL) != 2052UL) {
    char buf[64];
    if ((VX_TYPE_KERNEL) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_KERNEL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_KERNEL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_KERNEL", buf, "2052");
    return -1;
  }
  if ((VX_TYPE_PARAMETER) < 0 || (unsigned long)(VX_TYPE_PARAMETER) != 2053UL) {
    char buf[64];
    if ((VX_TYPE_PARAMETER) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_PARAMETER));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_PARAMETER));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_PARAMETER", buf, "2053");
    return -1;
  }
  if ((VX_TYPE_DELAY) < 0 || (unsigned long)(VX_TYPE_DELAY) != 2054UL) {
    char buf[64];
    if ((VX_TYPE_DELAY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_DELAY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_DELAY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_DELAY", buf, "2054");
    return -1;
  }
  if ((VX_TYPE_LUT) < 0 || (unsigned long)(VX_TYPE_LUT) != 2055UL) {
    char buf[64];
    if ((VX_TYPE_LUT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_LUT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_LUT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_LUT", buf, "2055");
    return -1;
  }
  if ((VX_TYPE_DISTRIBUTION) < 0 || (unsigned long)(VX_TYPE_DISTRIBUTION) != 2056UL) {
    char buf[64];
    if ((VX_TYPE_DISTRIBUTION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_DISTRIBUTION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_DISTRIBUTION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_DISTRIBUTION", buf, "2056");
    return -1;
  }
  if ((VX_TYPE_PYRAMID) < 0 || (unsigned long)(VX_TYPE_PYRAMID) != 2057UL) {
    char buf[64];
    if ((VX_TYPE_PYRAMID) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_PYRAMID));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_PYRAMID));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_PYRAMID", buf, "2057");
    return -1;
  }
  if ((VX_TYPE_THRESHOLD) < 0 || (unsigned long)(VX_TYPE_THRESHOLD) != 2058UL) {
    char buf[64];
    if ((VX_TYPE_THRESHOLD) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_THRESHOLD));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_THRESHOLD));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_THRESHOLD", buf, "2058");
    return -1;
  }
  if ((VX_TYPE_MATRIX) < 0 || (unsigned long)(VX_TYPE_MATRIX) != 2059UL) {
    char buf[64];
    if ((VX_TYPE_MATRIX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_MATRIX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_MATRIX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_MATRIX", buf, "2059");
    return -1;
  }
  if ((VX_TYPE_CONVOLUTION) < 0 || (unsigned long)(VX_TYPE_CONVOLUTION) != 2060UL) {
    char buf[64];
    if ((VX_TYPE_CONVOLUTION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_CONVOLUTION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_CONVOLUTION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_CONVOLUTION", buf, "2060");
    return -1;
  }
  if ((VX_TYPE_SCALAR) < 0 || (unsigned long)(VX_TYPE_SCALAR) != 2061UL) {
    char buf[64];
    if ((VX_TYPE_SCALAR) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_SCALAR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_SCALAR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_SCALAR", buf, "2061");
    return -1;
  }
  if ((VX_TYPE_ARRAY) < 0 || (unsigned long)(VX_TYPE_ARRAY) != 2062UL) {
    char buf[64];
    if ((VX_TYPE_ARRAY) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_ARRAY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_ARRAY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_ARRAY", buf, "2062");
    return -1;
  }
  if ((VX_TYPE_IMAGE) < 0 || (unsigned long)(VX_TYPE_IMAGE) != 2063UL) {
    char buf[64];
    if ((VX_TYPE_IMAGE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_IMAGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_IMAGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_IMAGE", buf, "2063");
    return -1;
  }
  if ((VX_TYPE_REMAP) < 0 || (unsigned long)(VX_TYPE_REMAP) != 2064UL) {
    char buf[64];
    if ((VX_TYPE_REMAP) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_REMAP));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_REMAP));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_REMAP", buf, "2064");
    return -1;
  }
  if ((VX_TYPE_ERROR) < 0 || (unsigned long)(VX_TYPE_ERROR) != 2065UL) {
    char buf[64];
    if ((VX_TYPE_ERROR) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_ERROR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_ERROR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_ERROR", buf, "2065");
    return -1;
  }
  if ((VX_TYPE_META_FORMAT) < 0 || (unsigned long)(VX_TYPE_META_FORMAT) != 2066UL) {
    char buf[64];
    if ((VX_TYPE_META_FORMAT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_META_FORMAT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_META_FORMAT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_META_FORMAT", buf, "2066");
    return -1;
  }
  if ((VX_TYPE_OBJECT_MAX) < 0 || (unsigned long)(VX_TYPE_OBJECT_MAX) != 2067UL) {
    char buf[64];
    if ((VX_TYPE_OBJECT_MAX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_TYPE_OBJECT_MAX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_TYPE_OBJECT_MAX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_type_e", "VX_TYPE_OBJECT_MAX", buf, "2067");
    return -1;
  }
  return _cffi_e_enum_vx_status_e(lib);
}

static int _cffi_e_enum_vx_vendor_id_e(PyObject *lib)
{
  if ((VX_ID_KHRONOS) < 0 || (unsigned long)(VX_ID_KHRONOS) != 0UL) {
    char buf[64];
    if ((VX_ID_KHRONOS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_KHRONOS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_KHRONOS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_KHRONOS", buf, "0");
    return -1;
  }
  if ((VX_ID_TI) < 0 || (unsigned long)(VX_ID_TI) != 1UL) {
    char buf[64];
    if ((VX_ID_TI) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_TI));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_TI));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_TI", buf, "1");
    return -1;
  }
  if ((VX_ID_QUALCOMM) < 0 || (unsigned long)(VX_ID_QUALCOMM) != 2UL) {
    char buf[64];
    if ((VX_ID_QUALCOMM) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_QUALCOMM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_QUALCOMM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_QUALCOMM", buf, "2");
    return -1;
  }
  if ((VX_ID_NVIDIA) < 0 || (unsigned long)(VX_ID_NVIDIA) != 3UL) {
    char buf[64];
    if ((VX_ID_NVIDIA) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_NVIDIA));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_NVIDIA));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_NVIDIA", buf, "3");
    return -1;
  }
  if ((VX_ID_ARM) < 0 || (unsigned long)(VX_ID_ARM) != 4UL) {
    char buf[64];
    if ((VX_ID_ARM) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_ARM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_ARM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_ARM", buf, "4");
    return -1;
  }
  if ((VX_ID_BDTI) < 0 || (unsigned long)(VX_ID_BDTI) != 5UL) {
    char buf[64];
    if ((VX_ID_BDTI) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_BDTI));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_BDTI));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_BDTI", buf, "5");
    return -1;
  }
  if ((VX_ID_RENESAS) < 0 || (unsigned long)(VX_ID_RENESAS) != 6UL) {
    char buf[64];
    if ((VX_ID_RENESAS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_RENESAS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_RENESAS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_RENESAS", buf, "6");
    return -1;
  }
  if ((VX_ID_VIVANTE) < 0 || (unsigned long)(VX_ID_VIVANTE) != 7UL) {
    char buf[64];
    if ((VX_ID_VIVANTE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_VIVANTE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_VIVANTE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_VIVANTE", buf, "7");
    return -1;
  }
  if ((VX_ID_XILINX) < 0 || (unsigned long)(VX_ID_XILINX) != 8UL) {
    char buf[64];
    if ((VX_ID_XILINX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_XILINX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_XILINX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_XILINX", buf, "8");
    return -1;
  }
  if ((VX_ID_AXIS) < 0 || (unsigned long)(VX_ID_AXIS) != 9UL) {
    char buf[64];
    if ((VX_ID_AXIS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_AXIS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_AXIS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_AXIS", buf, "9");
    return -1;
  }
  if ((VX_ID_MOVIDIUS) < 0 || (unsigned long)(VX_ID_MOVIDIUS) != 10UL) {
    char buf[64];
    if ((VX_ID_MOVIDIUS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_MOVIDIUS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_MOVIDIUS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_MOVIDIUS", buf, "10");
    return -1;
  }
  if ((VX_ID_SAMSUNG) < 0 || (unsigned long)(VX_ID_SAMSUNG) != 11UL) {
    char buf[64];
    if ((VX_ID_SAMSUNG) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_SAMSUNG));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_SAMSUNG));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_SAMSUNG", buf, "11");
    return -1;
  }
  if ((VX_ID_FREESCALE) < 0 || (unsigned long)(VX_ID_FREESCALE) != 12UL) {
    char buf[64];
    if ((VX_ID_FREESCALE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_FREESCALE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_FREESCALE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_FREESCALE", buf, "12");
    return -1;
  }
  if ((VX_ID_AMD) < 0 || (unsigned long)(VX_ID_AMD) != 13UL) {
    char buf[64];
    if ((VX_ID_AMD) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_AMD));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_AMD));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_AMD", buf, "13");
    return -1;
  }
  if ((VX_ID_BROADCOM) < 0 || (unsigned long)(VX_ID_BROADCOM) != 14UL) {
    char buf[64];
    if ((VX_ID_BROADCOM) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_BROADCOM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_BROADCOM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_BROADCOM", buf, "14");
    return -1;
  }
  if ((VX_ID_INTEL) < 0 || (unsigned long)(VX_ID_INTEL) != 15UL) {
    char buf[64];
    if ((VX_ID_INTEL) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_INTEL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_INTEL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_INTEL", buf, "15");
    return -1;
  }
  if ((VX_ID_MARVELL) < 0 || (unsigned long)(VX_ID_MARVELL) != 16UL) {
    char buf[64];
    if ((VX_ID_MARVELL) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_MARVELL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_MARVELL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_MARVELL", buf, "16");
    return -1;
  }
  if ((VX_ID_MEDIATEK) < 0 || (unsigned long)(VX_ID_MEDIATEK) != 17UL) {
    char buf[64];
    if ((VX_ID_MEDIATEK) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_MEDIATEK));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_MEDIATEK));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_MEDIATEK", buf, "17");
    return -1;
  }
  if ((VX_ID_ST) < 0 || (unsigned long)(VX_ID_ST) != 18UL) {
    char buf[64];
    if ((VX_ID_ST) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_ST));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_ST));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_ST", buf, "18");
    return -1;
  }
  if ((VX_ID_CEVA) < 0 || (unsigned long)(VX_ID_CEVA) != 19UL) {
    char buf[64];
    if ((VX_ID_CEVA) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_CEVA));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_CEVA));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_CEVA", buf, "19");
    return -1;
  }
  if ((VX_ID_ITSEEZ) < 0 || (unsigned long)(VX_ID_ITSEEZ) != 20UL) {
    char buf[64];
    if ((VX_ID_ITSEEZ) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_ITSEEZ));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_ITSEEZ));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_ITSEEZ", buf, "20");
    return -1;
  }
  if ((VX_ID_IMAGINATION) < 0 || (unsigned long)(VX_ID_IMAGINATION) != 21UL) {
    char buf[64];
    if ((VX_ID_IMAGINATION) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_IMAGINATION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_IMAGINATION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_IMAGINATION", buf, "21");
    return -1;
  }
  if ((VX_ID_COGNIVUE) < 0 || (unsigned long)(VX_ID_COGNIVUE) != 22UL) {
    char buf[64];
    if ((VX_ID_COGNIVUE) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_COGNIVUE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_COGNIVUE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_COGNIVUE", buf, "22");
    return -1;
  }
  if ((VX_ID_VIDEANTIS) < 0 || (unsigned long)(VX_ID_VIDEANTIS) != 23UL) {
    char buf[64];
    if ((VX_ID_VIDEANTIS) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_VIDEANTIS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_VIDEANTIS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_VIDEANTIS", buf, "23");
    return -1;
  }
  if ((VX_ID_MAX) < 0 || (unsigned long)(VX_ID_MAX) != 4095UL) {
    char buf[64];
    if ((VX_ID_MAX) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_MAX));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_MAX));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_MAX", buf, "4095");
    return -1;
  }
  if ((VX_ID_DEFAULT) < 0 || (unsigned long)(VX_ID_DEFAULT) != 4095UL) {
    char buf[64];
    if ((VX_ID_DEFAULT) < 0)
        snprintf(buf, 63, "%ld", (long)(VX_ID_DEFAULT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(VX_ID_DEFAULT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "vx_vendor_id_e", "VX_ID_DEFAULT", buf, "4095");
    return -1;
  }
  return _cffi_e_enum_vx_type_e(lib);
}

static int _cffi_const_VX_MAX_IMPLEMENTATION_NAME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MAX_IMPLEMENTATION_NAME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MAX_IMPLEMENTATION_NAME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_e_enum_vx_vendor_id_e(lib);
}

static int _cffi_const_VX_MAX_KERNEL_NAME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MAX_KERNEL_NAME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MAX_KERNEL_NAME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MAX_IMPLEMENTATION_NAME(lib);
}

static int _cffi_const_VX_MAX_LOG_MESSAGE_LEN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_MAX_LOG_MESSAGE_LEN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_MAX_LOG_MESSAGE_LEN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MAX_KERNEL_NAME(lib);
}

static int _cffi_const_VX_SCALE_UNITY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_SCALE_UNITY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_SCALE_UNITY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_MAX_LOG_MESSAGE_LEN(lib);
}

static int _cffi_const_VX_VERSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_VERSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_VERSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_SCALE_UNITY(lib);
}

static int _cffi_const_VX_VERSION_1_0(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(VX_VERSION_1_0);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "VX_VERSION_1_0", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_VX_VERSION(lib);
}

static void _cffi_check_struct__vx_border_mode_t(struct _vx_border_mode_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->mode) << 1);
  (void)((p->constant_value) << 1);
}
static PyObject *
_cffi_layout_struct__vx_border_mode_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_border_mode_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_border_mode_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_border_mode_t, mode),
    sizeof(((struct _vx_border_mode_t *)0)->mode),
    offsetof(struct _vx_border_mode_t, constant_value),
    sizeof(((struct _vx_border_mode_t *)0)->constant_value),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_border_mode_t(0);
}

static void _cffi_check_struct__vx_coordinates2d_t(struct _vx_coordinates2d_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->x) << 1);
  (void)((p->y) << 1);
}
static PyObject *
_cffi_layout_struct__vx_coordinates2d_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_coordinates2d_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_coordinates2d_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_coordinates2d_t, x),
    sizeof(((struct _vx_coordinates2d_t *)0)->x),
    offsetof(struct _vx_coordinates2d_t, y),
    sizeof(((struct _vx_coordinates2d_t *)0)->y),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_coordinates2d_t(0);
}

static void _cffi_check_struct__vx_coordinates3d_t(struct _vx_coordinates3d_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->x) << 1);
  (void)((p->y) << 1);
  (void)((p->z) << 1);
}
static PyObject *
_cffi_layout_struct__vx_coordinates3d_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_coordinates3d_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_coordinates3d_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_coordinates3d_t, x),
    sizeof(((struct _vx_coordinates3d_t *)0)->x),
    offsetof(struct _vx_coordinates3d_t, y),
    sizeof(((struct _vx_coordinates3d_t *)0)->y),
    offsetof(struct _vx_coordinates3d_t, z),
    sizeof(((struct _vx_coordinates3d_t *)0)->z),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_coordinates3d_t(0);
}

static void _cffi_check_struct__vx_delta_rectangle_t(struct _vx_delta_rectangle_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->delta_start_x) << 1);
  (void)((p->delta_start_y) << 1);
  (void)((p->delta_end_x) << 1);
  (void)((p->delta_end_y) << 1);
}
static PyObject *
_cffi_layout_struct__vx_delta_rectangle_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_delta_rectangle_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_delta_rectangle_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_delta_rectangle_t, delta_start_x),
    sizeof(((struct _vx_delta_rectangle_t *)0)->delta_start_x),
    offsetof(struct _vx_delta_rectangle_t, delta_start_y),
    sizeof(((struct _vx_delta_rectangle_t *)0)->delta_start_y),
    offsetof(struct _vx_delta_rectangle_t, delta_end_x),
    sizeof(((struct _vx_delta_rectangle_t *)0)->delta_end_x),
    offsetof(struct _vx_delta_rectangle_t, delta_end_y),
    sizeof(((struct _vx_delta_rectangle_t *)0)->delta_end_y),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_delta_rectangle_t(0);
}

static void _cffi_check_struct__vx_imagepatch_addressing_t(struct _vx_imagepatch_addressing_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->dim_x) << 1);
  (void)((p->dim_y) << 1);
  (void)((p->stride_x) << 1);
  (void)((p->stride_y) << 1);
  (void)((p->scale_x) << 1);
  (void)((p->scale_y) << 1);
  (void)((p->step_x) << 1);
  (void)((p->step_y) << 1);
}
static PyObject *
_cffi_layout_struct__vx_imagepatch_addressing_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_imagepatch_addressing_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_imagepatch_addressing_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_imagepatch_addressing_t, dim_x),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->dim_x),
    offsetof(struct _vx_imagepatch_addressing_t, dim_y),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->dim_y),
    offsetof(struct _vx_imagepatch_addressing_t, stride_x),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->stride_x),
    offsetof(struct _vx_imagepatch_addressing_t, stride_y),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->stride_y),
    offsetof(struct _vx_imagepatch_addressing_t, scale_x),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->scale_x),
    offsetof(struct _vx_imagepatch_addressing_t, scale_y),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->scale_y),
    offsetof(struct _vx_imagepatch_addressing_t, step_x),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->step_x),
    offsetof(struct _vx_imagepatch_addressing_t, step_y),
    sizeof(((struct _vx_imagepatch_addressing_t *)0)->step_y),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_imagepatch_addressing_t(0);
}

static void _cffi_check_struct__vx_kernel_info_t(struct _vx_kernel_info_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->enumeration) << 1);
  { char(*tmp)[256] = &p->name; (void)tmp; }
}
static PyObject *
_cffi_layout_struct__vx_kernel_info_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_kernel_info_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_kernel_info_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_kernel_info_t, enumeration),
    sizeof(((struct _vx_kernel_info_t *)0)->enumeration),
    offsetof(struct _vx_kernel_info_t, name),
    sizeof(((struct _vx_kernel_info_t *)0)->name),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_kernel_info_t(0);
}

static void _cffi_check_struct__vx_keypoint_t(struct _vx_keypoint_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->x) << 1);
  (void)((p->y) << 1);
  { float *tmp = &p->strength; (void)tmp; }
  { float *tmp = &p->scale; (void)tmp; }
  { float *tmp = &p->orientation; (void)tmp; }
  (void)((p->tracking_status) << 1);
  { float *tmp = &p->error; (void)tmp; }
}
static PyObject *
_cffi_layout_struct__vx_keypoint_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_keypoint_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_keypoint_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_keypoint_t, x),
    sizeof(((struct _vx_keypoint_t *)0)->x),
    offsetof(struct _vx_keypoint_t, y),
    sizeof(((struct _vx_keypoint_t *)0)->y),
    offsetof(struct _vx_keypoint_t, strength),
    sizeof(((struct _vx_keypoint_t *)0)->strength),
    offsetof(struct _vx_keypoint_t, scale),
    sizeof(((struct _vx_keypoint_t *)0)->scale),
    offsetof(struct _vx_keypoint_t, orientation),
    sizeof(((struct _vx_keypoint_t *)0)->orientation),
    offsetof(struct _vx_keypoint_t, tracking_status),
    sizeof(((struct _vx_keypoint_t *)0)->tracking_status),
    offsetof(struct _vx_keypoint_t, error),
    sizeof(((struct _vx_keypoint_t *)0)->error),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_keypoint_t(0);
}

static void _cffi_check_struct__vx_perf_t(struct _vx_perf_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->tmp) << 1);
  (void)((p->beg) << 1);
  (void)((p->end) << 1);
  (void)((p->sum) << 1);
  (void)((p->avg) << 1);
  (void)((p->min) << 1);
  (void)((p->num) << 1);
}
static PyObject *
_cffi_layout_struct__vx_perf_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_perf_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_perf_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_perf_t, tmp),
    sizeof(((struct _vx_perf_t *)0)->tmp),
    offsetof(struct _vx_perf_t, beg),
    sizeof(((struct _vx_perf_t *)0)->beg),
    offsetof(struct _vx_perf_t, end),
    sizeof(((struct _vx_perf_t *)0)->end),
    offsetof(struct _vx_perf_t, sum),
    sizeof(((struct _vx_perf_t *)0)->sum),
    offsetof(struct _vx_perf_t, avg),
    sizeof(((struct _vx_perf_t *)0)->avg),
    offsetof(struct _vx_perf_t, min),
    sizeof(((struct _vx_perf_t *)0)->min),
    offsetof(struct _vx_perf_t, num),
    sizeof(((struct _vx_perf_t *)0)->num),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_perf_t(0);
}

static void _cffi_check_struct__vx_rectangle_t(struct _vx_rectangle_t *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->start_x) << 1);
  (void)((p->start_y) << 1);
  (void)((p->end_x) << 1);
  (void)((p->end_y) << 1);
}
static PyObject *
_cffi_layout_struct__vx_rectangle_t(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _vx_rectangle_t y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _vx_rectangle_t),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _vx_rectangle_t, start_x),
    sizeof(((struct _vx_rectangle_t *)0)->start_x),
    offsetof(struct _vx_rectangle_t, start_y),
    sizeof(((struct _vx_rectangle_t *)0)->start_y),
    offsetof(struct _vx_rectangle_t, end_x),
    sizeof(((struct _vx_rectangle_t *)0)->end_x),
    offsetof(struct _vx_rectangle_t, end_y),
    sizeof(((struct _vx_rectangle_t *)0)->end_y),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__vx_rectangle_t(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_VX_VERSION_1_0(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout_struct__vx_border_mode_t", _cffi_layout_struct__vx_border_mode_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_coordinates2d_t", _cffi_layout_struct__vx_coordinates2d_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_coordinates3d_t", _cffi_layout_struct__vx_coordinates3d_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_delta_rectangle_t", _cffi_layout_struct__vx_delta_rectangle_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_imagepatch_addressing_t", _cffi_layout_struct__vx_imagepatch_addressing_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_kernel_info_t", _cffi_layout_struct__vx_kernel_info_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_keypoint_t", _cffi_layout_struct__vx_keypoint_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_perf_t", _cffi_layout_struct__vx_perf_t, METH_NOARGS, NULL},
  {"_cffi_layout_struct__vx_rectangle_t", _cffi_layout_struct__vx_rectangle_t, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "__pyvx_inc_vx",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit___pyvx_inc_vx(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (_cffi_const_VX_THRESHOLD_TYPE_RANGE(lib) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init__pyvx_inc_vx(void)
{
  PyObject *lib;
  lib = Py_InitModule("__pyvx_inc_vx", _cffi_methods);
  if (lib == NULL)
    return;
  if (_cffi_const_VX_THRESHOLD_TYPE_RANGE(lib) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
