from django.contrib import admin

# Register your models here.
from django.apps import apps

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except:
        pass
