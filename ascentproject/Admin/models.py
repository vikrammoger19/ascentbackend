from django.db import models

class Entity(models.Model):
    entity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    assigned_entities = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
