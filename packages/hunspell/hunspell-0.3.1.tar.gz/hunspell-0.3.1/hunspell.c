/*  hunspell.c
 *
 *  Copyright (C) 2009 - Sayamindu Dasgupta <sayamindu@gmail.com>
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published by
 *  the Free Software Foundation; either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Library General Public License for more details.
 *
 *  You should have received a copy of the GNU Library General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#include <Python.h>
#include <hunspell.h>

#ifndef PyVarObject_HEAD_INIT
	#define PyVarObject_HEAD_INIT(type, size) PyObject_HEAD_INIT(type) size,
#endif


/****************************************
                HunSpell
****************************************/

static PyObject *HunSpellError;

typedef struct {
	PyObject_HEAD 
	Hunhandle *handle;
	const char *encoding;
} HunSpell;

static int
HunSpell_init(HunSpell * self, PyObject *args, PyObject *kwds)
{
	PyObject *dpath;
	PyObject *apath;
    FILE *fh;

#if PY_VERSION_HEX < 0x03010000
	if (!PyArg_ParseTuple(args, "etet", Py_FileSystemDefaultEncoding, &dpath, Py_FileSystemDefaultEncoding, &apath))
#else
	if (!PyArg_ParseTuple(args, "O&O&", PyUnicode_FSConverter, &dpath, PyUnicode_FSConverter, &apath))
#endif
		return 1;

    /* Some versions of Hunspell_create() will succeed even if
    * there are no dictionary files. So test for permissions.
    */
    fh = fopen(dpath, "r");
    if (fh) {
        fclose(fh);
    } else {
        PyErr_SetFromErrno(HunSpellError);
        return -1;
    }

    fh = fopen(apath, "r");
    if (fh) {
        fclose(fh);
    } else {
        PyErr_SetFromErrno(HunSpellError);
        return -1;
    }

	self->handle = Hunspell_create(PyBytes_AsString(apath), PyBytes_AsString(dpath));
    if(!self->handle) {
        PyErr_SetString(HunSpellError, "Cannot open dictionary");
        return -1;
    }
	self->encoding = Hunspell_get_dic_encoding(self->handle);

	Py_DECREF(dpath);
	Py_DECREF(apath);

	return 0;
}

static void
HunSpell_dealloc(HunSpell * self)
{
	Hunspell_destroy(self->handle);
	Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
HunSpell_get_dic_encoding(HunSpell * self, PyObject *args)
{
	return Py_BuildValue("s", self->encoding);
}

static PyObject *
HunSpell_spell(HunSpell * self, PyObject *args)
{
	char *word;
	int retvalue;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;
	retvalue = Hunspell_spell(self->handle, word);
	PyMem_Free(word);

	return PyBool_FromLong(retvalue);
}


static PyObject *
HunSpell_suggest(HunSpell * self, PyObject *args)
{
	char *word, **slist;
	int i, num_slist, ret;
	PyObject *slist_list, *pystr;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;

	slist_list = PyList_New(0);
    if (!slist_list) {
        return NULL;
    }
	num_slist = Hunspell_suggest(self->handle, &slist, word);
	PyMem_Free(word);

	for (i = 0, ret = 0; !ret && i < num_slist; i++) {
        pystr = PyString_FromString(slist[i]);
        if (!pystr)
            break;
        ret = PyList_Append(slist_list, pystr);
        Py_DECREF(pystr);
	}

	Hunspell_free_list(self->handle, &slist, num_slist);
	return slist_list;
}

static PyObject *
HunSpell_analyze(HunSpell * self, PyObject *args)
{
	char *word, **slist;
	int i, num_slist, ret;
	PyObject *slist_list, *pystr;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;

	slist_list = PyList_New(0);
    if (!slist_list) {
        return NULL;
    }
	num_slist = Hunspell_analyze(self->handle, &slist, word);
	PyMem_Free(word);

	for (i = 0, ret = 0; !ret && i < num_slist; i++) {
        pystr = PyString_FromString(slist[i]);
        if (!pystr)
            break;
        ret = PyList_Append(slist_list, pystr);
        Py_DECREF(pystr);
	}

	Hunspell_free_list(self->handle, &slist, num_slist);
	return slist_list;
}

static PyObject *
HunSpell_stem(HunSpell * self, PyObject *args)
{
	char *word, **slist;
	int i, num_slist, ret;
	PyObject *slist_list, *pystr;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;

	slist_list = PyList_New(0);
    if (!slist_list) {
        return NULL;
    }
	num_slist = Hunspell_stem(self->handle, &slist, word);
	PyMem_Free(word);

	for (i = 0, ret = 0; !ret && i < num_slist; i++) {
        pystr = PyString_FromString(slist[i]);
        if (!pystr)
            break;
        ret = PyList_Append(slist_list, pystr);
        Py_DECREF(pystr);
	}

	Hunspell_free_list(self->handle, &slist, num_slist);
	return slist_list;
}

static PyObject *
HunSpell_generate(HunSpell * self, PyObject *args)
{
	char *word1, *word2, **slist;
	int i, num_slist, ret;
	PyObject *slist_list, *pystr;

	if (!PyArg_ParseTuple(args, "etet", self->encoding, &word1, self->encoding, &word2))
		return NULL;

	slist_list = PyList_New(0);
    if (!slist_list) {
        return NULL;
    }
	num_slist = Hunspell_generate(self->handle, &slist, word1, word2);
	PyMem_Free(word1);
	PyMem_Free(word2);

	for (i = 0, ret = 0; !ret && i < num_slist; i++) {
        pystr = PyString_FromString(slist[i]);
        if (!pystr)
            break;
        ret = PyList_Append(slist_list, pystr);
        Py_DECREF(pystr);
	}

	Hunspell_free_list(self->handle, &slist, num_slist);
	return slist_list;
}

static PyObject *
HunSpell_add(HunSpell * self, PyObject *args)
{
	char *word;
	int retvalue;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;
	retvalue = Hunspell_add(self->handle, word);
	PyMem_Free(word);

	return PyInt_FromLong(retvalue);
}

static PyObject *
HunSpell_add_with_affix(HunSpell * self, PyObject *args)
{
	char *word, *example;
	int retvalue;

	if (!PyArg_ParseTuple(args, "etet", self->encoding, &word, self->encoding, &example))
		return NULL;
	retvalue = Hunspell_add_with_affix(self->handle, word, example);
	PyMem_Free(word);
	PyMem_Free(example);

	return PyInt_FromLong(retvalue);
}

static PyObject *
HunSpell_remove(HunSpell * self, PyObject *args)
{
	char *word;
	int retvalue;

	if (!PyArg_ParseTuple(args, "et", self->encoding, &word))
		return NULL;
	retvalue = Hunspell_remove(self->handle, word);
	PyMem_Free(word);

	return PyInt_FromLong(retvalue);
}

static PyMethodDef HunSpell_methods[] = {
	{"get_dic_encoding", (PyCFunction) HunSpell_get_dic_encoding,
	 METH_NOARGS,
	 "Gets encoding of loaded dictionary."},
	{"spell", (PyCFunction) HunSpell_spell, METH_VARARGS,
	 "Checks the spelling of the given word."},
	{"suggest", (PyCFunction) HunSpell_suggest, METH_VARARGS,
	 "Provide suggestions for the given word."},
	{"analyze", (PyCFunction) HunSpell_analyze, METH_VARARGS,
	 "Provide morphological analysis for the given word."},
	{"stem", (PyCFunction) HunSpell_stem, METH_VARARGS,
	 "Stemmer method."},
	{"generate", (PyCFunction) HunSpell_generate, METH_VARARGS,
	 "Provide morphological generation for the given word."},
	{"add", (PyCFunction) HunSpell_add, METH_VARARGS,
	 "Adds the given word into the runtime dictionary"},
	{"add_with_affix", (PyCFunction) HunSpell_add_with_affix, METH_VARARGS,
	 "Adds the given word with affix flags of the example (a dictionary word) \
     into the runtime dictionary"},
	{"remove", (PyCFunction) HunSpell_remove, METH_VARARGS,
	 "Removes the given word from the runtime dictionary"},
	{NULL}
};

static PyTypeObject HunSpellType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"HunSpell",		/* tp_name */
	sizeof(HunSpell),	/* tp_basicsize */
	0,			/* tp_itemsize */
	(destructor) HunSpell_dealloc,	/* tp_dealloc */
	0,			/* tp_print */
	0,			/* tp_getattr */
	0,			/* tp_setattr */
	0,			/* tp_compare */
	0,			/* tp_repr */
	0,			/* tp_as_number */
	0,			/* tp_as_sequence */
	0,			/* tp_as_mapping */
	0,			/* tp_hash */
	0,			/* tp_call */
	0,			/* tp_str */
	0,			/* tp_getattro */
	0,			/* tp_setattro */
	0,			/* tp_as_buffer */
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,	/* tp_flags */
	"HunSpell object",	/* tp_doc */
	0,			/* tp_traverse */
	0,			/* tp_clear */
	0,			/* tp_richcompare */
	0,			/* tp_weaklistoffset */
	0,			/* tp_iter */
	0,			/* tp_iternext */
	HunSpell_methods,	/* tp_methods */
	0,			/* tp_members */
	0,			/* tp_getset */
	0,			/* tp_base */
	0,			/* tp_dict */
	0,			/* tp_descr_get */
	0,			/* tp_descr_set */
	0,			/* tp_dictoffset */
	(initproc) HunSpell_init,	/* tp_init */
	0,			/* tp_alloc */
	0,			/* tp_new */
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef hunspellmodule = {
	PyModuleDef_HEAD_INIT,
	"hunspell",	/* name of module */
	NULL,		/* module documentation, may be NULL */
	-1, /* TODO */	/* size of per-interpreter state of the module,
			   or -1 if the module keeps state in global variables. */
	HunSpell_methods
};
#endif

/******************** Module Initialization function ****************/

#if PY_MAJOR_VERSION >= 3
PyObject*
PyInit_hunspell(void)
{
	PyObject *mod;

	// Create the module
	mod = PyModule_Create(&hunspellmodule);
	if (mod == NULL) {
		return NULL;
	}

	// Fill in some slots in the type, and make it ready
	HunSpellType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&HunSpellType) < 0) {
		return NULL;
	}
	// Add the type to the module.
	Py_INCREF(&HunSpellType);
	PyModule_AddObject(mod, "HunSpell", (PyObject *)&HunSpellType);
    HunSpellError = PyErr_NewException("hunspell.error", NULL, NULL);
    Py_INCREF(HunSpellError);
	return mod;
}
#else
PyObject*
inithunspell(void)
{
	PyObject *mod;

	// Create the module
	mod = Py_InitModule3("hunspell", NULL,
			     "An extension for the Hunspell spell checker engine");
	if (mod == NULL) {
		return NULL;
	}

	// Fill in some slots in the type, and make it ready
	HunSpellType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&HunSpellType) < 0) {
		return NULL;
	}
	// Add the type to the module.
	Py_INCREF(&HunSpellType);
	PyModule_AddObject(mod, "HunSpell", (PyObject *)&HunSpellType);
    HunSpellError = PyErr_NewException("hunspell.error", NULL, NULL);
    Py_INCREF(HunSpellError);
	return mod;
}
#endif
