from django.db import models


#### ADMIN
class AdminUser(models.Model):
    email = models.CharField(max_length=300)
    passwd = models.CharField(max_length=300) # guardar md5

####
class Partida(models.Model):
    num_partida = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_started = models.DateTimeField(null=True)
    date_ended = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, default="INACTIVA") # INACTIVA, REGISTRANT, COMPLETA, ENJOC, FINISHED
    classe = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides
    registered = models.IntegerField(default=0)
    comment = models.CharField(max_length=100, null=True) # Per marcar aquelles partides invalides
    goal_achieved = models.BooleanField(default=False)
    threshold = models.FloatField(default=0)
    control = models.BooleanField(default=True) # Per sabre si esteim amb el setup CONTROL o EXPERIMENTAL

class User(models.Model):
    is_robot = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)

    date_register = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_ended = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    # Enquesta inicial
    nickname = models.CharField(max_length=100, default="")
    gender = models.CharField(max_length=2, default="")
    age = models.CharField(max_length=2, default="")
    studies = models.CharField(max_length=2, default="")
    postal_code = models.CharField(max_length=10, default="")

    num_jugador = models.IntegerField(null=True)
    acabat = models.BooleanField(default=False)
    num_seleccions = models.IntegerField(default=0)
    current_game = models.ForeignKey(Partida, null=True, related_name='current_game')

    status = models.CharField(max_length=10, default="")


class Story(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Partida, null=True)
    type = models.CharField(max_length=1, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_ended = models.DateTimeField(null=True)
    question1 = models.CharField(max_length=2, default="")
    question2 = models.CharField(max_length=2, default="")
    question3 = models.CharField(max_length=2, default="")

class PublicGoods(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Partida, null=True)
    selection = models.CharField(max_length=1, default="")
    is_robot = models.BooleanField(default=True)
    date_selection = models.DateTimeField(null=True)




