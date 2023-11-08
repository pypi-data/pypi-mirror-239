from .language_map import language_map


def create_code_cosmo(language):
    # Case in-sensitive
    language = language.lower()

    try:
        CodeCosmo = language_map[language]
        return CodeCosmo()
    except KeyError:
        raise ValueError(f"Unknown or unsupported language: {language}")
