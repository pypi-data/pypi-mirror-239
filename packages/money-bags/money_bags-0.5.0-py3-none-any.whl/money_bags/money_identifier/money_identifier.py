from money_bags.constants.country_constants import (
    ALL_COUNTRIES,
    UNKNOWN_COUNTRY,
    UNKNOWN_ISO,
    AFRICAN_COUNTRIES,
    NORTH_AMERICAN_COUNTRIES,
    ASIAN_COUNTRIES,
    OCEANIA_COUNTRIES,
    EUROPEAN_COUNTRIES,
    APAC_COUNTRY_REGIONS,
    EUROPEAN_COUNTRY_KEYS,
    EMERGING_MARKET_INSTRUMENT_GROUP,
    XS_COUNTRY_ISO_CODES,
    EMERGING_MARKETS,
)
from money_bags.constants.currency_constants import Currencies
from money_bags.constants.general_constants import (
    CURRENCY_STRING,
    COUNTRY_NAME,
    EMPTY_STRING,
)
from money_bags.constants.iso_details import ISO_DETAILS
from typing import Optional

from money_bags.constants.zone_constants import (
    RegionIssuance,
    NON_EURO_COUNTRIES,
    NON_EUROZONE_INSTRUMENT_GROUP,
    XS_COUNTRY_CODES,
)


class MoneyIdentifier:
    def __init__(
        self,
        currency: Optional[str] = EMPTY_STRING,
        issuing_country: Optional[str] = EMPTY_STRING,
        country_iso_code: Optional[str] = EMPTY_STRING,
        instrument_group: Optional[str] = EMPTY_STRING,
    ):
        self.currency = currency
        self.issuing_country = issuing_country
        self.country_iso_code = country_iso_code
        self.country_details = self.gather_country_details()
        self.zone_of_issuance = EMPTY_STRING
        self.instrument_group = instrument_group

    def find_country_from_iso_code(self) -> str:
        if self.country_details:
            return self.country_details[COUNTRY_NAME]
        return UNKNOWN_COUNTRY

    def find_iso_from_country(self) -> str:
        for region in ALL_COUNTRIES:
            if self.issuing_country in region.values():
                return next(
                    key
                    for key, value in region.items()
                    if value == self.issuing_country
                )
        return UNKNOWN_ISO

    def gather_country_details(self) -> dict:
        return ISO_DETAILS.get(self.country_iso_code)

    def find_currency_from_iso(self) -> str:
        if self.country_details:
            return self.country_details[CURRENCY_STRING]
        return UNKNOWN_ISO

    def is_apac_iso(self) -> bool:
        return (
            self.country_iso_code in APAC_COUNTRY_REGIONS
            or self.currency in Currencies.APAC.value
        )

    def is_eurozone_iso(self) -> bool:
        return (
            self.country_iso_code in EUROPEAN_COUNTRY_KEYS
            and self.country_iso_code not in NON_EURO_COUNTRIES
            or self.currency in Currencies.EURO.value
        ) and (
            self.instrument_group not in NON_EUROZONE_INSTRUMENT_GROUP,
            self.country_iso_code not in EMERGING_MARKETS["CEEMA"],
        )

    def is_non_eurozone_iso(self) -> bool:
        return (
            self.country_iso_code in EUROPEAN_COUNTRY_KEYS
            and self.country_iso_code in NON_EURO_COUNTRIES
        ) and (self.instrument_group not in NON_EUROZONE_INSTRUMENT_GROUP)

    def is_cross_zone_iso(self) -> bool:
        return self.instrument_group != EMPTY_STRING and (
            self.instrument_group in NON_EUROZONE_INSTRUMENT_GROUP
            or self.country_iso_code in XS_COUNTRY_CODES
        )

    def is_north_american_iso(self) -> bool:
        return self.country_iso_code in NORTH_AMERICAN_COUNTRIES

    def find_emerging_market(self) -> str:
        if (
            self.instrument_group in EMERGING_MARKET_INSTRUMENT_GROUP
            or self.country_iso_code in XS_COUNTRY_ISO_CODES
        ):
            for region in EMERGING_MARKETS.keys():
                if self.country_iso_code in EMERGING_MARKETS[region]:
                    return region
            return RegionIssuance.CROSS_ZONE.value
        return EMPTY_STRING

    def is_emerging_market(self) -> bool:
        return self.find_emerging_market() != EMPTY_STRING

    def find_zone_of_issuance(self) -> str:
        zone_conditions = [
            (self.is_north_american_iso(), RegionIssuance.NORTH_AMERICA.value),
            (self.is_eurozone_iso(), RegionIssuance.EUROZONE.value),
            (self.is_non_eurozone_iso(), RegionIssuance.NON_EUROZONE.value),
            (self.is_emerging_market(), self.find_emerging_market()),
            (self.is_apac_iso(), RegionIssuance.APAC.value),
            (self.is_cross_zone_iso(), RegionIssuance.CROSS_ZONE.value),
        ]

        for condition, result in zone_conditions:
            if condition:
                return result

        return RegionIssuance.UNKNOWN.value
