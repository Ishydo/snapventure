from __future__ import unicode_literals

import uuid
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from rest_framework.authtoken.models import Token

# Triggered whenever user has been created and added to database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __unicode__(self):
        return u'%s' % self.user.username

'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    pass
    #if created:
        #Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''

class Journey(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField()
    img_description = models.ImageField(blank=True)
    img_ambiance = models.ImageField(blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    private = models.BooleanField()
    active = models.BooleanField()
    deleted = models.BooleanField()
    creator = models.ForeignKey(Profile, related_name="creator_of_journey")
    inscriptions = models.ManyToManyField(
        Profile,
        through='Inscription',
        through_fields=('journey', 'profile'),
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('snapventure_journey_detail', args=(self.name,))


    def get_update_url(self):
        return reverse('snapventure_journey_update', args=(self.name,))

class Inscription(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Type(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField()


    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('snapventure_type_detail', args=(self.name,))


    def get_update_url(self):
        return reverse('snapventure_type_update', args=(self.name,))

class Step(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    content_text = models.TextField()
    content_url = models.URLField(blank=True)
    content_type = models.ForeignKey(Type)
    #order_id = models.IntegerField()
    journey = models.ForeignKey(Journey)
    qrcode_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    root = models.BooleanField(default=False)
    final = models.BooleanField(default=False)
    neighbours = models.ManyToManyField(
            'self',
            through='Edge',
            through_fields=('parent', 'child'),
            symmetrical=False
        )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('snapventure_step_detail', args=(self.name,))


    def get_update_url(self):
        return reverse('snapventure_step_update', args=(self.name,))


class Edge(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    parent = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="parent_node")
    child = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="child_node")

    def __unicode__(self):
        return u'%s with children %s' % (self.parent.name, self.child.name)

class State(models.Model):
    code = models.SmallIntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return u'%s - %s' % (self.code, self.name)

class Scan(models.Model):
    state = models.ForeignKey(State)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    step = models.ForeignKey(Step)
    profile = models.ForeignKey(Profile)

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.id

    def get_absolute_url(self):
        return reverse('snapventure_scan_detail', args=(self.id,))

    def get_update_url(self):
        return reverse('snapventure_scan_update', args=(self.id,))
