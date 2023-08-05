#ifndef __PYX_HAVE_API__lxml__etree
#define __PYX_HAVE_API__lxml__etree
#include "Python.h"
#include "lxml.etree.h"

static struct LxmlElement *(*__pyx_f_4lxml_5etree_deepcopyNodeToDocument)(struct LxmlDocument *, xmlNode *) = 0;
#define deepcopyNodeToDocument __pyx_f_4lxml_5etree_deepcopyNodeToDocument
static struct LxmlElementTree *(*__pyx_f_4lxml_5etree_elementTreeFactory)(struct LxmlElement *) = 0;
#define elementTreeFactory __pyx_f_4lxml_5etree_elementTreeFactory
static struct LxmlElementTree *(*__pyx_f_4lxml_5etree_newElementTree)(struct LxmlElement *, PyObject *) = 0;
#define newElementTree __pyx_f_4lxml_5etree_newElementTree
static struct LxmlElement *(*__pyx_f_4lxml_5etree_elementFactory)(struct LxmlDocument *, xmlNode *) = 0;
#define elementFactory __pyx_f_4lxml_5etree_elementFactory
static struct LxmlElement *(*__pyx_f_4lxml_5etree_makeElement)(PyObject *, struct LxmlDocument *, PyObject *, PyObject *, PyObject *, PyObject *, PyObject *) = 0;
#define makeElement __pyx_f_4lxml_5etree_makeElement
static struct LxmlElement *(*__pyx_f_4lxml_5etree_makeSubElement)(struct LxmlElement *, PyObject *, PyObject *, PyObject *, PyObject *, PyObject *) = 0;
#define makeSubElement __pyx_f_4lxml_5etree_makeSubElement
static void (*__pyx_f_4lxml_5etree_setElementClassLookupFunction)(_element_class_lookup_function, PyObject *) = 0;
#define setElementClassLookupFunction __pyx_f_4lxml_5etree_setElementClassLookupFunction
static PyObject *(*__pyx_f_4lxml_5etree_lookupDefaultElementClass)(PyObject *, PyObject *, xmlNode *) = 0;
#define lookupDefaultElementClass __pyx_f_4lxml_5etree_lookupDefaultElementClass
static PyObject *(*__pyx_f_4lxml_5etree_lookupNamespaceElementClass)(PyObject *, PyObject *, xmlNode *) = 0;
#define lookupNamespaceElementClass __pyx_f_4lxml_5etree_lookupNamespaceElementClass
static PyObject *(*__pyx_f_4lxml_5etree_callLookupFallback)(struct LxmlFallbackElementClassLookup *, struct LxmlDocument *, xmlNode *) = 0;
#define callLookupFallback __pyx_f_4lxml_5etree_callLookupFallback
static int (*__pyx_f_4lxml_5etree_tagMatches)(xmlNode *, const xmlChar *, const xmlChar *) = 0;
#define tagMatches __pyx_f_4lxml_5etree_tagMatches
static struct LxmlDocument *(*__pyx_f_4lxml_5etree_documentOrRaise)(PyObject *) = 0;
#define documentOrRaise __pyx_f_4lxml_5etree_documentOrRaise
static struct LxmlElement *(*__pyx_f_4lxml_5etree_rootNodeOrRaise)(PyObject *) = 0;
#define rootNodeOrRaise __pyx_f_4lxml_5etree_rootNodeOrRaise
static int (*__pyx_f_4lxml_5etree_hasText)(xmlNode *) = 0;
#define hasText __pyx_f_4lxml_5etree_hasText
static int (*__pyx_f_4lxml_5etree_hasTail)(xmlNode *) = 0;
#define hasTail __pyx_f_4lxml_5etree_hasTail
static PyObject *(*__pyx_f_4lxml_5etree_textOf)(xmlNode *) = 0;
#define textOf __pyx_f_4lxml_5etree_textOf
static PyObject *(*__pyx_f_4lxml_5etree_tailOf)(xmlNode *) = 0;
#define tailOf __pyx_f_4lxml_5etree_tailOf
static int (*__pyx_f_4lxml_5etree_setNodeText)(xmlNode *, PyObject *) = 0;
#define setNodeText __pyx_f_4lxml_5etree_setNodeText
static int (*__pyx_f_4lxml_5etree_setTailText)(xmlNode *, PyObject *) = 0;
#define setTailText __pyx_f_4lxml_5etree_setTailText
static PyObject *(*__pyx_f_4lxml_5etree_attributeValue)(xmlNode *, xmlAttr *) = 0;
#define attributeValue __pyx_f_4lxml_5etree_attributeValue
static PyObject *(*__pyx_f_4lxml_5etree_attributeValueFromNsName)(xmlNode *, const xmlChar *, const xmlChar *) = 0;
#define attributeValueFromNsName __pyx_f_4lxml_5etree_attributeValueFromNsName
static PyObject *(*__pyx_f_4lxml_5etree_getAttributeValue)(struct LxmlElement *, PyObject *, PyObject *) = 0;
#define getAttributeValue __pyx_f_4lxml_5etree_getAttributeValue
static PyObject *(*__pyx_f_4lxml_5etree_iterattributes)(struct LxmlElement *, int) = 0;
#define iterattributes __pyx_f_4lxml_5etree_iterattributes
static PyObject *(*__pyx_f_4lxml_5etree_collectAttributes)(xmlNode *, int) = 0;
#define collectAttributes __pyx_f_4lxml_5etree_collectAttributes
static int (*__pyx_f_4lxml_5etree_setAttributeValue)(struct LxmlElement *, PyObject *, PyObject *) = 0;
#define setAttributeValue __pyx_f_4lxml_5etree_setAttributeValue
static int (*__pyx_f_4lxml_5etree_delAttribute)(struct LxmlElement *, PyObject *) = 0;
#define delAttribute __pyx_f_4lxml_5etree_delAttribute
static int (*__pyx_f_4lxml_5etree_delAttributeFromNsName)(xmlNode *, const xmlChar *, const xmlChar *) = 0;
#define delAttributeFromNsName __pyx_f_4lxml_5etree_delAttributeFromNsName
static int (*__pyx_f_4lxml_5etree_hasChild)(xmlNode *) = 0;
#define hasChild __pyx_f_4lxml_5etree_hasChild
static xmlNode *(*__pyx_f_4lxml_5etree_findChild)(xmlNode *, Py_ssize_t) = 0;
#define findChild __pyx_f_4lxml_5etree_findChild
static xmlNode *(*__pyx_f_4lxml_5etree_findChildForwards)(xmlNode *, Py_ssize_t) = 0;
#define findChildForwards __pyx_f_4lxml_5etree_findChildForwards
static xmlNode *(*__pyx_f_4lxml_5etree_findChildBackwards)(xmlNode *, Py_ssize_t) = 0;
#define findChildBackwards __pyx_f_4lxml_5etree_findChildBackwards
static xmlNode *(*__pyx_f_4lxml_5etree_nextElement)(xmlNode *) = 0;
#define nextElement __pyx_f_4lxml_5etree_nextElement
static xmlNode *(*__pyx_f_4lxml_5etree_previousElement)(xmlNode *) = 0;
#define previousElement __pyx_f_4lxml_5etree_previousElement
static void (*__pyx_f_4lxml_5etree_appendChild)(struct LxmlElement *, struct LxmlElement *) = 0;
#define appendChild __pyx_f_4lxml_5etree_appendChild
static int (*__pyx_f_4lxml_5etree_appendChildToElement)(struct LxmlElement *, struct LxmlElement *) = 0;
#define appendChildToElement __pyx_f_4lxml_5etree_appendChildToElement
static PyObject *(*__pyx_f_4lxml_5etree_pyunicode)(const xmlChar *) = 0;
#define pyunicode __pyx_f_4lxml_5etree_pyunicode
static PyObject *(*__pyx_f_4lxml_5etree_utf8)(PyObject *) = 0;
#define utf8 __pyx_f_4lxml_5etree_utf8
static PyObject *(*__pyx_f_4lxml_5etree_getNsTag)(PyObject *) = 0;
#define getNsTag __pyx_f_4lxml_5etree_getNsTag
static PyObject *(*__pyx_f_4lxml_5etree_getNsTagWithEmptyNs)(PyObject *) = 0;
#define getNsTagWithEmptyNs __pyx_f_4lxml_5etree_getNsTagWithEmptyNs
static PyObject *(*__pyx_f_4lxml_5etree_namespacedName)(xmlNode *) = 0;
#define namespacedName __pyx_f_4lxml_5etree_namespacedName
static PyObject *(*__pyx_f_4lxml_5etree_namespacedNameFromNsName)(const xmlChar *, const xmlChar *) = 0;
#define namespacedNameFromNsName __pyx_f_4lxml_5etree_namespacedNameFromNsName
static void (*__pyx_f_4lxml_5etree_iteratorStoreNext)(struct LxmlElementIterator *, struct LxmlElement *) = 0;
#define iteratorStoreNext __pyx_f_4lxml_5etree_iteratorStoreNext
static void (*__pyx_f_4lxml_5etree_initTagMatch)(struct LxmlElementTagMatcher *, PyObject *) = 0;
#define initTagMatch __pyx_f_4lxml_5etree_initTagMatch
static xmlNs *(*__pyx_f_4lxml_5etree_findOrBuildNodeNsPrefix)(struct LxmlDocument *, xmlNode *, const xmlChar *, const xmlChar *) = 0;
#define findOrBuildNodeNsPrefix __pyx_f_4lxml_5etree_findOrBuildNodeNsPrefix
#if !defined(__Pyx_PyIdentifier_FromString)
#if PY_MAJOR_VERSION < 3
  #define __Pyx_PyIdentifier_FromString(s) PyString_FromString(s)
#else
  #define __Pyx_PyIdentifier_FromString(s) PyUnicode_FromString(s)
#endif
#endif

#ifndef __PYX_HAVE_RT_ImportModule
#define __PYX_HAVE_RT_ImportModule
static PyObject *__Pyx_ImportModule(const char *name) {
    PyObject *py_name = 0;
    PyObject *py_module = 0;
    py_name = __Pyx_PyIdentifier_FromString(name);
    if (!py_name)
        goto bad;
    py_module = PyImport_Import(py_name);
    Py_DECREF(py_name);
    return py_module;
bad:
    Py_XDECREF(py_name);
    return 0;
}
#endif

#ifndef __PYX_HAVE_RT_ImportFunction
#define __PYX_HAVE_RT_ImportFunction
static int __Pyx_ImportFunction(PyObject *module, const char *funcname, void (**f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    union {
        void (*fp)(void);
        void *p;
    } tmp;
    d = PyObject_GetAttrString(module, (char *)"__pyx_capi__");
    if (!d)
        goto bad;
    cobj = PyDict_GetItemString(d, funcname);
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C function %.200s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
#if PY_VERSION_HEX >= 0x02070000
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    tmp.p = PyCapsule_GetPointer(cobj, sig);
#else
    {const char *desc, *s1, *s2;
    desc = (const char *)PyCObject_GetDesc(cobj);
    if (!desc)
        goto bad;
    s1 = desc; s2 = sig;
    while (*s1 != '\0' && *s1 == *s2) { s1++; s2++; }
    if (*s1 != *s2) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, desc);
        goto bad;
    }
    tmp.p = PyCObject_AsVoidPtr(cobj);}
#endif
    *f = tmp.fp;
    if (!(*f))
        goto bad;
    Py_DECREF(d);
    return 0;
bad:
    Py_XDECREF(d);
    return -1;
}
#endif


static int import_lxml__etree(void) {
  PyObject *module = 0;
  module = __Pyx_ImportModule("lxml.etree");
  if (!module) goto bad;
  if (__Pyx_ImportFunction(module, "deepcopyNodeToDocument", (void (**)(void))&__pyx_f_4lxml_5etree_deepcopyNodeToDocument, "struct LxmlElement *(struct LxmlDocument *, xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "elementTreeFactory", (void (**)(void))&__pyx_f_4lxml_5etree_elementTreeFactory, "struct LxmlElementTree *(struct LxmlElement *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "newElementTree", (void (**)(void))&__pyx_f_4lxml_5etree_newElementTree, "struct LxmlElementTree *(struct LxmlElement *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "elementFactory", (void (**)(void))&__pyx_f_4lxml_5etree_elementFactory, "struct LxmlElement *(struct LxmlDocument *, xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "makeElement", (void (**)(void))&__pyx_f_4lxml_5etree_makeElement, "struct LxmlElement *(PyObject *, struct LxmlDocument *, PyObject *, PyObject *, PyObject *, PyObject *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "makeSubElement", (void (**)(void))&__pyx_f_4lxml_5etree_makeSubElement, "struct LxmlElement *(struct LxmlElement *, PyObject *, PyObject *, PyObject *, PyObject *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "setElementClassLookupFunction", (void (**)(void))&__pyx_f_4lxml_5etree_setElementClassLookupFunction, "void (_element_class_lookup_function, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "lookupDefaultElementClass", (void (**)(void))&__pyx_f_4lxml_5etree_lookupDefaultElementClass, "PyObject *(PyObject *, PyObject *, xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "lookupNamespaceElementClass", (void (**)(void))&__pyx_f_4lxml_5etree_lookupNamespaceElementClass, "PyObject *(PyObject *, PyObject *, xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "callLookupFallback", (void (**)(void))&__pyx_f_4lxml_5etree_callLookupFallback, "PyObject *(struct LxmlFallbackElementClassLookup *, struct LxmlDocument *, xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "tagMatches", (void (**)(void))&__pyx_f_4lxml_5etree_tagMatches, "int (xmlNode *, const xmlChar *, const xmlChar *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "documentOrRaise", (void (**)(void))&__pyx_f_4lxml_5etree_documentOrRaise, "struct LxmlDocument *(PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "rootNodeOrRaise", (void (**)(void))&__pyx_f_4lxml_5etree_rootNodeOrRaise, "struct LxmlElement *(PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "hasText", (void (**)(void))&__pyx_f_4lxml_5etree_hasText, "int (xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "hasTail", (void (**)(void))&__pyx_f_4lxml_5etree_hasTail, "int (xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "textOf", (void (**)(void))&__pyx_f_4lxml_5etree_textOf, "PyObject *(xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "tailOf", (void (**)(void))&__pyx_f_4lxml_5etree_tailOf, "PyObject *(xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "setNodeText", (void (**)(void))&__pyx_f_4lxml_5etree_setNodeText, "int (xmlNode *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "setTailText", (void (**)(void))&__pyx_f_4lxml_5etree_setTailText, "int (xmlNode *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "attributeValue", (void (**)(void))&__pyx_f_4lxml_5etree_attributeValue, "PyObject *(xmlNode *, xmlAttr *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "attributeValueFromNsName", (void (**)(void))&__pyx_f_4lxml_5etree_attributeValueFromNsName, "PyObject *(xmlNode *, const xmlChar *, const xmlChar *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "getAttributeValue", (void (**)(void))&__pyx_f_4lxml_5etree_getAttributeValue, "PyObject *(struct LxmlElement *, PyObject *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "iterattributes", (void (**)(void))&__pyx_f_4lxml_5etree_iterattributes, "PyObject *(struct LxmlElement *, int)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "collectAttributes", (void (**)(void))&__pyx_f_4lxml_5etree_collectAttributes, "PyObject *(xmlNode *, int)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "setAttributeValue", (void (**)(void))&__pyx_f_4lxml_5etree_setAttributeValue, "int (struct LxmlElement *, PyObject *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "delAttribute", (void (**)(void))&__pyx_f_4lxml_5etree_delAttribute, "int (struct LxmlElement *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "delAttributeFromNsName", (void (**)(void))&__pyx_f_4lxml_5etree_delAttributeFromNsName, "int (xmlNode *, const xmlChar *, const xmlChar *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "hasChild", (void (**)(void))&__pyx_f_4lxml_5etree_hasChild, "int (xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "findChild", (void (**)(void))&__pyx_f_4lxml_5etree_findChild, "xmlNode *(xmlNode *, Py_ssize_t)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "findChildForwards", (void (**)(void))&__pyx_f_4lxml_5etree_findChildForwards, "xmlNode *(xmlNode *, Py_ssize_t)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "findChildBackwards", (void (**)(void))&__pyx_f_4lxml_5etree_findChildBackwards, "xmlNode *(xmlNode *, Py_ssize_t)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "nextElement", (void (**)(void))&__pyx_f_4lxml_5etree_nextElement, "xmlNode *(xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "previousElement", (void (**)(void))&__pyx_f_4lxml_5etree_previousElement, "xmlNode *(xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "appendChild", (void (**)(void))&__pyx_f_4lxml_5etree_appendChild, "void (struct LxmlElement *, struct LxmlElement *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "appendChildToElement", (void (**)(void))&__pyx_f_4lxml_5etree_appendChildToElement, "int (struct LxmlElement *, struct LxmlElement *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "pyunicode", (void (**)(void))&__pyx_f_4lxml_5etree_pyunicode, "PyObject *(const xmlChar *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "utf8", (void (**)(void))&__pyx_f_4lxml_5etree_utf8, "PyObject *(PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "getNsTag", (void (**)(void))&__pyx_f_4lxml_5etree_getNsTag, "PyObject *(PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "getNsTagWithEmptyNs", (void (**)(void))&__pyx_f_4lxml_5etree_getNsTagWithEmptyNs, "PyObject *(PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "namespacedName", (void (**)(void))&__pyx_f_4lxml_5etree_namespacedName, "PyObject *(xmlNode *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "namespacedNameFromNsName", (void (**)(void))&__pyx_f_4lxml_5etree_namespacedNameFromNsName, "PyObject *(const xmlChar *, const xmlChar *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "iteratorStoreNext", (void (**)(void))&__pyx_f_4lxml_5etree_iteratorStoreNext, "void (struct LxmlElementIterator *, struct LxmlElement *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "initTagMatch", (void (**)(void))&__pyx_f_4lxml_5etree_initTagMatch, "void (struct LxmlElementTagMatcher *, PyObject *)") < 0) goto bad;
  if (__Pyx_ImportFunction(module, "findOrBuildNodeNsPrefix", (void (**)(void))&__pyx_f_4lxml_5etree_findOrBuildNodeNsPrefix, "xmlNs *(struct LxmlDocument *, xmlNode *, const xmlChar *, const xmlChar *)") < 0) goto bad;
  Py_DECREF(module); module = 0;
  return 0;
  bad:
  Py_XDECREF(module);
  return -1;
}

#endif /* !__PYX_HAVE_API__lxml__etree */
