from ninja_extra import NinjaExtraAPI
from tagger.controllers.categories import CategoryController
from ninja_jwt.controller import AsyncNinjaJWTDefaultController

api = NinjaExtraAPI(
    title = "Death Cause Tagger",
    description = "API Documentation for Death Cause Tagger Service.",
)
api.register_controllers(
    AsyncNinjaJWTDefaultController,
    CategoryController,
)