from datacenter.models import Schoolkid
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Commendation
from datacenter.models import Chastisement
from random import choice
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def fix_marks(fio):
    try:
        child=Schoolkid.objects.filter(full_name__contains=fio).get()
    except MultipleObjectsReturned:
        print('Количество найденных записей больше 1')
    except ObjectDoesNotExist:
        print('Ученика с таким ФИО нет в базе')
    bad_marks=Mark.objects.filter(schoolkid__full_name__contains=child.full_name, points__in=[2,3])
    for mark in bad_marks:
        mark.points=5
        mark.save()


def remove_chastisements(fio):
    try:
        child=Schoolkid.objects.filter(full_name__contains=fio).get()
    except MultipleObjectsReturned:
        print('Количество найденных записей больше 1')
    except ObjectDoesNotExist:
        print('Ученика с таким ФИО нет в базе')
    chastisement=Chastisement.objects.filter(schoolkid__full_name__contains=child.full_name)
    chastisement.delete()


def create_commendation(fio, subject):
    example_commendation = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', \
        'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', \
        'Именно этого я давно ждал от тебя!', 'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', \
        'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', \
        'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', \
        'Ты на верном пути!', 'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!', \
        'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!', \
        'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!', \
        'Теперь у тебя точно все получится!']
    try:
        child=Schoolkid.objects.filter(full_name__contains=fio).get()
    except MultipleObjectsReturned:
        print('Количество найденных записей больше 1')
    except ObjectDoesNotExist:
        print('Ученика с таким ФИО нет в базе')
    lesson=Lesson.objects.filter(year_of_study=child.year_of_study, group_letter=child.group_letter, subject__title=subject).first()
    Commendation.objects.create(text=choice(example_commendation), created=lesson.date, schoolkid=child, subject=lesson.subject, teacher=lesson.teacher)
