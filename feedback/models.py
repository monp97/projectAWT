from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from feedback import helpers

from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

class User(AbstractUser):
	isFaculty = models.BooleanField(default=False)
	profileImage = models.ImageField(null=True, blank=True, upload_to=helpers.PathAndRenameFile('profiles/images'))
	birthDate = models.DateField(blank=True, null=True)
	gender = models.CharField(blank=True, null=True, max_length=10)
	contact = models.CharField(blank=True, null=True, max_length=15, unique=True)
	email = models.EmailField(unique=True, max_length=255, verbose_name="Email Address")
	course = models.ForeignKey('Course', related_name='students', blank=True, null=True, on_delete=models.SET_NULL)
	startYear = models.IntegerField(default=2018)  # To identify the batch to which the student belongs for eg. "2017"-2020 for a 3 year course


class Course(models.Model):
	title = models.CharField(max_length=200)  # MCA, BTECH CSE...
	duration = models.IntegerField()  # in years

	def __str__(self):
		return self.title


class Paper(models.Model):
	kindChoices = (
		('lab', 'Lab'),
		('theory', 'Theory')
	)
	title = models.CharField(max_length=200)  # DS, algo, ...
	kind = models.CharField(max_length=20, choices=kindChoices)

	def __str__(self):
		return self.title



# Paper being offerred as a part of some course in a particular year (odd/even sem), taught by some faculty
# For every year (i.e. batch) separate PaperOfferings should be created for a course.
# For eg. separate offerings should exist for 1st Year MCA batches of 2018 and 2019 since they'll be taught by different faculties
# Redundancy can't be removed since course pattern may change in future and past course pattern should be intact.

class PaperOffering(models.Model):
	course = models.ForeignKey('Course', related_name='offerings', on_delete=models.CASCADE)
	paper = models.ForeignKey('Paper', related_name='offerings', on_delete=models.CASCADE)
	semester = models.IntegerField() # Semester 1,2,...8
	year = models.IntegerField()  # To identify the batch eg. "2018"
	faculty = models.ForeignKey('User', related_name='teachings', blank=True, null=True, on_delete=models.SET_NULL)  # Who taught this paper under the given course

	def has_feedback(self, user):
		return Feedback.objects.filter(owner=user, offering=self).exists()

	def __str__(self):
		return self.course.title + " " + str(self.year) + " => " + self.paper.title + " Semester " + str(self.semester)



class FeedbackQuestion(models.Model):
	kindChoices = (
		('lab', 'Lab'),
		('theory', 'Theory')
	)
	sNo = models.IntegerField(default=0)  # to decide order of questions, default is 0 i.e. first priority
	questionText = models.TextField()
	kind = models.CharField(max_length=20, choices=kindChoices)


class QuestionResponse(models.Model):
	rating = models.IntegerField()  # 1 to 10
	question = models.ForeignKey('FeedbackQuestion', related_name='responses', on_delete=models.CASCADE)
	feedback = models.ForeignKey('Feedback', related_name='responses', on_delete=models.CASCADE)


# Feedback for a single Paper Offering
# Students shall submit feedbacks for all paper offerings in a particular semester
class Feedback(models.Model):
	owner = models.ForeignKey('User', related_name='feedbacks', on_delete=models.CASCADE)
	offering = models.ForeignKey('PaperOffering', related_name='feedbacks', on_delete=models.CASCADE)
	remarks = models.TextField()  # student remarks

