from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_projects',
        limit_choices_to={'groups__name': 'Manager'}
    )

    developers = models.ManyToManyField(
        User,
        related_name='projects',
        limit_choices_to={'groups__name': 'Developer'},
        blank=True
    )

    class Meta:
        permissions = [
            ('can_create_projects', 'Can create projects'),
            ('cannot_create_projects', 'Can not create projects'),
            ('can_assign_developers', 'Can assign developers'),
        ]

    def __str__(self):
        return self.name
    


class Bug(models.Model):

    BUG_TYPE_CHOICES = [
        ('feature', 'Feature'),
        ('bug', 'Bug'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('started', 'Started'),
        ('resolved', 'Resolved'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    bug_type = models.CharField(max_length=10, choices=BUG_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    image = models.ImageField(upload_to='bug_images/', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_bugs',
        limit_choices_to={'groups__name': 'QA'}
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='assigned_bugs',
        limit_choices_to={'groups__name': 'Developer'},
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('project', 'title')
        permissions = [
            ('can_report_bugs', 'Can report bugs'),
            ('are_assigned_bugs', 'Are Assigned Bugs'),
        ]

    def __str__(self):
        return f"{self.title} - {self.project.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.bug_type not in dict(self.BUG_TYPE_CHOICES):
            raise ValidationError({'bug_type': 'Invalid bug type.'})

        if self.image:
            if self.image.size > 5 * 1024 * 1024:
                raise ValidationError({'image': 'Image size must be less than 5MB.'})
            if not self.image.name.lower().endswith(('.png', '.gif')):
                raise ValidationError({'image': 'Only .png or .gif files are allowed.'})
