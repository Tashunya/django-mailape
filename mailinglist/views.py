from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from mailinglist.models import MailingList
from mailinglist.forms import MailingListForm


class MailingListListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return MailingList.objects.filter(owner=self.request.user)


class CreateMailingListView(LoginRequiredMixin, CreateView):
    form_class = MailingListForm
    template_name = 'mailinglist/mailinglist_form.html'

    def get_initial(self):
        return {'owner': self.request.user.id}
