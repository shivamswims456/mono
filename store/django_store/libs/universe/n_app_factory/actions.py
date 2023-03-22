import os, re
import importlib, inspect
from django.apps import apps
from django.urls import path, include
from django.contrib.admin import site
from django.apps import AppConfig
from django.conf import settings

import pymysql
pymysql.install_as_MySQLdb()




def update_urlPatterns(**kwargs):
    #file, base_name, paths, base_url

    installedApps = [f"{app.__module__}.{app.__class__.__name__}"\
                     for app in apps.get_app_configs()]
    
    print(kwargs)
    
    return kwargs['paths']
    


    


def load_package(conf):

    conf = conf[settings.CICD_STAGE]
    packages = conf.get("packages", [])

    deniedApps = conf.get("exclude_nested", [])

    models_denied = conf.get("models_denied", {})


    deniedLocation = []
    appToBeLoaded = []
    app_paths = []
    app_names = []


    for package in packages:

        basePath = os.path.join(os.getcwd(), package)

        if not os.path.exists(basePath):

            raise Exception(f'App does not exists {basePath}')
        

        for folder, subfolder, files in os.walk(basePath):
            
            for file in files:

                    if file == "apps.py":
                        
                        spec = importlib.util.spec_from_file_location('apps', os.path.join(folder, file))
                        spec1 = importlib.util.spec_from_file_location('urls', os.path.join(folder, 'urls.py'))
                        
                        apps = importlib.util.module_from_spec(spec)
                        urls = importlib.util.module_from_spec(spec1)

                        spec.loader.exec_module(apps)
                        spec1.loader.exec_module(urls)
                        



                        classToImport = []

                        
                        folderSplit = folder.split(f'{os.path.sep}{package}{os.path.sep}')

                        folderPath = os.path.join(package, folderSplit[-1], "apps")\
                                     if len(folderSplit) > 1\
                                     else os.path.join(package, 'apps') 
                        
                        
                        folderDot = folderPath.replace(os.path.sep, '.')
                        appPath = folderDot.replace('.apps', '')
                        module_import = importlib.import_module(f"{folderDot}")
                        
                        for x in dir(apps):
                            if inspect.isclass(getattr(apps, x)) and x != "AppConfig":
                                 
                                klass = getattr(module_import, x)
                                classToImport.append(klass.__name__)
                                app_names.append(getattr(klass, "name"))
                                

                        if appPath not in deniedApps and all([location not in folder for location in deniedLocation]):
                            
                            urls_file = folderDot.replace('.apps', '.urls') 

                            app_paths.append(
                                path(urls.base_path, include(urls_file))
                            )
                            
                            for klass in classToImport:

                                ins_dot_name = f'{folderDot}.{klass}'
                                appToBeLoaded.append(ins_dot_name)



                        else:
                             
                            deniedLocation.append(folder)
                            
    settings.MODELS_DENIED.update(models_denied)
    settings.INSTALLED_APPS += appToBeLoaded + conf.get("template_apps", []) 
    settings.APP_NAMES += app_names                            


    return [app_paths, appToBeLoaded, app_names]
