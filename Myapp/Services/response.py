from django.http.response import JsonResponse, HttpResponse

def uls_response(status_code, message, data):
    data_dict = {"status": status_code, "message": message, "data":data}
    HttpResponse.status_code = status_code
    return JsonResponse(data_dict)