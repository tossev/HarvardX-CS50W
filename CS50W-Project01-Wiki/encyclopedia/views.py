from django.shortcuts import render, redirect
import markdown2
import random
from django import forms
from django.contrib import messages

from . import util


class UserForm(forms.Form):
    title = forms.CharField(label='',
                            min_length=1,
                            widget=forms.TextInput(attrs={'class': "col-md-2 form-control",
                                                          'placeholder': 'Title'}))
    text = forms.CharField(label='',
                           widget=forms.Textarea(
                               attrs={'class': 'form-control col-md-12',
                                      'placeholder': 'Your text here...'}))


def index(request):
    return render(request, "encyclopedia/index.html",
                  {"entries": util.list_entries()})


def entry(request, entry_name):
    entry_text = util.get_entry(entry_name)
    if entry_text:
        return render(request,
                      "encyclopedia/entry_page.html", {
                          "entry_title": util.entry_in_database(entry_name),
                          "text": markdown2.markdown(entry_text)})
    else:
        return render(request,
                      "encyclopedia/error.html", {
                          'title': 'Not found',
                          'message': 'Requested page was not found.'})


def random_entry(request):
    entries = util.list_entries()
    stop = len(entries) - 1
    return redirect('entry', entries[random.randint(0, stop)])


def search_results(request):
    if request.method == 'POST':
        search_input = request.POST.get('q')
        if search_input != '':
            if util.entry_in_database(search_input):
                return redirect('entry', search_input)
        return render(request,
                      "encyclopedia/search_results.html", {
                          'results': util.query_as_substring(search_input)})
    else:
        return redirect('index')


def new_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if util.entry_in_database(title):
                messages.add_message(request, messages.ERROR, 'Entry already exists.')
                return render(request, 'encyclopedia/new_page.html', {'form': form})
                # return render(request,
                #               "encyclopedia/error.html", {
                #                   'title': 'Duplicate error',
                #                   'message': 'Entry already exists.'})
            util.save_entry(title.capitalize(), form.cleaned_data['text'])
            return redirect('entry', title)
    else:
        form = UserForm()
    return render(request, 'encyclopedia/new_page.html', {'form': form})


def edit_page(request, entry_name):
    if request.method == 'POST':
        print('POST request')
        form = UserForm(request.POST)
        form.fields['title'].required = False
        if form.is_valid():
            util.save_entry(entry_name, form.cleaned_data['text'])
            return redirect('entry', entry_name)
    else:
        form = UserForm(initial={'text': util.get_entry(entry_name)})
    return render(request,
                  'encyclopedia/edit_page.html',{
                      'form': form,
                      'title': entry_name})
