from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from topic.models import Topic

admin.site.register(Topic, MPTTModelAdmin)