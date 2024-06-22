from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Question, Answer
from django.urls import reverse, reverse_lazy
from .forms import CommentForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def lik_view(request, pk):
    """ A function that allows users to post likes """
    if request.method == 'POST':
        request = get_object_or_404(Question, pk=pk)
        if request.user in question.likes.all():
            question.likes.remove(request.user)
            liked = False
        else:
            question.likes.add(request.user)
            liked = True
        return redirect('soac_base:question-detail', pk=pk)
    else:
        return HttpResponseBadRequest('Invalid request method.')

class QuestionListView(ListView):
    """ A class that list the recent questions based on Time """
    model = Question
    context_object_name = 'questions'
    order = ['-date_created']

class QuestionDetailView(DetailView):
    """A class that url the question and readmore"""
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data()
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

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

class AnswerCreateView(CreateView):
    """ A class that enable users to answer Questions """
    model = Answer
    form_class = CommentForm

    template_name = 'soac_base/question-answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('soac_base:question-lists')

class AnswerDetailView(CreateView):
    """ A class that shows the details of the answer """
    model = Answer
    form_class = CommentForm

    templete_name = 'soac_base/question-detail.html'

    def form_valid(self, form):
        form.instamce.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('soac_base:question-detail')
