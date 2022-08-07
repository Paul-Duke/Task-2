from faulthandler import disable
from hashlib import new
from logging import PlaceHolder
from multiprocessing import context
from tkinter import DISABLED
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from random import choice

from . import util

class NewPageForm(forms.Form):
    entryHead = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Page title. Please enter in English only'}
    ))
    entryBody = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Page text in Markdown style. Please enter in English only'}
    ))
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    markdownpage = Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render (request, "encyclopedia/fileNoneExist.html", {
        "entryHead": entry
    })  
    else:
        return render (request,"encyclopedia/entry.html", {
        "entry": markdownpage.convert(page),
        "entryHead": entry
    })


def search(request):
    search_page = request.GET.get("q")
    search_list = []
    if util.get_entry(search_page) is not None:
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": search_page}))
    else:
        search_page_lower = search_page.lower()
        entries = util.list_entries()
        for entry in entries:
           search_cycle = entry.lower().find(search_page_lower)
           if search_cycle != -1: 
              search_list.append(entry)
              print(search_list)
        if len(search_list)==0:
            return render (request, "encyclopedia/fileNoneExist.html", {
                "entryHead": search_page
        })
        else:
             return render (request, "encyclopedia/search_result.html", {
                "entries": search_list
        })
def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    markdownpage = Markdown()
    page = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": markdownpage.convert(page),
        "entryHead": entry
    })
def new_entry(request):
    markdownpage = Markdown()
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
           entryHead=form.cleaned_data['entryHead']
           entryBody=form.cleaned_data['entryBody']
           if entryHead in util.list_entries():
                error = "This page is exist. You can find it and change."
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "error": error,
                    "edit": False
                })
           else: 
               util.save_entry(entryHead, entryBody)
               return render (request,"encyclopedia/entry.html", {
                    "entry": markdownpage.convert(entryBody),
                    "entryHead": entryHead
               })
    return render(request, "encyclopedia/new_entry.html", {
        "form": NewPageForm() 
    })

def edit_page(request, entryHead):
    entryBody =util.get_entry(entryHead) 
    form = NewPageForm()
    form.fields['entryHead'].initial = entryHead
    form.fields['entryBody'].initial = entryBody
    form.fields['entryHead'].widget = forms.HiddenInput()
    if request.method == "POST":
        entryHead = request.POST['entryHead']
        entryBody = request.POST['entryBody']
        util.save_entry(entryHead, entryBody)
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'entry': entryHead}))
    return render (request,"encyclopedia/new_entry.html", {
                "form": form,
                "edit": True,
                "entryHead": form.fields['entryHead'].initial
    })

