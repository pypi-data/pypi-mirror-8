from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from compat import AUTH_USER_MODEL

class VoteManger(models.Manager):
    def filter(self, *args, **kwargs):
        if kwargs.has_key('content_object'):
            content_object = kwargs.pop('content_object')
            content_type = ContentType.objects.get_for_model(content_object)
            kwargs.update({
                    'content_type':content_type,
                    'object_id':content_object.pk
                    })
        return super(VoteManger, self).filter(*args, **kwargs)
    
class Vote(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    create_at = models.DateTimeField(auto_now_add=True)

    objects = VoteManger()
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    @classmethod
    def votes_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "content_type": ct
        }
        if instance is not None:
            kwargs["object_id"] = instance.pk
            
        return cls.objects.filter(**kwargs)
