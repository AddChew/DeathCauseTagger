from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, user_logged_in


class RegisterSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only = True, style = {'input_type': 'password'})
    password2 = serializers.CharField(write_only = True, style = {'input_type': 'password'})

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        validated_data['password'] = validated_data['password1']
        validated_data.pop('password1')
        validated_data.pop('password2')
        return self.Meta.model.objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields= (
            'username', 'password1', 'password2'
        )
        read_only_fields = ('id',)


class LoginSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        user_logged_in.send(sender = get_user_model(), user = user)
        token = super().get_token(user)
        user_data = RegisterSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key]= value
        return token