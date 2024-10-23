from rest_framework.views import exception_handler
from rest_framework.response import Response
def custom_exception_handler(exc, context):
    result= exception_handler(exc, context)
    if result is None:
        return Response({
            "status": 500,  
            "message": "An unexpected error occurred."
        }, status=500)

    if result is not None:
        status_code = result.status_code
        messages = result.data

        response = {
        "status": status_code,  
        "message": messages
        }

        return Response(response, status=response['status'])
