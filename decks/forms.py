from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Subject, Deck, Flashcard


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    
    # FLAW 2: Cryptographic Failure - Sensitive data stored in plaintext
    sensitive_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Store sensitive notes (currently unencrypted)'}),
        label='Sensitive Note'
    )
    
    # FIX 2: Use a CharField to display decrypted note for editing
    # sensitive_note = forms.CharField(
    #    required=False,
    #    widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Store sensitive notes (encrypted)'}),
    #    label='Sensitive Note'
    #)
    
    class Meta:
        model = Profile
        # FIX 2: Only include 'bio' here - remove 'sensitive_note'
        fields = ('bio', 'sensitive_note')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }
    
    def __init__(self, *args, **kwargs):
        """Decrypt note when form is initialized for display."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # FIX 2: Decrypt the sensitive_note for display in the form
            # self.fields['sensitive_note'].initial = self.instance.decrypt_note()
            # FLAW 2: To revert to plaintext, uncomment the line below and comment out the line above
            self.fields['sensitive_note'].initial = self.instance.sensitive_note or ''
    
    def save(self, commit=True):
        """Encrypt note before saving."""
        instance = super().save(commit=False)
        sensitive_note_plaintext = self.cleaned_data.get('sensitive_note', '')
        
        # FIX 2: Encrypt note before saving
        #if sensitive_note_plaintext:
        #    instance.encrypt_note(sensitive_note_plaintext)
        #else:
        #    instance.sensitive_note = None
        
        # FLAW 2: To revert to plaintext storage, uncomment the lines below and comment out the lines above
        instance.sensitive_note = sensitive_note_plaintext
        
        if commit:
            instance.save()
        return instance


class SubjectForm(forms.ModelForm):
    """Form for creating/updating subjects."""
    class Meta:
        model = Subject
        fields = ('name', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Subject name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description'}),
        }


class DeckForm(forms.ModelForm):
    """Form for creating/updating decks."""
    class Meta:
        model = Deck
        fields = ('subject', 'title')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Deck title'}),
        }


class FlashcardForm(forms.ModelForm):
    """Form for creating/updating flashcards."""
    class Meta:
        model = Flashcard
        fields = ('question', 'answer')
        widgets = {
            'question': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Question'}),
            'answer': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Answer'}),
        }


class SearchForm(forms.Form):
    """Form for searching flashcards."""
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search flashcards...'})
    )
