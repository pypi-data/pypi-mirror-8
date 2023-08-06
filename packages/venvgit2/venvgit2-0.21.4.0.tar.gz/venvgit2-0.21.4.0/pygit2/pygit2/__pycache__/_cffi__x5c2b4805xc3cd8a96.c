
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


#include <git2.h>

static void _cffi_check__git_buf(git_buf *p)
{
  /* only to generate compile-time warnings or errors */
  { char * *tmp = &p->ptr; (void)tmp; }
  (void)((p->asize) << 1);
  (void)((p->size) << 1);
}
static PyObject *
_cffi_layout__git_buf(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_buf y; };
  static Py_ssize_t nums[] = {
    sizeof(git_buf),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_buf, ptr),
    sizeof(((git_buf *)0)->ptr),
    offsetof(git_buf, asize),
    sizeof(((git_buf *)0)->asize),
    offsetof(git_buf, size),
    sizeof(((git_buf *)0)->size),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_buf(0);
}

static int _cffi_e__git_clone_local_t(PyObject *lib)
{
  if ((GIT_CLONE_LOCAL_AUTO) < 0 || (unsigned long)(GIT_CLONE_LOCAL_AUTO) != 0UL) {
    char buf[64];
    if ((GIT_CLONE_LOCAL_AUTO) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CLONE_LOCAL_AUTO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CLONE_LOCAL_AUTO));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_clone_local_t", "GIT_CLONE_LOCAL_AUTO", buf, "0");
    return -1;
  }
  if ((GIT_CLONE_LOCAL) < 0 || (unsigned long)(GIT_CLONE_LOCAL) != 1UL) {
    char buf[64];
    if ((GIT_CLONE_LOCAL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CLONE_LOCAL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CLONE_LOCAL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_clone_local_t", "GIT_CLONE_LOCAL", buf, "1");
    return -1;
  }
  if ((GIT_CLONE_NO_LOCAL) < 0 || (unsigned long)(GIT_CLONE_NO_LOCAL) != 2UL) {
    char buf[64];
    if ((GIT_CLONE_NO_LOCAL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CLONE_NO_LOCAL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CLONE_NO_LOCAL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_clone_local_t", "GIT_CLONE_NO_LOCAL", buf, "2");
    return -1;
  }
  if ((GIT_CLONE_LOCAL_NO_LINKS) < 0 || (unsigned long)(GIT_CLONE_LOCAL_NO_LINKS) != 3UL) {
    char buf[64];
    if ((GIT_CLONE_LOCAL_NO_LINKS) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CLONE_LOCAL_NO_LINKS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CLONE_LOCAL_NO_LINKS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_clone_local_t", "GIT_CLONE_LOCAL_NO_LINKS", buf, "3");
    return -1;
  }
  return 0;
}

static void _cffi_check__git_config_entry(git_config_entry *p)
{
  /* only to generate compile-time warnings or errors */
  { char const * *tmp = &p->name; (void)tmp; }
  { char const * *tmp = &p->value; (void)tmp; }
  { git_config_level_t *tmp = &p->level; (void)tmp; }
}
static PyObject *
_cffi_layout__git_config_entry(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_config_entry y; };
  static Py_ssize_t nums[] = {
    sizeof(git_config_entry),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_config_entry, name),
    sizeof(((git_config_entry *)0)->name),
    offsetof(git_config_entry, value),
    sizeof(((git_config_entry *)0)->value),
    offsetof(git_config_entry, level),
    sizeof(((git_config_entry *)0)->level),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_config_entry(0);
}

static int _cffi_e__git_config_level_t(PyObject *lib)
{
  if ((GIT_CONFIG_LEVEL_SYSTEM) < 0 || (unsigned long)(GIT_CONFIG_LEVEL_SYSTEM) != 1UL) {
    char buf[64];
    if ((GIT_CONFIG_LEVEL_SYSTEM) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_LEVEL_SYSTEM));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_LEVEL_SYSTEM));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_LEVEL_SYSTEM", buf, "1");
    return -1;
  }
  if ((GIT_CONFIG_LEVEL_XDG) < 0 || (unsigned long)(GIT_CONFIG_LEVEL_XDG) != 2UL) {
    char buf[64];
    if ((GIT_CONFIG_LEVEL_XDG) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_LEVEL_XDG));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_LEVEL_XDG));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_LEVEL_XDG", buf, "2");
    return -1;
  }
  if ((GIT_CONFIG_LEVEL_GLOBAL) < 0 || (unsigned long)(GIT_CONFIG_LEVEL_GLOBAL) != 3UL) {
    char buf[64];
    if ((GIT_CONFIG_LEVEL_GLOBAL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_LEVEL_GLOBAL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_LEVEL_GLOBAL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_LEVEL_GLOBAL", buf, "3");
    return -1;
  }
  if ((GIT_CONFIG_LEVEL_LOCAL) < 0 || (unsigned long)(GIT_CONFIG_LEVEL_LOCAL) != 4UL) {
    char buf[64];
    if ((GIT_CONFIG_LEVEL_LOCAL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_LEVEL_LOCAL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_LEVEL_LOCAL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_LEVEL_LOCAL", buf, "4");
    return -1;
  }
  if ((GIT_CONFIG_LEVEL_APP) < 0 || (unsigned long)(GIT_CONFIG_LEVEL_APP) != 5UL) {
    char buf[64];
    if ((GIT_CONFIG_LEVEL_APP) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_LEVEL_APP));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_LEVEL_APP));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_LEVEL_APP", buf, "5");
    return -1;
  }
  if ((GIT_CONFIG_HIGHEST_LEVEL) >= 0 || (long)(GIT_CONFIG_HIGHEST_LEVEL) != -1L) {
    char buf[64];
    if ((GIT_CONFIG_HIGHEST_LEVEL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_CONFIG_HIGHEST_LEVEL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_CONFIG_HIGHEST_LEVEL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_config_level_t", "GIT_CONFIG_HIGHEST_LEVEL", buf, "-1");
    return -1;
  }
  return _cffi_e__git_clone_local_t(lib);
}

static int _cffi_const_GIT_CREDTYPE_USERPASS_PLAINTEXT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_CREDTYPE_USERPASS_PLAINTEXT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_CREDTYPE_USERPASS_PLAINTEXT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return 0;
}

static int _cffi_const_GIT_CREDTYPE_SSH_KEY(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_CREDTYPE_SSH_KEY);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_CREDTYPE_SSH_KEY", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_CREDTYPE_USERPASS_PLAINTEXT(lib);
}

static int _cffi_const_GIT_CREDTYPE_SSH_CUSTOM(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_CREDTYPE_SSH_CUSTOM);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_CREDTYPE_SSH_CUSTOM", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_CREDTYPE_SSH_KEY(lib);
}

static int _cffi_const_GIT_CREDTYPE_DEFAULT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_CREDTYPE_DEFAULT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_CREDTYPE_DEFAULT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_CREDTYPE_SSH_CUSTOM(lib);
}

static int _cffi_e__git_delta_t(PyObject *lib)
{
  if ((GIT_DELTA_UNMODIFIED) < 0 || (unsigned long)(GIT_DELTA_UNMODIFIED) != 0UL) {
    char buf[64];
    if ((GIT_DELTA_UNMODIFIED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_UNMODIFIED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_UNMODIFIED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_UNMODIFIED", buf, "0");
    return -1;
  }
  if ((GIT_DELTA_ADDED) < 0 || (unsigned long)(GIT_DELTA_ADDED) != 1UL) {
    char buf[64];
    if ((GIT_DELTA_ADDED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_ADDED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_ADDED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_ADDED", buf, "1");
    return -1;
  }
  if ((GIT_DELTA_DELETED) < 0 || (unsigned long)(GIT_DELTA_DELETED) != 2UL) {
    char buf[64];
    if ((GIT_DELTA_DELETED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_DELETED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_DELETED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_DELETED", buf, "2");
    return -1;
  }
  if ((GIT_DELTA_MODIFIED) < 0 || (unsigned long)(GIT_DELTA_MODIFIED) != 3UL) {
    char buf[64];
    if ((GIT_DELTA_MODIFIED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_MODIFIED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_MODIFIED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_MODIFIED", buf, "3");
    return -1;
  }
  if ((GIT_DELTA_RENAMED) < 0 || (unsigned long)(GIT_DELTA_RENAMED) != 4UL) {
    char buf[64];
    if ((GIT_DELTA_RENAMED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_RENAMED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_RENAMED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_RENAMED", buf, "4");
    return -1;
  }
  if ((GIT_DELTA_COPIED) < 0 || (unsigned long)(GIT_DELTA_COPIED) != 5UL) {
    char buf[64];
    if ((GIT_DELTA_COPIED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_COPIED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_COPIED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_COPIED", buf, "5");
    return -1;
  }
  if ((GIT_DELTA_IGNORED) < 0 || (unsigned long)(GIT_DELTA_IGNORED) != 6UL) {
    char buf[64];
    if ((GIT_DELTA_IGNORED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_IGNORED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_IGNORED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_IGNORED", buf, "6");
    return -1;
  }
  if ((GIT_DELTA_UNTRACKED) < 0 || (unsigned long)(GIT_DELTA_UNTRACKED) != 7UL) {
    char buf[64];
    if ((GIT_DELTA_UNTRACKED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_UNTRACKED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_UNTRACKED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_UNTRACKED", buf, "7");
    return -1;
  }
  if ((GIT_DELTA_TYPECHANGE) < 0 || (unsigned long)(GIT_DELTA_TYPECHANGE) != 8UL) {
    char buf[64];
    if ((GIT_DELTA_TYPECHANGE) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DELTA_TYPECHANGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DELTA_TYPECHANGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_delta_t", "GIT_DELTA_TYPECHANGE", buf, "8");
    return -1;
  }
  return _cffi_e__git_config_level_t(lib);
}

static void _cffi_check__git_diff_delta(git_diff_delta *p)
{
  /* only to generate compile-time warnings or errors */
  { git_delta_t *tmp = &p->status; (void)tmp; }
  (void)((p->flags) << 1);
  (void)((p->similarity) << 1);
  (void)((p->nfiles) << 1);
  { git_diff_file *tmp = &p->old_file; (void)tmp; }
  { git_diff_file *tmp = &p->new_file; (void)tmp; }
}
static PyObject *
_cffi_layout__git_diff_delta(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_diff_delta y; };
  static Py_ssize_t nums[] = {
    sizeof(git_diff_delta),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_diff_delta, status),
    sizeof(((git_diff_delta *)0)->status),
    offsetof(git_diff_delta, flags),
    sizeof(((git_diff_delta *)0)->flags),
    offsetof(git_diff_delta, similarity),
    sizeof(((git_diff_delta *)0)->similarity),
    offsetof(git_diff_delta, nfiles),
    sizeof(((git_diff_delta *)0)->nfiles),
    offsetof(git_diff_delta, old_file),
    sizeof(((git_diff_delta *)0)->old_file),
    offsetof(git_diff_delta, new_file),
    sizeof(((git_diff_delta *)0)->new_file),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_diff_delta(0);
}

static void _cffi_check__git_diff_file(git_diff_file *p)
{
  /* only to generate compile-time warnings or errors */
  { git_oid *tmp = &p->id; (void)tmp; }
  { char const * *tmp = &p->path; (void)tmp; }
  (void)((p->size) << 1);
  (void)((p->flags) << 1);
  (void)((p->mode) << 1);
}
static PyObject *
_cffi_layout__git_diff_file(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_diff_file y; };
  static Py_ssize_t nums[] = {
    sizeof(git_diff_file),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_diff_file, id),
    sizeof(((git_diff_file *)0)->id),
    offsetof(git_diff_file, path),
    sizeof(((git_diff_file *)0)->path),
    offsetof(git_diff_file, size),
    sizeof(((git_diff_file *)0)->size),
    offsetof(git_diff_file, flags),
    sizeof(((git_diff_file *)0)->flags),
    offsetof(git_diff_file, mode),
    sizeof(((git_diff_file *)0)->mode),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_diff_file(0);
}

static void _cffi_check__git_diff_options(git_diff_options *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->flags) << 1);
  { git_submodule_ignore_t *tmp = &p->ignore_submodules; (void)tmp; }
  { git_strarray *tmp = &p->pathspec; (void)tmp; }
  { int(* *tmp)(git_diff const *, git_diff_delta const *, char const *, void *) = &p->notify_cb; (void)tmp; }
  { void * *tmp = &p->notify_payload; (void)tmp; }
  (void)((p->context_lines) << 1);
  (void)((p->interhunk_lines) << 1);
  (void)((p->id_abbrev) << 1);
  (void)((p->max_size) << 1);
  { char const * *tmp = &p->old_prefix; (void)tmp; }
  { char const * *tmp = &p->new_prefix; (void)tmp; }
}
static PyObject *
_cffi_layout__git_diff_options(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_diff_options y; };
  static Py_ssize_t nums[] = {
    sizeof(git_diff_options),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_diff_options, version),
    sizeof(((git_diff_options *)0)->version),
    offsetof(git_diff_options, flags),
    sizeof(((git_diff_options *)0)->flags),
    offsetof(git_diff_options, ignore_submodules),
    sizeof(((git_diff_options *)0)->ignore_submodules),
    offsetof(git_diff_options, pathspec),
    sizeof(((git_diff_options *)0)->pathspec),
    offsetof(git_diff_options, notify_cb),
    sizeof(((git_diff_options *)0)->notify_cb),
    offsetof(git_diff_options, notify_payload),
    sizeof(((git_diff_options *)0)->notify_payload),
    offsetof(git_diff_options, context_lines),
    sizeof(((git_diff_options *)0)->context_lines),
    offsetof(git_diff_options, interhunk_lines),
    sizeof(((git_diff_options *)0)->interhunk_lines),
    offsetof(git_diff_options, id_abbrev),
    sizeof(((git_diff_options *)0)->id_abbrev),
    offsetof(git_diff_options, max_size),
    sizeof(((git_diff_options *)0)->max_size),
    offsetof(git_diff_options, old_prefix),
    sizeof(((git_diff_options *)0)->old_prefix),
    offsetof(git_diff_options, new_prefix),
    sizeof(((git_diff_options *)0)->new_prefix),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_diff_options(0);
}

static int _cffi_e__git_direction(PyObject *lib)
{
  if ((GIT_DIRECTION_FETCH) < 0 || (unsigned long)(GIT_DIRECTION_FETCH) != 0UL) {
    char buf[64];
    if ((GIT_DIRECTION_FETCH) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DIRECTION_FETCH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DIRECTION_FETCH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_direction", "GIT_DIRECTION_FETCH", buf, "0");
    return -1;
  }
  if ((GIT_DIRECTION_PUSH) < 0 || (unsigned long)(GIT_DIRECTION_PUSH) != 1UL) {
    char buf[64];
    if ((GIT_DIRECTION_PUSH) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_DIRECTION_PUSH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_DIRECTION_PUSH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_direction", "GIT_DIRECTION_PUSH", buf, "1");
    return -1;
  }
  return _cffi_e__git_delta_t(lib);
}

static void _cffi_check__git_error(git_error *p)
{
  /* only to generate compile-time warnings or errors */
  { char * *tmp = &p->message; (void)tmp; }
  (void)((p->klass) << 1);
}
static PyObject *
_cffi_layout__git_error(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_error y; };
  static Py_ssize_t nums[] = {
    sizeof(git_error),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_error, message),
    sizeof(((git_error *)0)->message),
    offsetof(git_error, klass),
    sizeof(((git_error *)0)->klass),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_error(0);
}

static int _cffi_e__git_error_code(PyObject *lib)
{
  if ((GIT_OK) < 0 || (unsigned long)(GIT_OK) != 0UL) {
    char buf[64];
    if ((GIT_OK) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_OK));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_OK));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_OK", buf, "0");
    return -1;
  }
  if ((GIT_ERROR) >= 0 || (long)(GIT_ERROR) != -1L) {
    char buf[64];
    if ((GIT_ERROR) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_ERROR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_ERROR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_ERROR", buf, "-1");
    return -1;
  }
  if ((GIT_ENOTFOUND) >= 0 || (long)(GIT_ENOTFOUND) != -3L) {
    char buf[64];
    if ((GIT_ENOTFOUND) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_ENOTFOUND));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_ENOTFOUND));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_ENOTFOUND", buf, "-3");
    return -1;
  }
  if ((GIT_EEXISTS) >= 0 || (long)(GIT_EEXISTS) != -4L) {
    char buf[64];
    if ((GIT_EEXISTS) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EEXISTS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EEXISTS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EEXISTS", buf, "-4");
    return -1;
  }
  if ((GIT_EAMBIGUOUS) >= 0 || (long)(GIT_EAMBIGUOUS) != -5L) {
    char buf[64];
    if ((GIT_EAMBIGUOUS) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EAMBIGUOUS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EAMBIGUOUS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EAMBIGUOUS", buf, "-5");
    return -1;
  }
  if ((GIT_EBUFS) >= 0 || (long)(GIT_EBUFS) != -6L) {
    char buf[64];
    if ((GIT_EBUFS) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EBUFS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EBUFS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EBUFS", buf, "-6");
    return -1;
  }
  if ((GIT_EUSER) >= 0 || (long)(GIT_EUSER) != -7L) {
    char buf[64];
    if ((GIT_EUSER) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EUSER));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EUSER));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EUSER", buf, "-7");
    return -1;
  }
  if ((GIT_EBAREREPO) >= 0 || (long)(GIT_EBAREREPO) != -8L) {
    char buf[64];
    if ((GIT_EBAREREPO) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EBAREREPO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EBAREREPO));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EBAREREPO", buf, "-8");
    return -1;
  }
  if ((GIT_EUNBORNBRANCH) >= 0 || (long)(GIT_EUNBORNBRANCH) != -9L) {
    char buf[64];
    if ((GIT_EUNBORNBRANCH) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EUNBORNBRANCH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EUNBORNBRANCH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EUNBORNBRANCH", buf, "-9");
    return -1;
  }
  if ((GIT_EUNMERGED) >= 0 || (long)(GIT_EUNMERGED) != -10L) {
    char buf[64];
    if ((GIT_EUNMERGED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EUNMERGED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EUNMERGED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EUNMERGED", buf, "-10");
    return -1;
  }
  if ((GIT_ENONFASTFORWARD) >= 0 || (long)(GIT_ENONFASTFORWARD) != -11L) {
    char buf[64];
    if ((GIT_ENONFASTFORWARD) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_ENONFASTFORWARD));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_ENONFASTFORWARD));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_ENONFASTFORWARD", buf, "-11");
    return -1;
  }
  if ((GIT_EINVALIDSPEC) >= 0 || (long)(GIT_EINVALIDSPEC) != -12L) {
    char buf[64];
    if ((GIT_EINVALIDSPEC) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EINVALIDSPEC));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EINVALIDSPEC));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EINVALIDSPEC", buf, "-12");
    return -1;
  }
  if ((GIT_EMERGECONFLICT) >= 0 || (long)(GIT_EMERGECONFLICT) != -13L) {
    char buf[64];
    if ((GIT_EMERGECONFLICT) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_EMERGECONFLICT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_EMERGECONFLICT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_EMERGECONFLICT", buf, "-13");
    return -1;
  }
  if ((GIT_ELOCKED) >= 0 || (long)(GIT_ELOCKED) != -14L) {
    char buf[64];
    if ((GIT_ELOCKED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_ELOCKED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_ELOCKED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_ELOCKED", buf, "-14");
    return -1;
  }
  if ((GIT_PASSTHROUGH) >= 0 || (long)(GIT_PASSTHROUGH) != -30L) {
    char buf[64];
    if ((GIT_PASSTHROUGH) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_PASSTHROUGH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_PASSTHROUGH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_PASSTHROUGH", buf, "-30");
    return -1;
  }
  if ((GIT_ITEROVER) >= 0 || (long)(GIT_ITEROVER) != -31L) {
    char buf[64];
    if ((GIT_ITEROVER) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_ITEROVER));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_ITEROVER));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_error_code", "GIT_ITEROVER", buf, "-31");
    return -1;
  }
  return _cffi_e__git_direction(lib);
}

static void _cffi_check__git_index_time(git_index_time *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->seconds) << 1);
  (void)((p->nanoseconds) << 1);
}
static PyObject *
_cffi_layout__git_index_time(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_index_time y; };
  static Py_ssize_t nums[] = {
    sizeof(git_index_time),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_index_time, seconds),
    sizeof(((git_index_time *)0)->seconds),
    offsetof(git_index_time, nanoseconds),
    sizeof(((git_index_time *)0)->nanoseconds),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_index_time(0);
}

static int _cffi_e__git_ref_t(PyObject *lib)
{
  if ((GIT_REF_INVALID) < 0 || (unsigned long)(GIT_REF_INVALID) != 0UL) {
    char buf[64];
    if ((GIT_REF_INVALID) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REF_INVALID));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REF_INVALID));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_ref_t", "GIT_REF_INVALID", buf, "0");
    return -1;
  }
  if ((GIT_REF_OID) < 0 || (unsigned long)(GIT_REF_OID) != 1UL) {
    char buf[64];
    if ((GIT_REF_OID) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REF_OID));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REF_OID));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_ref_t", "GIT_REF_OID", buf, "1");
    return -1;
  }
  if ((GIT_REF_SYMBOLIC) < 0 || (unsigned long)(GIT_REF_SYMBOLIC) != 2UL) {
    char buf[64];
    if ((GIT_REF_SYMBOLIC) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REF_SYMBOLIC));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REF_SYMBOLIC));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_ref_t", "GIT_REF_SYMBOLIC", buf, "2");
    return -1;
  }
  if ((GIT_REF_LISTALL) < 0 || (unsigned long)(GIT_REF_LISTALL) != 3UL) {
    char buf[64];
    if ((GIT_REF_LISTALL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REF_LISTALL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REF_LISTALL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_ref_t", "GIT_REF_LISTALL", buf, "3");
    return -1;
  }
  return _cffi_e__git_error_code(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_BARE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_BARE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_BARE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_CREDTYPE_DEFAULT(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_NO_REINIT(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_NO_REINIT);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_NO_REINIT", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_BARE(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_NO_DOTGIT_DIR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_NO_DOTGIT_DIR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_NO_DOTGIT_DIR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_NO_REINIT(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_MKDIR(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_MKDIR);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_MKDIR", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_NO_DOTGIT_DIR(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_MKPATH(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_MKPATH);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_MKPATH", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_MKDIR(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_MKPATH(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_SHARED_UMASK(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_SHARED_UMASK);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_SHARED_UMASK", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_EXTERNAL_TEMPLATE(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_SHARED_GROUP(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_SHARED_GROUP);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_SHARED_GROUP", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_SHARED_UMASK(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_SHARED_ALL(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_SHARED_ALL);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_SHARED_ALL", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_REPOSITORY_INIT_SHARED_GROUP(lib);
}

static void _cffi_check__git_repository_init_options(git_repository_init_options *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->flags) << 1);
  (void)((p->mode) << 1);
  { char const * *tmp = &p->workdir_path; (void)tmp; }
  { char const * *tmp = &p->description; (void)tmp; }
  { char const * *tmp = &p->template_path; (void)tmp; }
  { char const * *tmp = &p->initial_head; (void)tmp; }
  { char const * *tmp = &p->origin_url; (void)tmp; }
}
static PyObject *
_cffi_layout__git_repository_init_options(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; git_repository_init_options y; };
  static Py_ssize_t nums[] = {
    sizeof(git_repository_init_options),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(git_repository_init_options, version),
    sizeof(((git_repository_init_options *)0)->version),
    offsetof(git_repository_init_options, flags),
    sizeof(((git_repository_init_options *)0)->flags),
    offsetof(git_repository_init_options, mode),
    sizeof(((git_repository_init_options *)0)->mode),
    offsetof(git_repository_init_options, workdir_path),
    sizeof(((git_repository_init_options *)0)->workdir_path),
    offsetof(git_repository_init_options, description),
    sizeof(((git_repository_init_options *)0)->description),
    offsetof(git_repository_init_options, template_path),
    sizeof(((git_repository_init_options *)0)->template_path),
    offsetof(git_repository_init_options, initial_head),
    sizeof(((git_repository_init_options *)0)->initial_head),
    offsetof(git_repository_init_options, origin_url),
    sizeof(((git_repository_init_options *)0)->origin_url),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__git_repository_init_options(0);
}

static int _cffi_e__git_submodule_ignore_t(PyObject *lib)
{
  if ((GIT_SUBMODULE_IGNORE_RESET) >= 0 || (long)(GIT_SUBMODULE_IGNORE_RESET) != -1L) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_RESET) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_RESET));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_RESET));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_RESET", buf, "-1");
    return -1;
  }
  if ((GIT_SUBMODULE_IGNORE_NONE) < 0 || (unsigned long)(GIT_SUBMODULE_IGNORE_NONE) != 1UL) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_NONE) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_NONE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_NONE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_NONE", buf, "1");
    return -1;
  }
  if ((GIT_SUBMODULE_IGNORE_UNTRACKED) < 0 || (unsigned long)(GIT_SUBMODULE_IGNORE_UNTRACKED) != 2UL) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_UNTRACKED) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_UNTRACKED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_UNTRACKED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_UNTRACKED", buf, "2");
    return -1;
  }
  if ((GIT_SUBMODULE_IGNORE_DIRTY) < 0 || (unsigned long)(GIT_SUBMODULE_IGNORE_DIRTY) != 3UL) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_DIRTY) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_DIRTY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_DIRTY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_DIRTY", buf, "3");
    return -1;
  }
  if ((GIT_SUBMODULE_IGNORE_ALL) < 0 || (unsigned long)(GIT_SUBMODULE_IGNORE_ALL) != 4UL) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_ALL) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_ALL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_ALL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_ALL", buf, "4");
    return -1;
  }
  if ((GIT_SUBMODULE_IGNORE_DEFAULT) < 0 || (unsigned long)(GIT_SUBMODULE_IGNORE_DEFAULT) != 0UL) {
    char buf[64];
    if ((GIT_SUBMODULE_IGNORE_DEFAULT) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_SUBMODULE_IGNORE_DEFAULT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_SUBMODULE_IGNORE_DEFAULT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_submodule_ignore_t", "GIT_SUBMODULE_IGNORE_DEFAULT", buf, "0");
    return -1;
  }
  return _cffi_e__git_ref_t(lib);
}

static int _cffi_e_enum_git_remote_completion_type(PyObject *lib)
{
  if ((GIT_REMOTE_COMPLETION_DOWNLOAD) < 0 || (unsigned long)(GIT_REMOTE_COMPLETION_DOWNLOAD) != 0UL) {
    char buf[64];
    if ((GIT_REMOTE_COMPLETION_DOWNLOAD) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REMOTE_COMPLETION_DOWNLOAD));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REMOTE_COMPLETION_DOWNLOAD));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_remote_completion_type", "GIT_REMOTE_COMPLETION_DOWNLOAD", buf, "0");
    return -1;
  }
  if ((GIT_REMOTE_COMPLETION_INDEXING) < 0 || (unsigned long)(GIT_REMOTE_COMPLETION_INDEXING) != 1UL) {
    char buf[64];
    if ((GIT_REMOTE_COMPLETION_INDEXING) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REMOTE_COMPLETION_INDEXING));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REMOTE_COMPLETION_INDEXING));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_remote_completion_type", "GIT_REMOTE_COMPLETION_INDEXING", buf, "1");
    return -1;
  }
  if ((GIT_REMOTE_COMPLETION_ERROR) < 0 || (unsigned long)(GIT_REMOTE_COMPLETION_ERROR) != 2UL) {
    char buf[64];
    if ((GIT_REMOTE_COMPLETION_ERROR) < 0)
        snprintf(buf, 63, "%ld", (long)(GIT_REMOTE_COMPLETION_ERROR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GIT_REMOTE_COMPLETION_ERROR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "git_remote_completion_type", "GIT_REMOTE_COMPLETION_ERROR", buf, "2");
    return -1;
  }
  return _cffi_e__git_submodule_ignore_t(lib);
}

static PyObject *
_cffi_f_git_blame_file(PyObject *self, PyObject *args)
{
  git_blame * * x0;
  git_repository * x1;
  char const * x2;
  git_blame_options * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_blame_file", &arg0, &arg1, &arg2, &arg3))
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(3), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_blame_file(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_blame_free(PyObject *self, PyObject *arg0)
{
  git_blame * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_blame_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_blame_get_hunk_byindex(PyObject *self, PyObject *args)
{
  git_blame * x0;
  uint32_t x1;
  Py_ssize_t datasize;
  git_blame_hunk const * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_blame_get_hunk_byindex", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, uint32_t);
  if (x1 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_blame_get_hunk_byindex(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(6));
}

static PyObject *
_cffi_f_git_blame_get_hunk_byline(PyObject *self, PyObject *args)
{
  git_blame * x0;
  uint32_t x1;
  Py_ssize_t datasize;
  git_blame_hunk const * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_blame_get_hunk_byline", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, uint32_t);
  if (x1 == (uint32_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_blame_get_hunk_byline(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(6));
}

static PyObject *
_cffi_f_git_blame_get_hunk_count(PyObject *self, PyObject *arg0)
{
  git_blame * x0;
  Py_ssize_t datasize;
  uint32_t result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_blame_get_hunk_count(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, uint32_t);
}

static PyObject *
_cffi_f_git_blame_init_options(PyObject *self, PyObject *args)
{
  git_blame_options * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_blame_init_options", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_blame_init_options(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_buf_free(PyObject *self, PyObject *arg0)
{
  git_buf * x0;
  Py_ssize_t datasize;

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
  { git_buf_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_checkout_head(PyObject *self, PyObject *args)
{
  git_repository * x0;
  git_checkout_options const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_checkout_head", &arg0, &arg1))
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
  { result = git_checkout_head(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_checkout_index(PyObject *self, PyObject *args)
{
  git_repository * x0;
  git_index * x1;
  git_checkout_options const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_checkout_index", &arg0, &arg1, &arg2))
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
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(8), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_checkout_index(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_checkout_init_options(PyObject *self, PyObject *args)
{
  git_checkout_options * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_checkout_init_options", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(10), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(10), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_checkout_init_options(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_checkout_tree(PyObject *self, PyObject *args)
{
  git_repository * x0;
  git_object const * x1;
  git_checkout_options const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_checkout_tree", &arg0, &arg1, &arg2))
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
      _cffi_type(11), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(11), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(8), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_checkout_tree(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_clone(PyObject *self, PyObject *args)
{
  git_repository * * x0;
  char const * x1;
  char const * x2;
  git_clone_options const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_clone", &arg0, &arg1, &arg2, &arg3))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(13), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(13), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_clone(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_clone_init_options(PyObject *self, PyObject *args)
{
  git_clone_options * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_clone_init_options", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_clone_init_options(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_clone_into(PyObject *self, PyObject *args)
{
  git_repository * x0;
  git_remote * x1;
  git_checkout_options const * x2;
  char const * x3;
  git_signature const * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:git_clone_into", &arg0, &arg1, &arg2, &arg3, &arg4))
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(8), arg2) < 0)
      return NULL;
  }

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
      _cffi_type(16), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(16), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_clone_into(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_add_file_ondisk(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  git_config_level_t x2;
  int x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_config_add_file_ondisk", &arg0, &arg1, &arg2, &arg3))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x2, _cffi_type(18), arg2) < 0)
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_add_file_ondisk(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_delete_entry(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_delete_entry", &arg0, &arg1))
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
  { result = git_config_delete_entry(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_find_global(PyObject *self, PyObject *arg0)
{
  git_buf * x0;
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
  { result = git_config_find_global(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_find_system(PyObject *self, PyObject *arg0)
{
  git_buf * x0;
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
  { result = git_config_find_system(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_find_xdg(PyObject *self, PyObject *arg0)
{
  git_buf * x0;
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
  { result = git_config_find_xdg(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_free(PyObject *self, PyObject *arg0)
{
  git_config * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_config_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_config_get_string(PyObject *self, PyObject *args)
{
  char const * * x0;
  git_config const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_config_get_string", &arg0, &arg1, &arg2))
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
      _cffi_type(20), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(20), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_get_string(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_iterator_free(PyObject *self, PyObject *arg0)
{
  git_config_iterator * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(21), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(21), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_config_iterator_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_config_iterator_new(PyObject *self, PyObject *args)
{
  git_config_iterator * * x0;
  git_config const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_iterator_new", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(22), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(22), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(20), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(20), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_iterator_new(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_multivar_iterator_new(PyObject *self, PyObject *args)
{
  git_config_iterator * * x0;
  git_config const * x1;
  char const * x2;
  char const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_config_multivar_iterator_new", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(22), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(22), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(20), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(20), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_multivar_iterator_new(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_new(PyObject *self, PyObject *arg0)
{
  git_config * * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(23), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_next(PyObject *self, PyObject *args)
{
  git_config_entry * * x0;
  git_config_iterator * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_next", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(24), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(24), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(21), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(21), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_next(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_open_ondisk(PyObject *self, PyObject *args)
{
  git_config * * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_open_ondisk", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(23), arg0) < 0)
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
  { result = git_config_open_ondisk(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_parse_bool(PyObject *self, PyObject *args)
{
  int * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_parse_bool", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(25), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(25), arg0) < 0)
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
  { result = git_config_parse_bool(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_parse_int64(PyObject *self, PyObject *args)
{
  int64_t * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_parse_int64", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(26), arg0) < 0)
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
  { result = git_config_parse_int64(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_set_bool(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_config_set_bool", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_set_bool(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_set_int64(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  int64_t x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_config_set_int64", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int64_t);
  if (x2 == (int64_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_set_int64(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_set_multivar(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  char const * x2;
  char const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_config_set_multivar", &arg0, &arg1, &arg2, &arg3))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_set_multivar(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_set_string(PyObject *self, PyObject *args)
{
  git_config * x0;
  char const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_config_set_string", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_set_string(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_config_snapshot(PyObject *self, PyObject *args)
{
  git_config * * x0;
  git_config * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_config_snapshot", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(23), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(17), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(17), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_config_snapshot(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_cred_ssh_key_new(PyObject *self, PyObject *args)
{
  git_cred * * x0;
  char const * x1;
  char const * x2;
  char const * x3;
  char const * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:git_cred_ssh_key_new", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(27), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(27), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_cred_ssh_key_new(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_cred_userpass_plaintext_new(PyObject *self, PyObject *args)
{
  git_cred * * x0;
  char const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_cred_userpass_plaintext_new", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(27), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(27), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_cred_userpass_plaintext_new(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_diff_index_to_workdir(PyObject *self, PyObject *args)
{
  git_diff * * x0;
  git_repository * x1;
  git_index * x2;
  git_diff_options const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_diff_index_to_workdir", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(9), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(29), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(29), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_diff_index_to_workdir(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_diff_init_options(PyObject *self, PyObject *args)
{
  git_diff_options * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_diff_init_options", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(30), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(30), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_diff_init_options(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_diff_tree_to_index(PyObject *self, PyObject *args)
{
  git_diff * * x0;
  git_repository * x1;
  git_tree * x2;
  git_index * x3;
  git_diff_options const * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:git_diff_tree_to_index", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(28), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(28), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(31), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(31), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(9), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(29), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(29), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_diff_tree_to_index(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_add(PyObject *self, PyObject *args)
{
  git_index * x0;
  git_index_entry const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_add", &arg0, &arg1))
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
      _cffi_type(32), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(32), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_add(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_add_all(PyObject *self, PyObject *args)
{
  git_index * x0;
  git_strarray const * x1;
  unsigned int x2;
  int(* x3)(char const *, char const *, void *);
  void * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:git_index_add_all", &arg0, &arg1, &arg2, &arg3, &arg4))
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
      _cffi_type(33), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(33), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, unsigned int);
  if (x2 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  x3 = (int(*)(char const *, char const *, void *))_cffi_to_c_pointer(arg3, _cffi_type(34));
  if (x3 == (int(*)(char const *, char const *, void *))NULL && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(35), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(35), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_add_all(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_add_bypath(PyObject *self, PyObject *args)
{
  git_index * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_add_bypath", &arg0, &arg1))
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
  { result = git_index_add_bypath(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_clear(PyObject *self, PyObject *arg0)
{
  git_index * x0;
  Py_ssize_t datasize;
  int result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_clear(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_conflict_get(PyObject *self, PyObject *args)
{
  git_index_entry const * * x0;
  git_index_entry const * * x1;
  git_index_entry const * * x2;
  git_index * x3;
  char const * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:git_index_conflict_get", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(36), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(36), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(36), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(9), arg3) < 0)
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_conflict_get(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_conflict_iterator_free(PyObject *self, PyObject *arg0)
{
  git_index_conflict_iterator * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(37), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(37), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_index_conflict_iterator_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_index_conflict_iterator_new(PyObject *self, PyObject *args)
{
  git_index_conflict_iterator * * x0;
  git_index * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_conflict_iterator_new", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(38), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(38), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_conflict_iterator_new(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_conflict_next(PyObject *self, PyObject *args)
{
  git_index_entry const * * x0;
  git_index_entry const * * x1;
  git_index_entry const * * x2;
  git_index_conflict_iterator * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_index_conflict_next", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(36), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(36), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(36), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(36), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(37), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(37), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_conflict_next(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_conflict_remove(PyObject *self, PyObject *args)
{
  git_index * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_conflict_remove", &arg0, &arg1))
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
  { result = git_index_conflict_remove(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_entrycount(PyObject *self, PyObject *arg0)
{
  git_index const * x0;
  Py_ssize_t datasize;
  size_t result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(39), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(39), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_entrycount(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_git_index_find(PyObject *self, PyObject *args)
{
  size_t * x0;
  git_index * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_index_find", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(40), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(40), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_find(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_free(PyObject *self, PyObject *arg0)
{
  git_index * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_index_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_index_get_byindex(PyObject *self, PyObject *args)
{
  git_index * x0;
  size_t x1;
  Py_ssize_t datasize;
  git_index_entry const * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_get_byindex", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, size_t);
  if (x1 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_get_byindex(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(32));
}

static PyObject *
_cffi_f_git_index_get_bypath(PyObject *self, PyObject *args)
{
  git_index * x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  git_index_entry const * result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_index_get_bypath", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_get_bypath(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(32));
}

static PyObject *
_cffi_f_git_index_has_conflicts(PyObject *self, PyObject *arg0)
{
  git_index const * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(39), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(39), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_has_conflicts(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_open(PyObject *self, PyObject *args)
{
  git_index * * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_open", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(41), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(41), arg0) < 0)
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
  { result = git_index_open(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_read(PyObject *self, PyObject *args)
{
  git_index * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_read", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_read(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_read_tree(PyObject *self, PyObject *args)
{
  git_index * x0;
  git_tree const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_read_tree", &arg0, &arg1))
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
      _cffi_type(42), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(42), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_read_tree(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_remove(PyObject *self, PyObject *args)
{
  git_index * x0;
  char const * x1;
  int x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_index_remove", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_remove(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_write(PyObject *self, PyObject *arg0)
{
  git_index * x0;
  Py_ssize_t datasize;
  int result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_write(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_write_tree(PyObject *self, PyObject *args)
{
  git_oid * x0;
  git_index * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_index_write_tree", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(43), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(43), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_write_tree(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_index_write_tree_to(PyObject *self, PyObject *args)
{
  git_oid * x0;
  git_index * x1;
  git_repository * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_index_write_tree_to", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(43), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(43), arg0) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(1), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_index_write_tree_to(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_add_refspec(PyObject *self, PyObject *args)
{
  git_push * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_push_add_refspec", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
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
  { result = git_push_add_refspec(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_finish(PyObject *self, PyObject *arg0)
{
  git_push * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_push_finish(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_free(PyObject *self, PyObject *arg0)
{
  git_push * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_push_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_push_new(PyObject *self, PyObject *args)
{
  git_push * * x0;
  git_remote * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_push_new", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(45), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(45), arg0) < 0)
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
  { result = git_push_new(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_status_foreach(PyObject *self, PyObject *args)
{
  git_push * x0;
  int(* x1)(char const *, char const *, void *);
  void * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_push_status_foreach", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
      return NULL;
  }

  x1 = (int(*)(char const *, char const *, void *))_cffi_to_c_pointer(arg1, _cffi_type(34));
  if (x1 == (int(*)(char const *, char const *, void *))NULL && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(35), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(35), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_push_status_foreach(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_unpack_ok(PyObject *self, PyObject *arg0)
{
  git_push * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_push_unpack_ok(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_push_update_tips(PyObject *self, PyObject *args)
{
  git_push * x0;
  git_signature const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_push_update_tips", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(44), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(44), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_push_update_tips(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_refspec_direction(PyObject *self, PyObject *arg0)
{
  git_refspec const * x0;
  Py_ssize_t datasize;
  git_direction result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_direction(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_deref((char *)&result, _cffi_type(47));
}

static PyObject *
_cffi_f_git_refspec_dst(PyObject *self, PyObject *arg0)
{
  git_refspec const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_dst(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_refspec_dst_matches(PyObject *self, PyObject *args)
{
  git_refspec const * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_refspec_dst_matches", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
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
  { result = git_refspec_dst_matches(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_refspec_force(PyObject *self, PyObject *arg0)
{
  git_refspec const * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_force(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_refspec_rtransform(PyObject *self, PyObject *args)
{
  git_buf * x0;
  git_refspec const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_refspec_rtransform", &arg0, &arg1, &arg2))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(46), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_rtransform(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_refspec_src(PyObject *self, PyObject *arg0)
{
  git_refspec const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_src(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_refspec_src_matches(PyObject *self, PyObject *args)
{
  git_refspec const * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_refspec_src_matches", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
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
  { result = git_refspec_src_matches(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_refspec_string(PyObject *self, PyObject *arg0)
{
  git_refspec const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(46), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_string(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_refspec_transform(PyObject *self, PyObject *args)
{
  git_buf * x0;
  git_refspec const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_refspec_transform", &arg0, &arg1, &arg2))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(46), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(46), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_refspec_transform(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_add_fetch(PyObject *self, PyObject *args)
{
  git_remote * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_add_fetch", &arg0, &arg1))
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
  { result = git_remote_add_fetch(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_add_push(PyObject *self, PyObject *args)
{
  git_remote * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_add_push", &arg0, &arg1))
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
  { result = git_remote_add_push(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_create(PyObject *self, PyObject *args)
{
  git_remote * * x0;
  git_repository * x1;
  char const * x2;
  char const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_remote_create", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(48), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(48), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_create(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_delete(PyObject *self, PyObject *arg0)
{
  git_remote * x0;
  Py_ssize_t datasize;
  int result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_delete(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_fetch(PyObject *self, PyObject *args)
{
  git_remote * x0;
  git_signature const * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_remote_fetch", &arg0, &arg1, &arg2))
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_fetch(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_free(PyObject *self, PyObject *arg0)
{
  git_remote * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_remote_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_remote_get_fetch_refspecs(PyObject *self, PyObject *args)
{
  git_strarray * x0;
  git_remote * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_get_fetch_refspecs", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(49), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(49), arg0) < 0)
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
  { result = git_remote_get_fetch_refspecs(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_get_push_refspecs(PyObject *self, PyObject *args)
{
  git_strarray * x0;
  git_remote * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_get_push_refspecs", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(49), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(49), arg0) < 0)
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
  { result = git_remote_get_push_refspecs(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_get_refspec(PyObject *self, PyObject *args)
{
  git_remote * x0;
  size_t x1;
  Py_ssize_t datasize;
  git_refspec const * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_get_refspec", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, size_t);
  if (x1 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_get_refspec(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(46));
}

static PyObject *
_cffi_f_git_remote_init_callbacks(PyObject *self, PyObject *args)
{
  git_remote_callbacks * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_init_callbacks", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(50), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(50), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_init_callbacks(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_list(PyObject *self, PyObject *args)
{
  git_strarray * x0;
  git_repository * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_list", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(49), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(49), arg0) < 0)
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_list(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_load(PyObject *self, PyObject *args)
{
  git_remote * * x0;
  git_repository * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_remote_load", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(48), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(48), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_load(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_name(PyObject *self, PyObject *arg0)
{
  git_remote const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(51), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(51), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_name(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_remote_pushurl(PyObject *self, PyObject *arg0)
{
  git_remote const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(51), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(51), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_pushurl(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_remote_refspec_count(PyObject *self, PyObject *arg0)
{
  git_remote * x0;
  Py_ssize_t datasize;
  size_t result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_refspec_count(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, size_t);
}

static PyObject *
_cffi_f_git_remote_rename(PyObject *self, PyObject *args)
{
  git_strarray * x0;
  git_remote * x1;
  char const * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_remote_rename", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(49), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(49), arg0) < 0)
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(2), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(2), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_rename(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_save(PyObject *self, PyObject *arg0)
{
  git_remote const * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(51), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(51), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_save(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_set_callbacks(PyObject *self, PyObject *args)
{
  git_remote * x0;
  git_remote_callbacks const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_set_callbacks", &arg0, &arg1))
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
      _cffi_type(52), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(52), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_set_callbacks(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_set_fetch_refspecs(PyObject *self, PyObject *args)
{
  git_remote * x0;
  git_strarray * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_set_fetch_refspecs", &arg0, &arg1))
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
      _cffi_type(49), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(49), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_set_fetch_refspecs(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_set_push_refspecs(PyObject *self, PyObject *args)
{
  git_remote * x0;
  git_strarray * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_set_push_refspecs", &arg0, &arg1))
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
      _cffi_type(49), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(49), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_set_push_refspecs(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_set_pushurl(PyObject *self, PyObject *args)
{
  git_remote * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_set_pushurl", &arg0, &arg1))
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
  { result = git_remote_set_pushurl(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_set_url(PyObject *self, PyObject *args)
{
  git_remote * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_remote_set_url", &arg0, &arg1))
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
  { result = git_remote_set_url(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_remote_stats(PyObject *self, PyObject *arg0)
{
  git_remote * x0;
  Py_ssize_t datasize;
  git_transfer_progress const * result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_stats(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(53));
}

static PyObject *
_cffi_f_git_remote_url(PyObject *self, PyObject *arg0)
{
  git_remote const * x0;
  Py_ssize_t datasize;
  char const * result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(51), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(51), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_remote_url(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(2));
}

static PyObject *
_cffi_f_git_repository_config(PyObject *self, PyObject *args)
{
  git_config * * x0;
  git_repository * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_repository_config", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(23), arg0) < 0)
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_config(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_config_snapshot(PyObject *self, PyObject *args)
{
  git_config * * x0;
  git_repository * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_repository_config_snapshot", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(23), arg0) < 0)
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_config_snapshot(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_free(PyObject *self, PyObject *arg0)
{
  git_repository * x0;
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
  { git_repository_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_git_repository_index(PyObject *self, PyObject *args)
{
  git_index * * x0;
  git_repository * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_repository_index", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(41), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(41), arg0) < 0)
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_index(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_init(PyObject *self, PyObject *args)
{
  git_repository * * x0;
  char const * x1;
  unsigned int x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_repository_init", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, unsigned int);
  if (x2 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_init(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_init_ext(PyObject *self, PyObject *args)
{
  git_repository * * x0;
  char const * x1;
  git_repository_init_options * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:git_repository_init_ext", &arg0, &arg1, &arg2))
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
      _cffi_type(2), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(2), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(54), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(54), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_init_ext(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_init_init_options(PyObject *self, PyObject *args)
{
  git_repository_init_options * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:git_repository_init_init_options", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(54), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(54), arg0) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_init_init_options(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_set_head(PyObject *self, PyObject *args)
{
  git_repository * x0;
  char const * x1;
  git_signature const * x2;
  char const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_repository_set_head", &arg0, &arg1, &arg2, &arg3))
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(16), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(16), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_set_head(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_set_head_detached(PyObject *self, PyObject *args)
{
  git_repository * x0;
  git_oid const * x1;
  git_signature const * x2;
  char const * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:git_repository_set_head_detached", &arg0, &arg1, &arg2, &arg3))
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
      _cffi_type(55), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(55), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(16), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(16), arg2) < 0)
      return NULL;
  }

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = git_repository_set_head_detached(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_repository_state_cleanup(PyObject *self, PyObject *arg0)
{
  git_repository * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = git_repository_state_cleanup(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_git_strarray_free(PyObject *self, PyObject *arg0)
{
  git_strarray * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(49), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(49), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { git_strarray_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_giterr_last(PyObject *self, PyObject *no_arg)
{
  git_error const * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = giterr_last(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(56));
}

static int _cffi_const_GIT_BLAME_OPTIONS_VERSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_BLAME_OPTIONS_VERSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_BLAME_OPTIONS_VERSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_e_enum_git_remote_completion_type(lib);
}

static int _cffi_const_GIT_CLONE_OPTIONS_VERSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_CLONE_OPTIONS_VERSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_CLONE_OPTIONS_VERSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_BLAME_OPTIONS_VERSION(lib);
}

static int _cffi_const_GIT_OID_RAWSZ(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_OID_RAWSZ);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_OID_RAWSZ", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_CLONE_OPTIONS_VERSION(lib);
}

static int _cffi_const_GIT_PATH_MAX(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_PATH_MAX);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_PATH_MAX", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_OID_RAWSZ(lib);
}

static int _cffi_const_GIT_REPOSITORY_INIT_OPTIONS_VERSION(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(GIT_REPOSITORY_INIT_OPTIONS_VERSION);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "GIT_REPOSITORY_INIT_OPTIONS_VERSION", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return _cffi_const_GIT_PATH_MAX(lib);
}

static void _cffi_check_struct_git_blame_hunk(struct git_blame_hunk *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->lines_in_hunk) << 1);
  { git_oid *tmp = &p->final_commit_id; (void)tmp; }
  (void)((p->final_start_line_number) << 1);
  { git_signature * *tmp = &p->final_signature; (void)tmp; }
  { git_oid *tmp = &p->orig_commit_id; (void)tmp; }
  { char const * *tmp = &p->orig_path; (void)tmp; }
  (void)((p->orig_start_line_number) << 1);
  { git_signature * *tmp = &p->orig_signature; (void)tmp; }
  { char *tmp = &p->boundary; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_blame_hunk(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_blame_hunk y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_blame_hunk),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_blame_hunk, lines_in_hunk),
    sizeof(((struct git_blame_hunk *)0)->lines_in_hunk),
    offsetof(struct git_blame_hunk, final_commit_id),
    sizeof(((struct git_blame_hunk *)0)->final_commit_id),
    offsetof(struct git_blame_hunk, final_start_line_number),
    sizeof(((struct git_blame_hunk *)0)->final_start_line_number),
    offsetof(struct git_blame_hunk, final_signature),
    sizeof(((struct git_blame_hunk *)0)->final_signature),
    offsetof(struct git_blame_hunk, orig_commit_id),
    sizeof(((struct git_blame_hunk *)0)->orig_commit_id),
    offsetof(struct git_blame_hunk, orig_path),
    sizeof(((struct git_blame_hunk *)0)->orig_path),
    offsetof(struct git_blame_hunk, orig_start_line_number),
    sizeof(((struct git_blame_hunk *)0)->orig_start_line_number),
    offsetof(struct git_blame_hunk, orig_signature),
    sizeof(((struct git_blame_hunk *)0)->orig_signature),
    offsetof(struct git_blame_hunk, boundary),
    sizeof(((struct git_blame_hunk *)0)->boundary),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_blame_hunk(0);
}

static void _cffi_check_struct_git_blame_options(struct git_blame_options *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->flags) << 1);
  (void)((p->min_match_characters) << 1);
  { git_oid *tmp = &p->newest_commit; (void)tmp; }
  { git_oid *tmp = &p->oldest_commit; (void)tmp; }
  (void)((p->min_line) << 1);
  (void)((p->max_line) << 1);
}
static PyObject *
_cffi_layout_struct_git_blame_options(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_blame_options y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_blame_options),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_blame_options, version),
    sizeof(((struct git_blame_options *)0)->version),
    offsetof(struct git_blame_options, flags),
    sizeof(((struct git_blame_options *)0)->flags),
    offsetof(struct git_blame_options, min_match_characters),
    sizeof(((struct git_blame_options *)0)->min_match_characters),
    offsetof(struct git_blame_options, newest_commit),
    sizeof(((struct git_blame_options *)0)->newest_commit),
    offsetof(struct git_blame_options, oldest_commit),
    sizeof(((struct git_blame_options *)0)->oldest_commit),
    offsetof(struct git_blame_options, min_line),
    sizeof(((struct git_blame_options *)0)->min_line),
    offsetof(struct git_blame_options, max_line),
    sizeof(((struct git_blame_options *)0)->max_line),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_blame_options(0);
}

static void _cffi_check_struct_git_checkout_options(struct git_checkout_options *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  (void)((p->checkout_strategy) << 1);
  (void)((p->disable_filters) << 1);
  (void)((p->dir_mode) << 1);
  (void)((p->file_mode) << 1);
  (void)((p->file_open_flags) << 1);
  (void)((p->notify_flags) << 1);
  { int(* *tmp)(git_checkout_notify_t, char const *, git_diff_file const *, git_diff_file const *, git_diff_file const *, void *) = &p->notify_cb; (void)tmp; }
  { void * *tmp = &p->notify_payload; (void)tmp; }
  { void(* *tmp)(char const *, size_t, size_t, void *) = &p->progress_cb; (void)tmp; }
  { void * *tmp = &p->progress_payload; (void)tmp; }
  { git_strarray *tmp = &p->paths; (void)tmp; }
  { git_tree * *tmp = &p->baseline; (void)tmp; }
  { char const * *tmp = &p->target_directory; (void)tmp; }
  { char const * *tmp = &p->ancestor_label; (void)tmp; }
  { char const * *tmp = &p->our_label; (void)tmp; }
  { char const * *tmp = &p->their_label; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_checkout_options(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_checkout_options y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_checkout_options),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_checkout_options, version),
    sizeof(((struct git_checkout_options *)0)->version),
    offsetof(struct git_checkout_options, checkout_strategy),
    sizeof(((struct git_checkout_options *)0)->checkout_strategy),
    offsetof(struct git_checkout_options, disable_filters),
    sizeof(((struct git_checkout_options *)0)->disable_filters),
    offsetof(struct git_checkout_options, dir_mode),
    sizeof(((struct git_checkout_options *)0)->dir_mode),
    offsetof(struct git_checkout_options, file_mode),
    sizeof(((struct git_checkout_options *)0)->file_mode),
    offsetof(struct git_checkout_options, file_open_flags),
    sizeof(((struct git_checkout_options *)0)->file_open_flags),
    offsetof(struct git_checkout_options, notify_flags),
    sizeof(((struct git_checkout_options *)0)->notify_flags),
    offsetof(struct git_checkout_options, notify_cb),
    sizeof(((struct git_checkout_options *)0)->notify_cb),
    offsetof(struct git_checkout_options, notify_payload),
    sizeof(((struct git_checkout_options *)0)->notify_payload),
    offsetof(struct git_checkout_options, progress_cb),
    sizeof(((struct git_checkout_options *)0)->progress_cb),
    offsetof(struct git_checkout_options, progress_payload),
    sizeof(((struct git_checkout_options *)0)->progress_payload),
    offsetof(struct git_checkout_options, paths),
    sizeof(((struct git_checkout_options *)0)->paths),
    offsetof(struct git_checkout_options, baseline),
    sizeof(((struct git_checkout_options *)0)->baseline),
    offsetof(struct git_checkout_options, target_directory),
    sizeof(((struct git_checkout_options *)0)->target_directory),
    offsetof(struct git_checkout_options, ancestor_label),
    sizeof(((struct git_checkout_options *)0)->ancestor_label),
    offsetof(struct git_checkout_options, our_label),
    sizeof(((struct git_checkout_options *)0)->our_label),
    offsetof(struct git_checkout_options, their_label),
    sizeof(((struct git_checkout_options *)0)->their_label),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_checkout_options(0);
}

static void _cffi_check_struct_git_clone_options(struct git_clone_options *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  { git_checkout_options *tmp = &p->checkout_opts; (void)tmp; }
  { git_remote_callbacks *tmp = &p->remote_callbacks; (void)tmp; }
  (void)((p->bare) << 1);
  (void)((p->ignore_cert_errors) << 1);
  { git_clone_local_t *tmp = &p->local; (void)tmp; }
  { char const * *tmp = &p->remote_name; (void)tmp; }
  { char const * *tmp = &p->checkout_branch; (void)tmp; }
  { git_signature * *tmp = &p->signature; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_clone_options(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_clone_options y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_clone_options),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_clone_options, version),
    sizeof(((struct git_clone_options *)0)->version),
    offsetof(struct git_clone_options, checkout_opts),
    sizeof(((struct git_clone_options *)0)->checkout_opts),
    offsetof(struct git_clone_options, remote_callbacks),
    sizeof(((struct git_clone_options *)0)->remote_callbacks),
    offsetof(struct git_clone_options, bare),
    sizeof(((struct git_clone_options *)0)->bare),
    offsetof(struct git_clone_options, ignore_cert_errors),
    sizeof(((struct git_clone_options *)0)->ignore_cert_errors),
    offsetof(struct git_clone_options, local),
    sizeof(((struct git_clone_options *)0)->local),
    offsetof(struct git_clone_options, remote_name),
    sizeof(((struct git_clone_options *)0)->remote_name),
    offsetof(struct git_clone_options, checkout_branch),
    sizeof(((struct git_clone_options *)0)->checkout_branch),
    offsetof(struct git_clone_options, signature),
    sizeof(((struct git_clone_options *)0)->signature),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_clone_options(0);
}

static void _cffi_check_struct_git_index_entry(struct git_index_entry *p)
{
  /* only to generate compile-time warnings or errors */
  { git_index_time *tmp = &p->ctime; (void)tmp; }
  { git_index_time *tmp = &p->mtime; (void)tmp; }
  (void)((p->dev) << 1);
  (void)((p->ino) << 1);
  (void)((p->mode) << 1);
  (void)((p->uid) << 1);
  (void)((p->gid) << 1);
  (void)((p->file_size) << 1);
  { git_oid *tmp = &p->id; (void)tmp; }
  (void)((p->flags) << 1);
  (void)((p->flags_extended) << 1);
  { char const * *tmp = &p->path; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_index_entry(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_index_entry y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_index_entry),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_index_entry, ctime),
    sizeof(((struct git_index_entry *)0)->ctime),
    offsetof(struct git_index_entry, mtime),
    sizeof(((struct git_index_entry *)0)->mtime),
    offsetof(struct git_index_entry, dev),
    sizeof(((struct git_index_entry *)0)->dev),
    offsetof(struct git_index_entry, ino),
    sizeof(((struct git_index_entry *)0)->ino),
    offsetof(struct git_index_entry, mode),
    sizeof(((struct git_index_entry *)0)->mode),
    offsetof(struct git_index_entry, uid),
    sizeof(((struct git_index_entry *)0)->uid),
    offsetof(struct git_index_entry, gid),
    sizeof(((struct git_index_entry *)0)->gid),
    offsetof(struct git_index_entry, file_size),
    sizeof(((struct git_index_entry *)0)->file_size),
    offsetof(struct git_index_entry, id),
    sizeof(((struct git_index_entry *)0)->id),
    offsetof(struct git_index_entry, flags),
    sizeof(((struct git_index_entry *)0)->flags),
    offsetof(struct git_index_entry, flags_extended),
    sizeof(((struct git_index_entry *)0)->flags_extended),
    offsetof(struct git_index_entry, path),
    sizeof(((struct git_index_entry *)0)->path),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_index_entry(0);
}

static void _cffi_check_struct_git_oid(struct git_oid *p)
{
  /* only to generate compile-time warnings or errors */
  { unsigned char(*tmp)[20] = &p->id; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_oid(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_oid y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_oid),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_oid, id),
    sizeof(((struct git_oid *)0)->id),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_oid(0);
}

static void _cffi_check_struct_git_remote_callbacks(struct git_remote_callbacks *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->version) << 1);
  { int(* *tmp)(char const *, int, void *) = &p->sideband_progress; (void)tmp; }
  { int(* *tmp)(git_remote_completion_type, void *) = &p->completion; (void)tmp; }
  { int(* *tmp)(git_cred * *, char const *, char const *, unsigned int, void *) = &p->credentials; (void)tmp; }
  { int(* *tmp)(git_transfer_progress const *, void *) = &p->transfer_progress; (void)tmp; }
  { int(* *tmp)(char const *, git_oid const *, git_oid const *, void *) = &p->update_tips; (void)tmp; }
  { void * *tmp = &p->payload; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_remote_callbacks(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_remote_callbacks y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_remote_callbacks),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_remote_callbacks, version),
    sizeof(((struct git_remote_callbacks *)0)->version),
    offsetof(struct git_remote_callbacks, sideband_progress),
    sizeof(((struct git_remote_callbacks *)0)->sideband_progress),
    offsetof(struct git_remote_callbacks, completion),
    sizeof(((struct git_remote_callbacks *)0)->completion),
    offsetof(struct git_remote_callbacks, credentials),
    sizeof(((struct git_remote_callbacks *)0)->credentials),
    offsetof(struct git_remote_callbacks, transfer_progress),
    sizeof(((struct git_remote_callbacks *)0)->transfer_progress),
    offsetof(struct git_remote_callbacks, update_tips),
    sizeof(((struct git_remote_callbacks *)0)->update_tips),
    offsetof(struct git_remote_callbacks, payload),
    sizeof(((struct git_remote_callbacks *)0)->payload),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_remote_callbacks(0);
}

static void _cffi_check_struct_git_signature(struct git_signature *p)
{
  /* only to generate compile-time warnings or errors */
  { char * *tmp = &p->name; (void)tmp; }
  { char * *tmp = &p->email; (void)tmp; }
  { git_time *tmp = &p->when; (void)tmp; }
}
static PyObject *
_cffi_layout_struct_git_signature(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_signature y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_signature),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_signature, name),
    sizeof(((struct git_signature *)0)->name),
    offsetof(struct git_signature, email),
    sizeof(((struct git_signature *)0)->email),
    offsetof(struct git_signature, when),
    sizeof(((struct git_signature *)0)->when),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_signature(0);
}

static void _cffi_check_struct_git_strarray(struct git_strarray *p)
{
  /* only to generate compile-time warnings or errors */
  { char * * *tmp = &p->strings; (void)tmp; }
  (void)((p->count) << 1);
}
static PyObject *
_cffi_layout_struct_git_strarray(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_strarray y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_strarray),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_strarray, strings),
    sizeof(((struct git_strarray *)0)->strings),
    offsetof(struct git_strarray, count),
    sizeof(((struct git_strarray *)0)->count),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_strarray(0);
}

static void _cffi_check_struct_git_time(struct git_time *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->time) << 1);
  (void)((p->offset) << 1);
}
static PyObject *
_cffi_layout_struct_git_time(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_time y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_time),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_time, time),
    sizeof(((struct git_time *)0)->time),
    offsetof(struct git_time, offset),
    sizeof(((struct git_time *)0)->offset),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_time(0);
}

static void _cffi_check_struct_git_transfer_progress(struct git_transfer_progress *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->total_objects) << 1);
  (void)((p->indexed_objects) << 1);
  (void)((p->received_objects) << 1);
  (void)((p->local_objects) << 1);
  (void)((p->total_deltas) << 1);
  (void)((p->indexed_deltas) << 1);
  (void)((p->received_bytes) << 1);
}
static PyObject *
_cffi_layout_struct_git_transfer_progress(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct git_transfer_progress y; };
  static Py_ssize_t nums[] = {
    sizeof(struct git_transfer_progress),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct git_transfer_progress, total_objects),
    sizeof(((struct git_transfer_progress *)0)->total_objects),
    offsetof(struct git_transfer_progress, indexed_objects),
    sizeof(((struct git_transfer_progress *)0)->indexed_objects),
    offsetof(struct git_transfer_progress, received_objects),
    sizeof(((struct git_transfer_progress *)0)->received_objects),
    offsetof(struct git_transfer_progress, local_objects),
    sizeof(((struct git_transfer_progress *)0)->local_objects),
    offsetof(struct git_transfer_progress, total_deltas),
    sizeof(((struct git_transfer_progress *)0)->total_deltas),
    offsetof(struct git_transfer_progress, indexed_deltas),
    sizeof(((struct git_transfer_progress *)0)->indexed_deltas),
    offsetof(struct git_transfer_progress, received_bytes),
    sizeof(((struct git_transfer_progress *)0)->received_bytes),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_git_transfer_progress(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_GIT_REPOSITORY_INIT_OPTIONS_VERSION(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__git_buf", _cffi_layout__git_buf, METH_NOARGS, NULL},
  {"_cffi_layout__git_config_entry", _cffi_layout__git_config_entry, METH_NOARGS, NULL},
  {"_cffi_layout__git_diff_delta", _cffi_layout__git_diff_delta, METH_NOARGS, NULL},
  {"_cffi_layout__git_diff_file", _cffi_layout__git_diff_file, METH_NOARGS, NULL},
  {"_cffi_layout__git_diff_options", _cffi_layout__git_diff_options, METH_NOARGS, NULL},
  {"_cffi_layout__git_error", _cffi_layout__git_error, METH_NOARGS, NULL},
  {"_cffi_layout__git_index_time", _cffi_layout__git_index_time, METH_NOARGS, NULL},
  {"_cffi_layout__git_repository_init_options", _cffi_layout__git_repository_init_options, METH_NOARGS, NULL},
  {"git_blame_file", _cffi_f_git_blame_file, METH_VARARGS, NULL},
  {"git_blame_free", _cffi_f_git_blame_free, METH_O, NULL},
  {"git_blame_get_hunk_byindex", _cffi_f_git_blame_get_hunk_byindex, METH_VARARGS, NULL},
  {"git_blame_get_hunk_byline", _cffi_f_git_blame_get_hunk_byline, METH_VARARGS, NULL},
  {"git_blame_get_hunk_count", _cffi_f_git_blame_get_hunk_count, METH_O, NULL},
  {"git_blame_init_options", _cffi_f_git_blame_init_options, METH_VARARGS, NULL},
  {"git_buf_free", _cffi_f_git_buf_free, METH_O, NULL},
  {"git_checkout_head", _cffi_f_git_checkout_head, METH_VARARGS, NULL},
  {"git_checkout_index", _cffi_f_git_checkout_index, METH_VARARGS, NULL},
  {"git_checkout_init_options", _cffi_f_git_checkout_init_options, METH_VARARGS, NULL},
  {"git_checkout_tree", _cffi_f_git_checkout_tree, METH_VARARGS, NULL},
  {"git_clone", _cffi_f_git_clone, METH_VARARGS, NULL},
  {"git_clone_init_options", _cffi_f_git_clone_init_options, METH_VARARGS, NULL},
  {"git_clone_into", _cffi_f_git_clone_into, METH_VARARGS, NULL},
  {"git_config_add_file_ondisk", _cffi_f_git_config_add_file_ondisk, METH_VARARGS, NULL},
  {"git_config_delete_entry", _cffi_f_git_config_delete_entry, METH_VARARGS, NULL},
  {"git_config_find_global", _cffi_f_git_config_find_global, METH_O, NULL},
  {"git_config_find_system", _cffi_f_git_config_find_system, METH_O, NULL},
  {"git_config_find_xdg", _cffi_f_git_config_find_xdg, METH_O, NULL},
  {"git_config_free", _cffi_f_git_config_free, METH_O, NULL},
  {"git_config_get_string", _cffi_f_git_config_get_string, METH_VARARGS, NULL},
  {"git_config_iterator_free", _cffi_f_git_config_iterator_free, METH_O, NULL},
  {"git_config_iterator_new", _cffi_f_git_config_iterator_new, METH_VARARGS, NULL},
  {"git_config_multivar_iterator_new", _cffi_f_git_config_multivar_iterator_new, METH_VARARGS, NULL},
  {"git_config_new", _cffi_f_git_config_new, METH_O, NULL},
  {"git_config_next", _cffi_f_git_config_next, METH_VARARGS, NULL},
  {"git_config_open_ondisk", _cffi_f_git_config_open_ondisk, METH_VARARGS, NULL},
  {"git_config_parse_bool", _cffi_f_git_config_parse_bool, METH_VARARGS, NULL},
  {"git_config_parse_int64", _cffi_f_git_config_parse_int64, METH_VARARGS, NULL},
  {"git_config_set_bool", _cffi_f_git_config_set_bool, METH_VARARGS, NULL},
  {"git_config_set_int64", _cffi_f_git_config_set_int64, METH_VARARGS, NULL},
  {"git_config_set_multivar", _cffi_f_git_config_set_multivar, METH_VARARGS, NULL},
  {"git_config_set_string", _cffi_f_git_config_set_string, METH_VARARGS, NULL},
  {"git_config_snapshot", _cffi_f_git_config_snapshot, METH_VARARGS, NULL},
  {"git_cred_ssh_key_new", _cffi_f_git_cred_ssh_key_new, METH_VARARGS, NULL},
  {"git_cred_userpass_plaintext_new", _cffi_f_git_cred_userpass_plaintext_new, METH_VARARGS, NULL},
  {"git_diff_index_to_workdir", _cffi_f_git_diff_index_to_workdir, METH_VARARGS, NULL},
  {"git_diff_init_options", _cffi_f_git_diff_init_options, METH_VARARGS, NULL},
  {"git_diff_tree_to_index", _cffi_f_git_diff_tree_to_index, METH_VARARGS, NULL},
  {"git_index_add", _cffi_f_git_index_add, METH_VARARGS, NULL},
  {"git_index_add_all", _cffi_f_git_index_add_all, METH_VARARGS, NULL},
  {"git_index_add_bypath", _cffi_f_git_index_add_bypath, METH_VARARGS, NULL},
  {"git_index_clear", _cffi_f_git_index_clear, METH_O, NULL},
  {"git_index_conflict_get", _cffi_f_git_index_conflict_get, METH_VARARGS, NULL},
  {"git_index_conflict_iterator_free", _cffi_f_git_index_conflict_iterator_free, METH_O, NULL},
  {"git_index_conflict_iterator_new", _cffi_f_git_index_conflict_iterator_new, METH_VARARGS, NULL},
  {"git_index_conflict_next", _cffi_f_git_index_conflict_next, METH_VARARGS, NULL},
  {"git_index_conflict_remove", _cffi_f_git_index_conflict_remove, METH_VARARGS, NULL},
  {"git_index_entrycount", _cffi_f_git_index_entrycount, METH_O, NULL},
  {"git_index_find", _cffi_f_git_index_find, METH_VARARGS, NULL},
  {"git_index_free", _cffi_f_git_index_free, METH_O, NULL},
  {"git_index_get_byindex", _cffi_f_git_index_get_byindex, METH_VARARGS, NULL},
  {"git_index_get_bypath", _cffi_f_git_index_get_bypath, METH_VARARGS, NULL},
  {"git_index_has_conflicts", _cffi_f_git_index_has_conflicts, METH_O, NULL},
  {"git_index_open", _cffi_f_git_index_open, METH_VARARGS, NULL},
  {"git_index_read", _cffi_f_git_index_read, METH_VARARGS, NULL},
  {"git_index_read_tree", _cffi_f_git_index_read_tree, METH_VARARGS, NULL},
  {"git_index_remove", _cffi_f_git_index_remove, METH_VARARGS, NULL},
  {"git_index_write", _cffi_f_git_index_write, METH_O, NULL},
  {"git_index_write_tree", _cffi_f_git_index_write_tree, METH_VARARGS, NULL},
  {"git_index_write_tree_to", _cffi_f_git_index_write_tree_to, METH_VARARGS, NULL},
  {"git_push_add_refspec", _cffi_f_git_push_add_refspec, METH_VARARGS, NULL},
  {"git_push_finish", _cffi_f_git_push_finish, METH_O, NULL},
  {"git_push_free", _cffi_f_git_push_free, METH_O, NULL},
  {"git_push_new", _cffi_f_git_push_new, METH_VARARGS, NULL},
  {"git_push_status_foreach", _cffi_f_git_push_status_foreach, METH_VARARGS, NULL},
  {"git_push_unpack_ok", _cffi_f_git_push_unpack_ok, METH_O, NULL},
  {"git_push_update_tips", _cffi_f_git_push_update_tips, METH_VARARGS, NULL},
  {"git_refspec_direction", _cffi_f_git_refspec_direction, METH_O, NULL},
  {"git_refspec_dst", _cffi_f_git_refspec_dst, METH_O, NULL},
  {"git_refspec_dst_matches", _cffi_f_git_refspec_dst_matches, METH_VARARGS, NULL},
  {"git_refspec_force", _cffi_f_git_refspec_force, METH_O, NULL},
  {"git_refspec_rtransform", _cffi_f_git_refspec_rtransform, METH_VARARGS, NULL},
  {"git_refspec_src", _cffi_f_git_refspec_src, METH_O, NULL},
  {"git_refspec_src_matches", _cffi_f_git_refspec_src_matches, METH_VARARGS, NULL},
  {"git_refspec_string", _cffi_f_git_refspec_string, METH_O, NULL},
  {"git_refspec_transform", _cffi_f_git_refspec_transform, METH_VARARGS, NULL},
  {"git_remote_add_fetch", _cffi_f_git_remote_add_fetch, METH_VARARGS, NULL},
  {"git_remote_add_push", _cffi_f_git_remote_add_push, METH_VARARGS, NULL},
  {"git_remote_create", _cffi_f_git_remote_create, METH_VARARGS, NULL},
  {"git_remote_delete", _cffi_f_git_remote_delete, METH_O, NULL},
  {"git_remote_fetch", _cffi_f_git_remote_fetch, METH_VARARGS, NULL},
  {"git_remote_free", _cffi_f_git_remote_free, METH_O, NULL},
  {"git_remote_get_fetch_refspecs", _cffi_f_git_remote_get_fetch_refspecs, METH_VARARGS, NULL},
  {"git_remote_get_push_refspecs", _cffi_f_git_remote_get_push_refspecs, METH_VARARGS, NULL},
  {"git_remote_get_refspec", _cffi_f_git_remote_get_refspec, METH_VARARGS, NULL},
  {"git_remote_init_callbacks", _cffi_f_git_remote_init_callbacks, METH_VARARGS, NULL},
  {"git_remote_list", _cffi_f_git_remote_list, METH_VARARGS, NULL},
  {"git_remote_load", _cffi_f_git_remote_load, METH_VARARGS, NULL},
  {"git_remote_name", _cffi_f_git_remote_name, METH_O, NULL},
  {"git_remote_pushurl", _cffi_f_git_remote_pushurl, METH_O, NULL},
  {"git_remote_refspec_count", _cffi_f_git_remote_refspec_count, METH_O, NULL},
  {"git_remote_rename", _cffi_f_git_remote_rename, METH_VARARGS, NULL},
  {"git_remote_save", _cffi_f_git_remote_save, METH_O, NULL},
  {"git_remote_set_callbacks", _cffi_f_git_remote_set_callbacks, METH_VARARGS, NULL},
  {"git_remote_set_fetch_refspecs", _cffi_f_git_remote_set_fetch_refspecs, METH_VARARGS, NULL},
  {"git_remote_set_push_refspecs", _cffi_f_git_remote_set_push_refspecs, METH_VARARGS, NULL},
  {"git_remote_set_pushurl", _cffi_f_git_remote_set_pushurl, METH_VARARGS, NULL},
  {"git_remote_set_url", _cffi_f_git_remote_set_url, METH_VARARGS, NULL},
  {"git_remote_stats", _cffi_f_git_remote_stats, METH_O, NULL},
  {"git_remote_url", _cffi_f_git_remote_url, METH_O, NULL},
  {"git_repository_config", _cffi_f_git_repository_config, METH_VARARGS, NULL},
  {"git_repository_config_snapshot", _cffi_f_git_repository_config_snapshot, METH_VARARGS, NULL},
  {"git_repository_free", _cffi_f_git_repository_free, METH_O, NULL},
  {"git_repository_index", _cffi_f_git_repository_index, METH_VARARGS, NULL},
  {"git_repository_init", _cffi_f_git_repository_init, METH_VARARGS, NULL},
  {"git_repository_init_ext", _cffi_f_git_repository_init_ext, METH_VARARGS, NULL},
  {"git_repository_init_init_options", _cffi_f_git_repository_init_init_options, METH_VARARGS, NULL},
  {"git_repository_set_head", _cffi_f_git_repository_set_head, METH_VARARGS, NULL},
  {"git_repository_set_head_detached", _cffi_f_git_repository_set_head_detached, METH_VARARGS, NULL},
  {"git_repository_state_cleanup", _cffi_f_git_repository_state_cleanup, METH_O, NULL},
  {"git_strarray_free", _cffi_f_git_strarray_free, METH_O, NULL},
  {"giterr_last", _cffi_f_giterr_last, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_blame_hunk", _cffi_layout_struct_git_blame_hunk, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_blame_options", _cffi_layout_struct_git_blame_options, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_checkout_options", _cffi_layout_struct_git_checkout_options, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_clone_options", _cffi_layout_struct_git_clone_options, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_index_entry", _cffi_layout_struct_git_index_entry, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_oid", _cffi_layout_struct_git_oid, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_remote_callbacks", _cffi_layout_struct_git_remote_callbacks, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_signature", _cffi_layout_struct_git_signature, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_strarray", _cffi_layout_struct_git_strarray, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_time", _cffi_layout_struct_git_time, METH_NOARGS, NULL},
  {"_cffi_layout_struct_git_transfer_progress", _cffi_layout_struct_git_transfer_progress, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x5c2b4805xc3cd8a96",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x5c2b4805xc3cd8a96(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (_cffi_const_GIT_REPOSITORY_INIT_SHARED_ALL(lib) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__x5c2b4805xc3cd8a96(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x5c2b4805xc3cd8a96", _cffi_methods);
  if (lib == NULL)
    return;
  if (_cffi_const_GIT_REPOSITORY_INIT_SHARED_ALL(lib) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
