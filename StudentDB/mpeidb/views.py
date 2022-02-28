import decimal
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic, View

from .forms import SemesterCreationForm
from .models import Semester, Discipline, ControlEvent, CourseWork, Report
from decimal import Decimal

def index(request):
    context = {
        'file_number': '№ЗК - 0020202158',
        'group': 'А-07-20',
        'group_1': 'А-04-20',
        'cardID': '0020202158',
        'faculty': 'Институт информационных и вычислительных технологий (ИВТИ, раннее АВТИ)',
        'field_study': 'Информатика и вычислительная техника 09.03.01',
        'department': 'Вычислительные машины, комплексы, системы и сети',
        'department_1': 'Диагностические информационные технологии (ДИТ)',
        'qualification': 'Бакалавр',
        'course': '2',
        'admission': '2020',
        'study_form': 'Очная, бюджет, платно (3 семестр)',
        'status': 'обучается',
    }
    return render(request, 'index.html', context)


# class Report:
#     def __init__(self, name='', sem='', type='', place='', leader_mpei='', leader='', role=''):
#         self.name = name
#         self.sem = sem
#         self.type = type
#         self.place = place
#         self.leader_mpei = leader_mpei
#         self.leader = leader
#         self.role = role


class Subject:
    def __init__(self, name, cform, mark='', date_mark='', retake='', km=None, p_mark='', score='', t_mark='',
                 teacher='', lector=''):
        if km is None:
            km = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        self.name = name
        self.control_form = cform
        self.mark = mark
        self.date_mark = date_mark
        self.retake = retake
        self.km = km
        self.p_mark = p_mark
        self.score = score
        self.t_mark = t_mark
        self.teacher = teacher
        self.lector = lector


class SubjectList:
    def __init__(self, semester):
        self.semester = semester

    def subjects(self):
        subjects = {}
        if self.semester == '1':
            km1 = ['', '', '', '5', '', '', '', '3', '', '', '', '5', '', '', '', '4']
            km2 = ['', '', '', '', '4', '', '', '', '4', '', '', '4', '', '', '', '3']
            km3 = ['', '', '', '', '5', '', '', '5', '', '', '', '5', '', '', '4', '']
            km4 = ['', '', '', '3', '', '', '', '4', '', '', '', '', '4', '', '', '4']
            km5 = ['', '', '', '4', '', '', '', '4', '', '', '', '4', '', '', '4', '']
            km6 = ['', '', '', '4', '', '', '', '4', '5', '', '', '5', '', '3', '4', '4']
            km8 = ['', '', '', '3', '', '', '', '5', '', '', '', '4 5', '', '', '', '3 4']
            km9_10 = ['', '', '', '5', '', '', '', '5', '', '', '', '5', '', '', '3', '']
            subjects = [
                Subject('Алгебра и аналитическая геометрия', 'АВТОМАТ', '"4" (хорошо)', '18.01.2021', 'нет', km1, '4',
                        '4,1', '4', 'Булычёва О.Н.', 'Гриценко С.А.'),
                Subject('Инженерная графика', 'Диф. Зачет', '"4"/зачтено', '29.12.2020', 'нет', km2, '4', '3,7', '4',
                        'Захарова А.И.', 'Поляков О.А.'),
                Subject('Иностранный язык (англ.)', 'Диф. Зачет', '"5"/зачтено', '29.12.2020', 'нет', km3, '5', '4,8', '5',
                        'Васильева Н.А.', '---'),
                Subject('История (история России, всеобщая история)', 'Зачет', 'Зачтено', '29.12.2020', 'нет', km4, '4',
                        '3,9', '4', 'Смирнова М.И.', 'Смирнова М.И.'),
                Subject('Математический анализ', 'АВТОМАТ', '"4" (хорошо)', '22.01.2021', 'нет', km5, '4', '4,0', '4',
                        'Вестфальский А.Е.', 'Симушев А.А.'),
                Subject('Программирование', 'Экзамен', '"5" (отлично)', '27.01.2021', 'нет', km6, '5', '4,2', '5',
                        'Гречкина П.В.', 'Гречкина П.В.'),
                Subject('Учебная практика: ознакомительная', 'Зачет', 'Зачтено', '23.12.2020', 'нет', None, '5', '--', '5',
                        'Иваненко К.А.', '---'),
                Subject('Физика', 'Экзамен', '"3" (удовлетворительно) /"2"', '11.02.2021 /12.01.2021', '3', km8, '2',
                        '3,9', '3', 'Семёнова О.И.', 'Корецкая И.В.'),
                Subject('Физическая культура и спорт', 'Зачет', 'Зачтено', '29.12.2020', 'нет', km9_10, '5', '4,5', '5',
                        'Королёв П.В.', 'Степанов Г.А.'),
                Subject('Элективные курсы по физической культуре и спорту', 'Зачет', 'Зачтено', '29.12.2020', 'нет', km9_10, '5',
                        '4,5', '5', 'Королёв П.В.', 'Степанов Г.А.'),
            ]
        elif self.semester == '2':
            subjects = [
                Subject('Иностранный язык (англ.)', 'Диф. Зачет', '"5"/зачтено', '18.06.2021', 'нет', [
                    '', '', '', '5', '', '', '', '5', '', '', '', '5', '', '', '5', ''
                ], '5', '5,0', '5', 'Васильева Н.А.', '---'),
                Subject('Информатика', 'Диф. Зачет', '"5"/зачтено', '21.06.2021', 'нет', [
                    '', '', '', '4', '', '5', '', '5', '', '5/2', '', '5', '', '', '', ''
                ], '5', '4,6', '5', 'Аляева Ю.В.', 'Крюков А.Ф.'),
                Subject('Математический анализ', 'Экзамен', '', '', '', [
                    '', '', '', '3/2', '', '', '', '3/2', '', '', '', '3/2', '', '', '', '3/2'
                ], '', '2,5', '', 'Булычёва О.Н.', 'Симушев А.А.'),
                Subject('Программирование', 'Экзамен', '"4" (хорошо)', '25.06.2021', 'нет', [
                    '', '', '', '3', '', '5', '', '4/2', '', '4/2', '', '', '', '5', '', '4/2'
                ], '4', '3,4', '4', 'Кожевников А.В.', 'Гречкина П.В.'),
                Subject('Проектная деятельность', 'Зачет', 'Зачтено', '18.06.2021', 'нет', [
                    '', '', '', '5', '', '', '', '5', '', '5', '', '5', '', '', '', '5'
                ], '5', '5,0', '5', 'Воронкина А.А.', 'Курилов С.Н.'),
                Subject('Учебная практика: профилирующая', 'Зачет', 'Зачтено', '14.06.2021', 'нет', [
                    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
                ], '5', '--', '5', 'Иваненко К.А.', '---'),
                Subject('Физика', 'Экзамен', '', '', '', [
                    '', '', '', '3', '', '', '', '3', '', '', '', '3/0 3', '', '', '', '3/2 3'
                ], '', '2,5', '', 'Коротких И.И.', 'Корецкая И.В.'),
                Subject('Физическая культура и спорт', 'Зачет', 'Зачтено', '21.06.2021', 'нет', [
                    '', '', '', '4', '', '', '', '5', '', '', '', '5', '', '', '5', ''
                ], '5', '4,8', '5', 'Королёв П.В.', 'Степанов Г.А.'),
                Subject('Элективные курсы по физической культуре и спорту', 'Зачет', 'Зачтено', '21.06.2021', 'нет', [
                    '', '', '', '4', '', '', '', '5', '', '', '', '5', '', '', '5', ''
                ], '5', '4,8', '5', 'Королёв П.В.', 'Степанов Г.А.'),
            ]
        return subjects

class Week:
    def __init__(self, number):
        self.kms = []
        self.number = number

class DisciplineObject:
    def __init__(self, discipline):
        self.discipline = discipline
        self.kms = ControlEvent.objects.filter(discipline=discipline)
        self.control_events = [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
        # #flag = False
        # #f_km = None
        # for i in range(16):
        #     flag = False
        #     f_km = None
        #     #w = Week(i)
        #     for km in self.kms:
        #         if km.number == i:
        #             flag = True
        #             # w.kms.append(km)
        #             f_km = km
        #     if flag:
        #         #if len(w.kms) == 1:
        #             if f_km.mark is None:
        #                 self.control_events[i] = '-1'
        #             elif f_km.mark == 2:
        #                 if f_km.ret_mark <= 2:
        #                     self.control_events[i] = str(f_km.mark)
        #                 else:
        #                     self.control_events[i] = str(f_km.ret_mark)+'/'+str(f_km.mark)
        #             elif f_km.mark == 0:
        #                 if f_km.ret_mark <= 2:
        #                     self.control_events[i] = str(f_km.mark)
        #                 else:
        #                     self.control_events[i] = str(f_km.ret_mark) + '/' + str(f_km.mark)
        #             else:
        #                 self.control_events[i] = str(f_km.mark)
        #         # elif len(w.kms) > 1:
        #         #     s = ''
        #         #     for k in w.kms:
        #         #         if k.mark is None:
        #         #             pass
        #     else:
        #         self.control_events[i] = '-2'

        # self.kms = []
        # for e in ce:
        #     self.kms.append(e)


def session(request):
    #semester = '0'
    current_week = '5'
    if request.GET['sem'] != '':
        sem = request.GET['sem']
    semester = Semester.objects.get(number=int(sem))
    disciplines = Discipline.objects.filter(semester=semester)
    discip_objects = []
    for d in disciplines:
        dis = DisciplineObject(d)
        discip_objects.append(dis)

    #subjects_list = SubjectList(semester)
    reports = Report.objects.all()
    course_works = CourseWork.objects.all()
    context = {
        'semester': semester,
        'subjects': discip_objects,
        'disciplines': disciplines,
        'week': current_week,
        'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'reports': reports,
        'course_works': course_works,
    }
    return render(request, 'session.html', context)


class Profile(View):
    template_name = 'profile.html'

    def get(self, request):
        context = {
            'user': request.user,

        }
        semesters = Semester.objects.all()
        reports = Report.objects.all()
        context['semesters'] = semesters
        context['reports'] = reports
        context['roles'] = ['Практикант', 'Сотрудник']
        context['types'] = ['Материалы прохождения практики']
        context['last_report_number'] = len(reports)+1
        context['course_works'] = CourseWork.objects.all()
        return render(request, 'profile.html', context)

    def post(self, request):
        if request.POST['subject'] == 'COURSE_WORKS_CREATE':
            discipline_name = request.POST['discipline']
            topic = request.POST['topic']
            manager = request.POST['manager']
            int_mark = request.POST['mark']
            cw = CourseWork()
            cw.discipline = discipline_name
            cw.topic = topic
            cw.manager = manager
            if int_mark == '5':
                cw.mark = '"5" (отлично)'
            if int_mark == '4':
                cw.mark = '"4" (хорошо)'
            if int_mark == '3':
                cw.mark = '"3" (удовл.)'
            if int_mark == '2':
                cw.mark = '"2" (неудовл.)'
            cw.save()
            return redirect('/profile')
        elif request.POST['subject'] == 'COURSE_WORKS_DEL':
            cw_topic = request.POST['work']
            cw = CourseWork.objects.get(topic=cw_topic)
            cw.delete()
            return redirect('/profile')
        elif request.POST['subject'] == 'REP_CREATE':
            number = len(Report.objects.all())+1
            sem = request.POST['sem']
            semester = Semester.objects.get(number=sem)
            type = request.POST['type']
            discipline = request.POST['discipline']
            leader = request.POST['leader']
            leader_mpei = request.POST['leader_mpei']
            place = request.POST['place']
            role = request.POST['role']
            r = Report()
            r.number = number
            r.semester = semester
            r.type = type
            r.discipline = discipline
            r.leader = leader
            r.leader_mpei = leader_mpei
            r.place = place
            r.role = role
            r.save()
            return redirect('/profile')
        elif request.POST['subject'] == 'REP_DELETE':
            number = request.POST['report']
            r = Report.objects.get(number=int(number))
            for i in range(int(number)+1, Report.objects.count()+1):
                rep = Report.objects.get(number=i)
                rep.number = i - 1
                rep.save()
            r.delete()
            return redirect('/profile')
        elif request.POST['subject'] == 'REP_DELETE_ALL':
            for r in Report.objects.all():
                r.delete()
            return redirect('/profile')


class CreateSemester(View):

    def get(self, request):
        context = {
            'user': request.user,
            'err': request.GET['err']
        }
        form = SemesterCreationForm()
        context['form'] = form
        return render(request, 'semesters/sem_create.html', context)

    def post(self, request):
        context = {
            'user': request.user,
        }
        data = request.POST
        name = data['name']
        number = data['number']
        course = data['course']
        s = Semester()
        if Semester.objects.filter(name=name).exists() or Semester.objects.filter(number=number).exists() or Semester.objects.filter(course=course).count() > 1:
            return redirect('/semesters/create?err=1')
        else:
            s.name = name
            s.number = int(number)
            s.course = int(course)
            s.save()
            return redirect('/profile')


class EditSemester(View):

    def get(self, request):
        context = {
            'user': request.user,
        }
        id = request.GET['id']
        s = Semester.objects.get(number=int(id))
        b = Discipline.objects.filter(semester=s).exists()
        if b:
            #disciplines.extend(list(Discipline.objects.get(semester=int(id))))
            # disciplines = [].append(Discipline.objects.get(semester=int(id)))
            context['disciplines'] = Discipline.objects.filter(semester=s)
        else:
            context['disciplines'] = []
        context['semester'] = s
        return render(request, 'semesters/sem_edit.html', context)

    def post(self, request):
        context = {
            'user': request.user,
        }
        subject = request.POST['subject']
        if subject == 'DELETE':
            sem = request.POST['sem']
            name = request.POST['dis']
            s = Semester.objects.get(number=int(sem))
            d = Discipline.objects.filter(semester=s).get(name=name)
            d.delete()
            return redirect('/semesters?id=' + sem)
        elif subject == 'DELETE_ALL':
            sem = request.POST['sem']
            s = Semester.objects.get(number=int(sem))
            ds = Discipline.objects.filter(semester=s)
            for d in ds:
                d.delete()
            return redirect('/semesters?id=' + sem)

class DeleteSemester(View):
    def get(self, request):
        id = request.GET['id']
        s = Semester.objects.get(number=int(id))
        disciplines = Discipline.objects.filter(semester=s)
        if disciplines.exists():
            for d in disciplines:
                d.delete()
        s.delete()
        return redirect('/profile')


class CreateDiscipline(View):

    def get(self, request):
        context = {'user': request.user}
        sem = int(request.GET['sem'])
        if 'error' not in request.GET.dict():
            context['error'] = 0
        else:
            context['error'] = 1
        context['control_forms'] = ['Экзамен', 'Зачет с оценкой', 'Зачет', 'Защита КР/КП']
        context['semester'] = sem
        return render(request, 'semesters/dis_create.html', context)

    def post(self, request):
        context = {
            'user': request.user,
        }
        data = request.POST
        name = data['name']
        sem = data['semester']
        s = Semester.objects.get(number=int(sem))
        if Discipline.objects.filter(semester=s).filter(name=name).exists():
            #sem = data['semester']
            #context['error'] = 1
            return redirect('/semesters/discipline/create?sem=' + sem + '&error=1', context=context)
        else:
            control = data['control']
            p_teacher = data['p_teacher']
            l_teacher = data['l_teacher']
            sem = data['semester']
            s = Semester.objects.get(number=int(sem))
            d = Discipline()
            d.name = name
            d.control = control
            d.p_teacher = p_teacher
            d.l_teacher = l_teacher
            d.save()
            d.semester.add(s)
            d.save()
            #context['disciplines'] = Discipline.objects.all()
            return redirect('/semesters?id='+sem, context=context)

class EditDisciplineKM(View):

    def get(self, request):
        context = {
            'user': request.user,
        }
        id = request.GET['sem']
        name = request.GET['name']
        s = Semester.objects.get(number=int(id))
        dis = Discipline.objects.filter(semester=s).get(name=name)
        b = ControlEvent.objects.filter(discipline=dis).filter(number=1).exists()
        if b:
            context['events'] = ControlEvent.objects.filter(discipline=dis)
        else:
            context['events'] = []
        context['control_forms'] = ['Экзамен', 'Зачет с оценкой', 'Зачет', 'АВТОМАТ', 'Защита КР/КП']
        context['semester'] = s
        context['discipline'] = dis
        return render(request, 'semesters/dis_km_edit.html', context)

    def post(self, request):
        context = {
            'user': request.user,
        }
        data = request.POST
        subject = data['subject']
        if subject == 'CREATE':
            number = data['number']
            desc = data['desc']
            week = data['week']
            weight = data['weight']

            name = data['discipline']
            sem = data['sem']

            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            ce = ControlEvent()
            ce.number = int(number)
            ce.week = int(week)
            ce.weight = int(weight)
            ce.desc = desc
            ce.discipline = dis
            ce.save()
            return redirect('/semesters/discipline?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'DELETE':
            name = data['discipline']
            sem = data['sem']
            number = data['km']
            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            ce = ControlEvent.objects.filter(discipline=dis).get(number=int(number))
            ce.delete()
            return redirect('/semesters/discipline?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'INFO':
            control = data['control']
            l_teacher = data['l_teacher']
            p_teacher = data['p_teacher']

            name = data['discipline']
            sem = data['sem']

            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            dis.control = control
            dis.l_teacher = l_teacher
            dis.p_teacher = p_teacher
            dis.save()
            return redirect('/semesters/discipline?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'EDIT':
            name = data['discipline']
            sem = data['sem']
            km = data['km']
            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            ce = ControlEvent.objects.filter(discipline=dis).get(number=int(km))
            number = data['number']
            desc = data['desc']
            weight = data['weight']
            week = data['week']
            if len(number) > 0:
                ce.number = int(number)
            if len(desc) > 0:
                ce.desc = desc
            if len(weight) > 0:
                ce.weight = int(weight)
            if len(week) > 0:
                ce.week = int(week)
            ce.save()
            return redirect('/semesters/discipline?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'DELETE_ALL':
            name = data['discipline']
            sem = data['sem']
            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            ce = ControlEvent.objects.filter(discipline=dis)
            for ev in ce:
                ev.delete()
            return redirect('/semesters/discipline?sem=' + str(s.number) + '&name=' + dis.name, context=context)

class EditDisciplineMarks(View):
    def get(self, request):
        context = {
            'user': request.user,
        }
        id = request.GET['sem']
        name = request.GET['name']
        s = Semester.objects.get(number=int(id))
        dis = Discipline.objects.filter(semester=s).get(name=name)
        b = ControlEvent.objects.filter(discipline=dis).filter(number=1).exists()
        if b:
            context['events'] = ControlEvent.objects.filter(discipline=dis)
        else:
            context['events'] = []
        context['semester'] = s
        context['discipline'] = dis
        context['control_forms'] = ['Экзамен', 'Зачет с оценкой', 'Зачет', 'АВТОМАТ', 'Защита КР/КП']
        context['ret_numbers'] = [1, 2, 3]
        return render(request, 'semesters/dis_marks.html', context)

    def post(self, request):
        context = {
            'user': request.user,
        }
        data = request.POST
        subject = data['subject']
        if subject == 'MIDCERT':
            midcert_mark = data['midcert_mark']
            retake = data['retake']
            total_mark = data['total_mark']
            date = data['date']
            auto = data['auto']
            examiner = data['examiner']
            name = data['discipline']
            sem = data['sem']
            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            dis.midcert_mark = int(midcert_mark)
            dis.retake = int(retake)
            dis.total_mark = int(total_mark)
            dis.examiner = examiner
            dis.date = date
            if auto == 'АВТОМАТ':
                dis.control = 'АВТОМАТ'
            elif auto == 'Экзамен':
                dis.control = 'Экзамен'
            elif auto == 'Зачет с оценкой':
                dis.control = 'Зачет с оценкой'
            elif auto == 'Зачет':
                dis.control = 'Зачет'
            if (dis.control == 'Экзамен' or dis.control == 'АВТОМАТ' or dis.control == 'Защита КР/КП') and dis.total_mark == 5:
                dis.mark = '"5" (отлично)'
            elif (dis.control == 'Экзамен' or dis.control == 'АВТОМАТ' or dis.control == 'Защита КР/КП') and dis.total_mark == 4:
                dis.mark = '"4" (хорошо)'
            elif (dis.control == 'Экзамен' or dis.control == 'АВТОМАТ' or dis.control == 'Защита КР/КП') and dis.total_mark == 3:
                dis.mark = '"3" (удовл.)'
            elif (dis.control == 'Экзамен' or dis.control == 'АВТОМАТ' or dis.control == 'Защита КР/КП') and dis.total_mark == 2:
                dis.mark = '"2" (неудовл.)'
            elif (dis.control == 'Зачет с оценкой') and dis.total_mark == 5:
                dis.mark = '"5"/зачтено'
            elif (dis.control == 'Зачет с оценкой') and dis.total_mark == 4:
                dis.mark = '"4"/зачтено'
            elif (dis.control == 'Зачет с оценкой') and dis.total_mark == 3:
                dis.mark = '"3"/зачтено'
            elif (dis.control == 'Зачет с оценкой') and dis.total_mark == 2:
                dis.mark = '"2"/не зачтено'
            elif (dis.control == 'Зачет') and dis.total_mark > 2:
                dis.mark = 'Зачтено'
            elif (dis.control == 'Зачет') and dis.total_mark == 2:
                dis.mark = 'Не зачтено'
            if dis.retake > 0:
                if dis.retake == 5:
                    dis.ret_mark = '"5" (отлично)'
                elif dis.retake == 4:
                    dis.ret_mark = '"4" (хорошо)'
                elif dis.retake == 3:
                    dis.ret_mark = '"3" (удовл.)'
                elif dis.retake == 2:
                    dis.ret_mark = '"2" (неудовл.)'
            dis.save()
            context['semester'] = s
            context['discipline'] = dis
            return redirect('/semesters/discipline_marks?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'SEMESTER':
            km_number = data['km']
            mark = data['mark']
            ret_count = data['ret_count']
            ret_mark = data['ret_mark']
            name = data['discipline']
            sem = data['sem']

            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            kms = ControlEvent.objects.filter(discipline=dis)
            km = kms.get(number=int(km_number))

            km.mark = int(mark)
            km.ret_count = int(ret_count)
            if km.ret_count == 0:
                km.retake = False
            else:
                km.retake = True
            if ret_mark == '-1':
                km.ret_mark = None
            else:
                km.ret_mark = int(ret_mark)
            km.save()
            flag = False
            #kms = ControlEvent.objects.filter(discipline=dis)
            for k in kms:
                if k.mark is not None:
                    flag = True
            score = 0
            if flag:
                for k in kms:
                    if k.mark is not None and k.retake:
                        score += ((k.mark + k.ret_mark + 2*(k.ret_count-1))/(k.ret_count+1))*k.weight
                    elif k.mark is not None:
                        score += k.mark*k.weight
                dis.score = round(Decimal(str(score/100)).quantize(Decimal('1.0'), rounding=decimal.ROUND_HALF_UP), 1)
                dis.save()
            context['semester'] = s
            context['discipline'] = dis
            return redirect('/semesters/discipline_marks?sem=' + str(s.number) + '&name=' + dis.name, context=context)
        elif subject == 'MIDCERT_RETAKE':
            name = data['discipline']
            sem = data['sem']
            s = Semester.objects.get(number=int(sem))
            dis = Discipline.objects.filter(semester=s).get(name=name)
            ret_number = data['retake_number']
            dis.ret_number = int(ret_number)
            dis.save()
            context['semester'] = s
            context['discipline'] = dis
            return redirect('/semesters/discipline_marks?sem=' + str(s.number) + '&name=' + dis.name, context=context)

class DeleteDiscipline(View):
    def get(self, request):
        all = request.GET['all']
        if all == '0':
            id = request.GET['id']
            name = request.GET['name']
            s = Semester.objects.get(number=int(id))
            discipline = Discipline.objects.filter(semester=s).get(name=name)
            discipline.delete()
            return redirect('/semesters?id=' + id)
        elif all == '1':
            id = request.GET['id']
            s = Semester.objects.get(number=int(id))
            disciplines = Discipline.objects.filter(semester=s)
            for d in disciplines:
                d.delete()
            return redirect('/semesters?id=' + id)


def progress(request):
    #semester = '0'
    current_week = '5'
    if request.GET['sem'] != '':
        sem = request.GET['sem']
    semester = Semester.objects.get(number=int(sem))
    disciplines = Discipline.objects.filter(semester=semester)
    discip_objects = []
    for d in disciplines:
        dis = DisciplineObject(d)
        discip_objects.append(dis)

    #subjects_list = SubjectList(semester)
    reports = [
        Report('Учебная: ознакомительная', '2020/2021 осенний (1 курс)', 'Материалы прохождения практики',
               'ФГБОУ ВО НИУ МЭИ', 'Иваненко Кирилл Андреевич', 'Иваненко Кирилл Андреевич', 'Практикант'),
        Report('Учебная: профилирующая', '2020/2021 весенний (1 курс)', 'Материалы прохождения практики',
               'ФГБОУ ВО НИУ МЭИ', 'Иваненко Кирилл Андреевич', 'Иваненко Кирилл Андреевич', 'Практикант'),
    ]
    course_works = CourseWork.objects.all()
    context = {
        'semester': semester,
        'subjects': discip_objects,
        'disciplines': disciplines,
        'week': current_week,
        'weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'reports': reports,
        'course_works': course_works,
    }
    return render(request, 'progress.html', context)


def marks(request):
    sem = request.GET['sem']
    #sem1 = Semester.objects.get(number=1)
    dis1 = Discipline.objects.filter(semester=Semester.objects.get(number=int(sem)))
    # dis2 = Discipline.objects.filter(semester=Semester.objects.get(number=2))
    # dis3 = Discipline.objects.filter(semester=Semester.objects.get(number=3))

    #dis = list(chain(dis1, dis2, dis3))

    for d in dis1:
        if d.date.count('/') > 0:
            tmp = d.date.split('/')[0]
            d.date = tmp

    exams = []
    zach = []
    for d in dis1:
        if d.control == 'АВТОМАТ' or d.control == 'Экзамен' or d.control == 'Защита КР/КП':
            exams.append(d)
        else:
            zach.append(d)

    context = {
        'semester': int(sem),
        # 'subjects': discip_objects,
        'disciplines': dis1,
        'exams': exams,
        'zach': zach,
    }
    return render(request, 'session/marks.html', context)
