
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



#include <lzma.h>
#include <stdlib.h>
void _pylzma_stream_init(lzma_stream *strm) {
    lzma_stream tmp = LZMA_STREAM_INIT; // macro from lzma.h
    *strm = tmp;
}

uint32_t _pylzma_block_header_size_decode(uint32_t b) {
    return lzma_block_header_size_decode(b); // macro from lzma.h
}


static void _cffi_check__lzma_allocator(lzma_allocator *p)
{
  /* only to generate compile-time warnings or errors */
  { void *(* *tmp)(void *, size_t, size_t) = &p->alloc; (void)tmp; }
  { void(* *tmp)(void *, void *) = &p->free; (void)tmp; }
  { void * *tmp = &p->opaque; (void)tmp; }
}
static PyObject *
_cffi_layout__lzma_allocator(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_allocator y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_allocator),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_allocator, alloc),
    sizeof(((lzma_allocator *)0)->alloc),
    offsetof(lzma_allocator, free),
    sizeof(((lzma_allocator *)0)->free),
    offsetof(lzma_allocator, opaque),
    sizeof(((lzma_allocator *)0)->opaque),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_allocator(0);
}

static void _cffi_check__lzma_block(lzma_block *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->header_size) << 1);
  (void)((p->check) << 1);
  (void)((p->compressed_size) << 1);
  { lzma_filter * *tmp = &p->filters; (void)tmp; }
}
static PyObject *
_cffi_layout__lzma_block(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_block y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_block),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_block, version),
    sizeof(((lzma_block *)0)->version),
    offsetof(lzma_block, header_size),
    sizeof(((lzma_block *)0)->header_size),
    offsetof(lzma_block, check),
    sizeof(((lzma_block *)0)->check),
    offsetof(lzma_block, compressed_size),
    sizeof(((lzma_block *)0)->compressed_size),
    offsetof(lzma_block, filters),
    sizeof(((lzma_block *)0)->filters),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_block(0);
}

static void _cffi_check__lzma_filter(lzma_filter *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->id) << 1);
  { void * *tmp = &p->options; (void)tmp; }
}
static PyObject *
_cffi_layout__lzma_filter(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_filter y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_filter),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_filter, id),
    sizeof(((lzma_filter *)0)->id),
    offsetof(lzma_filter, options),
    sizeof(((lzma_filter *)0)->options),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_filter(0);
}

static void _cffi_check__lzma_index_iter(lzma_index_iter *p)
{
  /* only to generate compile-time warnings or errors */
  /* cannot generate 'struct $1' in field 'stream': unknown type name */
  /* cannot generate 'struct $2' in field 'block': unknown type name */
}
static PyObject *
_cffi_layout__lzma_index_iter(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_index_iter y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_index_iter),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_index_iter, stream),
    sizeof(((lzma_index_iter *)0)->stream),
    offsetof(lzma_index_iter, block),
    sizeof(((lzma_index_iter *)0)->block),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_index_iter(0);
}

static void _cffi_check__lzma_options_bcj(lzma_options_bcj *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->start_offset) << 1);
}
static PyObject *
_cffi_layout__lzma_options_bcj(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_options_bcj y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_options_bcj),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_options_bcj, start_offset),
    sizeof(((lzma_options_bcj *)0)->start_offset),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_options_bcj(0);
}

static void _cffi_check__lzma_options_delta(lzma_options_delta *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->type) << 1);
  (void)((p->dist) << 1);
}
static PyObject *
_cffi_layout__lzma_options_delta(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_options_delta y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_options_delta),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_options_delta, type),
    sizeof(((lzma_options_delta *)0)->type),
    offsetof(lzma_options_delta, dist),
    sizeof(((lzma_options_delta *)0)->dist),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_options_delta(0);
}

static void _cffi_check__lzma_options_lzma(lzma_options_lzma *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->dict_size) << 1);
  (void)((p->lc) << 1);
  (void)((p->lp) << 1);
  (void)((p->pb) << 1);
  (void)((p->mode) << 1);
  (void)((p->nice_len) << 1);
  (void)((p->mf) << 1);
  (void)((p->depth) << 1);
}
static PyObject *
_cffi_layout__lzma_options_lzma(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_options_lzma y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_options_lzma),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_options_lzma, dict_size),
    sizeof(((lzma_options_lzma *)0)->dict_size),
    offsetof(lzma_options_lzma, lc),
    sizeof(((lzma_options_lzma *)0)->lc),
    offsetof(lzma_options_lzma, lp),
    sizeof(((lzma_options_lzma *)0)->lp),
    offsetof(lzma_options_lzma, pb),
    sizeof(((lzma_options_lzma *)0)->pb),
    offsetof(lzma_options_lzma, mode),
    sizeof(((lzma_options_lzma *)0)->mode),
    offsetof(lzma_options_lzma, nice_len),
    sizeof(((lzma_options_lzma *)0)->nice_len),
    offsetof(lzma_options_lzma, mf),
    sizeof(((lzma_options_lzma *)0)->mf),
    offsetof(lzma_options_lzma, depth),
    sizeof(((lzma_options_lzma *)0)->depth),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_options_lzma(0);
}

static void _cffi_check__lzma_stream(lzma_stream *p)
{
  /* only to generate compile-time warnings or errors */
  { uint8_t const * *tmp = &p->next_in; (void)tmp; }
  (void)((p->avail_in) << 1);
  (void)((p->total_in) << 1);
  { uint8_t * *tmp = &p->next_out; (void)tmp; }
  (void)((p->avail_out) << 1);
  (void)((p->total_out) << 1);
  { lzma_allocator * *tmp = &p->allocator; (void)tmp; }
}
static PyObject *
_cffi_layout__lzma_stream(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_stream y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_stream),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_stream, next_in),
    sizeof(((lzma_stream *)0)->next_in),
    offsetof(lzma_stream, avail_in),
    sizeof(((lzma_stream *)0)->avail_in),
    offsetof(lzma_stream, total_in),
    sizeof(((lzma_stream *)0)->total_in),
    offsetof(lzma_stream, next_out),
    sizeof(((lzma_stream *)0)->next_out),
    offsetof(lzma_stream, avail_out),
    sizeof(((lzma_stream *)0)->avail_out),
    offsetof(lzma_stream, total_out),
    sizeof(((lzma_stream *)0)->total_out),
    offsetof(lzma_stream, allocator),
    sizeof(((lzma_stream *)0)->allocator),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_stream(0);
}

static void _cffi_check__lzma_stream_flags(lzma_stream_flags *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->backward_size) << 1);
  (void)((p->check) << 1);
}
static PyObject *
_cffi_layout__lzma_stream_flags(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; lzma_stream_flags y; };
  static Py_ssize_t nums[] = {
    sizeof(lzma_stream_flags),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(lzma_stream_flags, version),
    sizeof(((lzma_stream_flags *)0)->version),
    offsetof(lzma_stream_flags, backward_size),
    sizeof(((lzma_stream_flags *)0)->backward_size),
    offsetof(lzma_stream_flags, check),
    sizeof(((lzma_stream_flags *)0)->check),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__lzma_stream_flags(0);
}

static int _cffi_const_LZMA_RUN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_RUN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_RUN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return 0;
}

static int _cffi_const_LZMA_FINISH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FINISH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FINISH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_RUN(lib);
}

static int _cffi_const_LZMA_INDEX_ITER_ANY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_INDEX_ITER_ANY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_INDEX_ITER_ANY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FINISH(lib);
}

static int _cffi_const_LZMA_INDEX_ITER_STREAM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_INDEX_ITER_STREAM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_INDEX_ITER_STREAM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_INDEX_ITER_ANY(lib);
}

static int _cffi_const_LZMA_INDEX_ITER_BLOCK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_INDEX_ITER_BLOCK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_INDEX_ITER_BLOCK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_INDEX_ITER_STREAM(lib);
}

static int _cffi_const_LZMA_INDEX_ITER_NONEMPTY_BLOCK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_INDEX_ITER_NONEMPTY_BLOCK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_INDEX_ITER_NONEMPTY_BLOCK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_INDEX_ITER_BLOCK(lib);
}

static int _cffi_const_LZMA_OK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_OK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_OK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_INDEX_ITER_NONEMPTY_BLOCK(lib);
}

static int _cffi_const_LZMA_STREAM_END(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_STREAM_END);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_STREAM_END", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_OK(lib);
}

static int _cffi_const_LZMA_NO_CHECK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_NO_CHECK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_NO_CHECK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_STREAM_END(lib);
}

static int _cffi_const_LZMA_UNSUPPORTED_CHECK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_UNSUPPORTED_CHECK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_UNSUPPORTED_CHECK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_NO_CHECK(lib);
}

static int _cffi_const_LZMA_GET_CHECK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_GET_CHECK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_GET_CHECK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_UNSUPPORTED_CHECK(lib);
}

static int _cffi_const_LZMA_MEM_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MEM_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MEM_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_GET_CHECK(lib);
}

static int _cffi_const_LZMA_MEMLIMIT_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MEMLIMIT_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MEMLIMIT_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MEM_ERROR(lib);
}

static int _cffi_const_LZMA_FORMAT_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FORMAT_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FORMAT_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MEMLIMIT_ERROR(lib);
}

static int _cffi_const_LZMA_OPTIONS_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_OPTIONS_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_OPTIONS_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FORMAT_ERROR(lib);
}

static int _cffi_const_LZMA_DATA_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_DATA_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_DATA_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_OPTIONS_ERROR(lib);
}

static int _cffi_const_LZMA_BUF_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_BUF_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_BUF_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_DATA_ERROR(lib);
}

static int _cffi_const_LZMA_PROG_ERROR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_PROG_ERROR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_PROG_ERROR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_BUF_ERROR(lib);
}

static PyObject *
_cffi_f__pylzma_block_header_size_decode(PyObject *self, PyObject *arg0)
{
  uint32_t x0;

  x0 = _cffi_to_c_int(arg0, uint32_t);
  if (x0 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { _pylzma_block_header_size_decode(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f__pylzma_stream_init(PyObject *self, PyObject *arg0)
{
  lzma_stream * x0;
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
  { _pylzma_stream_init(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_free(PyObject *self, PyObject *arg0)
{
  void * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(2), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_lzma_alone_decoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  uint64_t x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_alone_decoder", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_alone_decoder(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_alone_encoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  lzma_options_lzma * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_alone_encoder", &arg0, &arg1))
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
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(3), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_alone_encoder(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_auto_decoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  uint64_t x1;
  uint32_t x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:lzma_auto_decoder", &arg0, &arg1, &arg2))
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

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, uint32_t);
  if (x2 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_auto_decoder(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_block_compressed_size(PyObject *self, PyObject *args)
{
  lzma_block * x0;
  uint64_t x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_block_compressed_size", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(4), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_block_compressed_size(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_block_decoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  lzma_block * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_block_decoder", &arg0, &arg1))
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
      _cffi_type(4), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(4), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_block_decoder(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_block_header_decode(PyObject *self, PyObject *args)
{
  lzma_block * x0;
  lzma_allocator * x1;
  uint8_t const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:lzma_block_header_decode", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(4), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(6), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_block_header_decode(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_check_is_supported(PyObject *self, PyObject *arg0)
{
  int x0;
  _Bool result;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_check_is_supported(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, _Bool);
}

static PyObject *
_cffi_f_lzma_code(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_code", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_code(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_easy_encoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  uint32_t x1;
  int x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:lzma_easy_encoder", &arg0, &arg1, &arg2))
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

  x1 = _cffi_to_c_int(arg1, uint32_t);
  if (x1 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_easy_encoder(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_end(PyObject *self, PyObject *arg0)
{
  lzma_stream * x0;
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
  { lzma_end(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_lzma_get_check(PyObject *self, PyObject *arg0)
{
  lzma_stream const * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(7), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_get_check(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_block_count(PyObject *self, PyObject *arg0)
{
  lzma_index const * x0;
  Py_ssize_t datasize;
  uint64_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_block_count(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint64_t);
}

static PyObject *
_cffi_f_lzma_index_buffer_decode(PyObject *self, PyObject *args)
{
  lzma_index * * x0;
  uint64_t * x1;
  lzma_allocator * x2;
  uint8_t const * x3;
  size_t * x4;
  size_t x5;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:lzma_index_buffer_decode", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(9), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(10), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(10), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(5), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(6), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(11), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(11), arg4) < 0)
      return NULL;
  }

  x5 = _cffi_to_c_int(arg5, size_t);
  if (x5 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_buffer_decode(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_cat(PyObject *self, PyObject *args)
{
  lzma_index * x0;
  lzma_index * x1;
  lzma_allocator * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:lzma_index_cat", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(12), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(12), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(12), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(12), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(5), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_cat(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_dup(PyObject *self, PyObject *args)
{
  lzma_index const * x0;
  lzma_allocator * x1;
  Py_ssize_t datasize;
  lzma_index * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_dup", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_dup(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(12));
}

static PyObject *
_cffi_f_lzma_index_end(PyObject *self, PyObject *args)
{
  lzma_index * x0;
  lzma_allocator * x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_end", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(12), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(12), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { lzma_index_end(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_lzma_index_init(PyObject *self, PyObject *arg0)
{
  lzma_allocator * x0;
  Py_ssize_t datasize;
  lzma_index * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(5), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_init(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(12));
}

static PyObject *
_cffi_f_lzma_index_iter_init(PyObject *self, PyObject *args)
{
  lzma_index_iter * x0;
  lzma_index const * x1;
  Py_ssize_t datasize;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_iter_init", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(13), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(13), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(8), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { lzma_index_iter_init(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_lzma_index_iter_locate(PyObject *self, PyObject *args)
{
  lzma_index_iter * x0;
  uint64_t x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_iter_locate", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(13), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(13), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_iter_locate(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_iter_next(PyObject *self, PyObject *args)
{
  lzma_index_iter * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_iter_next", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(13), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(13), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_iter_next(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_size(PyObject *self, PyObject *arg0)
{
  lzma_index const * x0;
  Py_ssize_t datasize;
  uint64_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_size(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint64_t);
}

static PyObject *
_cffi_f_lzma_index_stream_padding(PyObject *self, PyObject *args)
{
  lzma_index * x0;
  uint64_t x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_index_stream_padding", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(12), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(12), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_stream_padding(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_index_stream_size(PyObject *self, PyObject *arg0)
{
  lzma_index const * x0;
  Py_ssize_t datasize;
  uint64_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_stream_size(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint64_t);
}

static PyObject *
_cffi_f_lzma_index_total_size(PyObject *self, PyObject *arg0)
{
  lzma_index const * x0;
  Py_ssize_t datasize;
  uint64_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_total_size(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint64_t);
}

static PyObject *
_cffi_f_lzma_index_uncompressed_size(PyObject *self, PyObject *arg0)
{
  lzma_index const * x0;
  Py_ssize_t datasize;
  uint64_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(8), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_index_uncompressed_size(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint64_t);
}

static PyObject *
_cffi_f_lzma_lzma_preset(PyObject *self, PyObject *args)
{
  lzma_options_lzma * x0;
  uint32_t x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_lzma_preset", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(3), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, uint32_t);
  if (x1 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_lzma_preset(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_properties_decode(PyObject *self, PyObject *args)
{
  lzma_filter * x0;
  lzma_allocator * x1;
  uint8_t const * x2;
  size_t x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:lzma_properties_decode", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(14), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(14), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(5), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(6), arg2) < 0)
      return NULL;
  }

  x3 = _cffi_to_c_int(arg3, size_t);
  if (x3 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_properties_decode(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_properties_encode(PyObject *self, PyObject *args)
{
  lzma_filter const * x0;
  uint8_t * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_properties_encode", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(15), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(15), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(16), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(16), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_properties_encode(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_properties_size(PyObject *self, PyObject *args)
{
  uint32_t * x0;
  lzma_filter const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_properties_size", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(17), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(17), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(15), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(15), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_properties_size(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_raw_decoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  lzma_filter const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_raw_decoder", &arg0, &arg1))
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
      _cffi_type(15), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(15), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_raw_decoder(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_raw_encoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  lzma_filter const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_raw_encoder", &arg0, &arg1))
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
      _cffi_type(15), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(15), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_raw_encoder(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_stream_decoder(PyObject *self, PyObject *args)
{
  lzma_stream * x0;
  uint64_t x1;
  uint32_t x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:lzma_stream_decoder", &arg0, &arg1, &arg2))
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

  x1 = _cffi_to_c_int(arg1, uint64_t);
  if (x1 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, uint32_t);
  if (x2 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_stream_decoder(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_stream_flags_compare(PyObject *self, PyObject *args)
{
  lzma_stream_flags const * x0;
  lzma_stream_flags const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_stream_flags_compare", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(18), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(18), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(18), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(18), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_stream_flags_compare(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_stream_footer_decode(PyObject *self, PyObject *args)
{
  lzma_stream_flags * x0;
  uint8_t const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_stream_footer_decode", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(19), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(6), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_stream_footer_decode(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_lzma_stream_header_decode(PyObject *self, PyObject *args)
{
  lzma_stream_flags * x0;
  uint8_t const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:lzma_stream_header_decode", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(19), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(6), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(6), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = lzma_stream_header_decode(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_malloc(PyObject *self, PyObject *arg0)
{
  size_t x0;
  void * result;

  x0 = _cffi_to_c_int(arg0, size_t);
  if (x0 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = malloc(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_realloc(PyObject *self, PyObject *args)
{
  void * x0;
  size_t x1;
  Py_ssize_t datasize;
  void * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:realloc", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(2), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, size_t);
  if (x1 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = realloc(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static int _cffi_const_LZMA_CHECK_CRC32(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CHECK_CRC32);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CHECK_CRC32", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return 0;
}

static int _cffi_const_LZMA_CHECK_CRC64(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CHECK_CRC64);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CHECK_CRC64", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CHECK_CRC32(lib);
}

static int _cffi_const_LZMA_CHECK_ID_MAX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CHECK_ID_MAX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CHECK_ID_MAX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CHECK_CRC64(lib);
}

static int _cffi_const_LZMA_CHECK_NONE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CHECK_NONE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CHECK_NONE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CHECK_ID_MAX(lib);
}

static int _cffi_const_LZMA_CHECK_SHA256(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CHECK_SHA256);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CHECK_SHA256", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CHECK_NONE(lib);
}

static int _cffi_const_LZMA_CONCATENATED(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_CONCATENATED);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_CONCATENATED", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CHECK_SHA256(lib);
}

static int _cffi_const_LZMA_DELTA_TYPE_BYTE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_DELTA_TYPE_BYTE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_DELTA_TYPE_BYTE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_CONCATENATED(lib);
}

static int _cffi_const_LZMA_FILTERS_MAX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTERS_MAX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTERS_MAX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_DELTA_TYPE_BYTE(lib);
}

static int _cffi_const_LZMA_FILTER_ARM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_ARM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_ARM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTERS_MAX(lib);
}

static int _cffi_const_LZMA_FILTER_ARMTHUMB(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_ARMTHUMB);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_ARMTHUMB", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_ARM(lib);
}

static int _cffi_const_LZMA_FILTER_DELTA(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_DELTA);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_DELTA", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_ARMTHUMB(lib);
}

static int _cffi_const_LZMA_FILTER_IA64(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_IA64);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_IA64", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_DELTA(lib);
}

static int _cffi_const_LZMA_FILTER_LZMA1(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_LZMA1);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_LZMA1", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_IA64(lib);
}

static int _cffi_const_LZMA_FILTER_LZMA2(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_LZMA2);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_LZMA2", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_LZMA1(lib);
}

static int _cffi_const_LZMA_FILTER_POWERPC(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_POWERPC);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_POWERPC", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_LZMA2(lib);
}

static int _cffi_const_LZMA_FILTER_SPARC(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_SPARC);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_SPARC", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_POWERPC(lib);
}

static int _cffi_const_LZMA_FILTER_X86(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_FILTER_X86);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_FILTER_X86", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_SPARC(lib);
}

static int _cffi_const_LZMA_MF_BT2(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MF_BT2);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MF_BT2", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_FILTER_X86(lib);
}

static int _cffi_const_LZMA_MF_BT3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MF_BT3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MF_BT3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MF_BT2(lib);
}

static int _cffi_const_LZMA_MF_BT4(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MF_BT4);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MF_BT4", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MF_BT3(lib);
}

static int _cffi_const_LZMA_MF_HC3(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MF_HC3);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MF_HC3", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MF_BT4(lib);
}

static int _cffi_const_LZMA_MF_HC4(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MF_HC4);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MF_HC4", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MF_HC3(lib);
}

static int _cffi_const_LZMA_MODE_FAST(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MODE_FAST);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MODE_FAST", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MF_HC4(lib);
}

static int _cffi_const_LZMA_MODE_NORMAL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_MODE_NORMAL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_MODE_NORMAL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MODE_FAST(lib);
}

static int _cffi_const_LZMA_PRESET_DEFAULT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_PRESET_DEFAULT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_PRESET_DEFAULT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_MODE_NORMAL(lib);
}

static int _cffi_const_LZMA_PRESET_EXTREME(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_PRESET_EXTREME);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_PRESET_EXTREME", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_PRESET_DEFAULT(lib);
}

static int _cffi_const_LZMA_STREAM_HEADER_SIZE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_STREAM_HEADER_SIZE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_STREAM_HEADER_SIZE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_PRESET_EXTREME(lib);
}

static int _cffi_const_LZMA_TELL_ANY_CHECK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_TELL_ANY_CHECK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_TELL_ANY_CHECK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_STREAM_HEADER_SIZE(lib);
}

static int _cffi_const_LZMA_TELL_NO_CHECK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_TELL_NO_CHECK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_TELL_NO_CHECK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_TELL_ANY_CHECK(lib);
}

static int _cffi_const_LZMA_VLI_UNKNOWN(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(LZMA_VLI_UNKNOWN);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "LZMA_VLI_UNKNOWN", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_TELL_NO_CHECK(lib);
}

static int _cffi_const_UINT64_MAX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(UINT64_MAX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "UINT64_MAX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_LZMA_VLI_UNKNOWN(lib);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_UINT64_MAX(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__lzma_allocator", _cffi_layout__lzma_allocator, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_block", _cffi_layout__lzma_block, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_filter", _cffi_layout__lzma_filter, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_index_iter", _cffi_layout__lzma_index_iter, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_options_bcj", _cffi_layout__lzma_options_bcj, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_options_delta", _cffi_layout__lzma_options_delta, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_options_lzma", _cffi_layout__lzma_options_lzma, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_stream", _cffi_layout__lzma_stream, METH_NOARGS, NULL},
  {"_cffi_layout__lzma_stream_flags", _cffi_layout__lzma_stream_flags, METH_NOARGS, NULL},
  {"_pylzma_block_header_size_decode", _cffi_f__pylzma_block_header_size_decode, METH_O, NULL},
  {"_pylzma_stream_init", _cffi_f__pylzma_stream_init, METH_O, NULL},
  {"free", _cffi_f_free, METH_O, NULL},
  {"lzma_alone_decoder", _cffi_f_lzma_alone_decoder, METH_VARARGS, NULL},
  {"lzma_alone_encoder", _cffi_f_lzma_alone_encoder, METH_VARARGS, NULL},
  {"lzma_auto_decoder", _cffi_f_lzma_auto_decoder, METH_VARARGS, NULL},
  {"lzma_block_compressed_size", _cffi_f_lzma_block_compressed_size, METH_VARARGS, NULL},
  {"lzma_block_decoder", _cffi_f_lzma_block_decoder, METH_VARARGS, NULL},
  {"lzma_block_header_decode", _cffi_f_lzma_block_header_decode, METH_VARARGS, NULL},
  {"lzma_check_is_supported", _cffi_f_lzma_check_is_supported, METH_O, NULL},
  {"lzma_code", _cffi_f_lzma_code, METH_VARARGS, NULL},
  {"lzma_easy_encoder", _cffi_f_lzma_easy_encoder, METH_VARARGS, NULL},
  {"lzma_end", _cffi_f_lzma_end, METH_O, NULL},
  {"lzma_get_check", _cffi_f_lzma_get_check, METH_O, NULL},
  {"lzma_index_block_count", _cffi_f_lzma_index_block_count, METH_O, NULL},
  {"lzma_index_buffer_decode", _cffi_f_lzma_index_buffer_decode, METH_VARARGS, NULL},
  {"lzma_index_cat", _cffi_f_lzma_index_cat, METH_VARARGS, NULL},
  {"lzma_index_dup", _cffi_f_lzma_index_dup, METH_VARARGS, NULL},
  {"lzma_index_end", _cffi_f_lzma_index_end, METH_VARARGS, NULL},
  {"lzma_index_init", _cffi_f_lzma_index_init, METH_O, NULL},
  {"lzma_index_iter_init", _cffi_f_lzma_index_iter_init, METH_VARARGS, NULL},
  {"lzma_index_iter_locate", _cffi_f_lzma_index_iter_locate, METH_VARARGS, NULL},
  {"lzma_index_iter_next", _cffi_f_lzma_index_iter_next, METH_VARARGS, NULL},
  {"lzma_index_size", _cffi_f_lzma_index_size, METH_O, NULL},
  {"lzma_index_stream_padding", _cffi_f_lzma_index_stream_padding, METH_VARARGS, NULL},
  {"lzma_index_stream_size", _cffi_f_lzma_index_stream_size, METH_O, NULL},
  {"lzma_index_total_size", _cffi_f_lzma_index_total_size, METH_O, NULL},
  {"lzma_index_uncompressed_size", _cffi_f_lzma_index_uncompressed_size, METH_O, NULL},
  {"lzma_lzma_preset", _cffi_f_lzma_lzma_preset, METH_VARARGS, NULL},
  {"lzma_properties_decode", _cffi_f_lzma_properties_decode, METH_VARARGS, NULL},
  {"lzma_properties_encode", _cffi_f_lzma_properties_encode, METH_VARARGS, NULL},
  {"lzma_properties_size", _cffi_f_lzma_properties_size, METH_VARARGS, NULL},
  {"lzma_raw_decoder", _cffi_f_lzma_raw_decoder, METH_VARARGS, NULL},
  {"lzma_raw_encoder", _cffi_f_lzma_raw_encoder, METH_VARARGS, NULL},
  {"lzma_stream_decoder", _cffi_f_lzma_stream_decoder, METH_VARARGS, NULL},
  {"lzma_stream_flags_compare", _cffi_f_lzma_stream_flags_compare, METH_VARARGS, NULL},
  {"lzma_stream_footer_decode", _cffi_f_lzma_stream_footer_decode, METH_VARARGS, NULL},
  {"lzma_stream_header_decode", _cffi_f_lzma_stream_header_decode, METH_VARARGS, NULL},
  {"malloc", _cffi_f_malloc, METH_O, NULL},
  {"realloc", _cffi_f_realloc, METH_VARARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_compiled_module",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__compiled_module(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (_cffi_const_LZMA_PROG_ERROR(lib) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_compiled_module(void)
{
  PyObject *lib;
  lib = Py_InitModule("_compiled_module", _cffi_methods);
  if (lib == NULL)
    return;
  if (_cffi_const_LZMA_PROG_ERROR(lib) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
