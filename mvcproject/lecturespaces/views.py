from django.shortcuts import render
from .models import UserSavedLecturespace, UserSavedFlashcard, Lecturespace
from .forms import LecturespaceForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

def index(request):
    return render(request, 'index.html')

def user_dashboard(request):
    saved_lecturespaces = UserSavedLecturespace.objects.filter(user=request.user)
    saved_flashcards = UserSavedFlashcard.objects.filter(user=request.user)
    return render(request, 'lecturespaces/user_dashboard.html', {
        'saved_lecturespaces': saved_lecturespaces,
        'saved_flashcards': saved_flashcards
    })


def create_lecturespace(request):
    if request.method == 'POST':
        form = LecturespaceForm(request.POST)
        if form.is_valid():
            lecturespace = form.save(commit=False)
            lecturespace.created_by = request.user
            lecturespace.save()
            return redirect('lecturespace_detail', lecturespace_id=lecturespace.id)
    else:
        form = LecturespaceForm()
    return render(request, 'lecturespaces/create_lecturespace.html', {'form': form})

def explore_lecturespaces(request):
    lecturespaces = Lecturespace.objects.all()
    return render(request, 'lecturespaces/explore_lecturespaces.html', {'lecturespaces': lecturespaces})

def lecturespace_detail(request, lecturespace_id):
    lecturespace = get_object_or_404(Lecturespace, id=lecturespace_id)
    return render(request, 'lecturespaces/lecturespace_detail.html', {'lecturespace': lecturespace})