from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


def birthday(request, pk=None):
    template = 'birthday/birthday.html'
    if pk is not None:
        # Получение существующей записи дня рождения для редактирования
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None

    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    context = {'form': form}

    if form.is_valid():
        # Сохранение данных формы при их валидации
        form.save()

        # Вычисление обратного отсчета до дня рождения
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        context.update({'birthday_countdown': birthday_countdown})

    return render(request, template, context)


def birthday_list(request):
    template = 'birthday/birthday_list.html'

    # Получение всех записей дня рождения
    birthdays = Birthday.objects.order_by('id')
    paginator = Paginator(birthdays, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


@require_POST
def delete_birthday(request, pk):
    template = 'birthday/birthday.html'

    # Получение существующей записи дня рождения для удаления
    instance = get_object_or_404(Birthday, pk=pk)
    form = BirthdayForm(instance=instance)
    context = {
        'form': form
    }

    if request.method == 'POST':
        # Удаление записи дня рождения
        instance.delete()
        return redirect('birthday:list')

    return render(request, template, context)
