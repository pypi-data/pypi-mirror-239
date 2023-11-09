from abc import ABC, abstractmethod
import json
import operator
import os
from logging import Logger
from multiprocessing.pool import ThreadPool
from typing import Dict, List, Optional, Any

from botocore.client import BaseClient
from lambda_thread_pool import LambdaThreadPool

from .constants import OS_PRODUCT_DESCRIPTION_MAP, REGIONS
from .exceptions import NoAvailabilityZonesError, InvalidStrategyError
from .types import (
    Ec2Price,
    Ec2PriceLoop,
    FinalSpotPriceStrategy,
    InstanceTypeInfo,
    InstanceTypeResponse,
    ProductDescription,
    UsageClass,
    InstanceType,
)


class SortStrategy(ABC):
    """Base class for sort strategies."""

    def __init__(
        self,
        region: str,
        pricing_client: BaseClient,
        ec2_client: BaseClient,
        logger: Logger,
        spot_price_history_concurrency: int = 10,
    ) -> None:
        self._logger = logger
        self._region = region
        self._pricing_client = pricing_client
        self._ec2_client = ec2_client
        self._spot_price_history_concurrency = spot_price_history_concurrency

    @abstractmethod
    def sort(
        self,
        instances: List[InstanceTypeInfo],
        product_description: ProductDescription,
        availability_zones: Optional[List[str]],
        final_spot_price_strategy: Optional[FinalSpotPriceStrategy],
    ) -> InstanceTypeResponse:
        pass


class SortOnDemandStrategy(SortStrategy):
    """Sort strategy for On-Demand EC2 instances."""

    def sort(
        self,
        instances: List[InstanceTypeInfo],
        product_description: ProductDescription,
        availability_zones: Optional[List[str]],
        final_spot_price_strategy: Optional[FinalSpotPriceStrategy],
    ) -> InstanceTypeResponse:
        operating_system = self._get_operating_system_by_product_description(
            product_description
        )
        ec2_prices = self._get_ec2_price(operating_system)
        ec2_instances = []

        for instance_info in instances:
            instance_type = instance_info["InstanceType"]
            if ec2_prices.get(instance_type):
                ec2_instances.append(
                    self._format_instance_entry(instance_info, ec2_prices)
                )
            else:
                self._logger.info(
                    f"The price for the {instance_type} instance type not found"
                )

        ec2_instances.sort(key=operator.itemgetter("price"))
        return ec2_instances

    def _format_instance_entry(
        self, instance_info: Dict[str, Any], ec2_prices: Dict[str, Ec2Price]
    ) -> InstanceType:
        # instance_info: Dict[str, Any], ec2_prices: Dict[str, Ec2Price]x
        instance_type = instance_info["InstanceType"]
        price_info = ec2_prices[instance_type]

        entry: InstanceType = {
            "instance_type": instance_type,
            "price": price_info["instance_price"],
            "vcpu": instance_info["VCpuInfo"]["DefaultVCpus"],
            "memory_gb": instance_info["MemoryInfo"]["SizeInMiB"] // 1024,
            "network_performance": instance_info["NetworkInfo"]["NetworkPerformance"],
            "storage": instance_info["InstanceStorageInfo"]["Disks"]
            if instance_info.get("InstanceStorageInfo")
            else "EBS Only",
        }

        if gpu_info := instance_info.get("GpuInfo"):
            entry["gpu_memory_gb"] = gpu_info["TotalGpuMemoryInMiB"] // 1024

        return entry

    @staticmethod
    def _get_operating_system_by_product_description(
        product_description: ProductDescription,
    ) -> str:
        return OS_PRODUCT_DESCRIPTION_MAP[product_description]

    @staticmethod
    def _parse_price_details(price: str) -> Ec2Price:
        details = json.loads(price)
        pricedimensions = next(iter(details["terms"]["OnDemand"].values()))[
            "priceDimensions"
        ]
        pricing_details = next(iter(pricedimensions.values()))
        instance_price = float(pricing_details["pricePerUnit"]["USD"])
        return {
            "instance_type": details["product"]["attributes"]["instanceType"],
            "vcpu": int(details["product"]["attributes"]["vcpu"]),
            "memory": float(details["product"]["attributes"]["memory"].split(" ")[0]),
            "os": details["product"]["attributes"]["operatingSystem"],
            "instance_price": instance_price,
        }

    def _get_ec2_price(self, operating_system: str) -> Dict[str, Ec2Price]:
        filters = [
            {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
            {
                "Type": "TERM_MATCH",
                "Field": "productFamily",
                "Value": "Compute Instance",
            },
            {"Type": "TERM_MATCH", "Field": "termType", "Value": "OnDemand"},
            {"Type": "TERM_MATCH", "Field": "location", "Value": REGIONS[self._region]},
            {
                "Type": "TERM_MATCH",
                "Field": "licenseModel",
                "Value": "No License required",
            },
            {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
            {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
            {
                "Type": "TERM_MATCH",
                "Field": "operatingSystem",
                "Value": operating_system,
            },
        ]

        records: Dict[str, Ec2Price] = {}
        next_token = None

        while True:
            request_parameters = {
                "ServiceCode": "AmazonEC2",
                "Filters": filters,
            }

            if next_token:
                request_parameters["NextToken"] = next_token

            response = self._pricing_client.get_products(**request_parameters)
            price_list = response.get("PriceList", [])

            if not price_list:
                break

            for price in price_list:
                price_details = self._parse_price_details(price)
                if price_details["instance_price"] <= 0:
                    continue
                records[price_details["instance_type"]] = price_details

            next_token = response.get("NextToken")
            if not next_token:
                break

        return records


class SortSpotStrategy(SortStrategy):
    """Sort strategy for Spot EC2 instances."""

    def __init__(
        self,
        region: str,
        pricing_client: BaseClient,
        ec2_client: BaseClient,
        logger: Logger,
        spot_price_history_concurrency: int,
    ):
        super().__init__(
            region, pricing_client, ec2_client, logger, spot_price_history_concurrency
        )
        self._pool_executor = self._get_thread_pool_executor()

    def sort(
        self,
        filtered_instances: List[InstanceTypeInfo],
        product_description: ProductDescription,
        availability_zones: Optional[List[str]],
        final_spot_price_strategy: FinalSpotPriceStrategy,
    ) -> InstanceTypeResponse:
        with self._pool_executor(self._spot_price_history_concurrency) as pool:
            async_results = [
                pool.apply_async(
                    self._ec2_instance_price_loop,
                    (
                        ec2_instance,
                        product_description,
                        availability_zones,
                        final_spot_price_strategy,
                    ),
                )
                for ec2_instance in filtered_instances
            ]

            ec2_instances = [result.get() for result in async_results if result.get()]

        ec2_instances.sort(key=operator.itemgetter("price"))

        return [
            self._enrich_instance_data(ec2_instance) for ec2_instance in ec2_instances
        ]

    @staticmethod
    def _enrich_instance_data(ec2_instance: Ec2PriceLoop) -> InstanceType:
        instance_info: InstanceTypeInfo = ec2_instance["ec2_instance"]
        entry: InstanceType = {
            "instance_type": instance_info["InstanceType"],
            "price": ec2_instance["price"],
            "az_price": ec2_instance["az_price"],
            "vcpu": instance_info["VCpuInfo"]["DefaultVCpus"],
            "memory_gb": instance_info["MemoryInfo"]["SizeInMiB"] // 1024,
            "network_performance": instance_info["NetworkInfo"]["NetworkPerformance"],
            "storage": instance_info["InstanceStorageInfo"]["Disks"]
            if instance_info.get("InstanceStorageInfo")
            else "EBS Only",
        }

        if gpu_info := instance_info.get("GpuInfo"):
            entry["gpu_memory_gb"] = gpu_info["TotalGpuMemoryInMiB"] // 1024

        if interruption_frequency := instance_info.get("InterruptionFrequency"):
            entry["interruption_frequency"] = interruption_frequency

        return entry

    @staticmethod
    def _get_thread_pool_executor() -> Any:
        return (
            ThreadPool
            if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is None
            else LambdaThreadPool
        )

    def _ec2_instance_price_loop(
        self,
        ec2_instance: InstanceTypeInfo,
        product_description: ProductDescription,
        availability_zones: Optional[List[str]],
        final_spot_price_strategy: FinalSpotPriceStrategy,
    ) -> Optional[Ec2PriceLoop]:
        instance_type = ec2_instance["InstanceType"]

        filters = [{"Name": "product-description", "Values": [product_description]}]

        if availability_zones:
            filters.append({"Name": "availability-zone", "Values": availability_zones})

        response = self._ec2_client.describe_spot_price_history(
            InstanceTypes=[instance_type], Filters=filters
        )

        if len(response["SpotPriceHistory"]) == 0:
            return None

        history_events = response["SpotPriceHistory"]

        az_price = {}

        if availability_zones is None:
            availability_zones = self._get_all_availability_zones_for_region()

        for availability_zone in availability_zones:
            for history_event in history_events:
                az = history_event["AvailabilityZone"]
                if availability_zone == az:
                    az_price[availability_zone] = float(history_event["SpotPrice"])
                    break

        strategy = final_spot_price_strategy

        values = az_price.values()

        if strategy == "average":
            spot_price = sum(values) / len(values)
        elif strategy == "max":
            spot_price = max(values)
        elif strategy == "min":
            spot_price = min(values)
        else:
            raise InvalidStrategyError(strategy)

        return {"price": spot_price, "ec2_instance": ec2_instance, "az_price": az_price}

    def _get_all_availability_zones_for_region(self) -> List[str]:
        """
        Retrieves all availability zones for the configured AWS region.

        Returns:
            List[str]: A list of availability zone names.

        Raises:
            Exception: If no availability zones are found for the region.
        """
        # Check if the availability zones have already been retrieved and cached.
        if not hasattr(self, "_availability_zones_cache"):
            response = self._ec2_client.describe_availability_zones()
            if availability_zones := [
                zone["ZoneName"] for zone in response.get("AvailabilityZones", [])
            ]:
                self._availability_zones_cache = availability_zones

            else:
                raise NoAvailabilityZonesError(self._region)

        return self._availability_zones_cache


class SortStrategyFactory:
    @staticmethod
    def get_strategy(
        usage_class: UsageClass,
        region: str,
        pricing_client: BaseClient,
        ec2_client: BaseClient,
        logger: Logger,
        spot_price_history_concurrency: int,
    ) -> SortStrategy:
        strategies = {
            UsageClass.ON_DEMAND.value: SortOnDemandStrategy,
            UsageClass.SPOT.value: SortSpotStrategy,
        }
        if usage_class in strategies:
            return strategies[usage_class](
                region,
                pricing_client,
                ec2_client,
                logger,
                spot_price_history_concurrency,
            )
        else:
            raise ValueError(f"Unsupported usage class: {usage_class}")
