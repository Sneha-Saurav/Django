
from django.conf import settings

class ErrorHandleException(object):
    def __init__(self, get_response):
        self.get_response  = get_response
    
    def __call__(self, request):
        # print("get response")
        return self.get_response(request)

    def process_exception(self,request, exception):
        # print(settings.SERVER) # import setting.py file 
        # print("response")
        print(exception)
        return None