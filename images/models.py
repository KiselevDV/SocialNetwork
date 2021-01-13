from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Image(models.Model):
    """Сохранение изображений добавленных в закладки"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Пользователь',
        related_name='images_created', on_delete=models.CASCADE)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name='Пользователь поставивший лайк',
        related_name='images_liked', blank=True)
    title = models.CharField('Заголовок картинки', max_length=200)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Файл изображения', upload_to='images/%Y/%m/%d')
    # db_index - создать индекс по этому полю
    created = models.DateField('Дата создания', auto_now_add=True)
    # Ссылка на оригинальную картинку
    url = models.URLField('ССылка на оригинальную картинку')
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Для автоматического создания slug из title"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
