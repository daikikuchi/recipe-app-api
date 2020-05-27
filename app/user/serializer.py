from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        # fields that are converted to and from json when we make HTTP Post
        # retrive that in view and save it to model
        fields = ('email', 'password', 'name')
        # allow us to configure extra settings
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # print(validated_data,'validated_data')
        # {'email': 'test@gmail.com', 'password': 'password', 'name': 'Test'}
        return get_user_model().objects.create_user(**validated_data)

    # purpose of this is to make sure the password is set using set_password
    # Instance is model instance, user object, data is fields that are updated
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # remove password from the validated data
        password = validated_data.pop('password', None)
        # Update the rest of validated data
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # attrs is every field that make up serializer
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        # Whenever override validate, return attrs
        return attrs
