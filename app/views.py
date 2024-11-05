import copy

from django.core.paginator import Paginator
from django.shortcuts import render

questions = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'Text of question {i}?'
    } for i in range(30)
]

answers = [
    {
        'user_id': i+5,
        'text': f'Text of asnwer {i}'
    } for i in range(10)
]

tags = [
    {
        'id': i,
        'text': f'Tag {i}'
    } for i in range(8)
]
def index(request):
    page = paginate(questions, request, 5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_object': page, 'tags': tags},
    )

def hot(request):
    hotQuestions = copy.deepcopy(questions)
    hotQuestions.reverse()
    page = paginate(hotQuestions, request, 5)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_object': page, 'tags': tags},
    )

def question(request, question_id):
    question = questions[question_id]
    page = paginate(answers, request, 5)
    return render(
        request, 'question.html',
        {'question': question, 'answers': page.object_list, 'page_object': page, 'tags': tags},
    )

def login(request):
    return render(
        request, 'login.html',
        {'tags': tags},
    )

def signup(request):
    return render(
        request, 'signup.html',
        {'tags': tags},
    )

def ask(request):
    return render(
        request, 'ask.html',
        {'tags': tags},
    )

def tag(request, tag_id):
    tagId = tags[tag_id]
    tempQuestions = copy.deepcopy(questions)
    for item in tempQuestions:
        item['title'] = item['title'] + '.' + str(tagId['id'])
    page = paginate(tempQuestions, request, 5)
    return render(
        request, 'tag.html',
        {'tag': tagId, 'questions': page.object_list, 'page_object': page, 'tags': tags},
    )

def paginate(objects_list, request, per_page):
    pageNumber = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.get_page(pageNumber)
    return page