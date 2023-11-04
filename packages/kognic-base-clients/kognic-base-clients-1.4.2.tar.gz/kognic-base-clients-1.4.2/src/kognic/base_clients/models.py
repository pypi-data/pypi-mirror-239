from typing import Dict, Optional, Union

from pydantic import BaseModel, ConfigDict

try:
    from pydantic.alias_generators import to_camel

    class BaseSerializer(BaseModel):
        model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel, from_attributes=True)

        @classmethod
        def from_json(cls, js: Dict):
            return cls.model_validate(js)

        def to_dict(self, by_alias=True) -> Dict:
            return self.model_dump(exclude_none=True, by_alias=by_alias)

except ImportError:
    # We are on pydantic < 2
    import warnings

    from humps import camelize as to_camel

    warnings.warn(
        "Support for pydantic<2 has been deprecated and will be removed in the next major version. Please update to pydantic>2",
        DeprecationWarning,
    )

    class BaseSerializer(BaseModel):
        @classmethod
        def from_json(cls, js: Dict):
            return cls.parse_obj(js)

        def to_dict(self, by_alias=True) -> Dict:
            return self.dict(exclude_none=True, by_alias=by_alias)

        class Config:
            alias_generator = to_camel
            allow_population_by_field_name = True
            orm_mode = True


CursorIdType = Union[int, str]


class PageMetadata(BaseSerializer):
    next_cursor_id: Optional[CursorIdType]


class PaginatedResponse(BaseSerializer):
    data: Union[dict, list]
    metadata: PageMetadata
