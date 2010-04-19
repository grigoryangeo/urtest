from django.contrib import admin
from urtest.enumerations.models import *


for model in OS, Browser, ProgramLanguage, TestingType, PayType, Language:
    admin.site.register(model)
