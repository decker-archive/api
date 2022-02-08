from django.http import request

# initial gets
auth = request.HttpHeaders.get("Authorization")
reason = request.HttpHeaders.get("X-Log-Reason")
user_agent = request.HttpHeaders.get("User-Agent")
# checks
