import logging
from typing import List, Literal, Optional, Union

from pydantic import (BaseModel, ConfigDict, Field, PositiveInt, StrictBool,
                      TypeAdapter, validator)

from .schema_utils import find_duplicates, is_sorted

log = logging.getLogger('Validation')

PROXIED_VALUES = Literal['false', 'true']
TYPES_VALUES = Literal['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'CAA', 'SRV', 'PTR',
                       'SOA', 'NS', 'DS', 'DNSKEY', 'LOC', 'NAPTR', 'SSHFP',
                       'SVCB', 'TSLA', 'URI', 'SPF']


# Same schema to validate tfplan.json, Cloudflare output and the csv file
class Record(BaseModel):
    # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = None
    name: str
    type: TYPES_VALUES
    value: str = Field(alias='content')
    ttl: PositiveInt
    proxied: Union[StrictBool, PROXIED_VALUES]

    @validator('name')
    def no_trailing_dot(cls, value):
        if value.strip().endswith('.'):
            raise ValueError('dns entry are not allowed to end with a "."')
        return value

    def get_uuid(self):
        return tuple(self.name, self.value)

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.type, self.value)


RecordList = TypeAdapter(List[Record])


def check_records(records):
    records = RecordList.validate_python(records)
    duplicates = list(find_duplicates(records, key=lambda x: x.name))
    if duplicates:
        log.warn(('There are duplicate entries,'
                  'be sure that it is what you want: {}').format(duplicates))
    if not is_sorted(records, key=lambda x: x.name):
        log.warn('Records are not sorted, please sort them')
    return records
