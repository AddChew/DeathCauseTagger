from typing import List

from ninja_extra import api_controller, http_get, http_post, http_put, ControllerBase
from ninja_jwt.authentication import AsyncJWTTokenUserAuth

from states.models import State
from users.models import User
from states.schemas import Mappings


@api_controller(
    prefix_or_class = "/states",
    tags = ["states"],
    permissions = [],
    auth = AsyncJWTTokenUserAuth(),
)
class StateController(ControllerBase):
    """
    State API Controller.
    """
    queryset = State.objects.all()

    @http_post()
    async def create_state(self, data: Mappings):
        # state = State.objects.create(**data.model_dump(), created_by, updated_by, is_active_updated_by)
        user = self.context.request.user
        print(user.id)
        # self.context.request.user

        pass



    # @http_get()
    # async def read_states(self, created_by = None) -> List[CategorySchema]:
    #     """
    #     Read states.
    #     """
    #     pass

# TODO: validate data json in controllers, to do in client side as well

# data = {
#     "mappings": [
#         {
#             "description": "death cause 1",
#             "duration": 365, 
#             "match": {
#                 "description": "match",
#                 "code": "code",
#             },
#             "options": [
#                 {
#                     "description": "match",
#                     "code": "code",
#                     "score": 1,
#                  }
#             ]
#         }
#     ],
#     "page": 0,
# }
# Mappings.model_validate(data)