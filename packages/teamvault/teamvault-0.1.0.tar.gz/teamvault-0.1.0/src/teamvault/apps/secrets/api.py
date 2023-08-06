from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import AccessRequest, Secret, SecretRevision


ACCESS_POLICY_REPR = {
    Secret.ACCESS_POLICY_ANY: "any",
    Secret.ACCESS_POLICY_HIDDEN: "hidden",
    Secret.ACCESS_POLICY_REQUEST: "request",
}
REPR_ACCESS_POLICY = {v: k for k, v in ACCESS_POLICY_REPR.items()}

STATUS_REPR = {
    Secret.STATUS_DELETED: "deleted",
    Secret.STATUS_NEEDS_CHANGING: "needs_changing",
    Secret.STATUS_OK: "ok",
}
REPR_STATUS = {v: k for k, v in STATUS_REPR.items()}


class AccessRequestSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(
        view_name='api.access-request_detail',
    )
    requester = serializers.Field(
        source='requester.username',
    )
    secret = serializers.HyperlinkedRelatedField(
        queryset=Secret.objects.exclude(status=Secret.STATUS_DELETED),
        view_name='api.secret_detail',
    )
    reviewers = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.exclude(is_active=False),
        slug_field='username',
    )

    class Meta:
        model = AccessRequest
        fields = (
            'api_url',
            'closed',
            'closed_by',
            'created',
            'secret',
            'reason_request',
            'reason_rejected',
            'requester',
            'reviewers',
            'status',
        )
        read_only_fields = (
            'closed',
            'closed_by',
            'created',
        )


class AccessRequestDetail(generics.RetrieveUpdateAPIView):
    model = AccessRequest
    serializer_class = AccessRequestSerializer

    def get_object(self):
        obj = get_object_or_404(AccessRequest, pk=self.kwargs['pk'])
        if (
            not self.request.user == obj.requester and
            not self.request.user in obj.reviewers and
            not self.request.user.is_superuser
        ):
            self.permission_denied(self.request)
        return obj

    def pre_save(self, obj):
        previous_state = AccessRequest.objects.get(pk=obj.pk)
        if (
            previous_state.status != AccessRequest.STATUS_PENDING or
            obj.status == AccessRequest.STATUS_PENDING or
            self.request.user not in previous_state.reviewers.all() or
            obj.password != previous_state.password
        ):
            self.permission_denied(self.request)

    def post_save(self, obj, created=False):
        #obj.handle_status() TODO
        pass


class AccessRequestList(generics.ListCreateAPIView):
    model = AccessRequest
    paginate_by = 50
    serializer_class = AccessRequestSerializer

    def get_queryset(self):
        return AccessRequest.get_all_readable_by_user(self.request.user)

    def pre_save(self, obj):
        obj.reason_rejected = ""
        obj.requester = self.request.user
        obj.status = AccessRequest.STATUS_PENDING

    def post_save(self, obj, created=False):
        if created:
            obj.assign_reviewers()


class SecretRevisionSerializer(serializers.HyperlinkedModelSerializer):
    api_url = serializers.HyperlinkedIdentityField(
        view_name='api.secret-revision_detail',
    )
    created_by = serializers.Field(
        source='set_by.username',
    )
    data_url = serializers.CharField(
        read_only=True,
        required=False,
        source='id',
    )

    def to_representation(self, instance):
        rep = super(SecretSerializer, self).to_representation(instance)
        rep['data_url'] = reverse(
            'api.secret-revision_data',
            kwargs={'pk': instance.pk},
            request=self.context['request'],
        )
        return rep

    class Meta:
        model = SecretRevision
        fields = (
            'api_url',
            'created',
            'created_by',
            'secret_url',
        )
        read_only_fields = (
            'created',
        )


class SecretSerializer(serializers.HyperlinkedModelSerializer):
    allowed_groups = serializers.SlugRelatedField(
        many=True,
        queryset=Group.objects.all(),
        slug_field='name',
    )
    allowed_users = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.exclude(is_active=False),
        slug_field='username',
    )
    api_url = serializers.HyperlinkedIdentityField(
        view_name='api.secret_detail',
    )
    created_by = serializers.CharField(
        read_only=True,
        required=False,
        source='created_by.username',
    )
    current_revision = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='api.secret-revision_detail',
    )
    data_readable = serializers.BooleanField(
        read_only=True,
        required=False,
        source='id',
    )
    data_url = serializers.CharField(
        read_only=True,
        required=False,
        source='id',
    )
    password = serializers.CharField(
        required=False,
        write_only=True,
    )

    def create(self, validated_data):
        allowed_groups = validated_data.pop('allowed_groups', [])
        allowed_users = validated_data.pop('allowed_users', [])

        if 'password' in validated_data:
            data = validated_data.pop('password')

        instance = self.Meta.model.objects.create(**validated_data)

        instance.allowed_groups = allowed_groups
        instance.allowed_users = allowed_users
        instance._data = data
        return instance

    def to_internal_value(self, data):
        try:
            data['access_policy'] = REPR_ACCESS_POLICY[data.get('access_policy', None)]
        except KeyError:
            # Validation will catch it
            pass

        try:
            data['status'] = REPR_STATUS[data.get('status', None)]
        except KeyError:
            # Validation will catch it
            pass

        return super(SecretSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        rep = super(SecretSerializer, self).to_representation(instance)
        rep['access_policy'] = ACCESS_POLICY_REPR[rep['access_policy']]
        rep['data_readable'] = instance.is_readable_by_user(self.context['request'].user)
        if not instance.current_revision:
            # password has not been set yet
            rep['data_url'] = None
        else:
            rep['data_url'] = reverse(
                'api.secret-revision_data',
                kwargs={'pk': instance.current_revision.pk},
                request=self.context['request'],
            )
        rep['status'] = STATUS_REPR[rep['status']]
        return rep

    def update(self, instance, validated_data):
        data = None
        if 'password' in validated_data:
            data = validated_data.pop('password')
        instance._data = data
        return instance

    class Meta:
        model = Secret
        fields = (
            'access_policy',
            'allowed_groups',
            'allowed_users',
            'api_url',
            'created',
            'created_by',
            'current_revision',
            'data_readable',
            'data_url',
            'description',
            'last_read',
            'name',
            'needs_changing_on_leave',
            'password',
            'status',
            'url',
            'username',
        )
        read_only_fields = (
            'created',
            'last_read',
        )


class SecretDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Secret
    serializer_class = SecretSerializer

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.pre_delete(obj)
        obj.status = Secret.STATUS_DELETED
        obj.save()
        self.post_delete(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        obj = get_object_or_404(Secret, pk=self.kwargs['pk'])
        if not obj.is_visible_to_user(self.request.user):
            self.permission_denied(self.request)
        return obj

    def perform_update(self, serializer):
        instance = serializer.save()
        if hasattr(instance, '_data'):
            instance.set_data(self.request.user, instance._data)
            del instance._data


class SecretList(generics.ListCreateAPIView):
    model = Secret
    paginate_by = 50
    serializer_class = SecretSerializer

    def get_queryset(self):
        return Secret.get_all_visible_to_user(self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        if hasattr(instance, '_data'):
            instance.set_data(self.request.user, instance._data)
            del instance._data


class SecretRevisionDetail(generics.RetrieveAPIView):
    model = SecretRevision
    serializer_class = SecretRevisionSerializer

    def get_object(self):
        obj = get_object_or_404(SecretRevision, pk=self.kwargs['pk'])
        obj.secret.check_access(self.request.user)
        return obj


@api_view(['GET'])
def data_get(request, pk):
    obj = get_object_or_404(SecretRevision, pk=pk)
    obj.secret.check_access(request.user)
    return Response({'password': obj.secret.get_data(request.user)})
