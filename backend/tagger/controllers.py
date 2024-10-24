import pandas as pd

from typing import Iterable, List
from asgiref.sync import sync_to_async
from pydantic import BaseModel, RootModel

from django.db.models.query import QuerySet
from ninja_extra import api_controller, route

from ninja_jwt.authentication import AsyncJWTTokenUserAuth
from django.contrib.postgres.search import TrigramSimilarity

from periods.models import Period
from mappings.models import Mapping
from tagger.schemas import TagSchema, DeathCauseSchema, MappingSchema, PeriodSchema


@api_controller(
    prefix_or_class = "/tag",
    tags = ["tag"],
    permissions = [],
    auth = AsyncJWTTokenUserAuth(),
)
class TaggerController:
    """
    Tagger API Controller.
    """
    @route.post(exclude_none = True)
    async def tag_death_causes(self, data: RootModel[List[DeathCauseSchema]], sync: bool = False) -> List[TagSchema]:
        """
        Tag batch death causes.
        """
        data = pd.DataFrame(data.model_dump())
        data["description"] = data["description"].str.upper()
        mappings = Mapping.objects.filter(
            death_cause__description__in = data["description"].values,
            is_active = True,
            is_open = False
        ).select_related("code", "death_cause")

        schema = RootModel[List[MappingSchema]]
        df_mappings = await self.to_dataframe(mappings, schema)
        df_mappings = df_mappings.rename(columns = {"death_cause": "description"})

        data = data.merge(df_mappings, on = "description", how = "left")
        periods = Period.objects.filter(
            code_input__description__in = df_mappings["code"].values,
            is_active = True,
        )
        df_periods = await self.to_dataframe(periods, schema = RootModel[List[PeriodSchema]])

        data = data.merge(df_periods, on = "code", how = "left")
        data["code"] = data.apply(self.account_period, axis = 1)
        mappings = Mapping.objects.filter(
            code__description__in = data["code"].values,
            is_option = True,
            is_active = True,
            is_open = False,
        )

        df_tags = await self.to_dataframe(mappings, schema)
        df_tags["tag"] = df_tags.to_dict("records")

        data = data.merge(df_tags, on = "code", how = "left")
        missing_tag = data["tag"].isna()

        if missing_tag.sum() > 0:
            options_all = []
            for record in data[missing_tag].itertuples():
                mappings = Mapping.objects.filter(is_active = True, is_open = False) \
                                          .annotate(score = TrigramSimilarity(
                                              "death_cause__description", record.description)) \
                                          .order_by("-score") \
                                          .select_related("code") \
                                          [:100]
                options = await self.retrieve_options(mappings)
                options_all.append({
                    "description": record.description, "period": record.period, "options": options
                })
            
            df_options = pd.DataFrame(options_all)
            data = data.merge(df_options, on = ["description", "period"], how = "left")

        return data.replace({pd.NA: None}).to_dict("records")

    @staticmethod
    @sync_to_async
    def retrieve_options(mappings: Iterable[Mapping]) -> List[Mapping]:
        """
        Retrieve option mappings with scores.

        Args:
            mappings (Iterable[Mapping]): Top N most similar mappings to query.

        Returns:
            List[Mapping]: Option mappings.
        """
        options = []
        for mapping in mappings:
            option = mapping.code.mappings.get(
                is_active = True,
                is_option = True,
                is_open = False
            )
            if option not in options:
                options.append(option)

            if len(options) == 5:
                return options
        return options

    @staticmethod
    @sync_to_async
    def to_dataframe(queryset: QuerySet, schema: BaseModel) -> pd.DataFrame:
        """
        Transform QuerySet to dataframe.

        Args:
            queryset (QuerySet): QuerySet to transform to dataframe.
            schema (BaseModel): Schema to transform QuerySet to pydantic model object.

        Returns:
            pd.DataFrame: QuerySet dataframe.
        """
        obj = schema(list(queryset))
        return pd.DataFrame(obj.model_dump())

    @staticmethod
    def account_period(record: pd.Series) -> str:
        """
        Retrieve code based on period.

        Args:
            record (pd.Series): Dataframe record.

        Returns:
            str: Code corresponding to period.
        """
        if not isinstance(record.code, str):
            return record.code
        
        if record.period < record.threshold:
            return record.code_below
        
        elif record.period == record.threshold:
            return record.code_equal
        
        else:
            return record.code_above
