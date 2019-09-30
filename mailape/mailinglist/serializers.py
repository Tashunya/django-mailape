from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MailingList, Subscriber


class MailingListSerializer(serializers.HyperlinkedModelSerializer):
    """
    HyperlinkedModelSerializer shows hyperlink to any related model
    """
    # PrimaryKeyRelatedField returns related object's pk,
    # when related model doesn't have a serializer or related API view
    owner = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all())

    class Meta:
        model = MailingList
        fields = ('url', 'id', 'name', 'owner', 'subscriber_set')
        read_only_fields = ('subscriber_set', )
        # extra args to field's constructor
        extra_kwargs = {
            # name of MailingList API detail view
            'url': {'view_name': 'mailinglist:api-mailing-list-detail'},
            # name of Subscriber API detail view
            'subscriber_set': {'view_name': 'mailinglist:api-subscriber-detail'},
        }


class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailing_list')
        extra_kwargs = {
            'url': {'view_name': 'mailinglist:api-subscriber-detail'},
            'mailing_list': {'view_name': 'mailinglist:api-mailing-list-detail'},
        }


class ReadOnlyEmailSubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ('url', 'id', 'email', 'confirmed', 'mailing_list')
        read_only_fields = ('email', 'mailing_list', )
        extra_kwargs = {
            'url': {'view_name': 'mailinglist:api-subscriber-detail'},
            'mailing_list': {'view_name': 'mailinglist:api-mailing-list-detail'},
        }
