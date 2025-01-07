from django.contrib import admin

from .models import (
Candidate, Major, Subject,
Author, Test, UserTest,
Question, UserAnswer
)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    pass

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    pass

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    pass


