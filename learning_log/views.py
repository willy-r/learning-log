from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Entry, Topic
from .forms import EntryForm, TopicForm


def owner_check(user, owner):
    if user != owner:
        raise Http404


def index(request):
    return render(request, 'learning_log/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    paginator = Paginator(topics, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'learning_log/topics.html', context)


def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if not topic.public and request.user != topic.owner:
        raise Http404  
    entries = topic.entry_set.order_by('-date_added')
    paginator = Paginator(entries, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'topic': topic, 
        'page_obj': page_obj,
    }
    return render(request, 'learning_log/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            if new_topic.public:
                new_topic.make_public()
            new_topic.save()
            # Redirects to /topics/<int:topic_id>/
            return HttpResponseRedirect(
                reverse('learning_log:topic', args=(new_topic.id,))
            )
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    owner_check(request.user, topic.owner)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # Redirects to /topics/<int:topic_id>/
            return HttpResponseRedirect(
                reverse('learning_log:topic', args=(topic.id,))
            )
    context = {
        'topic': topic,
        'form': form,
    }
    return render(request, 'learning_log/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic
    owner_check(request.user, topic.owner)

    if request.method != 'POST':
        # Populate the form with the entry data.
        form = EntryForm(instance=entry)
    else:
        # Create and save the form with the new entry data.
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            # Redirects to /topics/<int:topic_id>/ 
            return HttpResponseRedirect(
                reverse('learning_log:topic', args=(topic.id,))
            )
    context = {
        'entry': entry,
        'topic': topic,
        'form': form,
    }
    return render(request, 'learning_log/edit_entry.html', context)

