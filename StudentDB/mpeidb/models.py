from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = User


class Semester(models.Model):
    # название семестра (пример: "2020/2021, Осенний семестр")
    name = models.CharField(max_length=35)

    # # изучаемые в семестре дисциплины
    # disciplines = models.ManyToOneRel(Discipline, on_delete=models.CASCADE)

    # номер семестра (в общем, не относительно данного курса)
    number = models.IntegerField()

    # номер курса
    course = models.IntegerField()


class Discipline(models.Model):
    # название, наименование
    name = models.CharField(max_length=120)

    # семестры, в которых изучается дисциплина
    semester = models.ManyToManyField(Semester)

    # форма контроля (экзамен, автомат, зачёт, зачёт с оценкой (дифференцированный зачёт))
    control = models.CharField(max_length=20)

    # итоговая оценка за дисциплину (исп. для зачётной книжки)
    mark = models.CharField(max_length=30)

    # итоговая оценка за дисциплину
    total_mark = models.IntegerField(null=True)

    # дата выставления итоговой оценки / оценки за ППА-1, ППА-2 (повторн. пром. аттестацию №1,2)
    date = models.CharField(max_length=30)

    # пересдача =<оценка>, если была или =-1, если не было пересдачи или не ожидается вовсе. Если ожидается, то =-2.
    retake = models.IntegerField(null=True)

    # номер ППА (если была)
    ret_number = models.IntegerField(null=True)

    # оценка за пересдачу (для зачётной книжки)
    ret_mark = models.CharField(default='', max_length=30)

    # # контрольные мероприятия
    # events = models.ManyToOneRel(ControlEvent, on_delete=models.CASCADE)

    # лектор
    l_teacher = models.CharField(max_length=120)

    # преподаватель семинаров (практических занятий)
    p_teacher = models.CharField(max_length=120)

    # экзаменатор (кто принимал экзамен)
    examiner = models.CharField(max_length=120, default='')

    # вес дисциплины в ЗЕ (зачётных единицах) - нереализованно пока что
    weight = models.IntegerField(null=True)

    # балл "текущего контроля"
    score = models.FloatField(null=True)

    # оценка за ПА (промежуточную аттестацию(до пересдачи))
    midcert_mark = models.IntegerField(null=True)


class ControlEvent(models.Model):
    # номер недели
    week = models.IntegerField()

    # дисциплина
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    # описание
    desc = models.CharField(max_length=320)

    # номер контрольного мероприятия по счёту
    number = models.IntegerField()

    # оценка за км
    mark = models.IntegerField(null=True)

    # пересдавалась?
    retake = models.BooleanField(default=False)

    # пересданная оценка
    ret_mark = models.IntegerField(null=True)

    # кол-во пересдач
    ret_count = models.IntegerField(null=True)

    # вес км
    weight = models.IntegerField(default=0)


class CourseWork(models.Model):
    # дисциплина
    discipline = models.CharField(max_length=120, default='')

    # тема
    topic = models.CharField(max_length=200, default='')

    # руководитель
    manager = models.CharField(max_length=120, default='')

    # оценка
    mark = models.CharField(max_length=30)


class Report(models.Model):
    # номер порядковый
    number = models.IntegerField()

    # семестр
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    # тип отчёта
    type = models.CharField(max_length=120, default='')

    # дисциплина
    discipline = models.CharField(max_length=120, default='')

    # руководитель от предприятия
    leader = models.CharField(max_length=120, default='')

    # руководитель от МЭИ
    leader_mpei = models.CharField(max_length=120, default='')

    # в качестве кого работал (роль)
    role = models.CharField(max_length=120, default='')

    # место прохождения практики
    place = models.CharField(max_length=120, default='')