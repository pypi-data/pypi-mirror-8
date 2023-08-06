
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


#include <string.h>
#include "../glview.h"

void glutMainLoopEvent(void);

static int glut_initiated=0;
static struct glview **windows;
static int n_windows=0;
static int escaped_pressed=0;

#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

void keyboard(unsigned char key, int x, int y) {
  if (key == 27) {
    escaped_pressed=1;
  }
}

void reshape(int w, int h) {
  int i = glutGetWindow();
  if (i < n_windows) {
    float scale=min( ((float)w)/((float)(windows[i]->width)), 
                     ((float)h)/((float)(windows[i]->height)) );
    float dx=(w-scale*(windows[i]->width))/2;
    float dy=(h-scale*(windows[i]->height))/2;
    glViewport(dx, dy, scale*windows[i]->width, scale*windows[i]->height);
  }
}



struct glview *glview_create(int width, int height, int pixel_type, int pixel_size, char *name) {
  if (!glut_initiated) {
    int ac=0;
    char *av[]={"pr"};
    glutInit(&ac,av);
    glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE);
    glut_initiated = 1;
  }

  struct glview *m = malloc(sizeof(struct glview));
  m->name = strdup(name);

  int w=width, h=height;
  while (w<600) {w*=2; h*=2;}
  glutInitWindowSize(w,h);
  m->win=glutCreateWindow(m->name);

  n_windows = max(m->win + 1, n_windows);
  windows = realloc(windows, n_windows * sizeof(struct glview *));
  windows[m->win] = m;

  m->width = width;
  m->height = height;
  m->pixel_type = pixel_type;
  m->pixel_size = pixel_size;

  glEnable(GL_TEXTURE_RECTANGLE_NV);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0, 1, 0, 1);

  unsigned int tex;
  glGenTextures(1, &tex);
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, tex);
  glTexParameteri(GL_TEXTURE_RECTANGLE_NV,GL_TEXTURE_MAG_FILTER,GL_NEAREST);
  glTexParameteri(GL_TEXTURE_RECTANGLE_NV,GL_TEXTURE_MIN_FILTER,GL_NEAREST);

  glTexImage2D(
    GL_TEXTURE_RECTANGLE_NV,    /* texture target */
    0,                          /* mipmap level */
    pixel_type,                 /* texture internal format */
    width,                      /* width */
    height,                     /* height */
    0,                          /* border */
    pixel_type,                 /* pixel format of the image */
    pixel_size,                 /* channel type */
    NULL                        /* image data */
    );
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, 0);
  m->tex=tex;
  glutKeyboardFunc(keyboard);
  glutReshapeFunc(reshape); 

  return m;
}

int glview_next(struct glview *m, unsigned char *imageData) {
  glutSetWindow(m->win);
  glBindTexture(GL_TEXTURE_RECTANGLE_NV, m->tex);
  glTexSubImage2D(GL_TEXTURE_RECTANGLE_NV,0,
      0,0,m->width,m->height,
      m->pixel_type, m->pixel_size, imageData);
  glClearColor(0.0, 0.0, 0.0, 1.0);
  glClear(GL_COLOR_BUFFER_BIT);

  glBegin(GL_QUADS);
  {
    glTexCoord2i(0, m->height);        glVertex2i(0, 0);
    glTexCoord2i(m->width, m->height); glVertex2i(1, 0);
    glTexCoord2i(m->width, 0);         glVertex2i(1, 1);
    glTexCoord2i(0, 0);                glVertex2i(0, 1);
  }
  glEnd();

  glutSwapBuffers();

  //glutMainLoop();
  glutMainLoopEvent();
  return escaped_pressed;
}

void glview_release(struct glview *m) {
  free(m);
}


static PyObject *
_cffi_f_glview_create(PyObject *self, PyObject *args)
{
  int x0;
  int x1;
  int x2;
  int x3;
  char * x4;
  Py_ssize_t datasize;
  struct glview * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:glview_create", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(0), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = glview_create(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}

static PyObject *
_cffi_f_glview_next(PyObject *self, PyObject *args)
{
  struct glview * x0;
  unsigned char * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:glview_next", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = glview_next(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_glview_release(PyObject *self, PyObject *arg0)
{
  struct glview * x0;
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
  { glview_release(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static int _cffi_const_GL_RGB(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GL_RGB);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GL_RGB", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return 0;
}

static int _cffi_const_GL_UNSIGNED_BYTE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GL_UNSIGNED_BYTE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GL_UNSIGNED_BYTE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GL_RGB(lib);
}

static void _cffi_check_struct_glview(struct glview *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->width) << 1);
  (void)((p->height) << 1);
}
static PyObject *
_cffi_layout_struct_glview(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct glview y; };
  static Py_ssize_t nums[] = {
    sizeof(struct glview),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct glview, width),
    sizeof(((struct glview *)0)->width),
    offsetof(struct glview, height),
    sizeof(((struct glview *)0)->height),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_glview(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_GL_UNSIGNED_BYTE(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"glview_create", _cffi_f_glview_create, METH_VARARGS, NULL},
  {"glview_next", _cffi_f_glview_next, METH_VARARGS, NULL},
  {"glview_release", _cffi_f_glview_release, METH_O, NULL},
  {"_cffi_layout_struct_glview", _cffi_layout_struct_glview, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x73f4d49ex1798e227",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x73f4d49ex1798e227(void)
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
init_cffi__x73f4d49ex1798e227(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x73f4d49ex1798e227", _cffi_methods);
  if (lib == NULL)
    return;
  if (0 < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
