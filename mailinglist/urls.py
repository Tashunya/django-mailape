from django.urls import path
from mailinglist import views

app_name = 'mailinglist'

urlpatterns = [
    path('', views.MailingListListView.as_view(), name='mailinglist_list'),
    path('new', views.CreateMailingListView.as_view(), name='create_mailinglist'),
    path('<uuid:pk>/delete', views.DeleteMailingListView.as_view(),
         name='delete_mailinglist'),
]
