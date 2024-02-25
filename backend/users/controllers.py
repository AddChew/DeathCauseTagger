from asgiref.sync import sync_to_async

from ninja_extra.permissions import AllowAny
from ninja_extra import api_controller, http_post
from ninja_jwt.controller import (
    AsyncTokenObtainPairController,
    AsyncTokenVerificationController,
    AsyncTokenBlackListController,
)

from users.schemas import RegisterTokenObtainPairInputSchema


class AsyncTokenObtainPairController(AsyncTokenObtainPairController):
    """
    NinjaJWT Async Token controller mixin for obtaining and refreshing tokens.
    """
    @http_post(
        "/register",
        response=RegisterTokenObtainPairInputSchema.get_response_schema(),
        url_name="token_register",
    )
    async def register_user(self, user_token: RegisterTokenObtainPairInputSchema):
        """
        Register user.
        """
        await sync_to_async(user_token.check_user_authentication_rule)()
        return user_token.to_response_schema()


@api_controller("/token", permissions=[AllowAny], tags=["token"], auth=None)
class AsyncNinjaJWTDefaultController(
    AsyncTokenVerificationController,
    AsyncTokenObtainPairController,
    AsyncTokenBlackListController,
    ):
    """
    NinjaJWT Async Default controller for obtaining and refreshing tokens.
    """
    auto_import = True
