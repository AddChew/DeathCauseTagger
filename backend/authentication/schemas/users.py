from typing import Dict, Type, cast
from pydantic import model_validator

from ninja import ModelSchema, Schema
from ninja.schema import DjangoGetter

from ninja_extra import status
from ninja_extra.exceptions import APIException

from ninja_jwt.settings import api_settings
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.exceptions import DetailDictMixin, ValidationError
from ninja_jwt.schema import TokenInputSchemaMixin, TokenObtainPairOutputSchema

from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AbstractUser, update_last_login


User = get_user_model()
user_name_field = User.USERNAME_FIELD


class RegistrationFailed(DetailDictMixin, APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Failed to register user.")
    default_code = "register_fail"


class RegisterTokenInputSchemaMixin(TokenInputSchemaMixin):
    _default_error_messages = {
        "existing_user": _("Username already exists"),
        "no_active_account": _("No active account found with the given credentials")
    }

    @classmethod
    def validate_values(cls, values: Dict) -> Dict:
        if user_name_field not in values and "password" not in values:
            raise ValidationError(
                {
                    user_name_field: f"{user_name_field} is required",
                    "password": "password is required",
                }
            )

        if not values.get(user_name_field):
            raise ValidationError(
                {user_name_field: f"{user_name_field} is required"}
            )

        if not values.get("password"):
            raise ValidationError({"password": "password is required"})
        
        try:
            User.objects.create_user(**values)
            _user = authenticate(**values)
            cls._user = _user

        except IntegrityError:
            raise RegistrationFailed(
                cls._default_error_messages["existing_user"],
            )        

        return values


class RegisterTokenObtainInputSchemaBase(ModelSchema, RegisterTokenInputSchemaMixin):
    class Config:
        # extra = "allow"
        model = get_user_model()
        model_fields = ["password", user_name_field]

    @model_validator(mode="before")
    def validate_inputs(cls, values: DjangoGetter) -> DjangoGetter:
        input_values = values._obj
        if isinstance(input_values, dict):
            values._obj.update(cls.validate_values(input_values))
            return values
        return values

    @model_validator(mode="after")
    def post_validate(cls, values: Dict) -> dict:
        return cls.post_validate_schema(values)

    @classmethod
    def post_validate_schema(cls, values: Dict) -> dict:
        """
        This is a post validate process which is common for any token generating schema.
        :param values:
        :return:
        """
        # get_token can return values that wants to apply to `OutputSchema`

        data = cls.get_token(cls._user)

        if not isinstance(data, dict):
            raise Exception("`get_token` must return a `typing.Dict` type.")

        # a workaround for extra attributes since adding extra=allow in modelconfig adds `addition_props`
        # field to the schema
        values.__dict__.update(token_data=data)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, cls._user)

        return values

    def get_response_schema_init_kwargs(self) -> dict:
        return dict(
            self.dict(exclude={"password"}), **self.__dict__.get("token_data", {})
        )

    def to_response_schema(self):
        _schema_type = self.get_response_schema()
        return _schema_type(**self.get_response_schema_init_kwargs())
    

class RegisterTokenObtainPairInputSchema(RegisterTokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return TokenObtainPairOutputSchema

    @classmethod
    def get_token(cls, user: AbstractUser) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        refresh = cast(RefreshToken, refresh)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        return values