from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Question, Answer

# Create your views here.

def home(request):
    return render(request, 'home.html')

class QuestionListView(ListView):
    """ A class that list the recent questions based on Time """
    model = Question
    context_object_name = 'questions'
    order = ['-date_created']

class QuestionDetailView(DetailView):
    """A class that url the question and readmore"""
    model = Question

class QuestionCreateView(LoginRequiredMixin, CreateView):
    """ A class that allows users to post questions """
    model = Question
    fields = ['title', 'content']
    context_object_name = 'questions'

    def form_valid(self, form):
        """ function that validates the form """
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ A class that permits users to update their questions """
    model = Question
    fields = ['title', 'content']
    permission_required = 'soac_base.change_question'

    def form_valid(self, form):
        """ function that validates the form"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def has_permission(self):
        """
        A help function to map the request with the update permissions 
        """
        question = self.get_object()
        return super().has_permission() and question.user == self.request.user

class QuestionDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """ An instance that permits the rightful user to delete their question """
    model = Question
    context_object_name = 'question'
    permission_required = 'soa_base.delete_question'
    successful_url = "/"

    def has_permission(self):
        """ A function that map the request with the delete permissions """
        question = self.get_object()
        return super().has_permission() and question.user == self.request.user
