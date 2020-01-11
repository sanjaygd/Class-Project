from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


User = get_user_model()


def get_profile_upload_to(instance,filename):
    new_filename = '{}.{}'.format(uuid4,filename.split('.')[-1])
    return "profile/{}/{}".format(instance.user.id, new_filename)


class ProfileImage(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_profile_upload_to)
    uploaded = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,null=True, blank=True)
    location = models.CharField(max_length=50,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)



    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
