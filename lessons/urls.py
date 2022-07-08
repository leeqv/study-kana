from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    re_path(r'^(?P<menu>study|review|watchlist)\/$', views.menu_view, name="menu"),
    re_path(r'^(?P<menu>study|review)\/((?P<kana>[HK])-(?P<lesson_number>\d+)(\/(?P<letter>[a-zA-Z]{0,3}))*)+\/$', views.lesson_view, name="lesson"), 
    path("update_watchlist/", views.update_watchlist, name="update_watchlist"),  
    
    re_path(r'^(quiz)\/((?P<kana>[HK])-(?P<quiz_number>\d+)*)+\/$', views.quiz_view, name="quiz"),   
    re_path(r'^(load_quiz)\/((?P<kana>[HK])/(?P<quiz_number>\d+)*)+\/$', views.load_quiz, name="load_quiz"), 
    re_path(r'^(check_answer)\/((?P<kana>[HK])/(?P<quiz_number>\d+)*)+\/$', views.check_answer, name="check_answer"),   
    re_path(r'^(save_score)\/((?P<kana>[HK])/(?P<quiz_number>\d+)*)+\/$', views.save_score, name="save_score"), 

    path("profile/", views.profile_view, name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = views.error_404
handler500 = views.error_500