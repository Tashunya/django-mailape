from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import MailingList, Subscriber
from .factories import SubscriberFactory


class MockSendEmailToSubscriberTask:
    """
    TestCase mixin
    """
    def setUp(self):
        """
        Creates a patch, saves it as an attr of object,
        starts a patch, saves mock obj as attr of object,
        calls parent's setUp() to set up TestCase
        :return:
        """
        self.send_confirmation_email_patch = patch(
            'mailinglist.tasks.send_confirmation_email_to_subscriber')
        self.send_confirmation_email_mock = self.send_confirmation_email_patch.start()
        super.setUp()

    def tearDown(self):
        """
        Stops the patch,
        removes reference to mock,
        calls parent's tearDown() to complete cleanup
        :return:
        """
        self.send_confirmation_email_patch.stop()
        self.send_confirmation_email_mock = None
        super().tearDown()


class SubscriberCreationTestCase(MockSendEmailToSubscriberTask, TestCase):
    """
    Using TestCase mixin to patch tasks
    """
    def test_calling_create_queues_confirmation_email_task(self):
        """
        tests Subscriber creation
        :return:
        """
        user = get_user_model().objects.create_user(
            username='unit test runner')
        mailing_list = MailingList.objects.create(
            name='unit test',
            owner=user,)
        Subscriber.objects.create(
            email='unittest@example.com',
            mailing_list=mailing_list,)
        self.assertEqual(self.send_confirmation_email_mock.delay.call_count, 1)


class SubscriberManagerTestCase(TestCase):
    """
    tests using patch with factories
    """
    def testConfirmedSubscribersForMailingList(self):
        """
        tests confirmed_subscribers_for_mailing_list()
        :return:
        """
        mailing_list = MailingList.objects.create(
            name='unit test',
            owner=get_user_model().objects.create_user(username='unit test'))
        confirmed_users = [
            SubscriberFactory(confirmed=True, mailing_list=mailing_list) for n in range(3)]
        confirmed_users_qs = Subscriber.objects.confirmed_subscribers_for_mailing_list(
            mailing_list=mailing_list)
        self.assertEqual(len(confirmed_users), confirmed_users_qs.count())
        for user in confirmed_users_qs:
            self.assertIn(user, confirmed_users)
