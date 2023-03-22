import os, re
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):

    help = 'creates app according to salesstair guidelines'

    def create_urls_py(self, location, app_name, base_path):

        with open(os.path.join(os.path.dirname(__file__), "urls_skeleton.py"), "r") as f:

            urls_py = f.read()

            path = ""
            if base_path == "":
                path = f"{app_name}"

            for section in base_path.split("."):
                
                path += f'{section.split("__")[-1]}/'

            
            
            urls_py = urls_py.replace('base_path = ""', f'''base_path = "{path}"''')
            urls_py = urls_py.replace('app_name = "app_name"', f'app_name = "{app_name}"')
            
        

        with open(os.path.join(location, 'urls.py'), 'w+') as f:
            
            f.write(urls_py)


    def update_admin_py(self, location):

        with open(os.path.join(os.path.dirname(__file__), "admin_skeleton.py"), "r") as f:

            admin_content = f.read()

        print(location)
        with open(os.path.join(location, 'admin.py'), "w") as f:

            f.write(admin_content)



    def update_app_py(self, location, app_name):
        
        with open(os.path.join(location, 'apps.py'), 'r+') as f:

            content = f.read()
            update_content = re.sub('name(.*?)$', f"name = '{app_name}'", content)
            f.truncate(0)
            f.seek(0)
            f.write(update_content)
    
    def add_arguments(self, parser):
        
        parser.add_argument('--app_name', action='store', type=str, help='name of the app to be creted', required=True)
        parser.add_argument('--app_parent', action='store', type=str, help='name of the parent app under which is being created')
        parser.add_argument('--app_location', action='store', type=str, help='name of the app to be creted')
    
    def handle_defaults(self, options):

        if options['app_location'] == None and options['app_parent'] != None:

            raise Exception('app_location must be provided for app_parent implementaion')
        

        options['base_apps_py_name'], options['base_app_name'] = [options['app_name']]*2

        if options['app_parent'] != None:

            
            options['base_app_name'] = f"{options['app_parent']}__{options['app_name']}"  

            
            options['base_apps_py_name'] = f"{options['app_parent']}.{options['base_app_name']}" 

        

        if options['app_location'] == None:

            options['app_location'] = options['app_name']

        else:

            options['app_location'] = os.path.join(*options['app_location'].split("/"), options['base_app_name'])

            os.makedirs(options['app_location'])


        
        return options        

    def handle(self, *args, **options):

        levels = settings.APP_SUBLEVELS

        options = self.handle_defaults(options)


        command = ['startapp', options['base_app_name']]
        parentUrls_import = ''
         

        if options['app_parent'] != None:
            
            command.append(options['app_location'])
            parentUrls_import = options['base_apps_py_name']

        call_command(*command)

        self.update_app_py(options['app_location'], options['base_apps_py_name'])
        self.update_admin_py(options['app_location'])
        self.create_urls_py(options['app_location'], options['base_app_name'], parentUrls_import)


        #childApp Logic

        for level in levels:

            controlApp_Name = f"{options['base_app_name']}__{level}"
            controlApp_Path = os.path.join(options['app_location'], controlApp_Name)
            controlApp_apps_Name = f"{options['base_apps_py_name']}.{controlApp_Name}"

            os.makedirs(controlApp_Path)

            call_command('startapp', controlApp_Name, controlApp_Path)

            self.update_app_py(controlApp_Path, controlApp_apps_Name)
            self.update_admin_py(controlApp_Path)
            self.create_urls_py(controlApp_Path, controlApp_Name, controlApp_apps_Name)





