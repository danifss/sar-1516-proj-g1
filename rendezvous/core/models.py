from __future__ import unicode_literals

from django.db import models


### USER
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    userSalt = models.CharField(max_length=64, blank=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'ID {0} - {1} - ({2}/{3}/{4})'.format(
            self.userID,
            self.username,
            self.createdOn.day,
            self.createdOn.month,
            self.createdOn.year
        )


### SERVICE (Available services in this network)
class Service(models.Model):
    serviceID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True)
    ip = models.CharField(max_length=15, unique=True)
    port = models.IntegerField()
    createdOn = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'ID {0} - {1} - ({2}/{3}/{4})'.format(
            self.serviceID,
            self.name,
            self.createdOn.day,
            self.createdOn.month,
            self.createdOn.year
        )


### BROKER (Others broker PSW on the network)
# class Broker(models.Model):
#     brokerID = models.AutoField(primary_key=True)
#     # user = models.ForeignKey(User)
#     name = models.CharField(max_length=50, unique=True)
#     ip = models.CharField(max_length=15, unique=True)
#     port = models.IntegerField()
#     description = models.CharField(max_length=250, blank=True)
#     createdOn = models.DateTimeField(auto_now_add=True)
#
#     def __unicode__(self):
#         return u'ID {0} - {1} - ({2}/{3}/{4})'.format(
#             self.brokerID,
#             self.name,
#             self.createdOn.day,
#             self.createdOn.month,
#             self.createdOn.year
#         )
