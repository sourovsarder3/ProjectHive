from django.db import models
from django.db.models import Q
from datetime import datetime
from django.core.exceptions import ValidationError


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        workspaceID = kwargs.get('workspace')
        lookup = (Q(first_person=user) | Q(
            second_person=user)) & Q(workspace=workspaceID)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=244, unique=True)
    password = models.CharField(max_length=500)
    forget_pass_code = models.CharField(max_length=255, null=True)
    date_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class WorkSpace(models.Model):
    workspaceName = models.CharField(max_length=100)
    workspaceDescription = models.TextField(blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreated = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.workspaceName


class WorkspaceMembership(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateJoined = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = (("workspace", "user"),)

    def __str__(self):
        return f"{self.user} is a member of {self.workspace}"


class Channel(models.Model):
    channelName = models.CharField(max_length=100)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.workspace}: {self.channelName}"


class PrivateChannelMembership(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateJoined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.channel.channelName}: {self.user}"


class ChannelMessage(models.Model):
    message = models.TextField()
    has_file = models.CharField(max_length=1, null=True)
    file_type = models.CharField(max_length=255, null=True)
    file = models.TextField(null=True)
    send_by = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name='message_channel')
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.send_by}: {self.message}"


class Thread(models.Model):
    first_person = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='thread_first_person')
    second_person = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='thread_second_person')
    workspace = models.ForeignKey(
        WorkSpace, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person', 'workspace']

    def clean(self):
        reverse_pair = Thread.objects.filter(
            first_person=self.second_person,
            second_person=self.first_person,
            workspace=self.workspace
        )
        if reverse_pair.exists():
            print('The pair already exists in reverse order')
            raise ValidationError('The pair already exists in reverse order')

    def __str__(self):
        return f"{self.first_person} & {self.second_person}"


class ChatMessage(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name='chatmessage_thread')
    send_by = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    has_file = models.CharField(max_length=1, null=True)
    file_type = models.CharField(max_length=255, null=True)
    file = models.TextField(null=True)
    date_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.send_by} -> {self.message}"


class SeenByChannel(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(
        ChannelMessage, on_delete=models.CASCADE, related_name='message_seen_by')
    seen_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.message} -> {self.seen_by}"


class Invitation(models.Model):
    send_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='send_by')
    send_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='send_to')
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sent by {self.send_by}"
