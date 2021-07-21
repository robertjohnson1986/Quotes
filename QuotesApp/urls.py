from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('post_title', views.post_title),
    path('post description', views.post_description),
    path('like_message/<int:id>', views.like),
    path('like_message1/<int:id>', views.like1),
    path('unlike_message/<int:id>', views.unlike),
    # path('delete_comment/<int:id>', views.delete_comment),
    path('delete_message/<int:id>', views.delete_message),
    path('quote_page/<int:user_id>', views.quote_page),
    path('update/<int:id>', views.update),
    path('edit/<int:id>', views.edit),
    path('stats', views.stats),
    path('make_a_wish', views.make)
    # path('grant_wish/<int:id>', views.grant_wish)

]