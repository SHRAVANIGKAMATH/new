from django.contrib.auth.models import AbstractUser
from django.db import models
import re

class CustomUser(AbstractUser):
    usn = models.CharField(max_length=10, unique=True, null=True, blank=True)
    faculty_id = models.CharField(max_length=7, unique=True, null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def save(self, *args, **kwargs):
        if self.is_teacher:
            self.is_student = False
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        usn_pattern = re.compile(r'^\d[A-Za-z]{2}\d{2}[A-Za-z]{2}\d{3}$')
        faculty_id_pattern = re.compile(r'^[A-Za-z]{2}\d{5}$')
        if self.usn and not usn_pattern.match(self.usn):
            raise ValueError("USN must be in the format 1N2A2N2A3N (e.g., 1AB12CD123).")
        if self.faculty_id and not faculty_id_pattern.match(self.faculty_id):
            raise ValueError("Faculty ID must be in the format 2A5N (e.g., AB12345).")