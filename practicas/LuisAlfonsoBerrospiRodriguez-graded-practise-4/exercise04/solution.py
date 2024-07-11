import cv2
import numpy as np


import cv2
import numpy as np

def stitch_images(full_path_input_image, blender, features_finder, features_matcher, warper, full_path_output_image):
    # Load images
    images = [cv2.imread(image_path) for image_path in full_path_input_image]

    # Create stitcher
    stitcher = cv2.Stitcher_create().create()

    # Set the features finder
    if features_finder == 'AKAZE':
        stitcher.setFeaturesFinder(cv2.detail_AKAZEFeaturesFinder_create())
    elif features_finder == 'ORB':
        stitcher.setFeaturesFinder(cv2.detail_ORBFeaturesFinder_create())
    elif features_finder == 'SIFT':
        stitcher.setFeaturesFinder(cv2.detail_SIFTFeaturesFinder_create())
    elif features_finder == 'SURF':
        stitcher.setFeaturesFinder(cv2.detail_SURFFeaturesFinder_create())

    # Set the features matcher
    if features_matcher == 'AffineBestOf2Nearest':
        stitcher.setFeaturesMatcher(cv2.detail_AffineBestOf2NearestMatcher_create(False))
    elif features_matcher == 'BestOf2NearestRange':
        stitcher.setFeaturesMatcher(cv2.detail_BestOf2NearestRangeMatcher_create(False, 0.3))

    # Set the warper
    if warper == 'Affine':
        stitcher.setWarper(cv2.PyAffineWarper())
    elif warper == 'CompressedRectilinearPortrait':
        stitcher.setWarper(cv2.PyCompressedRectilinearPortraitWarper())
    elif warper == 'CompressedRectilinear':
        stitcher.setWarper(cv2.PyCompressedRectilinearWarper())
    elif warper == 'Cylindrical':
        stitcher.setWarper(cv2.PyCylindricalWarper())
    elif warper == 'Fisheye':
        stitcher.setWarper(cv2.PyFisheyeWarper())
    elif warper == 'Mercator':
        stitcher.setWarper(cv2.PyMercatorWarper())
    elif warper == 'PaniniPortrait':
        stitcher.setWarper(cv2.PyPaniniPortraitWarper())
    elif warper == 'Panini':
        stitcher.setWarper(cv2.PyPaniniWarper())
    elif warper == 'Plane':
        stitcher.setWarper(cv2.PyPlaneWarper())
    elif warper == 'Spherical':
        stitcher.setWarper(cv2.PySphericalWarper())
    elif warper == 'Stereographic':
        stitcher.setWarper(cv2.PyStereographicWarper())
    elif warper == 'TransverseMercator':
        stitcher.setWarper(cv2.PyTransverseMercatorWarper())

    # Set the blender
    if blender == 'FeatherBlender':
        stitcher.setBlender(cv2.detail_FeatherBlender_create())
    elif blender == 'MultiBandBlender':
        stitcher.setBlender(cv2.detail_MultiBandBlender_create())

    # Stitch images
    status, pano = stitcher.stitch(images)
    
    if status == cv2.Stitcher_OK:
        cv2.imwrite(full_path_output_image, pano)
        print('Stitching successful, output saved to:', full_path_output_image)
    else:
        print('Stitching failed.')


if __name__ == "__main__":
    stitch_images(
        full_path_input_image=[
            'images-for-stitcher/panorama1-input-1.jpg',
            'images-for-stitcher/panorama1-input-2.jpg',
            'images-for-stitcher/panorama1-input-3.jpg',
            'images-for-stitcher/panorama1-input-4.jpg',
            'images-for-stitcher/panorama1-input-5.jpg',
            'images-for-stitcher/panorama1-input-6.jpg',
        ],
        blender="MultiBandBlender",
        features_finder="SIFT",
        features_matcher="BestOf2NearestRange",
        warper="Mercator",
        full_path_output_image='panorama1-mercator.jpg'
    )
