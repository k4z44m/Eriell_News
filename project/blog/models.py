from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile




class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Здесь будет описание', verbose_name='описание')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Изображение')
    # null = True - пустое поле может быть, blank = True - поле можно не заполнять
    views = models .IntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # auto_now_add=True возьмет автоматически время когда статья была создана
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    # auto_now = True возьмет время любого изменения
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://drasler.ru/wp-content/uploads/2019/04/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%BD%D1%8B%D0%B5-%D0%BE%D0%B1%D0%BE%D0%B8-%D0%BD%D0%B0-%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD-%D0%B4%D0%BB%D1%8F-%D0%BC%D0%B0%D0%BB%D1%8C%D1%87%D0%B8%D0%BA%D0%BE%D0%B2-15-%D0%BB%D0%B5%D1%82-%D0%BF%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BA%D0%B0-1.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE,
                                related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Comment text: ', default='please, prompt text here')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    parent = models.ForeignKey('self', default=None, blank=True,
                               null=True, on_delete=models.CASCADE,
                               related_name='children', verbose_name='Parent')

    def __str__(self):
        return f'{self.user} - {self.text[:10]}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    instagram_url = models.CharField(default=None, null=True, blank=True, max_length=255)
    telegram_url = models.CharField(default=None, null=True, blank=True, max_length=255)
    facebook_url = models.CharField(default=None, null=True, blank=True, max_length=255)
    youtube_url = models.CharField(default=None, null=True, blank=True, max_length=255)

    def get_bio(self):
        if self.bio:
            return self.bio
        else:
            return 'Not written in profile'

    def get_instagram_url(self):
        if self.bio:
            return self.instagram_url
        else:
            return 'Not written in profile'

    def get_telegram_url(self):
        if self.bio:
            return self.telegram_url
        else:
            return 'Not written in profile'

    def get_facebook_url(self):
        if self.bio:
            return self.facebook_url
        else:
            return 'Not written in profile'

    def get_youtube_url(self):
        if self.bio:
            return self.youtube_url
        else:
            return 'Not written in profile'

    def get_image(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://bootdey.com/img/Content/avatar/avatar7.png'




    # def get_image(self):
    #     if self.image:
    #         image = Image.open(self.image.path)
    #         if image.width > 315 or image.height > 315:
    #             output_size = (315, 315)
    #             image.thumbnail(output_size)
    #         img_io = BytesIO()
    #         image.save(img_io, format='JPEG', quality=90)
    #         file = InMemoryUploadedFile(img_io, None, self.image.name, 'image/jpeg', img_io.getbuffer().nbytes, None)
    #         return file
    #     else:
    #         return 'https://bootdey.com/img/Content/avatar/avatar7.png'






    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'



