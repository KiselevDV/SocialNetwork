from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image

from common.decorators import ajax_required


@login_required
def image_create(request):
    """Добавить изображение"""
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


def image_detail(request, id, slug):
    """Сведения об изображении"""
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {
        'section': 'images',
        'image': image,
    })


@ajax_required
@login_required
@require_POST
def image_like(request):
    """Возможность ставить лайк"""
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    """Все картинки"""
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})
