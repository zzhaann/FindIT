from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, JobsForm
from .models import Jobs
from django.contrib import messages



@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = JobsForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.creator = request.user
            job.save()
            return redirect('jobs')
        else:
            error = "Form is wrong"
    form = JobsForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create_job.html', context)


def job(request):
    jobs = Jobs.objects.all()
    return render(request, 'main/job_list.html', {'title': 'Работа', 'jobs': jobs})






def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.role == 'employer':
                return redirect('create_job')
            return redirect('jobs')
        else:
            # Добавляем все ошибки формы в сообщения
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CustomUserCreationForm()  # Пустая форма для GET-запроса
    return render(request, 'main/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == 'employer':
                return redirect('create_job')
            return redirect('jobs')
        else:
            # Убираем глобальные ошибки
            return render(request, 'main/login.html', {
                'username': username,  # сохраняем введенные данные
                'errors': True  # для повторной отрисовки формы с подсветкой ошибок
            })

    return render(request, 'main/login.html')


@login_required
def index(request):
    return render(request, 'main/index.html')
