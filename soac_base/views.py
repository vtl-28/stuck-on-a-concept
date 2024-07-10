from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Question, Answer
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import CommentForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def features(request):
    return render(request, 'features.html')


@login_required
def like_view(request, pk):
    """ A function that allows users to post likes """
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('soac_base:question-detail', args=[str(pk)]))

class QuestionListView(ListView):
    """ A class that list the recent questions based on Time """
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

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

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """ A class that permits users to update their questions """
    model = Question
    fields = ['title', 'content']
    permission_required = 'soac_base.change_question'

    def form_valid(self, form):
        """ function that validates the form"""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False
class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """ An instance that permits the rightful user to delete their question """
    model = Question
    context_object_name = 'question'
    success_url = "/questions"

    def test_func(self):
        questions = self.get_object()
        if self.request.user == questions.user:
            return True
        return False

class AnswerCreateView(LoginRequiredMixin,CreateView):
    """ A class that enable users to answer Questions """
    model = Answer
    form_class = CommentForm
    context_object_name =  'question'

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
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('soac_base:question-detail')
