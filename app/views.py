import copy

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

questions = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'Text of question {i}?',
        'userTag': {'one', 'two', 'three'}
    } for i in range(30)
]

answers = [
    {
        'user_id': i + 5,
        'text': f'Text of asnwer {i}'
    } for i in range(10)
]

tags = [
    {
        'id': 'one'
    },
    {
        'id': 'two'
    },
    {
        'id': 'three'
    },
    {
        'id': 'four'
    },
    {
        'id': 'five'
    },
    {
        'id': 'six'
    },
    {
        'id': 'seven'
    }
]


def index(request):
    isLogged = request.session.get('isLogged', True)
    page = paginate(questions, request, 5)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_object': page, 'tags': tags, 'isLogged': isLogged},
    )


def hot(request):
    isLogged = request.session.get('isLogged', True)
    hotQuestions = copy.deepcopy(questions)
    hotQuestions.reverse()
    page = paginate(hotQuestions, request, 5)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_object': page, 'tags': tags, 'isLogged': isLogged},
    )


def question(request, question_id):
    isLogged = request.session.get('isLogged', True)
    question = questions[question_id]
    page = paginate(answers, request, 5)
    return render(
        request, 'question.html',
        {'question': question, 'answers': page.object_list, 'page_object': page, 'tags': tags, 'isLogged': isLogged},
    )


def login(request):
    isLogged = request.session.get('isLogged', False)
    return render(
        request, 'login.html',
        {'tags': tags, 'isLogged': isLogged},
    )


def signup(request):
    isLogged = request.session.get('isLogged', False)
    return render(
        request, 'signup.html',
        {'tags': tags, 'isLogged': isLogged},
    )


def ask(request):
    isLogged = request.session.get('isLogged', True)
    return render(
        request, 'ask.html',
        {'tags': tags, 'isLogged': isLogged},
    )


def tag(request, tag_id):
    isLogged = request.session.get('isLogged', True)
    page = paginate(questions, request, 5)
    return render(
        request, 'tag.html',
        {'tag': tag_id, 'questions': page.object_list, 'page_object': page, 'tags': tags, 'isLogged': isLogged},
    )

def settings(request):
    isLogged = request.session.get('isLogged', True)
    return render(
        request, 'settings.html',
        {'tags': tags, 'isLogged': isLogged},
    )

def paginate(objects_list, request, per_page):
    pageNumber = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.get_page(pageNumber)
    return page
