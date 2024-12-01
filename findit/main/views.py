from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ResumeForm, JobsForm
from .models import Application, Resume, Jobs
from .models import CustomUser
from .models import Message
from .forms import MessageForm
from django.shortcuts import render, redirect
from django.db.models import Q
from django.conf import settings


@login_required
def employer_profile(request):
    # Получаем все вакансии, созданные текущим пользователем
    jobs = Jobs.objects.filter(creator=request.user)

    # Передаем список вакансий в шаблон
    return render(request, 'main/employer_profile.html', {'jobs': jobs})

@login_required
def worker_chats(request):
    # Получаем список работодателей, с которыми есть переписка
    employers = CustomUser.objects.filter(
        sent_messages__recipient=request.user
    ).distinct()

    return render(request, 'main/worker_chats.html', {'employers': employers})


@login_required
def chat_with_employer(request, employer_id):
    # Получаем работодателя, с которым будет открыт чат
    employer = get_object_or_404(CustomUser, id=employer_id)

    # Фильтруем сообщения между работником и этим работодателем
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=employer)) |
        (Q(sender=employer) & Q(recipient=request.user))
    ).order_by('timestamp')

    # Обрабатываем отправку нового сообщения
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=employer, content=content)
            return redirect('chat_with_employer', employer_id=employer.id)

    return render(request, 'main/chat_with_employer.html', {'messages': messages, 'employer': employer})


@login_required
def chat_with_worker(request, worker_id):
    worker = get_object_or_404(CustomUser, id=worker_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=worker)) |
        (Q(sender=worker) & Q(recipient=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=worker, content=content)

    return render(request, 'main/chat.html', {'worker': worker, 'messages': messages})





def worker_profile(request, id):
    worker = get_object_or_404(CustomUser, id=id)
    try:
        resume = Resume.objects.get(user=worker)
    except Resume.DoesNotExist:
        resume = None  # если резюме не существует, можно отобразить сообщение или пустые поля

    return render(request, 'main/worker_profile.html', {'worker': worker, 'resume': resume})

@login_required
def edit_resume(request):
    user = request.user
    try:
        resume = Resume.objects.get(user=user)
        form = ResumeForm(request.POST or None, request.FILES or None, instance=resume)
    except Resume.DoesNotExist:
        form = ResumeForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        resume = form.save(commit=False)
        resume.user = user
        resume.save()
        messages.success(request, 'Резюме обновлено!')
        return redirect('worker_profile', id=user.id)  # Можно вернуть пользователя на страницу профиля, если это необходимо

    return render(request, 'main/edit_resume.html', {'form': form})





@login_required
def employer_dashboard(request):
    if request.user.role == 'employer':
        jobs = request.user.created_jobs.all()
        return render(request, 'main/employer_dashboard.html', {'jobs': jobs})
    return redirect('jobs')




from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Jobs, Application

@login_required
def apply(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)

    # Проверка, что пользователь является работником
    if request.user.role != 'worker':
        messages.error(request, 'Только работники могут откликаться на вакансии.')
        return redirect('jobs')

    # Проверяем, что работник уже не откликнулся на эту вакансию
    if Application.objects.filter(job=job, worker=request.user).exists():
        messages.error(request, 'Вы уже откликнулись на эту вакансию.')
        return redirect('jobs')

    if request.method == 'POST':
        Application.objects.create(job=job, worker=request.user)

        # Отправка уведомления работодателю
        send_mail(
            'Новый отклик на вашу вакансию',
            f'Пользователь {request.user.username} откликнулся на вашу работу: {job.title}.',
            settings.DEFAULT_FROM_EMAIL,
            [job.creator.email],
            fail_silently=False,
        )

        # Уведомление для работника
        messages.success(request, 'Вы успешно откликнулись на вакансию!')

    return redirect('jobs')

@login_required
def create_job_and_company(request):
    form_job = JobsForm(request.POST or None, request.FILES or None)
    error = ''

    if request.user.role == 'employer':
        if form_job.is_valid():
            job = form_job.save(commit=False)
            job.creator = request.user  # Устанавливаем создателя вакансии
            job.save()  # Сохраняем вакансию

            return redirect('employer_dashboard')  # Перенаправляем на страницу работодателя
        else:
            error = "Пожалуйста, исправьте ошибки в формах."

    return render(request, 'main/create_job.html', {
        'form_job': form_job,
        'error': error,
    })




def job(request):
    jobs = Jobs.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(task__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    user_role = request.user.role if request.user.is_authenticated else None

    return render(request, 'main/job_list.html', {
        'title': 'Работа',
        'jobs': jobs,
        'user_role': user_role,
        'search_query': search_query,
    })


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'employer':
                return redirect('employer_dashboard')
            return redirect('jobs')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'main/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'employer':
                return redirect('employer_dashboard')
            return redirect('jobs')
        else:
            return render(request, 'main/login.html', {'errors': True})

    return render(request, 'main/login.html')



def index(request):
    return render(request, 'main/index.html')
