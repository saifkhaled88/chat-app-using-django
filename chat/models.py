from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager





# Custom User Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
    
#         if not username:
#             raise ValueError("The username field must be set")
        
#         # Create the user instance
#         user = self.model(username=username, **extra_fields)
        
#         # Set the password securely (hashed)
#         user.set_password(password)
        
#         # Save the user instance to the database
#         user.save(using=self._db)
        
#         return user


class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    #objects = CustomUserManager()

    # Custom related_name for 'groups' to avoid conflict
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related_name to avoid conflicts
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    # Custom related_name for 'user_permissions' to avoid conflict
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Custom related_name to avoid conflicts
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



    def __str__(self):
        return self.username
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(
        'chat.CustomUser', related_name='sent_messages',on_delete=models.CASCADE
        )
    receiver = models.ForeignKey(
        'chat.CustomUser', related_name='received_messages',on_delete=models.CASCADE
        )
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    