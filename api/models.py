from django.db import models
import binascii
import os


class Member(models.Model):
    """
    Custom user model for the application.
    Not using Django's built-in User model as per requirements.
    """
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'members'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been authenticated.
        Required for DRF compatibility.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way to tell if the user is anonymous.
        Required for DRF compatibility.
        """
        return False

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission.
        Required for DRF permission classes compatibility.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app.
        Required for DRF permission classes compatibility.
        """
        return True


class Token(models.Model):
    """
    Authorization token for Member authentication.
    """
    key = models.CharField(max_length=40, unique=True)
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='tokens'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tokens'

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key


class Message(models.Model):
    """
    Message model for storing chat messages.
    """
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.member.username}: {self.text[:50]}'
