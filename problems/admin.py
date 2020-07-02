from django.contrib import admin

# Register your models here.
from problems.models import Problem, Tag
from submissions.models import Language, Submission


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem_code', 'title', 'problem_tags', 'author',)
    filter_horizontal = ('tags',)


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Submission)
