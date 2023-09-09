from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """
    ChoiceInline is responsible for display the choices editing
    when editing a question in the /admin/.
    """
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """
    QuestionAdmin is responsible for configuring the questions in the /admin/.
    """
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently',
                    'can_vote')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
