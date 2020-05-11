"""URL patterns for learning_log app."""

from django.urls import path

from . import views


app_name = 'learning_log'

urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    
    # ex: /topics/
    path('topics/', views.topics, name='topics'),

    # ex: /topics/1/
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # ex: /new_topic/
    path('new_topic/', views.new_topic, name='new_topic'),

    # ex: /new_entry/1/
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # ex: /edit_entry/1/
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]

