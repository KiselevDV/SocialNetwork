from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from urllib import request

from .models import Image


class ImageCreateForm(forms.ModelForm):
    """Форма сохранения объекта (картинки)"""

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # Заменили виджет по умолчанию на (forms.HiddenInput)
        widgets = {'url': forms.HiddenInput, }

    def clean_url(self):
        """Проверка поля 'url' из 'fields'"""
        url = self.cleaned_data['url']
        valid_extension = ['jpg', 'jpeg']
        # получаем в переменную 'extension' расширение файла
        extension = url.rsplit('.', 1)[1].lower()
        # проверка файлов на то, что-бы они оканчивались на 'jpg' или 'jpeg'
        if extension not in valid_extension:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """Переопределение метода save"""
        # Создаёт объект из формы, вызывая метод 'save' не сохраняет
        image = super(ImageCreateForm, self).save(commit=False)
        # Получаем url из 'cleaned_data'
        image_url = self.cleaned_data['url']
        # Генериут название картинки из slug + расширение
        image_name = '{}.{}'.format(
            slugify(image.title),
            image_url.rsplit('.', 1)[1].lower()
        )

        # Скачиваем изображение по указанному адресу с помощью 'urllib'
        # response - объект скачанного файла
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        # Сохраняем в БД если commit=True
        if commit:
            image.save()
        return image
