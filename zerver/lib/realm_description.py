from zerver.lib.cache import (
    cache_with_key,
    realm_rendered_description_cache_key,
    realm_text_description_cache_key,
)
from zerver.lib.html_to_text import html_to_text
from zerver.lib.markdown import markdown_convert
from zerver.models import Realm


@cache_with_key(realm_rendered_description_cache_key, timeout=3600 * 24 * 7)
def get_realm_rendered_description(realm: Realm) -> str:
    # Use cached rendered description if available
    if realm.rendered_description:
        return realm.rendered_description

    # Cache miss - render and store
    realm_description_raw = realm.description or "The coolest place in the universe."
    rendered_content = markdown_convert(
        realm_description_raw, message_realm=realm, no_previews=True
    ).rendered_content

    # Save the rendered description to database
    realm.rendered_description = rendered_content
    realm.save(update_fields=["rendered_description"])

    return rendered_content


@cache_with_key(realm_text_description_cache_key, timeout=3600 * 24 * 7)
def get_realm_text_description(realm: Realm) -> str:
    html_description = get_realm_rendered_description(realm)
    return html_to_text(html_description, {"p": " | ", "li": " * "})
