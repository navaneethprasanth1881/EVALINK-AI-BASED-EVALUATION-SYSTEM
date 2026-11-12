"""
Module 4 - Claude OCR

Configuration

Contains model, OCR, image, and output settings.

IMPORTANT:
The Anthropic API key is NOT stored here.
It should be provided through an environment variable.
"""


class ClaudeOCRConfig:

    # =========================================================
    # API SETTINGS
    # =========================================================

    # API key environment variable
    API_KEY_ENV = "ANTHROPIC_API_KEY"

    # Claude model
    #
    # Keep this configurable so that we can change the model
    # without modifying the OCR code.
    MODEL = "claude-sonnet-4-20250514"

    # Maximum output tokens
    MAX_TOKENS = 12000

    # Temperature
    #
    # OCR should be deterministic.
    TEMPERATURE = 0.0

    # =========================================================
    # OCR SETTINGS
    # =========================================================

    # Strict OCR mode
    STRICT_MODE = True

    # Do not evaluate answers
    ENABLE_EVALUATION = False

    # Allow minor spelling/grammar normalization
    ALLOW_MINOR_CORRECTION = True

    # Never add missing concepts or keywords
    ALLOW_KEYWORD_ADDITION = False

    # Ignore crossed-out / struck-through text
    IGNORE_STRUCK_TEXT = True

    # Preserve equations
    PRESERVE_EQUATIONS = True

    # Preserve figures
    PRESERVE_FIGURES = True

    # Detect continuation between pages
    DETECT_CONTINUATION = True

    # =========================================================
    # IMAGE SETTINGS
    # =========================================================

    # Maximum image dimension sent to Claude
    MAX_IMAGE_WIDTH = 1568
    MAX_IMAGE_HEIGHT = 1568

    # Minimum useful image dimension
    MIN_IMAGE_WIDTH = 200
    MIN_IMAGE_HEIGHT = 200

    # Supported image format
    IMAGE_FORMAT = "PNG"

    # =========================================================
    # PROCESSING SETTINGS
    # =========================================================

    # Process only pages identified by Module 3
    PROCESS_ANSWER_PAGES_ONLY = True

    # Process cover page separately
    PROCESS_COVER_PAGE = True

    # =========================================================
    # OUTPUT
    # =========================================================

    OUTPUT_FOLDER = "output/module_4"

    OCR_JSON_FILENAME = "ocr_result.json"

    OCR_RAW_FILENAME = "claude_raw_responses.json"

    SAVE_RAW_RESPONSE = True

    SAVE_OCR_JSON = True

    # =========================================================
    # RETRY SETTINGS
    # =========================================================

    MAX_RETRIES = 3

    RETRY_DELAY_SECONDS = 2

    # =========================================================
    # VALIDATION
    # =========================================================

    REQUIRE_JSON_RESPONSE = True

    REQUIRE_ANSWER_NUMBER = True

    REQUIRE_ANSWER_TEXT = True