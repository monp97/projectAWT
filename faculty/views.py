from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

from feedback.models import *

# Create your views here.


class FeedbackStatistic:
	questionText = ""
	averageRating = 0

class PaperStatistic:
	paperTitle = ""
	averageRating = 0


@login_required
def index(request):
	if not request.user.isFaculty:
		return redirect("/")
	teachings = request.user.teachings
	papers_taught = set()
	for teaching in teachings.all():
		papers_taught.add(teaching.paper.title)

	questionResponses = QuestionResponse.objects.filter(feedback__offering__faculty=request.user)
	statistics = []

	for question in FeedbackQuestion.objects.all():
		avg = 0.0
		for questionResponse in questionResponses.filter(question=question).all():
			avg += questionResponse.rating
		avg = avg / questionResponses.filter(question=question).count()
		statistic = FeedbackStatistic()
		statistic.questionText = question.questionText
		statistic.averageRating = avg
		statistics.append(statistic)

	paperStatistics = []

	for paper in Paper.objects.all():
		if teachings.filter(paper=paper).exists():
			avg = 0.0
			for questionResponse in questionResponses.filter(feedback__offering__paper=paper).all():
				avg += questionResponse.rating
			avg = avg / questionResponses.filter(feedback__offering__paper=paper).count()
			paperStatistic = PaperStatistic()
			paperStatistic.paperTitle = paper.title
			paperStatistic.averageRating = avg
			paperStatistics.append(paperStatistic)

	context = {
		'teachings': teachings,
		'papers': papers_taught,
		'statistics': statistics,
		'paperStatistics': paperStatistics,
	}

	return render(request, 'faculty/index.html', context)
