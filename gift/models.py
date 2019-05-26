from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime as dt
from django.db import models

# Create your models here.


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    Profile_photo = models.ImageField(upload_to='images/', blank=True)
    Bio = models.TextField(max_length=50, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    rate = models.ManyToManyField(
        'Project', related_name='image', max_length=30)

    def save_profile(self):
        self.save()

    @classmethod
    def get_by_id(cls, id):
        details = Profile.objects.get(user=id)
        return details

    @classmethod
    def filter_by_id(cls, id):
        details = Profile.objects.filter(user=id).first()
        return details

    @classmethod
    def search_user(cls, name):
        userprof = Profile.objects.filter(user__username__icontains=name)
        return userprof


class Project(models.Model):
    screenshot = models.ImageField(upload_to='images/')
    project_name = models.CharField(max_length=10)
    project_url = models.CharField(max_length=50)
    location = models.CharField(max_length=10)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE , null=True, related_name='project')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()

    @classmethod
    def get_project(cls, profile):
        project = Project.objects.filter(Profile__pk=profile)
        return project

    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_profile(cls, search_term):
        projo = cls.objects.filter(profile__name__icontains=search_term)
        return projo

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk=profile)
        return project

    @classmethod
    def find_project_id(cls, id):
        identity = Project.objects.get(pk=id)
        return identity


class Rate(models.Model):
    design = models.CharField(max_length=30)
    usability = models.CharField(max_length=8)
    creativity = models.CharField(max_length=8, blank=True, null=True)
    average = models.FloatField(max_length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rate', null=True)

    def __str__(self):
        return self.design

    class Meta:
        ordering = ['-id']

    def save_rate(self):
        self.save()

    @classmethod
    def get_rate(cls, profile):
        rate = Rate.objects.filter(Profile__pk=profile)
        return rate

    @classmethod
    def get_all_rating(cls):
        rating = Rate.objects.all()
        return rating
