from typing import Optional
import boto3
import click
import os
from boto3 import Session


class Context:
    __profile: str = ""
    __region: str = ""

    def __init__(
        self, debug: bool, profile: Optional[str], region: Optional[str]
    ) -> None:
        self.__debug = debug
        self.profile = profile or ""
        self.region = region or ""

    @property
    def session(self) -> Session:
        if self.profile:
            return boto3.session.Session(profile_name=self.profile)

        return boto3.session.Session(region_name=self.region)

    @property
    def profile(self) -> str:
        return self.__profile

    @profile.setter
    def profile(self, value: str) -> None:
        if value:
            self.debug(f"AWS profile: {value} is used for this session")
        self.__profile = value

    @property
    def region(self) -> str:
        return self.__region

    @region.setter
    def region(self, value: str) -> None:
        if value:
            self.debug(f"AWS region: {value} is used for this session")
        self.__region = value

    def debug(self, message: str) -> None:
        if self.__debug:
            click.echo(message)

    @staticmethod
    def info(message: str) -> None:
        click.echo(message)
