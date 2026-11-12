"""
Module 2 - Image Preprocessing

Configuration File

Contains all preprocessing parameters.
Changing preprocessing behavior only
requires editing this file.
"""


class PreprocessingConfig:

    ###########################################################
    # GENERAL
    ###########################################################

    ENABLE_DESKEW = True

    ENABLE_DENOISE = True

    ENABLE_CONTRAST = True

    ENABLE_SHADOW_REMOVAL = True

    ENABLE_THRESHOLDING = True

    ###########################################################
    # DENOISING
    ###########################################################

    # OpenCV Fast Non Local Means

    DENOISE_H = 10

    DENOISE_TEMPLATE_WINDOW = 7

    DENOISE_SEARCH_WINDOW = 21

    ###########################################################
    # CONTRAST
    ###########################################################

    # CLAHE Parameters

    CLAHE_CLIP_LIMIT = 2.0

    CLAHE_GRID_SIZE = (8, 8)

    ###########################################################
    # SHADOW REMOVAL
    ###########################################################

    SHADOW_BLUR_KERNEL = 21

    ###########################################################
    # THRESHOLDING
    ###########################################################

    THRESHOLD_METHOD = "adaptive"
    # adaptive / otsu

    ADAPTIVE_BLOCK_SIZE = 21

    ADAPTIVE_C = 10

    ###########################################################
    # DESKEW
    ###########################################################

    MAX_DESKEW_ANGLE = 15

    ###########################################################
    # OUTPUT
    ###########################################################

    OUTPUT_FOLDER = "output/module_2"

    SAVE_PREPROCESSED_IMAGES = True

    SAVE_PREPROCESSED_PDF = True