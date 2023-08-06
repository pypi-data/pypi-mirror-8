/*
 * wlp.c - Copyright 2000, 2001 by Cosimo Alfarano <Alfarano@CS.UniBo.It>
 * You can use this software under the terms of the GPL. If we meet some day,
 * and you think this stuff is worth it, you can buy me a beer in return.
 *
 * Thanks to md for this useful formula. Beer is beer.
 */

#include <Python.h>
#include <stdio.h>
#include <unistd.h>

#include "structs.h"
#include "macro.h"


static FILE *fd = NULL;

struct wlp_list_t *list;

static PyObject *node2dict(struct wlp_node_t *node);



/* 
 * wlp_setfilebyname(): get FILE* fd from filename string.
 */

static PyObject *wlp_setfilebyname(PyObject *self, PyObject *args) {
	char *file;

	
	DBG("setfilebyname\n");
	if (!PyArg_ParseTuple(args, "s", &file))
		return NULL;

	if((fd = fopen(file,"r"))) {
		return Py_None;
	} else {
		PyErr_SetFromErrno(PyExc_Exception);
/*	
		    PyErr_SetString(PyExc_Exception,
		    (errno<=sys_nerr-1)?
		    sys_errlist[errno]:
		    "Unknown Error on fopen() of confifuration file");
*/		
		return NULL;
	}
}



/* 
 * wlp_setfilebydf(): get FILE* fd from FileObject.
 */

static PyObject *wlp_setfilebyfd(PyObject *self, PyObject *args) {
	PyObject *file = NULL;
	
        if(!PyArg_ParseTuple(args, "O", &file))
		return NULL;

	if(!file)
		return NULL;

	if(!PyFile_Check(file))
		return NULL;

	fd = PyFile_AsFile(file);

	return Py_None;
}

/* 
 * wlp_mkdict(): make a dictonary of the form
 * {ownername: {var1: val1, var2: val2,...}}
 */

static PyObject *wlp_mkdict(PyObject *self, PyObject *args) {
	PyObject *pydicttmp = NULL;
	PyObject *pydict = PyDict_New();
	struct wlp_node_t *tmp;
	int count;

	if(!pydict)
		return NULL;

	/* fopen()*/
	if(fd)
		parse(fd);
	else
		return Py_None;
	
	if(list)
		for(tmp = list->head, count = 0;
		    tmp != list->head || count == 0;
		    tmp = tmp->next, count++) {
			DBG("FOUND(%d) '%s' ('%s': '%s')\n",count,tmp->owner,tmp->left,tmp->right);
			pydicttmp = PyDict_GetItem(pydict,
				PyString_FromString(tmp->owner));

			if(!pydicttmp) {
				DBG("%s: owner not found, create new item\n",
					tmp->owner);
				PyDict_SetItemString(pydict,
					tmp->owner,
					node2dict(tmp));
			} else {
				DBG("%s: owner found,appendig items\n",
					tmp->owner);
				PyDict_SetItemString(pydicttmp,
					tmp->left,
					Py_BuildValue("s",tmp->right));
				PyDict_SetItemString(pydict,
					tmp->owner,
					pydicttmp);
			}
		}

	return pydict;
}

/* 
 * node2dict(): transoform a wlp_node_t node in a python dictionary of the form
 *	 { var: val }
 * to be used by mkdict()
 */

static PyObject *node2dict(struct wlp_node_t *node) {
	PyObject *dict = PyDict_New();

	if(!dict)
		dict = Py_None;
	else {
		PyDict_SetItem(dict,
			Py_BuildValue("s",node->left),
			Py_BuildValue("s",node->right));
	}

	return dict;

}

static PyMethodDef wlp_methods[] = {
	{"mkdict", wlp_mkdict, METH_VARARGS},
	{"setfilebyname", wlp_setfilebyname, METH_VARARGS},
	{"setfilebyfd", wlp_setfilebyfd, METH_VARARGS},
	{NULL,NULL}
};


void initwlp() {
	(void) Py_InitModule("wlp",wlp_methods);
}
