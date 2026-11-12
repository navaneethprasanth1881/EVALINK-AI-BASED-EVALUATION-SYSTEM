"""
Module 1 - Image Quality Assessment

Configuration file.

Stores all threshold values used throughout the
quality assessment module.

Changing any quality criteria only requires
editing this file.
"""


class QualityConfig:

    #########################################################
    # PDF SETTINGS
    #########################################################

    # DPI used when converting PDF pages to images
    PDF_DPI = 300

    #########################################################
    # BLUR DETECTION
    #########################################################

    # Variance of Laplacian threshold
    BLUR_THRESHOLD = 100.0

    #########################################################
    # BRIGHTNESS
    #########################################################

    # Mean grayscale intensity

    MIN_BRIGHTNESS = 70
    MAX_BRIGHTNESS = 190

    #########################################################
    # CONTRAST
    #########################################################

    # Standard deviation of grayscale intensity

    MIN_CONTRAST = 40

    #########################################################
    # NOISE
    #########################################################

    # Estimated using standard deviation
    # of image residual after denoising

    MAX_NOISE = 30

    #########################################################
    # SHADOW DETECTION
    #########################################################

    # Percentage of dark pixels allowed

    MAX_SHADOW_PERCENTAGE = 25

    #########################################################
    # RESOLUTION
    #########################################################

    MIN_WIDTH = 1200
    MIN_HEIGHT = 1600

    #########################################################
    # OUTPUT
    #########################################################

    OUTPUT_FOLDER = "output/module_1"

    SAVE_VISUALIZATIONS = True

    SAVE_REPORT = True