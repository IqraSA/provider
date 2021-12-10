#
# Copyright 2021 Ocean Protocol Foundation
# SPDX-License-Identifier: Apache-2.0
#
import json
import logging

from flask.wrappers import Response
from ocean_provider.utils.url import is_url

logger = logging.getLogger(__name__)

STRIPPED_URL_MSG = "<URL stripped for security reasons>"


def service_unavailable(error, context, custom_logger=None):
    error = strip_and_replace_urls(str(error))

    text_items = []
    for key, value in context.items():
        value = value if isinstance(value, str) else json.dumps(value)
        text_items.append(key + "=" + value)

    logger_message = ",".join(text_items)
    custom_logger = custom_logger if custom_logger else logger
    custom_logger.error(f"error: {error}, payload: {logger_message}", exc_info=1)

    return Response(
        json.dumps({"error": str(error), "context": context}),
        503,
        headers={"content-type": "application/json"},
    )


def strip_and_replace_urls(err_str: str) -> str:
    tokens = []
    for token in err_str.split():
        tokens += [STRIPPED_URL_MSG] if is_url(token) else [token]
    return " ".join(tokens)