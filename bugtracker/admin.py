from django.contrib import admin
from urtest.bugtracker.models import Bug, Tester, Project, Customer, PhysCustomer, UrCustomer, OSystem, Browser, ProgramLang, TestingType, PayingType, Language


admin.site.register(Bug)
admin.site.register(Tester)
admin.site.register(Project)
admin.site.register(Customer)
admin.site.register(UrCustomer)
admin.site.register(PhysCustomer)
admin.site.register(OSystem)
admin.site.register(Browser)
admin.site.register(ProgramLang)
admin.site.register(TestingType)
admin.site.register(PayingType)
admin.site.register(Language)

