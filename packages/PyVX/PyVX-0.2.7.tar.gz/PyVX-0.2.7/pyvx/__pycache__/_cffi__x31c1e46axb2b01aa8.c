
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


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>

#include "../avplay.h"

static int libav_initiated = 0;

struct avplay *avplay_new(char *fn) {
    struct avplay *p = calloc(sizeof(struct  avplay), 1);
    if (!libav_initiated) {
        av_register_all();
        avcodec_register_all();
        avdevice_register_all();
        avformat_network_init();
        libav_initiated = 1;
    }

    AVInputFormat   *iFormat = NULL; 
    int v4l = 0;
    if (!strncmp(fn, "v4l2://", 7)) {
        fn += 7;
        v4l = 1;
    } else if (!strncmp(fn, "/dev/video", 10)) {
        v4l = 1;
    }
    if (v4l) {
        const char      formatName[] = "video4linux2";
        if (!(iFormat = av_find_input_format(formatName))) { 
             printf("can't find input format %s\n", formatName); 
             return NULL; 
        }
    } 

    
    p->format_ctx = avformat_alloc_context();
    if (avformat_open_input(&p->format_ctx, fn, iFormat, NULL) != 0) return NULL;
    if (avformat_find_stream_info(p->format_ctx, NULL) < 0) return NULL;
    int i;
    p->video_stream_index = -1;
    for (i=0; i < p->format_ctx->nb_streams; i++) {
        if (p->format_ctx->streams[i]->codec->coder_type == AVMEDIA_TYPE_VIDEO) {
            p->video_stream_index = i;
            break;
        }
    }
    if (p->video_stream_index == -1) return NULL;
    p->codec_ctx = p->format_ctx->streams[p->video_stream_index]->codec;
    p->codec = avcodec_find_decoder(p->codec_ctx->codec_id);
    if (p->codec == NULL) return NULL;
 
    if (avcodec_open2(p->codec_ctx, p->codec,NULL) < 0) return NULL;
#if LIBAVCODEC_VERSION_INT >= AV_VERSION_INT(55,28,1)
    p->frame    = av_frame_alloc();
#else
    p->frame = avcodec_alloc_frame();
#endif

    uint8_t *buffer;
    int numBytes;
 
#ifdef AV_PIX_FMT_RGB24
    enum AVPixelFormat pFormat = AV_PIX_FMT_RGB24;
#else
    enum PixelFormat pFormat = PIX_FMT_RGB24;
#endif

    numBytes = avpicture_get_size(pFormat, p->codec_ctx->width, p->codec_ctx->height);
    buffer = (uint8_t *) av_malloc(numBytes*sizeof(uint8_t));
    if (!buffer) return NULL;

    p->convert_ctx = sws_getCachedContext(NULL, p->codec_ctx->width, 
                                              p->codec_ctx->height, p->codec_ctx->pix_fmt,
                                              p->codec_ctx->width, p->codec_ctx->height, 
                                              pFormat, SWS_BICUBIC, NULL, NULL, NULL);

    p->width = p->codec_ctx->width;
    p->height = p->codec_ctx->height;
    return p;
}

int avplay_next(struct avplay *p, uint8_t *img) {
    while (1) {
        AVPacket packet;
        int frame_ok = av_read_frame(p->format_ctx, &packet);
        if (frame_ok < 0) packet.size = 0;
        if(packet.stream_index == p->video_stream_index) {
            if (packet.size == 54) { // Hack to remove Axis system-timestamps
                uint32_t *data = (uint32_t *) packet.data;
                if (data[4] == 0xAAAAAAAA) continue;
            }
            int frameFinished;
            avcodec_decode_video2(p->codec_ctx, p->frame, &frameFinished, &packet);
            if (frameFinished) {
                p->pts = p->frame->pkt_pts;
                uint8_t *const planes[] = {img};
                const int strides[] = {p->width * 3};
                sws_scale(p->convert_ctx, 
                          (const uint8_t * const *) ((AVPicture*)p->frame)->data, 
                          ((AVPicture*)p->frame)->linesize, 0,
                          p->codec_ctx->height,
                          planes, strides);
                return 0;
            } else if (frame_ok < 0) {
                return -1;
            }
        }
    }
}

void avplay_seek(struct avplay *p, int64_t pts) {
    av_seek_frame(p->format_ctx, p->video_stream_index, pts, 0);
}



static PyObject *
_cffi_f_avplay_new(PyObject *self, PyObject *arg0)
{
  char * x0;
  Py_ssize_t datasize;
  struct avplay * result;

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
  { result = avplay_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(1));
}

static PyObject *
_cffi_f_avplay_next(PyObject *self, PyObject *args)
{
  struct avplay * x0;
  uint8_t * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:avplay_next", &arg0, &arg1))
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
  { result = avplay_next(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static void _cffi_check_struct_avplay(struct avplay *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->width) << 1);
  (void)((p->height) << 1);
}
static PyObject *
_cffi_layout_struct_avplay(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct avplay y; };
  static Py_ssize_t nums[] = {
    sizeof(struct avplay),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct avplay, width),
    sizeof(((struct avplay *)0)->width),
    offsetof(struct avplay, height),
    sizeof(((struct avplay *)0)->height),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_avplay(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return 0;
}

static PyMethodDef _cffi_methods[] = {
  {"avplay_new", _cffi_f_avplay_new, METH_O, NULL},
  {"avplay_next", _cffi_f_avplay_next, METH_VARARGS, NULL},
  {"_cffi_layout_struct_avplay", _cffi_layout_struct_avplay, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x31c1e46axb2b01aa8",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x31c1e46axb2b01aa8(void)
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
init_cffi__x31c1e46axb2b01aa8(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x31c1e46axb2b01aa8", _cffi_methods);
  if (lib == NULL)
    return;
  if (0 < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
