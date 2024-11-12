from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Question, Answer, Tag

def index(request):
    """Отображение списка новых вопросов."""
    isLogged = request.session.get('isLogged', True)
    questions = Question.objects.get_new_questions()  # Выборка новых вопросов
    page = paginate(questions, request, per_page=5)  # Передаем вопросы первым параметром
    tags = Tag.objects.all()[:10]  # Ограничение на 10 тегов для отображения
    return render(request, 'index.html', {
        'questions': page.object_list,
        'page_object': page,
        'tags': tags,
        'isLogged': isLogged,
    })



def hot(request):
    """Отображение списка популярных вопросов."""
    isLogged = request.session.get('isLogged', True)
    hotQuestions = Question.objects.get_best_questions()  # Выборка "лучших" вопросов
    page = paginate(hotQuestions, request, per_page=5)
    tags = Tag.objects.all()[:10]
    return render(request, 'hot.html', {
        'questions': page.object_list,
        'page_object': page,
        'tags': tags,
        'isLogged': isLogged,
    })


def question(request, question_id):
    """Отображение страницы конкретного вопроса с ответами."""
    isLogged = request.session.get('isLogged', True)
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    page = paginate(answers, request, per_page=5)
    tags = Tag.objects.all()[:10]
    return render(request, 'question.html', {
        'question': question,
        'answers': page.object_list,
        'page_object': page,
        'tags': tags,
        'isLogged': isLogged,
    })


def login(request):
    """Отображение страницы входа."""
    isLogged = request.session.get('isLogged', False)
    tags = Tag.objects.all()[:10]
    return render(request, 'login.html', {'tags': tags, 'isLogged': isLogged})


def signup(request):
    """Отображение страницы регистрации."""
    isLogged = request.session.get('isLogged', False)
    tags = Tag.objects.all()[:10]
    return render(request, 'signup.html', {'tags': tags, 'isLogged': isLogged})


def ask(request):
    """Отображение страницы для создания нового вопроса."""
    isLogged = request.session.get('isLogged', True)
    tags = Tag.objects.all()[:10]
    return render(request, 'ask.html', {'tags': tags, 'isLogged': isLogged})


def tag(request, tag_id):
    """Отображение вопросов по определенному тегу."""
    isLogged = request.session.get('isLogged', True)
    tag = get_object_or_404(Tag, name=str(tag_id))  # Преобразуем tag_id в строку
    questions = Question.objects.filter(tags=tag).order_by('-created_at')
    page = paginate(questions, request, per_page=5)
    tags = Tag.objects.all()[:10]
    return render(request, 'tag.html', {
        'tag': tag,
        'questions': page.object_list,
        'page_object': page,
        'tags': tags,
        'isLogged': isLogged,
    })



def settings(request):
    """Отображение страницы настроек пользователя."""
    isLogged = request.session.get('isLogged', True)
    tags = Tag.objects.all()[:10]
    return render(request, 'settings.html', {'tags': tags, 'isLogged': isLogged})

def paginate(objects_list, request, per_page):
    pageNumber = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    page = paginator.get_page(pageNumber)
    return page
