from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib import messages
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from .forms import VideoForm
# from .models import Video

from django.shortcuts import get_object_or_404, render
from django.db.models import F
# from .models import Ad
from django.http import HttpResponseForbidden
from django.db.models import Exists, OuterRef

def logout_view(request):
    """
    Этот метод выполняет выход пользователя из системы и перенаправляет его на домашнюю страницу.
    """
    logout(request)
    return redirect('home')

def home(request):
    """
    Вызывает страницу home.html .
    """
    # User = get_user_model()
    # user = get_object_or_404(User)
    # room = f"user_{user.username}"

    # ads = User.objects.all()
    ads = (
        User.objects
        .filter(groups__name="streamer")
        # .annotate(has_ads=Exists(Ad.objects.filter(user=OuterRef("pk"))))   # вывести только тех стримеров у которых
        # .filter(has_ads=True)                                               # есть объявления
        .distinct()
        .order_by("username")
    )
    paginator = Paginator(ads, 36)  # 6 объявлений на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {
        'page_obj': page_obj, 'ads': ads
    })














    # return render(request, 'home.html')

def signup(request):
    """
    Вызывает страницу для подписи объявлений.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/accounts/profile/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required  # Проверяет регистрацию пользователя
def add_ad(request):
    """
    Этот метод считывает данные объектов из класса Advertisement, проверяет были ли запрос "POST", обрабатывает
    данные формы, если все поля заполнены полностью, корректны и содержат все необходимые данные. Затем, при
    добавлении данных, автоматически устанавливает автора как текущего авторизованного пользователя. Если запроса "POST"
    не было, то возвращаемся к предыдущей странице без изменений.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user.groups.filter(name="streamer").exists():
        return render(request, "errors/advertisment_streamers.html", status=403)

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            # ad.name = request.user
            ad.status = 'В ожидании'
            ad.save()
            return redirect('ads:add_ad')
    else:
        form = AdForm()
    return render(request, 'ads_ads/add_ad.html', {'form': form})

class SearchResultsView(ListView):
    model = Ad
    template_name = 'ads_ads/search_results.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q')
        object_list = Ad.objects.filter(
            Q(title__icontains=query) | Q(title_image__icontains=query) | Q(title_video__icontains=query) |
            Q(title_audio__icontains=query) | Q(category__icontains=query) | Q(status__icontains=query)
        )
        return object_list

class HomePageView(TemplateView):
    template_name = 'ads_ads/search.html'


def ad_detail(request, pk):
    """
    Вызывает страницу ad_detail.html. При это атомарно подсчитывает количество просмотров.
    """
    # print(request)
    ad = Ad.objects.get(pk=pk)

    image = get_object_or_404(Ad, id=pk)
    image.views_image = F('views_image') + 1
    image.save()

    video = get_object_or_404(Ad, id=pk)
    video.views_video = F('views_video') + 1
    video.save()

    audio = get_object_or_404(Ad, id=pk)
    audio.views_audio = F('views_audio') + 1
    audio.save()
    # print(str(render(request, 'ads_ads/ad_detail.html', {'ad': ad})))
    return render(request, 'ads_ads/ad_detail.html', {'ad': ad})

@login_required
def delete_ad(request, pk):
    """
    Этот метод считывает данные объектов из класса Advertisement, проверяет были ли запрос "POST", после чего удаляет
    объявление и возвращается в окно объявления.
    :param request:
    :param pk:
    :return:
    """
    ad = Ad.objects.get(pk=pk)
    if ad.status != 'Принято':
        if request.method == "POST":
            ad.delete()
            return redirect('ads:ad_list')
        else:
            None
        return render(request, 'ads_ads/delete_ad.html', {'ad': ad})
    else:
        return redirect('ads:ad_list')

@login_required    # Проверяет регистрацию пользователя
def edit_ad(request, pk):
    """
    Этот метод считывает данные объектов из класса Advertisement, проверяет были ли запрос "POST", обрабатывает
    данные формы, если все поля заполнены полностью, корректны и содержат все необходимые данные. Затем, при
    редактировании, автоматически устанавливает автора как текущего авторизованного пользователя. Если запроса "POST"
    не было, то возвращаемся к предыдущей странице без изменений.
    :param request:
    :param pk:
    :return:
    """
    ads = Ad.objects.get(pk=pk)
    if ads.status != 'Принято' and ads.user == request.user:      # Проверяет является ли пользователь автором
        if request.method == "POST":
            form = AdForm(request.POST, request.FILES, instance=ads)
            if form.is_valid():
                # ads.instance.user = request.user
                # form.save()
                img_obj = form.instance
                form.save()
                # Перенаправляет на страницу с сохраненными исправлениями.
                return redirect('ads:ad_detail', pk=img_obj.pk)
        else:
            # вызов функции которая отобразит в браузере указанный шаблон с данными формы и объявления.
            messages.error(request, 'Вы можете редактировать только свои объявления')
            form = AdForm(instance=ads)
        return render(request, 'ads_ads/edit_ad.html',
                      {'form': form, 'ads': ads})
    return redirect('ads:ad_detail', pk=pk)


@login_required
def create_proposal(request):
    if request.method == "POST":
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            # ad.name = request.user
            ad.status = 'В ожидании'
            ad.save()
            return redirect('ads:create_proposal')
    else:
        form = ExchangeProposalForm()
    return render(request, 'ads_ads/create_proposal.html', {'form': form})

@login_required
def add_proposal(request):
    """
    Вызывает страницу advertisement_list.html.
    """
    exc = ExchangeProposal.objects.all()
    return render(request, 'ads_ads/manage_proposal.html', {'exc': exc})

def profile(request):
    """
    Вызывает страницу home.html.
    """
    return render(request, 'home.html')

@login_required
def ad_list(request):
    """
    Этот метод выводит пагинацию.
    """
    # ads = Ad.objects.all()
    ads = (
        Ad.objects
        .filter(user__groups__name="streamer")   # только стримеры
        .filter(status="accepted")              # если нужно только принятые
        .select_related("user")
        .order_by("-created_at")
    )
    paginator = Paginator(ads, 3)  # 6 объявлений на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ads_ads/ad_list.html', {
        'page_obj': page_obj, 'ads': ads
    })

@login_required  # Проверяет регистрацию пользователя
def edit_exc(request, pk):
    """
    Этот метод считывает данные объектов из класса Advertisement, проверяет были ли запрос "POST", обрабатывает
    данные формы, если все поля заполнены полностью, корректны и содержат все необходимые данные. Затем, при
    редактировании, автоматически устанавливает автора как текущего авторизованного пользователя. Если запроса "POST"
    не было, то возвращаемся к предыдущей странице без изменений.
    :param request:
    :param pk:
    :return:
    """
    print(request, pk)
    ads = ExchangeProposal.objects.get(pk=pk)
    if request.method == "POST":
        form = ExchangeProposalForm(request.POST, request.FILES, instance=ads)
        if form.is_valid():
            form.save()
            # Перенаправляет на страницу с сохраненными исправлениями.
            return redirect('ads:add_proposal')
    else:
        # вызов функции которая отобразит в браузере указанный шаблон с данными формы и объявления.
        form = ExchangeProposalForm(instance=ads)
    return render(request, 'ads_ads/edit_exc.html',
                  {'form': form, 'ads': ads})





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def go_live(request):
    # user сам будет вещать в комнату user_<id>

    if not request.user.groups.filter(name="streamer").exists():
        # return HttpResponseForbidden("Доступ только для стримеров")
        return render(request, "errors/only_streamers.html", status=403)
    room = f"user_{request.user.id}"
    return render(request, "stream/go_live.html", {"room": room})

# def watch_stream(request, user_id: int):
#     # любой может смотреть (если нужно ограничить — добавим проверки)
#     ads = Ad.objects.get(pk=user_id)
#     if ads.user == request.user:
#
#
#     user = get_object_or_404(User, id=user_id)
#     room = f"user_{user.id}"
#     return render(request, "stream/watch.html", {"room": room, "stream_user": user})


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import Ad

def watch_stream(request, user_id: int):
    stream_user = get_object_or_404(User, id=user_id)
    room = f"user_{stream_user.id}"

    # Все объявления этого пользователя
    user_ads = Ad.objects.filter(user=stream_user).order_by("-created_at")

    # Если нужно показывать только принятые/активные:
    # user_ads = Ad.objects.filter(user=stream_user, status="accepted").order_by("-created_at")

    return render(request, "stream/watch.html", {
        "room": room,
        "stream_user": stream_user,
        "user_ads": user_ads,
    })



from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .forms import SignUpForm

def _signup_with_group(request, group_name: str, template: str):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, template, {"form": form})


def signup_viewer(request):
    return _signup_with_group(request, "viewer", "registration/signup_viewer.html")


def signup_streamer(request):
    return _signup_with_group(request, "streamer", "registration/signup_streamer.html")


from django.shortcuts import render, redirect
from django.contrib import messages






def dev_password_page(request):
    if request.method == 'GET':
        next_url = request.GET.get('next')
        if next_url:
            request.session['next_url'] = next_url

    if request.method == 'POST':
        password = request.POST.get('password')

        if password == "super_secret_password_123":
            request.session['dev_authenticated'] = True
            request.session.set_expiry(900)

            next_url = request.session.pop('next_url', None)

            if next_url:
                return redirect(next_url)

            return redirect('home')

        messages.error(request, "Неверный пароль!")

    return render(request, 'dev_password_page.html')
