from django.conf import settings
import sys
sys.path += [str(settings.SUPER_BASE), str(settings.STORE), str(settings.UNIVERSE)]
from store.django_store.libs.universe.n_app_factory.actions import load_package

#supper base added to route
#Should only be used for import of standard libs and sdks


stages = {
            "DEV":{"packages":[],
                   "template_apps":['n_app_factory',
                                    'django_sso.sso_gateway',
                                    'allauth', 
                                    'allauth.account', 
                                    'allauth.socialaccount',
                                    'django_db_logger'],
                    "exclude_nested":[],
                    "models_denied":{}},
            
            "STAGE":{"packages":[],
                   "template_apps":[],
                    "exclude_nested":[],
                    "models_denied":{}},
            
            "BETA":{"packages":[],
                   "template_apps":[],
                    "exclude_nested":[],
                    "models_denied":{}},
                    
            "PROD":{"packages":[],
                   "template_apps":[],
                    "exclude_nested":[],
                    "models_denied":{}}
        }


load_package(stages)

