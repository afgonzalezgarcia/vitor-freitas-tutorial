from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from .models import Board, Post, Topic
from .forms import NewTopicForm

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html',  locals())

def board_topics(request, pk=None):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html',  {'board': board})

def new_topic(request, pk=None):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
