from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
import json

class nameBasedBlocking:

    def __init__(self, get_response):
        
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):

        return self.get_response(request)


    def process_view(self, request, view_func, view_args, view_kwargs):
        
        host = request.get_host()
        port_split = host.split(":")
        #first subdomain is considered
        service_search_param = port_split[-1] if len(port_split) > 0 else host.split(".")[0]
        


        if "ApplicationLevel" in request.path:

            if request.method in ["POST", "PUT"]:

                try:
                    
                    json_request = json.loads(request.body)

                except:

                    return HttpResponseForbidden('{"error":"bad token"}')
                
                token_served = json_request.get("token") if request.method == "POST" else json_request.get("token")

                service_token = settings.SSO_TOKEN 

                if service_token != token_served:
                    
                    return HttpResponseForbidden('{"error":"bad token"}')


            else:

                return HttpResponseNotAllowed(["POST", "PUT", "PATCH"],'{"error":"Method not allowed"}')

        request.csrf_processing_done = True

        return None