from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title = "Death Cause Tagger",
    description = "API Documentation for Death Cause Tagger Service.",
)
api.auto_discover_controllers()
