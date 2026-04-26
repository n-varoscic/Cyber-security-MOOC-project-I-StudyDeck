from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subjects/', views.subject_list, name='subjects'),
    path('subjects/create/', views.create_subject, name='create_subject'),
    path('subjects/<int:subject_id>/decks/', views.deck_list, name='deck_list'),
    path('subjects/<int:subject_id>/decks/create/', views.create_deck, name='create_deck'),
    path('decks/<int:deck_id>/', views.view_deck, name='view_deck'),
    path('decks/<int:deck_id>/study/', views.study_deck, name='study_deck'),
    path('decks/<int:deck_id>/flashcards/create/', views.create_flashcard, name='create_flashcard'),
    path('flashcards/<int:flashcard_id>/edit/', views.edit_flashcard, name='edit_flashcard'),
    path('flashcards/<int:flashcard_id>/delete/', views.delete_flashcard, name='delete_flashcard'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
]
