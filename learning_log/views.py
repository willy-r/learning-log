from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Entry, Topic
from .forms import EntryForm, TopicForm


def check_topic_owner(current_user, topic_owner):
    """Raises a Http404 if the current user is not the topic owner."""
    if current_user != topic_owner:
        raise Http404


def index(request):
    return render(request, 'learning_log/index.html')


@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user)
    paginator = Paginator(topics, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'learning_log/topics.html', context)


def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if not topic.public and request.user != topic.owner:
        raise Http404
    entries = topic.entry_set.all()
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
            new_topic.save()
            # Redirects to /topics/<int:topic_id>/
            return redirect(
                reverse('learning_log:topic', args=(new_topic.id,))
            )
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)


@login_required
def edit_topic(request, topic_id):
    """Edits a specific topic."""
    topic = get_object_or_404(Topic, pk=topic_id)
    check_topic_owner(request.user, topic.owner)

    if request.method != 'POST':
        # Shows the form with the topic data.
        form = TopicForm(instance=topic)
    else:
        # POST data submitted; validate the form with the new data and
        # the topic data, then save the updated topic.
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            # Redirects to the edited topic.
            return redirect(reverse('learning_log:topic', args=(topic.id,)))

    context = {
        'topic': topic,
        'form': form,
    }
    return render(request, 'learning_log/edit_topic.html', context)


@login_required
def delete_topic(request, topic_id):
    """Deletes a topic and the entries from this topic completly."""
    topic = get_object_or_404(Topic, pk=topic_id)
    check_topic_owner(request.user, topic.owner)

    # Topic will be delete if the request method is 'POST'
    # (there will be a form asking if the user really want delete the
    # topic, if the user click on the submit button, the topic is
    # deleted).
    if request.method == 'POST':
        topic.delete()
        # Redirects to the topic list.
        return redirect(reverse('learning_log:topics'))

    context = {'topic': topic}
    return render(request, 'learning_log/delete_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    check_topic_owner(request.user, topic.owner)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # Redirects to /topics/<int:topic_id>/
            return redirect(
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
    check_topic_owner(request.user, topic.owner)

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            # Redirects to /topics/<int:topic_id>/
            return redirect(
                reverse('learning_log:topic', args=(topic.id,))
            )
    context = {
        'entry': entry,
        'topic': topic,
        'form': form,
    }
    return render(request, 'learning_log/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    """Deletes an entry completly."""
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic
    check_topic_owner(request.user, topic.owner)

    # Deletes the entry and redirects to the topic of the entry deleted.
    entry.delete()
    return redirect(reverse('learning_log:topic', args=(topic.id,)))
