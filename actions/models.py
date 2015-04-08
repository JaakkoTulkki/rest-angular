from django.db import models


class Action(models.Model):
    cause_member = models.ForeignKey('causes.CauseMembers')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)