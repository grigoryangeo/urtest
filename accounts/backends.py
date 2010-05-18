# File encoding: utf-8

from django.contrib.auth.backends import ModelBackend
from accounts.models import UserProxy

class UrtestUserModelBackend(ModelBackend):
    """Бекенд для аутенфикации по моделям urtest
    
    Возвращает детальный профиль пользователя
    """
    def authenticate(self, username=None, password=None):
	try:
	    user = UserProxy.objects.get(username=username)
	    if user.check_password(password):
		return user.get_detail()
	except UserProxy.DoesNotExist:
	    return None

    def get_user(self, user_id):
	try:
	    return UserProxy.objects.get(pk=user_id).get_detail()
	except UserProxy.DoesNotExist:
	    return None

