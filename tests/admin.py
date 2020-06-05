from django.contrib import admin


# Register your models here.
from tests.models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('problem', 'name', 'position', 'input', 'output')


admin.site.register(Test, TestAdmin)
