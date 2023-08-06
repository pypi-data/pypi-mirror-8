/*
 * structs.c - Copyright 2000 by Cosimo Alfarano <Alfarano@CS.UniBo.It>
 * You can use this software under the terms of the GPL. If we meet some day,
 * and you think this stuff is worth it, you can buy me a beer in return.
 *
 * Thanks to md for this useful formula. Beer is beer.
 */


#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

#include "structs.h"
#include "macro.h"

struct wlp_node_t *wlpn_add(struct wlp_list_t *list,struct wlp_node_t *node)
{
	struct wlp_node_t *ret;
	
	if(node) {
		node->next = list->head;
		node->prev = list->tail;
		
		list->tail->next = node;
		list->head->prev = node;

		list->tail = node;

		list->count++;
		
		ret = node;
	} else {
		DBG("cannot add %s %s to list. NULL pointer?\n",
			node->left,node->right);
		ret = NULL;	
	}

	return ret;
}

void wlpn_free(struct wlp_node_t *node)
{
	free(node->left);
	free(node->right);
	free(node->owner);
	free(node);
}


struct wlp_node_t *wlpn_alloc(const char empty)
{
	static struct wlp_node_t *node;

	node = calloc(sizeof(struct wlp_node_t),1);

	if (!node) {
		perror("wlpn_create malloc");	
		
	/* calloc set *node to zero, it I don't want alloc anything,
	   leave it untouched, else alloc fields */
	} else if (!empty) {
		node->left = calloc(LINELEN+1,1);
		if (!node->left) {
			perror("wlpn_create malloc (left)");
			free(node);
			node = NULL;
		}

		/*if node is NULL, previous calloc returned error...*/
		if(node && !(node->right = calloc(LINELEN+1,1))) {
			perror("wlpn_create malloc (right)");
			free(node);
			node = NULL;
		}
	
		if(node && !(node->owner = calloc(LINELEN+1,1))) {
			perror("wlpn_create malloc (owner)");
			free(node);
			node = NULL;
		}
	}	
	return node;
}

struct wlp_list_t *wlpl_init(struct wlp_node_t *node)
{
	static struct wlp_list_t *list;

	list = malloc(sizeof(struct wlp_list_t));

	if (list) {
		list->head = node;
		list->tail = list->head;

		list->head->next = list->head;
		list->head->prev = list->head;

		list->count=1;
	} else {
                perror("wlpl_init malloc");
                return NULL;
	}
	
	return list;
}


struct wlp_node_t *wlpn_searchowner(struct wlp_list_t *mbl,const char *owner)
{
	struct wlp_node_t *ret;

	DBG("searching for %s\n",owner);

	if(!mbl)
		ret = NULL;
	else {
		int found = FALSE;
		ret = mbl->head;

		do {
			if(!strcmp(owner,ret->owner)) {
				DBG("found!\n");
				found = TRUE;
			} else {
				DBG("not found: %s\n",ret->onwer);
				ret = ret->next;
			}
		} while(ret != mbl->head && !found);

		if(!found)
			ret = NULL;
	}

	DBG("%s\n", (ret)?ret->owner:"not found");
	
	return ret;
}


struct wlp_node_t *wlpn_extract(struct wlp_list_t *list,struct wlp_node_t *node)
{
	struct wlp_node_t *ret;
	
	if(list && node) {
		node->prev->next = node->next;
		node->next->prev = node->prev;

		if(list->tail == node)
			list->tail = node->prev;
		if(list->head == node)
			list->head = node->next;

		list->count--;
		
		ret = node;
	} else {
		DBG("wlpn_extract: list addr %l and node %l (one is NULL)\n",list,addr)
		ret = NULL;
	}

	return ret;
}
