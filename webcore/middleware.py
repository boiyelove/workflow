from django.utils.deprecation import MiddlewareMixin
from django.db.models import F
from .models import VisitedUrl

class UrlViewCountMiddleWare(MiddlewareMixin):
	def process_request(self, request):
		user = None
		if request.user.is_authenticated:
			user = request.user
		url, created = VisitedUrl.objects.get_or_create(
			url = request.get_full_path(),
			user = user)
		url.views = F('views') + 1
		url.save()
		return None
