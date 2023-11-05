import typer
import asyncio
from rich import print


from .main import trydan_status, trydan_set

from ipaddress import ip_address

app = typer.Typer()


@app.command()
def status(ip: str) -> None:
    """Retrieve Trydan Status."""
    print("Connecting to %s", ip_address(ip))

    asyncio.run(trydan_status(ip))


@app.command()
def set(ip: str, keyword: str, value: str) -> None:
    """Set KeyWord value in Trydan."""
    print("Connecting to %s", ip_address(ip))

    asyncio.run(trydan_set(ip, keyword, value))
