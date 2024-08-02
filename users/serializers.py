from rest_framework import serializers
from django.contrib.auth.models import Group

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')
    groups = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_active', 'groups']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.groups.set(groups)
        return user

    def update(self, instance, validated_data):
        groups = validated_data.pop('groups', [])
        instance = super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        instance.groups.set(groups)
        return instance




