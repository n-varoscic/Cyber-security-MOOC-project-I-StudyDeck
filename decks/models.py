from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

# EDUCATIONAL NOTE: In production this key must come from an environment variable
# and stay the same across restarts, otherwise encrypted data becomes unreadable.
# Example: FERNET_KEY = os.environ.get('FERNET_KEY')
FERNET_KEY = b'LncVivs03xmpnB-G9JWPElqux_YQnZhlVVNLdHLEWVY='

class Profile(models.Model):
    """User profile with intentional plaintext storage vulnerability."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default='')

    # FLAW 2: Cryptographic Failure - Sensitive data stored in plaintext
    sensitive_note = models.TextField(blank=True, default='')

    # FIX 2: Store encrypted bytes instead of plaintext
    # sensitive_note = models.BinaryField(blank=True, null=True, editable=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def encrypt_note(self, plaintext):
        """Encrypt a string and store it in sensitive_note."""
        f = Fernet(FERNET_KEY)
        self.sensitive_note = f.encrypt(plaintext.encode())

    def decrypt_note(self):
        """Decrypt and return the sensitive_note as a string."""
        if not self.sensitive_note:
            return ''
        f = Fernet(FERNET_KEY)
        return f.decrypt(bytes(self.sensitive_note)).decode()

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Subject(models.Model):
    """Study subject owned by a user."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']


class Deck(models.Model):
    """Deck of flashcards within a subject."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='decks')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Flashcard(models.Model):
    """Individual flashcard within a deck."""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question[:50]
    
    class Meta:
        ordering = ['created_at']
