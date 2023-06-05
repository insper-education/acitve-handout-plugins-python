from urllib.parse import unquote_plus
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view

from core.models import Course, Exercise, TelemetryData
from dashboard.query import StudentStats


@api_view()
@login_required
def student_dashboard(request, course_name):
    student = request.user

    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)

    tag_tree_yaml = json.loads(request.GET.get('tag-tree', '{}'))

    student_stats = StudentStats(student, course, tag_tree_yaml)

    return render(request, 'dashboard/student-dashboard.html', {
        'referer': request.META.get('HTTP_REFERER', ''),
        'course': course,
        'tags': student_stats.tags,
        'tag_tree': student_stats.tag_tree,
        'tag_stats': student_stats.stats_by_tag_group,
        'total_exercises': student_stats.total_exercises,
        'exercise_count_by_tag_slug_and_date': student_stats.exercise_count_by_tag_slug_and_date,
    })

@api_view()
@login_required
def instructor_courses(request):
    courses = Course.objects.all()
    return render(request, 'dashboard/instructor-courses.html',{"courses" : courses})

@api_view()
@login_required
def instructor_dashboard(request, course_name):

    def convert_to_valid_json(data):
        data = data.replace("'", '"').replace('"', r'\"')
        return data
    course_name = unquote_plus(course_name)
    course = get_object_or_404(Course, name=course_name)
    exercises = Exercise.objects.filter(course=course)
    data_list = []
    for ex in exercises:
        answers = {}
        correct = []
        tags = [tag.name for tag in ex.tags.all()]
        telemetry = list(TelemetryData.objects.filter(exercise=ex, last=True).values_list('log', flat=True))
        if 'choice-exercise' in tags:
            answers = {x:telemetry.count(x) for x in telemetry}
        elif 'parsons-exercise' in tags:
            # count number of times that each code key value inside telemetry ocurred
            answers = {x['code']: telemetry.count(x) for x in telemetry}
            #create correct_list that gets all items that mach condition
            correct = [x['code'] for x in telemetry if (x['correct'] and x['code'])]
            #remove duplicates
            correct = list(dict.fromkeys(correct))

        data = {
            "name" : ex.slug,
            "tags" : tags,
            "telemetry" : {
                "x" : list(answers.values()),
                "y" : [convert_to_valid_json(x) for x in answers.keys() if x != ''],
                "correct": [convert_to_valid_json(answer) for answer in correct]
            }
        }
        data_list.append(data)
    return render(request, 'dashboard/instructor-dashboard.html',{"data" : data_list})