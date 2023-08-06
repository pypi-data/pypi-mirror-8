
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



#include "gphoto2/gphoto2-context.h"
#include "gphoto2/gphoto2-camera.h"
#include <time.h>

typedef struct {
    unsigned long  size;
    char*          data;
} StreamingBuffer;


static void _cffi_check__CameraAbilities(CameraAbilities *p)
{
  /* only to generate compile-time warnings or errors */
  { char(*tmp)[128] = &p->model; (void)tmp; }
  (void)((p->usb_vendor) << 1);
  (void)((p->usb_product) << 1);
  (void)((p->usb_class) << 1);
  (void)((p->usb_subclass) << 1);
  (void)((p->usb_protocol) << 1);
  { char(*tmp)[1024] = &p->library; (void)tmp; }
  { char(*tmp)[1024] = &p->id; (void)tmp; }
}
static PyObject *
_cffi_layout__CameraAbilities(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; CameraAbilities y; };
  static Py_ssize_t nums[] = {
    sizeof(CameraAbilities),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(CameraAbilities, model),
    sizeof(((CameraAbilities *)0)->model),
    offsetof(CameraAbilities, usb_vendor),
    sizeof(((CameraAbilities *)0)->usb_vendor),
    offsetof(CameraAbilities, usb_product),
    sizeof(((CameraAbilities *)0)->usb_product),
    offsetof(CameraAbilities, usb_class),
    sizeof(((CameraAbilities *)0)->usb_class),
    offsetof(CameraAbilities, usb_subclass),
    sizeof(((CameraAbilities *)0)->usb_subclass),
    offsetof(CameraAbilities, usb_protocol),
    sizeof(((CameraAbilities *)0)->usb_protocol),
    offsetof(CameraAbilities, library),
    sizeof(((CameraAbilities *)0)->library),
    offsetof(CameraAbilities, id),
    sizeof(((CameraAbilities *)0)->id),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__CameraAbilities(0);
}

static int _cffi_e__CameraCaptureType(PyObject *lib)
{
  if ((GP_CAPTURE_IMAGE) < 0 || (unsigned long)(GP_CAPTURE_IMAGE) != 0UL) {
    char buf[64];
    if ((GP_CAPTURE_IMAGE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_CAPTURE_IMAGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_CAPTURE_IMAGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraCaptureType", "GP_CAPTURE_IMAGE", buf, "0");
    return -1;
  }
  if ((GP_CAPTURE_MOVIE) < 0 || (unsigned long)(GP_CAPTURE_MOVIE) != 1UL) {
    char buf[64];
    if ((GP_CAPTURE_MOVIE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_CAPTURE_MOVIE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_CAPTURE_MOVIE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraCaptureType", "GP_CAPTURE_MOVIE", buf, "1");
    return -1;
  }
  if ((GP_CAPTURE_SOUND) < 0 || (unsigned long)(GP_CAPTURE_SOUND) != 2UL) {
    char buf[64];
    if ((GP_CAPTURE_SOUND) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_CAPTURE_SOUND));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_CAPTURE_SOUND));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraCaptureType", "GP_CAPTURE_SOUND", buf, "2");
    return -1;
  }
  return 0;
}

static int _cffi_e__CameraEventType(PyObject *lib)
{
  if ((GP_EVENT_UNKNOWN) < 0 || (unsigned long)(GP_EVENT_UNKNOWN) != 0UL) {
    char buf[64];
    if ((GP_EVENT_UNKNOWN) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_EVENT_UNKNOWN));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_EVENT_UNKNOWN));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraEventType", "GP_EVENT_UNKNOWN", buf, "0");
    return -1;
  }
  if ((GP_EVENT_TIMEOUT) < 0 || (unsigned long)(GP_EVENT_TIMEOUT) != 1UL) {
    char buf[64];
    if ((GP_EVENT_TIMEOUT) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_EVENT_TIMEOUT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_EVENT_TIMEOUT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraEventType", "GP_EVENT_TIMEOUT", buf, "1");
    return -1;
  }
  if ((GP_EVENT_FILE_ADDED) < 0 || (unsigned long)(GP_EVENT_FILE_ADDED) != 2UL) {
    char buf[64];
    if ((GP_EVENT_FILE_ADDED) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_EVENT_FILE_ADDED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_EVENT_FILE_ADDED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraEventType", "GP_EVENT_FILE_ADDED", buf, "2");
    return -1;
  }
  if ((GP_EVENT_FOLDER_ADDED) < 0 || (unsigned long)(GP_EVENT_FOLDER_ADDED) != 3UL) {
    char buf[64];
    if ((GP_EVENT_FOLDER_ADDED) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_EVENT_FOLDER_ADDED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_EVENT_FOLDER_ADDED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraEventType", "GP_EVENT_FOLDER_ADDED", buf, "3");
    return -1;
  }
  if ((GP_EVENT_CAPTURE_COMPLETE) < 0 || (unsigned long)(GP_EVENT_CAPTURE_COMPLETE) != 4UL) {
    char buf[64];
    if ((GP_EVENT_CAPTURE_COMPLETE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_EVENT_CAPTURE_COMPLETE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_EVENT_CAPTURE_COMPLETE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraEventType", "GP_EVENT_CAPTURE_COMPLETE", buf, "4");
    return -1;
  }
  return _cffi_e__CameraCaptureType(lib);
}

static int _cffi_e__CameraFileAccessType(PyObject *lib)
{
  if ((GP_FILE_ACCESSTYPE_MEMORY) < 0 || (unsigned long)(GP_FILE_ACCESSTYPE_MEMORY) != 0UL) {
    char buf[64];
    if ((GP_FILE_ACCESSTYPE_MEMORY) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_ACCESSTYPE_MEMORY));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_ACCESSTYPE_MEMORY));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileAccessType", "GP_FILE_ACCESSTYPE_MEMORY", buf, "0");
    return -1;
  }
  if ((GP_FILE_ACCESSTYPE_FD) < 0 || (unsigned long)(GP_FILE_ACCESSTYPE_FD) != 1UL) {
    char buf[64];
    if ((GP_FILE_ACCESSTYPE_FD) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_ACCESSTYPE_FD));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_ACCESSTYPE_FD));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileAccessType", "GP_FILE_ACCESSTYPE_FD", buf, "1");
    return -1;
  }
  if ((GP_FILE_ACCESSTYPE_HANDLER) < 0 || (unsigned long)(GP_FILE_ACCESSTYPE_HANDLER) != 2UL) {
    char buf[64];
    if ((GP_FILE_ACCESSTYPE_HANDLER) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_ACCESSTYPE_HANDLER));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_ACCESSTYPE_HANDLER));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileAccessType", "GP_FILE_ACCESSTYPE_HANDLER", buf, "2");
    return -1;
  }
  return _cffi_e__CameraEventType(lib);
}

static int _cffi_e__CameraFileInfoFields(PyObject *lib)
{
  if ((GP_FILE_INFO_NONE) < 0 || (unsigned long)(GP_FILE_INFO_NONE) != 0UL) {
    char buf[64];
    if ((GP_FILE_INFO_NONE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_NONE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_NONE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_NONE", buf, "0");
    return -1;
  }
  if ((GP_FILE_INFO_TYPE) < 0 || (unsigned long)(GP_FILE_INFO_TYPE) != 1UL) {
    char buf[64];
    if ((GP_FILE_INFO_TYPE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_TYPE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_TYPE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_TYPE", buf, "1");
    return -1;
  }
  if ((GP_FILE_INFO_SIZE) < 0 || (unsigned long)(GP_FILE_INFO_SIZE) != 4UL) {
    char buf[64];
    if ((GP_FILE_INFO_SIZE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_SIZE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_SIZE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_SIZE", buf, "4");
    return -1;
  }
  if ((GP_FILE_INFO_WIDTH) < 0 || (unsigned long)(GP_FILE_INFO_WIDTH) != 8UL) {
    char buf[64];
    if ((GP_FILE_INFO_WIDTH) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_WIDTH));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_WIDTH));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_WIDTH", buf, "8");
    return -1;
  }
  if ((GP_FILE_INFO_HEIGHT) < 0 || (unsigned long)(GP_FILE_INFO_HEIGHT) != 16UL) {
    char buf[64];
    if ((GP_FILE_INFO_HEIGHT) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_HEIGHT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_HEIGHT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_HEIGHT", buf, "16");
    return -1;
  }
  if ((GP_FILE_INFO_PERMISSIONS) < 0 || (unsigned long)(GP_FILE_INFO_PERMISSIONS) != 32UL) {
    char buf[64];
    if ((GP_FILE_INFO_PERMISSIONS) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_PERMISSIONS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_PERMISSIONS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_PERMISSIONS", buf, "32");
    return -1;
  }
  if ((GP_FILE_INFO_STATUS) < 0 || (unsigned long)(GP_FILE_INFO_STATUS) != 64UL) {
    char buf[64];
    if ((GP_FILE_INFO_STATUS) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_STATUS));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_STATUS));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_STATUS", buf, "64");
    return -1;
  }
  if ((GP_FILE_INFO_MTIME) < 0 || (unsigned long)(GP_FILE_INFO_MTIME) != 128UL) {
    char buf[64];
    if ((GP_FILE_INFO_MTIME) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_MTIME));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_MTIME));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_MTIME", buf, "128");
    return -1;
  }
  if ((GP_FILE_INFO_ALL) < 0 || (unsigned long)(GP_FILE_INFO_ALL) != 255UL) {
    char buf[64];
    if ((GP_FILE_INFO_ALL) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_INFO_ALL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_INFO_ALL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileInfoFields", "GP_FILE_INFO_ALL", buf, "255");
    return -1;
  }
  return _cffi_e__CameraFileAccessType(lib);
}

static void _cffi_check__CameraFilePath(CameraFilePath *p)
{
  /* only to generate compile-time warnings or errors */
  { char(*tmp)[128] = &p->name; (void)tmp; }
  { char(*tmp)[1024] = &p->folder; (void)tmp; }
}
static PyObject *
_cffi_layout__CameraFilePath(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; CameraFilePath y; };
  static Py_ssize_t nums[] = {
    sizeof(CameraFilePath),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(CameraFilePath, name),
    sizeof(((CameraFilePath *)0)->name),
    offsetof(CameraFilePath, folder),
    sizeof(((CameraFilePath *)0)->folder),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__CameraFilePath(0);
}

static int _cffi_e__CameraFilePermissions(PyObject *lib)
{
  if ((GP_FILE_PERM_NONE) < 0 || (unsigned long)(GP_FILE_PERM_NONE) != 0UL) {
    char buf[64];
    if ((GP_FILE_PERM_NONE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_PERM_NONE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_PERM_NONE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFilePermissions", "GP_FILE_PERM_NONE", buf, "0");
    return -1;
  }
  if ((GP_FILE_PERM_READ) < 0 || (unsigned long)(GP_FILE_PERM_READ) != 1UL) {
    char buf[64];
    if ((GP_FILE_PERM_READ) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_PERM_READ));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_PERM_READ));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFilePermissions", "GP_FILE_PERM_READ", buf, "1");
    return -1;
  }
  if ((GP_FILE_PERM_DELETE) < 0 || (unsigned long)(GP_FILE_PERM_DELETE) != 2UL) {
    char buf[64];
    if ((GP_FILE_PERM_DELETE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_PERM_DELETE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_PERM_DELETE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFilePermissions", "GP_FILE_PERM_DELETE", buf, "2");
    return -1;
  }
  if ((GP_FILE_PERM_ALL) < 0 || (unsigned long)(GP_FILE_PERM_ALL) != 255UL) {
    char buf[64];
    if ((GP_FILE_PERM_ALL) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_PERM_ALL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_PERM_ALL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFilePermissions", "GP_FILE_PERM_ALL", buf, "255");
    return -1;
  }
  return _cffi_e__CameraFileInfoFields(lib);
}

static int _cffi_e__CameraFileStatus(PyObject *lib)
{
  if ((GP_FILE_STATUS_NOT_DOWNLOADED) < 0 || (unsigned long)(GP_FILE_STATUS_NOT_DOWNLOADED) != 0UL) {
    char buf[64];
    if ((GP_FILE_STATUS_NOT_DOWNLOADED) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_STATUS_NOT_DOWNLOADED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_STATUS_NOT_DOWNLOADED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileStatus", "GP_FILE_STATUS_NOT_DOWNLOADED", buf, "0");
    return -1;
  }
  if ((GP_FILE_STATUS_DOWNLOADED) < 0 || (unsigned long)(GP_FILE_STATUS_DOWNLOADED) != 1UL) {
    char buf[64];
    if ((GP_FILE_STATUS_DOWNLOADED) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_STATUS_DOWNLOADED));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_STATUS_DOWNLOADED));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileStatus", "GP_FILE_STATUS_DOWNLOADED", buf, "1");
    return -1;
  }
  return _cffi_e__CameraFilePermissions(lib);
}

static int _cffi_e__CameraFileType(PyObject *lib)
{
  if ((GP_FILE_TYPE_PREVIEW) < 0 || (unsigned long)(GP_FILE_TYPE_PREVIEW) != 0UL) {
    char buf[64];
    if ((GP_FILE_TYPE_PREVIEW) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_PREVIEW));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_PREVIEW));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_PREVIEW", buf, "0");
    return -1;
  }
  if ((GP_FILE_TYPE_NORMAL) < 0 || (unsigned long)(GP_FILE_TYPE_NORMAL) != 1UL) {
    char buf[64];
    if ((GP_FILE_TYPE_NORMAL) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_NORMAL));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_NORMAL));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_NORMAL", buf, "1");
    return -1;
  }
  if ((GP_FILE_TYPE_RAW) < 0 || (unsigned long)(GP_FILE_TYPE_RAW) != 2UL) {
    char buf[64];
    if ((GP_FILE_TYPE_RAW) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_RAW));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_RAW));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_RAW", buf, "2");
    return -1;
  }
  if ((GP_FILE_TYPE_AUDIO) < 0 || (unsigned long)(GP_FILE_TYPE_AUDIO) != 3UL) {
    char buf[64];
    if ((GP_FILE_TYPE_AUDIO) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_AUDIO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_AUDIO));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_AUDIO", buf, "3");
    return -1;
  }
  if ((GP_FILE_TYPE_EXIF) < 0 || (unsigned long)(GP_FILE_TYPE_EXIF) != 4UL) {
    char buf[64];
    if ((GP_FILE_TYPE_EXIF) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_EXIF));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_EXIF));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_EXIF", buf, "4");
    return -1;
  }
  if ((GP_FILE_TYPE_METADATA) < 0 || (unsigned long)(GP_FILE_TYPE_METADATA) != 5UL) {
    char buf[64];
    if ((GP_FILE_TYPE_METADATA) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_FILE_TYPE_METADATA));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_FILE_TYPE_METADATA));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraFileType", "GP_FILE_TYPE_METADATA", buf, "5");
    return -1;
  }
  return _cffi_e__CameraFileStatus(lib);
}

static void _cffi_check__CameraText(CameraText *p)
{
  /* only to generate compile-time warnings or errors */
  { char(*tmp)[32768] = &p->text; (void)tmp; }
}
static PyObject *
_cffi_layout__CameraText(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; CameraText y; };
  static Py_ssize_t nums[] = {
    sizeof(CameraText),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(CameraText, text),
    sizeof(((CameraText *)0)->text),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__CameraText(0);
}

static int _cffi_e__CameraWidgetType(PyObject *lib)
{
  if ((GP_WIDGET_WINDOW) < 0 || (unsigned long)(GP_WIDGET_WINDOW) != 0UL) {
    char buf[64];
    if ((GP_WIDGET_WINDOW) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_WINDOW));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_WINDOW));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_WINDOW", buf, "0");
    return -1;
  }
  if ((GP_WIDGET_SECTION) < 0 || (unsigned long)(GP_WIDGET_SECTION) != 1UL) {
    char buf[64];
    if ((GP_WIDGET_SECTION) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_SECTION));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_SECTION));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_SECTION", buf, "1");
    return -1;
  }
  if ((GP_WIDGET_TEXT) < 0 || (unsigned long)(GP_WIDGET_TEXT) != 2UL) {
    char buf[64];
    if ((GP_WIDGET_TEXT) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_TEXT));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_TEXT));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_TEXT", buf, "2");
    return -1;
  }
  if ((GP_WIDGET_RANGE) < 0 || (unsigned long)(GP_WIDGET_RANGE) != 3UL) {
    char buf[64];
    if ((GP_WIDGET_RANGE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_RANGE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_RANGE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_RANGE", buf, "3");
    return -1;
  }
  if ((GP_WIDGET_TOGGLE) < 0 || (unsigned long)(GP_WIDGET_TOGGLE) != 4UL) {
    char buf[64];
    if ((GP_WIDGET_TOGGLE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_TOGGLE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_TOGGLE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_TOGGLE", buf, "4");
    return -1;
  }
  if ((GP_WIDGET_RADIO) < 0 || (unsigned long)(GP_WIDGET_RADIO) != 5UL) {
    char buf[64];
    if ((GP_WIDGET_RADIO) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_RADIO));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_RADIO));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_RADIO", buf, "5");
    return -1;
  }
  if ((GP_WIDGET_MENU) < 0 || (unsigned long)(GP_WIDGET_MENU) != 6UL) {
    char buf[64];
    if ((GP_WIDGET_MENU) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_MENU));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_MENU));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_MENU", buf, "6");
    return -1;
  }
  if ((GP_WIDGET_BUTTON) < 0 || (unsigned long)(GP_WIDGET_BUTTON) != 7UL) {
    char buf[64];
    if ((GP_WIDGET_BUTTON) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_BUTTON));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_BUTTON));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_BUTTON", buf, "7");
    return -1;
  }
  if ((GP_WIDGET_DATE) < 0 || (unsigned long)(GP_WIDGET_DATE) != 8UL) {
    char buf[64];
    if ((GP_WIDGET_DATE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_WIDGET_DATE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_WIDGET_DATE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "CameraWidgetType", "GP_WIDGET_DATE", buf, "8");
    return -1;
  }
  return _cffi_e__CameraFileType(lib);
}

static int _cffi_e__GPLogLevel(PyObject *lib)
{
  if ((GP_LOG_ERROR) < 0 || (unsigned long)(GP_LOG_ERROR) != 0UL) {
    char buf[64];
    if ((GP_LOG_ERROR) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_LOG_ERROR));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_LOG_ERROR));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "GPLogLevel", "GP_LOG_ERROR", buf, "0");
    return -1;
  }
  if ((GP_LOG_VERBOSE) < 0 || (unsigned long)(GP_LOG_VERBOSE) != 1UL) {
    char buf[64];
    if ((GP_LOG_VERBOSE) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_LOG_VERBOSE));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_LOG_VERBOSE));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "GPLogLevel", "GP_LOG_VERBOSE", buf, "1");
    return -1;
  }
  if ((GP_LOG_DEBUG) < 0 || (unsigned long)(GP_LOG_DEBUG) != 2UL) {
    char buf[64];
    if ((GP_LOG_DEBUG) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_LOG_DEBUG));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_LOG_DEBUG));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "GPLogLevel", "GP_LOG_DEBUG", buf, "2");
    return -1;
  }
  if ((GP_LOG_DATA) < 0 || (unsigned long)(GP_LOG_DATA) != 3UL) {
    char buf[64];
    if ((GP_LOG_DATA) < 0)
        snprintf(buf, 63, "%ld", (long)(GP_LOG_DATA));
    else
        snprintf(buf, 63, "%lu", (unsigned long)(GP_LOG_DATA));
    PyErr_Format(_cffi_VerificationError,
                 "enum %s: %s has the real value %s, not %s",
                 "GPLogLevel", "GP_LOG_DATA", buf, "3");
    return -1;
  }
  return _cffi_e__CameraWidgetType(lib);
}

static void _cffi_check__StreamingBuffer(StreamingBuffer *p)
{
  /* only to generate compile-time warnings or errors */
  (void)((p->size) << 1);
  { char * *tmp = &p->data; (void)tmp; }
}
static PyObject *
_cffi_layout__StreamingBuffer(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; StreamingBuffer y; };
  static Py_ssize_t nums[] = {
    sizeof(StreamingBuffer),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(StreamingBuffer, size),
    sizeof(((StreamingBuffer *)0)->size),
    offsetof(StreamingBuffer, data),
    sizeof(((StreamingBuffer *)0)->data),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check__StreamingBuffer(0);
}

static PyObject *
_cffi_f_gp_abilities_list_detect(PyObject *self, PyObject *args)
{
  CameraAbilitiesList * x0;
  GPPortInfoList * x1;
  CameraList * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_abilities_list_detect", &arg0, &arg1, &arg2, &arg3))
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
  { result = gp_abilities_list_detect(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_abilities_list_free(PyObject *self, PyObject *arg0)
{
  CameraAbilitiesList * x0;
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
  { result = gp_abilities_list_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_abilities_list_load(PyObject *self, PyObject *args)
{
  CameraAbilitiesList * x0;
  GPContext * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_abilities_list_load", &arg0, &arg1))
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
  { result = gp_abilities_list_load(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_abilities_list_new(PyObject *self, PyObject *arg0)
{
  CameraAbilitiesList * * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_abilities_list_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_autodetect(PyObject *self, PyObject *args)
{
  CameraList * x0;
  GPContext * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_autodetect", &arg0, &arg1))
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
  { result = gp_camera_autodetect(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_capture(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraCaptureType x1;
  CameraFilePath * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_capture", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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

  if (_cffi_to_c((char *)&x1, _cffi_type(6), arg1) < 0)
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(7), arg2) < 0)
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
  { result = gp_camera_capture(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_capture_preview(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraFile * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_capture_preview", &arg0, &arg1, &arg2))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_capture_preview(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_exit(PyObject *self, PyObject *args)
{
  Camera * x0;
  GPContext * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_exit", &arg0, &arg1))
    return NULL;

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
  { result = gp_camera_exit(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_file_delete(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_file_delete", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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
  { result = gp_camera_file_delete(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_file_get(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  CameraFileType x3;
  CameraFile * x4;
  GPContext * x5;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:gp_camera_file_get", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

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
      _cffi_type(9), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(9), arg2) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x3, _cffi_type(10), arg3) < 0)
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(8), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca(datasize);
    memset((void *)x5, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(3), arg5) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_file_get(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_file_get_info(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  CameraFileInfo * x3;
  GPContext * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:gp_camera_file_get_info", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

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
      _cffi_type(11), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(11), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(3), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_file_get_info(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_file_read(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  CameraFileType x3;
  uint64_t x4;
  char * x5;
  uint64_t * x6;
  GPContext * x7;
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

  if (!PyArg_ParseTuple(args, "OOOOOOOO:gp_camera_file_read", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5, &arg6, &arg7))
    return NULL;

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
      _cffi_type(9), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(9), arg2) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x3, _cffi_type(10), arg3) < 0)
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint64_t);
  if (x4 == (uint64_t)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(12), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca(datasize);
    memset((void *)x5, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(12), arg5) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(13), arg6, (char **)&x6);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x6 = alloca(datasize);
    memset((void *)x6, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x6, _cffi_type(13), arg6) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg7, (char **)&x7);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x7 = alloca(datasize);
    memset((void *)x7, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x7, _cffi_type(3), arg7) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_file_read(x0, x1, x2, x3, x4, x5, x6, x7); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_file_set_info(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  CameraFileInfo x3;
  GPContext * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:gp_camera_file_set_info", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

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
      _cffi_type(9), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(9), arg2) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x3, _cffi_type(14), arg3) < 0)
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(3), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_file_set_info(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_delete_all(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_folder_delete_all", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_folder_delete_all(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_list_files(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  CameraList * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_folder_list_files", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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
  { result = gp_camera_folder_list_files(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_list_folders(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  CameraList * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_folder_list_folders", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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
  { result = gp_camera_folder_list_folders(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_make_dir(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_folder_make_dir", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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
  { result = gp_camera_folder_make_dir(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_put_file(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  CameraFileType x3;
  CameraFile * x4;
  GPContext * x5;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;
  PyObject *arg5;

  if (!PyArg_ParseTuple(args, "OOOOOO:gp_camera_folder_put_file", &arg0, &arg1, &arg2, &arg3, &arg4, &arg5))
    return NULL;

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
      _cffi_type(9), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(9), arg2) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x3, _cffi_type(10), arg3) < 0)
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(8), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(8), arg4) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg5, (char **)&x5);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x5 = alloca(datasize);
    memset((void *)x5, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x5, _cffi_type(3), arg5) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_folder_put_file(x0, x1, x2, x3, x4, x5); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_folder_remove_dir(PyObject *self, PyObject *args)
{
  Camera * x0;
  char const * x1;
  char const * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_folder_remove_dir", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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
  { result = gp_camera_folder_remove_dir(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_free(PyObject *self, PyObject *arg0)
{
  Camera * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_camera_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_abilities(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraAbilities * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_get_abilities", &arg0, &arg1))
    return NULL;

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
  { result = gp_camera_get_abilities(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_about(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraText * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_get_about", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_get_about(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_config(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraWidget * * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_get_config", &arg0, &arg1, &arg2))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_get_config(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_manual(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraText * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_get_manual", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_get_manual(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_storageinfo(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraStorageInformation * * x1;
  int * x2;
  GPContext * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_camera_get_storageinfo", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(19), arg2) < 0)
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
  { result = gp_camera_get_storageinfo(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_get_summary(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraText * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_get_summary", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_get_summary(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_init(PyObject *self, PyObject *args)
{
  Camera * x0;
  GPContext * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_init", &arg0, &arg1))
    return NULL;

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
  { result = gp_camera_init(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_new(PyObject *self, PyObject *arg0)
{
  Camera * * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(20), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(20), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_ref(PyObject *self, PyObject *arg0)
{
  Camera * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_camera_ref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_set_config(PyObject *self, PyObject *args)
{
  Camera * x0;
  CameraWidget * x1;
  GPContext * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_camera_set_config", &arg0, &arg1, &arg2))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(3), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_set_config(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_set_port_info(PyObject *self, PyObject *args)
{
  Camera * x0;
  struct _GPPortInfo * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_set_port_info", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(22), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(22), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_set_port_info(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_trigger_capture(PyObject *self, PyObject *args)
{
  Camera * x0;
  GPContext * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_camera_trigger_capture", &arg0, &arg1))
    return NULL;

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
  { result = gp_camera_trigger_capture(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_unref(PyObject *self, PyObject *arg0)
{
  Camera * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_camera_unref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_camera_wait_for_event(PyObject *self, PyObject *args)
{
  Camera * x0;
  int x1;
  CameraEventType * x2;
  void * * x3;
  GPContext * x4;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_ParseTuple(args, "OOOOO:gp_camera_wait_for_event", &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(23), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(23), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(24), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(24), arg3) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg4, (char **)&x4);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x4 = alloca(datasize);
    memset((void *)x4, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x4, _cffi_type(3), arg4) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_camera_wait_for_event(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_context_new(PyObject *self, PyObject *no_arg)
{
  GPContext * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_context_new(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(3));
}

static PyObject *
_cffi_f_gp_context_ref(PyObject *self, PyObject *arg0)
{
  GPContext * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { gp_context_ref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_gp_context_unref(PyObject *self, PyObject *arg0)
{
  GPContext * x0;
  Py_ssize_t datasize;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { gp_context_unref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
_cffi_f_gp_file_adjust_name_for_mime_type(PyObject *self, PyObject *arg0)
{
  CameraFile * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_file_adjust_name_for_mime_type(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_detect_mime_type(PyObject *self, PyObject *arg0)
{
  CameraFile * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_file_detect_mime_type(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_free(PyObject *self, PyObject *arg0)
{
  CameraFile * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_file_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_get_data_and_size(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * * x1;
  unsigned long * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_file_get_data_and_size", &arg0, &arg1, &arg2))
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
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(27), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(27), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_get_data_and_size(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_get_mime_type(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_get_mime_type", &arg0, &arg1))
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
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_get_mime_type(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_get_mtime(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  long * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_get_mtime", &arg0, &arg1))
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
      _cffi_type(28), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(28), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_get_mtime(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_get_name(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_get_name", &arg0, &arg1))
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
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_get_name(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_get_name_by_type(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * x1;
  CameraFileType x2;
  char * * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_file_get_name_by_type", &arg0, &arg1, &arg2, &arg3))
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
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(9), arg1) < 0)
      return NULL;
  }

  if (_cffi_to_c((char *)&x2, _cffi_type(10), arg2) < 0)
    return NULL;

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
  { result = gp_file_get_name_by_type(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_new(PyObject *self, PyObject *arg0)
{
  CameraFile * * x0;
  Py_ssize_t datasize;
  int result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_new_from_fd(PyObject *self, PyObject *args)
{
  CameraFile * * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_new_from_fd", &arg0, &arg1))
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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_new_from_fd(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_new_from_handler(PyObject *self, PyObject *args)
{
  CameraFile * * x0;
  CameraFileHandler * x1;
  void * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_file_new_from_handler", &arg0, &arg1, &arg2))
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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(31), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(31), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(32), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_new_from_handler(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_ref(PyObject *self, PyObject *arg0)
{
  CameraFile * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_file_ref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_set_data_and_size(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char * x1;
  unsigned long x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_file_set_data_and_size", &arg0, &arg1, &arg2))
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
      _cffi_type(12), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(12), arg1) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, unsigned long);
  if (x2 == (unsigned long)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_file_set_data_and_size(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_set_mime_type(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_set_mime_type", &arg0, &arg1))
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
  { result = gp_file_set_mime_type(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_set_name(PyObject *self, PyObject *args)
{
  CameraFile * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_file_set_name", &arg0, &arg1))
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
  { result = gp_file_set_name(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_file_unref(PyObject *self, PyObject *arg0)
{
  CameraFile * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_file_unref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_list_count(PyObject *self, PyObject *arg0)
{
  CameraList * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_list_count(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_list_free(PyObject *self, PyObject *arg0)
{
  CameraList * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_list_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_list_get_name(PyObject *self, PyObject *args)
{
  CameraList * x0;
  int x1;
  char const * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_list_get_name", &arg0, &arg1, &arg2))
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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(26), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_list_get_name(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_list_get_value(PyObject *self, PyObject *args)
{
  CameraList * x0;
  int x1;
  char const * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_list_get_value", &arg0, &arg1, &arg2))
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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(26), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_list_get_value(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_list_new(PyObject *self, PyObject *arg0)
{
  CameraList * * x0;
  Py_ssize_t datasize;
  int result;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(33), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = alloca(datasize);
    memset((void *)x0, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(33), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_list_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_log_add_func(PyObject *self, PyObject *args)
{
  GPLogLevel x0;
  void(* x1)(GPLogLevel, char const *, char const *, void *);
  void * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_log_add_func", &arg0, &arg1, &arg2))
    return NULL;

  if (_cffi_to_c((char *)&x0, _cffi_type(34), arg0) < 0)
    return NULL;

  x1 = (void(*)(GPLogLevel, char const *, char const *, void *))_cffi_to_c_pointer(arg1, _cffi_type(35));
  if (x1 == (void(*)(GPLogLevel, char const *, char const *, void *))NULL && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(32), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(32), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_log_add_func(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_list_free(PyObject *self, PyObject *arg0)
{
  GPPortInfoList * x0;
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
  { result = gp_port_info_list_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_list_get_info(PyObject *self, PyObject *args)
{
  GPPortInfoList * x0;
  int x1;
  struct _GPPortInfo * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_port_info_list_get_info", &arg0, &arg1, &arg2))
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_port_info_list_get_info(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_list_load(PyObject *self, PyObject *arg0)
{
  GPPortInfoList * x0;
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
  { result = gp_port_info_list_load(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_list_lookup_path(PyObject *self, PyObject *args)
{
  GPPortInfoList * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_port_info_list_lookup_path", &arg0, &arg1))
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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_port_info_list_lookup_path(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_list_new(PyObject *self, PyObject *arg0)
{
  GPPortInfoList * * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_port_info_list_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_port_info_new(PyObject *self, PyObject *arg0)
{
  struct _GPPortInfo * * x0;
  Py_ssize_t datasize;
  int result;

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

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_port_info_new(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_result_as_string(PyObject *self, PyObject *arg0)
{
  int x0;
  char const * result;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_result_as_string(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_pointer((char *)result, _cffi_type(9));
}

static PyObject *
_cffi_f_gp_widget_add_choice(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_add_choice", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_add_choice(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_append(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  CameraWidget * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_append", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_append(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_changed(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_changed(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_count_children(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_count_children(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_count_choices(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_count_choices(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_free(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_free(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_child(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int x1;
  CameraWidget * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_get_child", &arg0, &arg1, &arg2))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(17), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(17), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_child(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_child_by_id(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int x1;
  CameraWidget * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_get_child_by_id", &arg0, &arg1, &arg2))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(17), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(17), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_child_by_id(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_child_by_label(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * x1;
  CameraWidget * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_get_child_by_label", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(17), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(17), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_child_by_label(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_child_by_name(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * x1;
  CameraWidget * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_get_child_by_name", &arg0, &arg1, &arg2))
    return NULL;

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
      _cffi_type(17), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(17), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_child_by_name(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_choice(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int x1;
  char const * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_get_choice", &arg0, &arg1, &arg2))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(26), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_choice(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_id(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_id", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(19), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_id(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_info(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_info", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_info(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_label(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_label", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_label(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_name(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_name", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(26), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(26), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_name(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_parent(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  CameraWidget * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_parent", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_get_parent(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_range(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  float * x1;
  float * x2;
  float * x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_widget_get_range", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(38), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(38), arg1) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(38), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(38), arg2) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(38), arg3, (char **)&x3);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x3 = alloca(datasize);
    memset((void *)x3, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x3, _cffi_type(38), arg3) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_range(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_readonly(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_readonly", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(19), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_readonly(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_root(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  CameraWidget * * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_root", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_get_root(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_type(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  CameraWidgetType * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_type", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(39), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(39), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_get_type(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_get_value(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  void * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_get_value", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_get_value(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_new(PyObject *self, PyObject *args)
{
  CameraWidgetType x0;
  char const * x1;
  CameraWidget * * x2;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:gp_widget_new", &arg0, &arg1, &arg2))
    return NULL;

  if (_cffi_to_c((char *)&x0, _cffi_type(40), arg0) < 0)
    return NULL;

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
      _cffi_type(17), arg2, (char **)&x2);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x2 = alloca(datasize);
    memset((void *)x2, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x2, _cffi_type(17), arg2) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_new(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_prepend(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  CameraWidget * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_prepend", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_prepend(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_ref(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_ref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_changed(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_set_changed", &arg0, &arg1))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_set_changed(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_info(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_set_info", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_set_info(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_name(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  char const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_set_name", &arg0, &arg1))
    return NULL;

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
  { result = gp_widget_set_name(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_range(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  float x1;
  float x2;
  float x3;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:gp_widget_set_range", &arg0, &arg1, &arg2, &arg3))
    return NULL;

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

  x1 = _cffi_to_c_float(arg1);
  if (x1 == (float)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_float(arg2);
  if (x2 == (float)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_float(arg3);
  if (x3 == (float)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_set_range(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_readonly(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  int x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_set_readonly", &arg0, &arg1))
    return NULL;

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

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_set_readonly(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_set_value(PyObject *self, PyObject *args)
{
  CameraWidget * x0;
  void const * x1;
  Py_ssize_t datasize;
  int result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:gp_widget_set_value", &arg0, &arg1))
    return NULL;

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

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(41), arg1, (char **)&x1);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x1 = alloca(datasize);
    memset((void *)x1, 0, datasize);
    if (_cffi_convert_array_from_object((char *)x1, _cffi_type(41), arg1) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = gp_widget_set_value(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static PyObject *
_cffi_f_gp_widget_unref(PyObject *self, PyObject *arg0)
{
  CameraWidget * x0;
  Py_ssize_t datasize;
  int result;

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
  { result = gp_widget_unref(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  return _cffi_from_c_int(result, int);
}

static void _cffi_check_struct__CameraFileHandler(struct _CameraFileHandler *p)
{
  /* only to generate compile-time warnings or errors */
  { int(* *tmp)(void *, uint64_t *) = &p->size; (void)tmp; }
  { int(* *tmp)(void *, unsigned char *, uint64_t *) = &p->read; (void)tmp; }
  { int(* *tmp)(void *, unsigned char *, uint64_t *) = &p->write; (void)tmp; }
}
static PyObject *
_cffi_layout_struct__CameraFileHandler(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _CameraFileHandler y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _CameraFileHandler),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _CameraFileHandler, size),
    sizeof(((struct _CameraFileHandler *)0)->size),
    offsetof(struct _CameraFileHandler, read),
    sizeof(((struct _CameraFileHandler *)0)->read),
    offsetof(struct _CameraFileHandler, write),
    sizeof(((struct _CameraFileHandler *)0)->write),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__CameraFileHandler(0);
}

static void _cffi_check_struct__CameraFileInfo(struct _CameraFileInfo *p)
{
  /* only to generate compile-time warnings or errors */
  { CameraFileInfoPreview *tmp = &p->preview; (void)tmp; }
  { CameraFileInfoFile *tmp = &p->file; (void)tmp; }
}
static PyObject *
_cffi_layout_struct__CameraFileInfo(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _CameraFileInfo y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _CameraFileInfo),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _CameraFileInfo, preview),
    sizeof(((struct _CameraFileInfo *)0)->preview),
    offsetof(struct _CameraFileInfo, file),
    sizeof(((struct _CameraFileInfo *)0)->file),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__CameraFileInfo(0);
}

static void _cffi_check_struct__CameraFileInfoFile(struct _CameraFileInfoFile *p)
{
  /* only to generate compile-time warnings or errors */
  { CameraFileInfoFields *tmp = &p->fields; (void)tmp; }
  { CameraFileStatus *tmp = &p->status; (void)tmp; }
  (void)((p->size) << 1);
  { char(*tmp)[64] = &p->type; (void)tmp; }
  (void)((p->width) << 1);
  (void)((p->height) << 1);
  { CameraFilePermissions *tmp = &p->permissions; (void)tmp; }
  (void)((p->mtime) << 1);
}
static PyObject *
_cffi_layout_struct__CameraFileInfoFile(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _CameraFileInfoFile y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _CameraFileInfoFile),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _CameraFileInfoFile, fields),
    sizeof(((struct _CameraFileInfoFile *)0)->fields),
    offsetof(struct _CameraFileInfoFile, status),
    sizeof(((struct _CameraFileInfoFile *)0)->status),
    offsetof(struct _CameraFileInfoFile, size),
    sizeof(((struct _CameraFileInfoFile *)0)->size),
    offsetof(struct _CameraFileInfoFile, type),
    sizeof(((struct _CameraFileInfoFile *)0)->type),
    offsetof(struct _CameraFileInfoFile, width),
    sizeof(((struct _CameraFileInfoFile *)0)->width),
    offsetof(struct _CameraFileInfoFile, height),
    sizeof(((struct _CameraFileInfoFile *)0)->height),
    offsetof(struct _CameraFileInfoFile, permissions),
    sizeof(((struct _CameraFileInfoFile *)0)->permissions),
    offsetof(struct _CameraFileInfoFile, mtime),
    sizeof(((struct _CameraFileInfoFile *)0)->mtime),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__CameraFileInfoFile(0);
}

static void _cffi_check_struct__CameraFileInfoPreview(struct _CameraFileInfoPreview *p)
{
  /* only to generate compile-time warnings or errors */
  { CameraFileInfoFields *tmp = &p->fields; (void)tmp; }
  { CameraFileStatus *tmp = &p->status; (void)tmp; }
  (void)((p->size) << 1);
  { char(*tmp)[64] = &p->type; (void)tmp; }
  (void)((p->width) << 1);
  (void)((p->height) << 1);
}
static PyObject *
_cffi_layout_struct__CameraFileInfoPreview(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct _CameraFileInfoPreview y; };
  static Py_ssize_t nums[] = {
    sizeof(struct _CameraFileInfoPreview),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct _CameraFileInfoPreview, fields),
    sizeof(((struct _CameraFileInfoPreview *)0)->fields),
    offsetof(struct _CameraFileInfoPreview, status),
    sizeof(((struct _CameraFileInfoPreview *)0)->status),
    offsetof(struct _CameraFileInfoPreview, size),
    sizeof(((struct _CameraFileInfoPreview *)0)->size),
    offsetof(struct _CameraFileInfoPreview, type),
    sizeof(((struct _CameraFileInfoPreview *)0)->type),
    offsetof(struct _CameraFileInfoPreview, width),
    sizeof(((struct _CameraFileInfoPreview *)0)->width),
    offsetof(struct _CameraFileInfoPreview, height),
    sizeof(((struct _CameraFileInfoPreview *)0)->height),
    -1
  };
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct__CameraFileInfoPreview(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_e__GPLogLevel(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"_cffi_layout__CameraAbilities", _cffi_layout__CameraAbilities, METH_NOARGS, NULL},
  {"_cffi_layout__CameraFilePath", _cffi_layout__CameraFilePath, METH_NOARGS, NULL},
  {"_cffi_layout__CameraText", _cffi_layout__CameraText, METH_NOARGS, NULL},
  {"_cffi_layout__StreamingBuffer", _cffi_layout__StreamingBuffer, METH_NOARGS, NULL},
  {"gp_abilities_list_detect", _cffi_f_gp_abilities_list_detect, METH_VARARGS, NULL},
  {"gp_abilities_list_free", _cffi_f_gp_abilities_list_free, METH_O, NULL},
  {"gp_abilities_list_load", _cffi_f_gp_abilities_list_load, METH_VARARGS, NULL},
  {"gp_abilities_list_new", _cffi_f_gp_abilities_list_new, METH_O, NULL},
  {"gp_camera_autodetect", _cffi_f_gp_camera_autodetect, METH_VARARGS, NULL},
  {"gp_camera_capture", _cffi_f_gp_camera_capture, METH_VARARGS, NULL},
  {"gp_camera_capture_preview", _cffi_f_gp_camera_capture_preview, METH_VARARGS, NULL},
  {"gp_camera_exit", _cffi_f_gp_camera_exit, METH_VARARGS, NULL},
  {"gp_camera_file_delete", _cffi_f_gp_camera_file_delete, METH_VARARGS, NULL},
  {"gp_camera_file_get", _cffi_f_gp_camera_file_get, METH_VARARGS, NULL},
  {"gp_camera_file_get_info", _cffi_f_gp_camera_file_get_info, METH_VARARGS, NULL},
  {"gp_camera_file_read", _cffi_f_gp_camera_file_read, METH_VARARGS, NULL},
  {"gp_camera_file_set_info", _cffi_f_gp_camera_file_set_info, METH_VARARGS, NULL},
  {"gp_camera_folder_delete_all", _cffi_f_gp_camera_folder_delete_all, METH_VARARGS, NULL},
  {"gp_camera_folder_list_files", _cffi_f_gp_camera_folder_list_files, METH_VARARGS, NULL},
  {"gp_camera_folder_list_folders", _cffi_f_gp_camera_folder_list_folders, METH_VARARGS, NULL},
  {"gp_camera_folder_make_dir", _cffi_f_gp_camera_folder_make_dir, METH_VARARGS, NULL},
  {"gp_camera_folder_put_file", _cffi_f_gp_camera_folder_put_file, METH_VARARGS, NULL},
  {"gp_camera_folder_remove_dir", _cffi_f_gp_camera_folder_remove_dir, METH_VARARGS, NULL},
  {"gp_camera_free", _cffi_f_gp_camera_free, METH_O, NULL},
  {"gp_camera_get_abilities", _cffi_f_gp_camera_get_abilities, METH_VARARGS, NULL},
  {"gp_camera_get_about", _cffi_f_gp_camera_get_about, METH_VARARGS, NULL},
  {"gp_camera_get_config", _cffi_f_gp_camera_get_config, METH_VARARGS, NULL},
  {"gp_camera_get_manual", _cffi_f_gp_camera_get_manual, METH_VARARGS, NULL},
  {"gp_camera_get_storageinfo", _cffi_f_gp_camera_get_storageinfo, METH_VARARGS, NULL},
  {"gp_camera_get_summary", _cffi_f_gp_camera_get_summary, METH_VARARGS, NULL},
  {"gp_camera_init", _cffi_f_gp_camera_init, METH_VARARGS, NULL},
  {"gp_camera_new", _cffi_f_gp_camera_new, METH_O, NULL},
  {"gp_camera_ref", _cffi_f_gp_camera_ref, METH_O, NULL},
  {"gp_camera_set_config", _cffi_f_gp_camera_set_config, METH_VARARGS, NULL},
  {"gp_camera_set_port_info", _cffi_f_gp_camera_set_port_info, METH_VARARGS, NULL},
  {"gp_camera_trigger_capture", _cffi_f_gp_camera_trigger_capture, METH_VARARGS, NULL},
  {"gp_camera_unref", _cffi_f_gp_camera_unref, METH_O, NULL},
  {"gp_camera_wait_for_event", _cffi_f_gp_camera_wait_for_event, METH_VARARGS, NULL},
  {"gp_context_new", _cffi_f_gp_context_new, METH_NOARGS, NULL},
  {"gp_context_ref", _cffi_f_gp_context_ref, METH_O, NULL},
  {"gp_context_unref", _cffi_f_gp_context_unref, METH_O, NULL},
  {"gp_file_adjust_name_for_mime_type", _cffi_f_gp_file_adjust_name_for_mime_type, METH_O, NULL},
  {"gp_file_detect_mime_type", _cffi_f_gp_file_detect_mime_type, METH_O, NULL},
  {"gp_file_free", _cffi_f_gp_file_free, METH_O, NULL},
  {"gp_file_get_data_and_size", _cffi_f_gp_file_get_data_and_size, METH_VARARGS, NULL},
  {"gp_file_get_mime_type", _cffi_f_gp_file_get_mime_type, METH_VARARGS, NULL},
  {"gp_file_get_mtime", _cffi_f_gp_file_get_mtime, METH_VARARGS, NULL},
  {"gp_file_get_name", _cffi_f_gp_file_get_name, METH_VARARGS, NULL},
  {"gp_file_get_name_by_type", _cffi_f_gp_file_get_name_by_type, METH_VARARGS, NULL},
  {"gp_file_new", _cffi_f_gp_file_new, METH_O, NULL},
  {"gp_file_new_from_fd", _cffi_f_gp_file_new_from_fd, METH_VARARGS, NULL},
  {"gp_file_new_from_handler", _cffi_f_gp_file_new_from_handler, METH_VARARGS, NULL},
  {"gp_file_ref", _cffi_f_gp_file_ref, METH_O, NULL},
  {"gp_file_set_data_and_size", _cffi_f_gp_file_set_data_and_size, METH_VARARGS, NULL},
  {"gp_file_set_mime_type", _cffi_f_gp_file_set_mime_type, METH_VARARGS, NULL},
  {"gp_file_set_name", _cffi_f_gp_file_set_name, METH_VARARGS, NULL},
  {"gp_file_unref", _cffi_f_gp_file_unref, METH_O, NULL},
  {"gp_list_count", _cffi_f_gp_list_count, METH_O, NULL},
  {"gp_list_free", _cffi_f_gp_list_free, METH_O, NULL},
  {"gp_list_get_name", _cffi_f_gp_list_get_name, METH_VARARGS, NULL},
  {"gp_list_get_value", _cffi_f_gp_list_get_value, METH_VARARGS, NULL},
  {"gp_list_new", _cffi_f_gp_list_new, METH_O, NULL},
  {"gp_log_add_func", _cffi_f_gp_log_add_func, METH_VARARGS, NULL},
  {"gp_port_info_list_free", _cffi_f_gp_port_info_list_free, METH_O, NULL},
  {"gp_port_info_list_get_info", _cffi_f_gp_port_info_list_get_info, METH_VARARGS, NULL},
  {"gp_port_info_list_load", _cffi_f_gp_port_info_list_load, METH_O, NULL},
  {"gp_port_info_list_lookup_path", _cffi_f_gp_port_info_list_lookup_path, METH_VARARGS, NULL},
  {"gp_port_info_list_new", _cffi_f_gp_port_info_list_new, METH_O, NULL},
  {"gp_port_info_new", _cffi_f_gp_port_info_new, METH_O, NULL},
  {"gp_result_as_string", _cffi_f_gp_result_as_string, METH_O, NULL},
  {"gp_widget_add_choice", _cffi_f_gp_widget_add_choice, METH_VARARGS, NULL},
  {"gp_widget_append", _cffi_f_gp_widget_append, METH_VARARGS, NULL},
  {"gp_widget_changed", _cffi_f_gp_widget_changed, METH_O, NULL},
  {"gp_widget_count_children", _cffi_f_gp_widget_count_children, METH_O, NULL},
  {"gp_widget_count_choices", _cffi_f_gp_widget_count_choices, METH_O, NULL},
  {"gp_widget_free", _cffi_f_gp_widget_free, METH_O, NULL},
  {"gp_widget_get_child", _cffi_f_gp_widget_get_child, METH_VARARGS, NULL},
  {"gp_widget_get_child_by_id", _cffi_f_gp_widget_get_child_by_id, METH_VARARGS, NULL},
  {"gp_widget_get_child_by_label", _cffi_f_gp_widget_get_child_by_label, METH_VARARGS, NULL},
  {"gp_widget_get_child_by_name", _cffi_f_gp_widget_get_child_by_name, METH_VARARGS, NULL},
  {"gp_widget_get_choice", _cffi_f_gp_widget_get_choice, METH_VARARGS, NULL},
  {"gp_widget_get_id", _cffi_f_gp_widget_get_id, METH_VARARGS, NULL},
  {"gp_widget_get_info", _cffi_f_gp_widget_get_info, METH_VARARGS, NULL},
  {"gp_widget_get_label", _cffi_f_gp_widget_get_label, METH_VARARGS, NULL},
  {"gp_widget_get_name", _cffi_f_gp_widget_get_name, METH_VARARGS, NULL},
  {"gp_widget_get_parent", _cffi_f_gp_widget_get_parent, METH_VARARGS, NULL},
  {"gp_widget_get_range", _cffi_f_gp_widget_get_range, METH_VARARGS, NULL},
  {"gp_widget_get_readonly", _cffi_f_gp_widget_get_readonly, METH_VARARGS, NULL},
  {"gp_widget_get_root", _cffi_f_gp_widget_get_root, METH_VARARGS, NULL},
  {"gp_widget_get_type", _cffi_f_gp_widget_get_type, METH_VARARGS, NULL},
  {"gp_widget_get_value", _cffi_f_gp_widget_get_value, METH_VARARGS, NULL},
  {"gp_widget_new", _cffi_f_gp_widget_new, METH_VARARGS, NULL},
  {"gp_widget_prepend", _cffi_f_gp_widget_prepend, METH_VARARGS, NULL},
  {"gp_widget_ref", _cffi_f_gp_widget_ref, METH_O, NULL},
  {"gp_widget_set_changed", _cffi_f_gp_widget_set_changed, METH_VARARGS, NULL},
  {"gp_widget_set_info", _cffi_f_gp_widget_set_info, METH_VARARGS, NULL},
  {"gp_widget_set_name", _cffi_f_gp_widget_set_name, METH_VARARGS, NULL},
  {"gp_widget_set_range", _cffi_f_gp_widget_set_range, METH_VARARGS, NULL},
  {"gp_widget_set_readonly", _cffi_f_gp_widget_set_readonly, METH_VARARGS, NULL},
  {"gp_widget_set_value", _cffi_f_gp_widget_set_value, METH_VARARGS, NULL},
  {"gp_widget_unref", _cffi_f_gp_widget_unref, METH_O, NULL},
  {"_cffi_layout_struct__CameraFileHandler", _cffi_layout_struct__CameraFileHandler, METH_NOARGS, NULL},
  {"_cffi_layout_struct__CameraFileInfo", _cffi_layout_struct__CameraFileInfo, METH_NOARGS, NULL},
  {"_cffi_layout_struct__CameraFileInfoFile", _cffi_layout_struct__CameraFileInfoFile, METH_NOARGS, NULL},
  {"_cffi_layout_struct__CameraFileInfoPreview", _cffi_layout_struct__CameraFileInfoPreview, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x13480f64x52a9c355",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x13480f64x52a9c355(void)
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
init_cffi__x13480f64x52a9c355(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x13480f64x52a9c355", _cffi_methods);
  if (lib == NULL)
    return;
  if (0 < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
