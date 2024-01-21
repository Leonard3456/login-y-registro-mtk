from django.shortcuts import render, redirect, get_object_or_404 #el 404 sirve para el apartado de vistas de lista de tareas
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #cuando se ejecuta se da un formulario
from django.contrib.auth import login, logout, authenticate #crea una cookies y autenticar
from django.contrib.auth.models import User 
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

from .forms import TaskForm

# Create your views here.

#def seria como crear una función
def signup(request): #instancia request
    #se utiliza para acceder a los datos del formulario enviado por el cliente
    if request.method == 'GET': ###GET solicitar datos del servidor
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        ###POST enviar datos al servidor
        if request.POST["password1"] == request.POST["password2"]: #registrar usuario
           #Try y except sirve para errores
           #Intentar crear un nuevo usuario con los datos proporcionados
            try:
                user = User.objects.create_user( #crear usuario
                    request.POST["username"], password=request.POST["password1"])
                user.save() #almacena en la base de datos       
                
                login(request, user)   # Iniciar sesión automáticamente después del registro
                
                return redirect('tasks') #Redirecciona a task  
            
            #VERIFICA SI HAY UN USUARIO IGUAL
            except IntegrityError: #el integrityerror es para cuando pasa el erorr de tener dos usuarios iguales
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "El usuario ya existe"})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Las contraseñas no coinciden"})


@login_required #el login requerido es por una libreria de django
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks}) 

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required #crear tareas
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user #para no tener conflicto cuando ya se inicio seión
            new_task.save() #para guardar la tarea en la base de datos
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error al crear la tarea."})


def home(request):
    return render(request, 'home.html')


@login_required
def signout(request): #cuando inicias sesión recien esta el logout
    logout(request)
    return redirect('home')


def signin(request): #para iniciar sesión cuando ya se registro
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrecta."})

        login(request, user)
        return redirect('tasks')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error al actualizar la tarea.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')