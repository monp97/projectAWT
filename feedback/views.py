from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

from .models import *
import datetime

# Create your views here.


@login_required
def index(request):
	user = request.user
	course = user.course
	if user.course is not None:
		semester = user.get_semester()
		paper_offerings = course.offerings.filter(year=user.startYear, semester=semester)
		print(paper_offerings.count())
		context = {
			'course': course,
			'semester': semester,
			'paper_offerings': paper_offerings,
		}

		return render(request, 'feedback/index.html', context)
	return HttpResponse("User " + user.username + " is not registered for any course!")


@login_required()
def user_feedback(request):
	if request.method == 'GET':
		offering_id = request.GET.get("offering_id", 0)
		try:
			paper_offering = PaperOffering.objects.get(pk=offering_id)
			questions = FeedbackQuestion.objects.filter(kind=paper_offering.paper.kind)
			context = {
				'paper_offering': paper_offering,
				'questions': questions,
			}
			return render(request, 'feedback/user_feedback.html', context)
		except PaperOffering.DoesNotExist:
			return redirect("/")
	else:
		data = json.loads(request.body)
		paper_offering = PaperOffering.objects.get(pk=data["paper_offering"])
		feedback = Feedback()
		feedback.offering = paper_offering
		feedback.owner = request.user
		feedback.remarks = data["remarks"]
		feedback.save()
		question_responses = data["questions_responses"]
		for question_response in question_responses:
			QuestionResponse.objects.create(
				question=FeedbackQuestion.objects.get(pk=question_response["question"]),
				rating=question_response["rating"],
				feedback=feedback
			)
		response = {
			"status": "OK"
		}

		return HttpResponse(json.dumps(response))
