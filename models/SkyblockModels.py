from pydantic import BaseModel, Field, AfterValidator, AliasChoices, AwareDatetime, AliasPath
from typing import Annotated, Optional, Union
import re


class Perk(BaseModel):
	name: str
	description: Annotated[str, AfterValidator(lambda x: re.sub(r'§.', '', x))]
	is_minister_perk: Annotated[Optional[bool], Field(alias='minister', exclude_if=lambda x: x is None)] = None

class Mayor(BaseModel):
	name: str
	spec: Annotated[str, Field(alias='key')]
	perks: Annotated[Union[list[Perk], Perk], Field(validation_alias=AliasChoices('perks', 'perk'))]
	votes: Annotated[Optional[int], Field(exclude_if=lambda x: x is None)] = None

class Election(BaseModel):
	year:  int
	candidates: list[Mayor]

class CurrentMayor(Mayor):
	minister: Mayor
	election: Election

class MayoralResponse(BaseModel):
	current_election: Annotated[Optional[Election], Field(alias='current')] = None
	current_mayor: Annotated[CurrentMayor, Field(alias='mayor')]
	last_updated: Annotated[AwareDatetime, Field(alias='lastUpdated')]


class Summary(BaseModel):
	amount: int
	price_per_unit: Annotated[float, Field(alias='pricePerUnit')]
	orders: int

class QuickStatus(BaseModel):
	product_id: Annotated[str, Field(alias='productId')]
	sell_price: Annotated[float, Field(alias='sellPrice')]
	sell_volume: Annotated[int, Field(alias='sellVolume')]
	sell_moving_week: Annotated[int, Field(alias='sellMovingWeek')]
	sell_orders: Annotated[int, Field(alias='sellOrders')]
	buy_price: Annotated[float, Field(alias='buyPrice')]
	buy_volume: Annotated[int, Field(alias='buyVolume')]
	buy_moving_week: Annotated[int, Field(alias='buyMovingWeek')]
	buy_orders: Annotated[int, Field(alias='buyOrders')]

class BazaarResponse(BaseModel):
	product_id: AwareDatetime
	sell_summary: list[Summary]
	buy_summary: list[Summary]
	quick_status: QuickStatus

