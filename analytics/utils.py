
# get the IP from the user accessing the site
# get the headers from the access

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # method to get IP
    else:
        ip = request.META.get("REMOTE_ADDR", "Could Not Find")
    return ip