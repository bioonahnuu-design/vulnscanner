import ipaddress
import os
import socket
from urllib.parse import urlsplit


class TargetValidationError(ValueError):
    """Raised when a scan target is invalid or not permitted."""


def normalize_target(raw_target):
    """
    Convert a URL, hostname, or IP input into a clean hostname.

    Examples:
        https://example.com/login -> example.com
        example.com/path          -> example.com
        203.0.113.10              -> 203.0.113.10
    """

    target = str(raw_target or "").strip()

    if not target:
        raise TargetValidationError("Target is required.")

    if len(target) > 253:
        raise TargetValidationError("Target is too long.")

    parsed = urlsplit(
        target if "://" in target else f"//{target}"
    )

    if parsed.username or parsed.password:
        raise TargetValidationError(
            "Credentials are not allowed in the target."
        )

    try:
        if parsed.port is not None:
            raise TargetValidationError(
                "Custom ports are not supported."
            )
    except ValueError as error:
        raise TargetValidationError(
            "Target contains an invalid port."
        ) from error

    hostname = parsed.hostname

    if not hostname:
        raise TargetValidationError(
            "Enter a valid hostname or IPv4 address."
        )

    hostname = hostname.rstrip(".").lower()

    if any(character.isspace() for character in hostname):
        raise TargetValidationError(
            "Target must not contain spaces."
        )

    return hostname


def resolve_target(target):
    """
    Resolve the target to IPv4 and reject private/local addresses by default.

    Private targets can only be enabled locally with:
        ALLOW_PRIVATE_TARGETS=true
    """

    allow_private = (
        os.getenv("ALLOW_PRIVATE_TARGETS", "false").lower()
        == "true"
    )

    try:
        address_info = socket.getaddrinfo(
            target,
            None,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as error:
        raise TargetValidationError(
            "Target could not be resolved."
        ) from error

    addresses = sorted(
        {item[4][0] for item in address_info}
    )

    if not addresses:
        raise TargetValidationError(
            "Target does not have a valid IPv4 address."
        )

    for address in addresses:
        parsed_ip = ipaddress.ip_address(address)

        if not allow_private and not parsed_ip.is_global:
            raise TargetValidationError(
                "Private, local, loopback, and reserved targets are blocked."
            )

    return addresses[0]


def validate_target(raw_target):
    """Normalize and resolve a target in one call."""

    target = normalize_target(raw_target)
    ip_address = resolve_target(target)

    return target, ip_address