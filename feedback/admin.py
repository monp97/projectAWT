from django.contrib import admin
from feedback.models import User,Course,Paper,PaperOffering,FeedbackQuestion,Feedback,QuestionResponse

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Paper)
admin.site.register(PaperOffering)
admin.site.register(FeedbackQuestion)
admin.site.register(QuestionResponse)
admin.site.register(Feedback)
