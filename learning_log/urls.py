"""URL patterns for learning_log app."""

from django.urls import path

from . import views


app_name = 'learning_log'

urlpatterns = [
    # Ex: /
    path('', views.index, name='index'),

    # Ex: /topics/
    path('topics/', views.topics, name='topics'),

    # Ex: /topics/1/
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Ex: /new_topic/
    path('new_topic/', views.new_topic, name='new_topic'),

    # Ex: /edit_topic/1/
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),

    # Ex: /delete_topic/1/
    path('delete_topic/<int:topic_id>/',
         views.delete_topic,
         name='delete_topic'),

    # Ex: /new_entry/1/
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # Ex: /edit_entry/1/
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

    # Ex: /delete_entry/1/
    path('delete_entry/<int:entry_id>/',
         views.delete_entry,
         name='delete_entry'),
]
