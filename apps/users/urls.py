
# users/views.py (тестовый)
from django.shortcuts import render
from .forms import UserRegistrationForm

def test_form(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Пользователь создан: {user.username}")
            return render(request, 'test_success.html')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'test_form.html', {'form': form})