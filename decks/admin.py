from django.contrib import admin
from .models import Profile, Subject, Deck, Flashcard

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'owner', 'created_at')
    search_fields = ('title', 'owner__username')
    list_filter = ('subject', 'created_at')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('question', 'deck', 'created_at')
    search_fields = ('question', 'deck__title')
    list_filter = ('deck', 'created_at')
