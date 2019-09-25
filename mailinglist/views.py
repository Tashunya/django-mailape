from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from mailinglist.models import MailingList


class MailingListListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)
