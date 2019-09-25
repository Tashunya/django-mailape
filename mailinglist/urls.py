from django.urls import path
from mailinglist import views

app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailingListListView.as_view(), name='mailinglist_list'),
]
