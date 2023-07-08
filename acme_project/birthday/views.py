from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

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


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10 



class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass

class BirthdayDetailView(DetailView):
    model = Birthday

