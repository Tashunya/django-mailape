from unittest.mock import patch
import factory
from .models import Subscriber


class SubscriberFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: f'foo.{n}@example.com')

    class Meta:
        model = Subscriber

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        overrides default _create() to apply task patch before calling _create()
        then calls save() and tries to queue send_confirmation_email task
        the task will be replaced by mock
        :param model_class:
        :param args:
        :param kwargs:
        :return:
        """
        with patch('mailinglist.models.tasks.send_confirmation_email_to_subscriber'):
            return super()._create(model_class=model_class, *args, **kwargs)
