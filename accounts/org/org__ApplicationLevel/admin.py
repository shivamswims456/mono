from django.contrib import admin
from django.conf import settings
from django.apps import apps 
from django.contrib.admin.sites import AlreadyRegistered

package = __package__.split(".")[-1]

if __package__ in settings.APP_NAMES:

        models = list(apps.get_app_config(package).get_models())

        deniedModels = settings.MODELS_DENIED.get(package, [])

        for model in models:

            if model.__name__ not in deniedModels:

                try:

                    admin.site.register(model)

                except AlreadyRegistered:

                    pass