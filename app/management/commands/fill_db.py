from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
import random


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data quantity')

    def handle(self, *args, **options):
        User.objects.all().delete()
        Tag.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()

        ratio = options['ratio']

        # Создаем пользователей, проверяя наличие пользователя с таким именем
        users = []
        for i in range(ratio):
            username = f'user{i}'
            user, created = User.objects.get_or_create(username=username, defaults={'password': 'password123'})
            if created:
                users.append(user)

        # Создаем профили для новых пользователей
        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles)

        # Создаем теги
        tags = [Tag(name=str(i)) for i in range(ratio)]
        Tag.objects.bulk_create(tags)

        # Создаем вопросы
        questions = []
        for i in range(ratio * 10):
            author = random.choice(users)
            question = Question(
                title=f'Question {i}',
                text='Sample question text',
                author=author,
            )
            questions.append(question)
        Question.objects.bulk_create(questions)

        # Добавляем теги к вопросам
        all_questions = Question.objects.all()
        all_tags = list(Tag.objects.all())
        for question in all_questions:
            question.tags.add(*random.sample(all_tags, k=min(3, len(all_tags))))

        # Создаем ответы
        answers = []
        for i in range(ratio * 100):
            question = random.choice(all_questions)
            author = random.choice(users)
            answer = Answer(
                text=f'Answer text {i}',
                author=author,
                question=question
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)

        # Создаем лайки для вопросов
        question_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(all_questions)
            question_like = QuestionLike(user=user, question=question)
            question_likes.append(question_like)
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)

        # Создаем лайки для ответов
        all_answers = Answer.objects.all()
        answer_likes = []
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(all_answers)
            answer_like = AnswerLike(user=user, answer=answer)
            answer_likes.append(answer_like)
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Database filled with test data.'))
