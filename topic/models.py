from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Topic(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __repr__(self):
        return f'Topic: {self.name}'
    
    def __str__(self):
        return f'{self.id}: {self.name}'
