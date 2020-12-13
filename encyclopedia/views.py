from django.shortcuts import render
import markdown
from . import util,forms
from .forms import add_entry
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from django import forms as f

form = forms.NewSearchForm()

def index(request):
    
    return render(request, "index.html", {
        "entries": util.list_entries(),
        "form" : form
    })

def entry(request, entry):
    markdowner = markdown.Markdown()
    entrypage = util.get_entry(entry)
    if entrypage is None:
        return render(request,"noexist.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "entry.html", {
            "entry": markdowner.convert(entrypage),
            "entryTitle": entry
        })

def new_entry(request):
    if request.method == "POST":
        form = add_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Title"]
            content = form.cleaned_data["Content"]
            print(form.cleaned_data["Edit"])
            if util.get_entry(title) is None:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            elif form.cleaned_data["Edit"] is True:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))

            else:
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
        else:
            return render(request, "add.html", {
                "form": form
            })
    else: 
        return render(request, "add.html", {
                "form": add_entry()
        })
        

def search(request):
    if request.method == "GET":
        form = forms.NewSearchForm(request.GET)
      
        if form.is_valid():
            searchquery = form.cleaned_data["search"].lower()
            all_entries = util.list_entries()
            
       
            files=[filename for filename in all_entries if searchquery in filename.lower()]
    

            if len(files) == 0:


                return render(request,"noexist.html")

            
            elif len(files) == 1 and files[0].lower() == searchquery:

                title = files[0]
                return entry(request, title)

            
            else: 

                title = [filename for filename in files if searchquery == filename.lower()]

                if len(title)>0:
                    return get_page(request, title[0])
                else:
                    return render(request,"search_results.html",{
                        'results':files,
                        "form":form

                    })

        else:
            # not a valid request
            return index(request)


    return index(request)


def random_page(request):

    return entry(request,choice( util.list_entries()))


def edit_page(request, entry):
    entry_page = util.get_entry(entry)
    if entry_page is None: 
       return render(request, "noexist.html")
    else: 
        form = add_entry()
        form.fields["Title"].widget = f.TextInput(attrs={
        'placeholder': entry
        })
        form.fields["Content"].widget = f.Textarea(attrs={
        'placeholder': entry_page
        })
        form.fields["Edit"].intial = True
        return render(request, "add.html", {
            "form": form, 
            "entryTitle": form.fields["Title"].widget
        })