from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ImageCreateForm


@login_required
def image_create(request):
    """"""
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # С помощью метода 'cleaned_data' преобразовываем данные 'form'
            # В виде словаря и записываем их в переменную  'cd'
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # Привязываем  текущего пользователя к созданному объекту
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            # Перенаправляем пользователя на страницу сохранённого изображения
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET запроса
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {
        'section': 'images',
        'form': form,
    })

