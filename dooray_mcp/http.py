"""HTTP helpers for the Dooray API."""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = "https://api.dooray.com"


def _get_token() -> str:
    token = os.environ.get("DOORAY_API_TOKEN")
    if not token:
        raise RuntimeError("DOORAY_API_TOKEN environment variable is not set")
    return token


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"dooray-api {_get_token()}",
        "Content-Type": "application/json",
    }


def _unwrap(resp: httpx.Response) -> Any:
    """Raise on HTTP or Dooray-level errors, return the 'result' payload."""
    resp.raise_for_status()
    data = resp.json()
    header = data.get("header", {})
    if not header.get("isSuccessful", False):
        code = header.get("resultCode", "?")
        msg = header.get("resultMessage", "unknown error")
        raise RuntimeError(f"Dooray API error {code}: {msg}")
    return data.get("result")


async def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers(), timeout=30) as client:
        resp = await client.get(path, params=params)
        return _unwrap(resp)


async def _post(path: str, body: dict[str, Any]) -> Any:
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers(), timeout=30) as client:
        resp = await client.post(path, json=body)
        return _unwrap(resp)


async def _put(path: str, body: dict[str, Any] | None = None) -> Any:
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers(), timeout=30) as client:
        resp = await client.put(path, json=body or {})
        return _unwrap(resp)


async def _delete(path: str) -> Any:
    async with httpx.AsyncClient(base_url=BASE_URL, headers=_headers(), timeout=30) as client:
        resp = await client.delete(path)
        return _unwrap(resp)
