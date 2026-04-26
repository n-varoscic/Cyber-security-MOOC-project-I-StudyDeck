import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Profile, Subject, Deck, Flashcard
from .forms import (
    UserRegistrationForm, ProfileForm, SubjectForm, 
    DeckForm, FlashcardForm, SearchForm
)

logger = logging.getLogger(__name__)


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            logger.info(f'New user registered: {user.username}')
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f'User logged in: {username}')
            return redirect('dashboard')
        else:
            # FLAW 5: Security Logging and Monitoring Failures
            # No logging of failed login attempts

            messages.error(request, 'Invalid username or password.')
            
            # FIX 5: Implement proper logging of failed login attempts for security monitoring
            #logger.warning(f'Failed login attempt for username: {username}')
        
            return redirect('login')
    
    return render(request, 'login.html')


@login_required
def logout_view(request):
    """User logout view."""
    logger.info(f'User logged out: {request.user.username}')
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    """User dashboard showing their subjects and decks."""
    subjects = Subject.objects.filter(owner=request.user)
    decks = Deck.objects.filter(owner=request.user)
    
    return render(request, 'dashboard.html', {
        'subjects': subjects,
        'decks': decks,
    })


@login_required
def subject_list(request):
    """List user's subjects."""
    subjects = Subject.objects.filter(owner=request.user)
    return render(request, 'subjects.html', {'subjects': subjects})


@login_required
def create_subject(request):
    """Create a new subject."""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.owner = request.user
            subject.save()
            logger.info(f'Subject created: {subject.name} by {request.user.username}')
            messages.success(request, 'Subject created successfully!')
            return redirect('subjects')
    else:
        form = SubjectForm()
    
    return render(request, 'create_subject.html', {'form': form})


@login_required
def deck_list(request, subject_id):
    """List decks in a subject."""
    subject = get_object_or_404(Subject, id=subject_id, owner=request.user)
    decks = subject.decks.all()
    
    return render(request, 'decks.html', {
        'subject': subject,
        'decks': decks,
    })


@login_required
def create_deck(request, subject_id):
    """Create a new deck."""
    subject = get_object_or_404(Subject, id=subject_id, owner=request.user)
    
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.owner = request.user
            deck.subject = subject
            deck.save()
            logger.info(f'Deck created: {deck.title} by {request.user.username}')
            messages.success(request, 'Deck created successfully!')
            return redirect('deck_list', subject_id=subject_id)
    else:
        form = DeckForm()
        form.fields['subject'].initial = subject
    
    return render(request, 'create_deck.html', {
        'form': form,
        'subject': subject,
    })


@login_required
def view_deck(request, deck_id):
    """View flashcards in a deck."""
    # FLAW 1: Broken Access Control
    # The deck is fetched by ID only, without checking if the user owns it.
    # An attacker can modify the URL to view/edit other users' decks.
    deck = Deck.objects.get(id=deck_id)
    
    # FIX 1: Check ownership before returning data
    #deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    
    flashcards = deck.flashcards.all()
    
    return render(request, 'flashcards.html', {
        'deck': deck,
        'flashcards': flashcards,
    })


@login_required
def create_flashcard(request, deck_id):
    """Create a new flashcard."""
    deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.deck = deck
            flashcard.save()
            logger.info(f'Flashcard created in deck: {deck.title} by {request.user.username}')
            messages.success(request, 'Flashcard created successfully!')
            return redirect('view_deck', deck_id=deck_id)
    else:
        form = FlashcardForm()
    
    return render(request, 'create_flashcard.html', {
        'form': form,
        'deck': deck,
    })


@login_required
def edit_flashcard(request, flashcard_id):
    """Edit a flashcard."""
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    deck = flashcard.deck
    
    # Verify ownership
    if deck.owner != request.user:
        logger.warning(f'Unauthorized access attempt by {request.user.username} to flashcard {flashcard_id}')
        raise Http404()
    
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            flashcard = form.save()
            logger.info(f'Flashcard updated by {request.user.username}')
            messages.success(request, 'Flashcard updated successfully!')
            return redirect('view_deck', deck_id=deck.id)
    else:
        form = FlashcardForm(instance=flashcard)
    
    return render(request, 'edit_flashcard.html', {
        'form': form,
        'flashcard': flashcard,
        'deck': deck,
    })


@login_required
def delete_flashcard(request, flashcard_id):
    """Delete a flashcard."""
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    deck = flashcard.deck
    
    if deck.owner != request.user:
        logger.warning(f'Unauthorized delete attempt by {request.user.username} to flashcard {flashcard_id}')
        raise Http404()
    
    if request.method == 'POST':
        deck_id = deck.id
        flashcard.delete()
        logger.info(f'Flashcard deleted by {request.user.username}')
        messages.success(request, 'Flashcard deleted successfully!')
        return redirect('view_deck', deck_id=deck_id)
    
    return render(request, 'delete_flashcard.html', {'flashcard': flashcard})


@login_required
def profile(request):
    """User profile page."""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            logger.info(f'Profile updated by {request.user.username}')
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def search(request):
    """Search flashcards - contains SQL injection vulnerability."""
    form = SearchForm()
    flashcards = []
    
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query', '')
        
        if query:
            # FLAW 3: A03 Injection - SQL Injection vulnerability
            # Using raw string concatenation with user input is dangerous
            # An attacker can inject SQL commands like: ' OR '1'='1
            from django.db import connection
            with connection.cursor() as cursor:
                # Vulnerable code - DO NOT USE IN PRODUCTION
                sql = f"SELECT * FROM decks_flashcard WHERE question LIKE '%{query}%' OR answer LIKE '%{query}%'"
                cursor.execute(sql)
                columns = [col[0] for col in cursor.description]
                flashcards = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # FIX 3: Use Django ORM instead of raw SQL
            #flashcards = Flashcard.objects.filter(
            #    question__icontains=query
            #) | Flashcard.objects.filter(
            #    answer__icontains=query
            #)
            
            logger.info(f'Search performed by {request.user.username} with query: {query}')
    
    return render(request, 'search.html', {
        'form': form,
        'flashcards': flashcards,
    })


@login_required
def study_deck(request, deck_id):
    """Study mode for flashcards in a deck."""
    # FLAW 1: No access control check (same vulnerability as view_deck)
    deck = Deck.objects.get(id=deck_id)
    
    # FIX 1: Check ownership before returning data
    # deck = get_object_or_404(Deck, id=deck_id, owner=request.user)
    
    flashcards = list(deck.flashcards.all())
    
    if not flashcards:
        messages.warning(request, 'This deck has no flashcards yet.')
        return redirect('view_deck', deck_id=deck_id)
    
    # Get current card index from query parameter
    card_index = int(request.GET.get('card', 0))
    if card_index < 0 or card_index >= len(flashcards):
        card_index = 0
    
    current_card = flashcards[card_index]
    total_cards = len(flashcards)
    
    # Calculate progress
    progress_percent = int((card_index + 1) / total_cards * 100)
    remaining_cards = total_cards - card_index - 1
    
    logger.info(f'User {request.user.username} studying deck {deck.title}')
    
    return render(request, 'study_deck.html', {
        'deck': deck,
        'current_card': current_card,
        'card_index': card_index,
        'total_cards': total_cards,
        'progress_percent': progress_percent,
        'remaining_cards': remaining_cards,
        'next_card_index': card_index + 1 if card_index < total_cards - 1 else None,
        'prev_card_index': card_index - 1 if card_index > 0 else None,
    })


def index(request):
    """Home page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')
