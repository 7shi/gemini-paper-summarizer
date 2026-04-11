import locale

# Mapping of full language names to language codes
lang_map = {
    "chinese": "zh",
    "english": "en",
    "esperanto": "eo",
    "french": "fr",
    "german": "de",
    "japanese": "ja",
    "korean": "ko",
    "spanish": "es",
}

# Available language codes (derived from lang_map values)
lang_codes = sorted(lang_map.values())

def init(language=None):
    """
    Select the appropriate language module based on user input or system locale.

    Args:
        language (str, optional): Explicitly specified language. Defaults to None.

    Returns:
        module: Selected language module (ja, en, eo, es, fr, de, zh, ko)
    """
    # Normalize language input
    normalized_lang = (language or locale.getlocale()[0] or "en").lower()

    # Select language module: check full name mappings, then language codes directly
    selected_lang = "en"
    for k, v in lang_map.items():
        if normalized_lang.startswith(k):
            selected_lang = v
            break
    else:
        for code in lang_codes:
            if normalized_lang.startswith(code):
                selected_lang = code
                break

    # Import the selected language module
    match selected_lang:
        case 'de':
            from . import de as lang_module
        case 'eo':
            from . import eo as lang_module
        case 'es':
            from . import es as lang_module
        case 'fr':
            from . import fr as lang_module
        case 'ja':
            from . import ja as lang_module
        case 'ko':
            from . import ko as lang_module
        case 'zh':
            from . import zh as lang_module
        case _:
            from . import en as lang_module

    return lang_module
