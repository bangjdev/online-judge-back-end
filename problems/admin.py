from django.contrib import admin

# Register your models here.
from problems.models import Problem, Tag, Test
from submissions.models import Language, Submission


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('task_code', 'title', 'problem_tags', 'author',)
    filter_horizontal = ('tags',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('task', 'name', 'position', 'input', 'output')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Submission)
admin.site.register(Test, TestAdmin)
