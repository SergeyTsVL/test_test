from django import forms
from .models import Ad, ExchangeProposal, Viewer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class ViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = ['user']




class AdForm(forms.ModelForm):
    """
    Этот блок кода определяет метаданные (Meta) для модели Ad. model = Ad: Это указывает Django,
    что эти метаданные относятся к модели Advertisement. Это не обязательно нужно явно указывать, так как Django обычно
    может определить это автоматически.
    fields = ['id', 'user', 'title', ...] Это список полей модели, которые будут отображаться в форме модели. В
    данном случае это заголовок объявления (title), пользователь (user), ...
    """
    class Meta:
        model = Ad
        fields = ['id', 'user', 'title', 'description', 'title_image', 'image_url', 'title_video', 'video_file', 'title_audio',
                  'audio_file', 'category', 'status']
        labels = {
            'title_image': 'Название изображения',
            'image_url': 'Изображение',
            'video_file': 'Видеофайл',
            'title_video': 'Название видео',
            'title_audio': 'Название аудио файла',
            'audio_file': 'Аудио файл'
        }
        widgets = {
            'image_url': forms.FileInput(attrs={'accept': 'image/*'}),
            'video_file': forms.FileInput(attrs={'accept': 'video/*'}),
            'audio_file': forms.FileInput(attrs={'accept': 'audio/*'})
        }

class ExchangeProposalForm(forms.ModelForm):
    """
    Этот блок кода определяет метаданные (Meta) для модели Ad. model = Ad: Это указывает Django,
    что эти метаданные относятся к модели Advertisement. Это не обязательно нужно явно указывать, так как Django обычно
    может определить это автоматически.
    fields = ['id', 'user', 'title', ...] Это список полей модели, которые будут отображаться в форме модели. В
    данном случае это заголовок объявления (title), пользователь (user), ...
    """
    class Meta:
        model = ExchangeProposal
        fields = ['id', 'ad_sender', 'ad_receiver', 'comment', 'status']


# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ('title', 'video_file')
#         labels = {
#             'title': 'Название видео',
#             'video_file': 'Выберите видеофайл'
#         }

class SignUpForm(UserCreationForm):
    """
    Этот класс SignUpForm представляет собой кастомную форму регистрации пользователя, которая расширяет стандартную
    форму UserCreationForm. UserCreationForm - Это стандартная форма Django для регистрации новых пользователей.
    SignUpForm расширяет UserCreationForm, что позволяет переопределить некоторые аспекты формы, если необходимо.
    Использование Meta позволяет задать метаданные формы без необходимости создавать отдельный экземпляр класса.
    Поле fields определяет, какие поля формы будут отображаться. В данном случае это базовые поля для регистрации
    пользователя.
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)


