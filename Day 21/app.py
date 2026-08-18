import cv2
import numpy as np
import gradio as gr
import os
from datetime import datetime



# FOLDERS

INPUT_FOLDER = "Day 21/images/inputImages"
OUTPUT_FOLDER = "Day 21/images/outputImages"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ORB FEATURE MATCHING FUNCTION

def match_features(image1, image2):

    # CHECK INPUT IMAGES

    if image1 is None or image2 is None:

        return (
            None,
            "Please upload both images.",
            "0",
            "0",
            "0"
        )


    # CONVERT IMAGES TO GRAYSCALE

    gray1 = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)

    # CREATE ORB DETECTOR

    orb = cv2.ORB_create(
        nfeatures=1000,
        scaleFactor=1.2,
        nlevels=8,
        edgeThreshold=31,
        firstLevel=0,
        WTA_K=2,
        scoreType=cv2.ORB_HARRIS_SCORE,
        patchSize=31,
        fastThreshold=20
    )


    # DETECT KEYPOINTS AND DESCRIPTORS

    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    # Count keypoints
    keypoints_count1 = len(keypoints1)
    keypoints_count2 = len(keypoints2)


    # CHECK DESCRIPTORS

    if descriptors1 is None or descriptors2 is None:

        return (
            None,
            "Could not find enough features in one or both images.",
            str(keypoints_count1),
            str(keypoints_count2),
            "0"
        )


    # 6. CREATE BRUTE FORCE MATCHER

    # ORB uses binary descriptors.
    # Hamming distance is therefore used.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

    # KNN MATCHING
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    
    # GOOD MATCH FILTERING

    good_matches = []
    ratio_threshold = 0.75


    for pair in matches:

        # Make sure two matches exist
        if len(pair) == 2:

            best_match, second_match = pair
            # Lowe's ratio test
            if best_match.distance < (
                ratio_threshold * second_match.distance
            ):

                good_matches.append(best_match)


    # SORT GOOD MATCHES
    good_matches = sorted(
        good_matches,
        key=lambda match: match.distance
    )


    # DISPLAY BEST 50 MATCHES
    display_matches = good_matches[:50]


    # DRAW MATCHES

    matched_image = cv2.drawMatches(
        image1,
        keypoints1,
        image2,
        keypoints2,
        display_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )


    # SAVE RESULT

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"orb_feature_matches_{timestamp}.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    cv2.imwrite(output_path, matched_image)


    # CONVERT BGR TO RGB FOR GRADIO
    matched_image_rgb = cv2.cvtColor(matched_image,cv2.COLOR_BGR2RGB)


    # INFORMATION

    information = f"""
### Feature Matching Results

**Image 1 keypoints:** {keypoints_count1}
**Image 2 keypoints:** {keypoints_count2}
**Total good matches:** {len(good_matches)}
**Matches displayed:** {len(display_matches)}
**Ratio threshold:** {ratio_threshold}
### Output
The matched image has been saved to:
`{output_path}`
"""


    # RETURN RESULTS

    return (
        matched_image_rgb,
        information,
        str(keypoints_count1),
        str(keypoints_count2),
        str(len(good_matches))
    )


# GRADIO APPLICATION

with gr.Blocks(
    title="Image Feature Matching System"
) as app:


    # TITLE

    gr.Markdown(
        """
        # 🔍 Image Feature Matching System

        Upload two similar images to detect ORB keypoints
        and find matching features between them.
        """
    )


    # INPUT IMAGES

    with gr.Row():

        image_input1 = gr.Image(type="numpy", label="Image 1")
        image_input2 = gr.Image(type="numpy", label="Image 2")


    # BUTTON

    match_button = gr.Button(
        "🔍 Find Matching Features",
        variant="primary"
    )


    # STATISTICS

    with gr.Row():

        keypoints_output1 = gr.Textbox(
            label="Image 1 Keypoints",
            interactive=False
        )

        keypoints_output2 = gr.Textbox(
            label="Image 2 Keypoints",
            interactive=False
        )

        good_matches_output = gr.Textbox(
            label="Good Matches",
            interactive=False
        )


    # MATCHED IMAGE

    matched_output = gr.Image(
        type="numpy",
        label="Matched Features"
    )


    # INFORMATION

    result_information = gr.Markdown(
        """
        Upload two images and click
        **Find Matching Features**.
        """
    )


    # SAMPLE IMAGES

    gr.Markdown(
        """
        ## 📷 Sample Images

        You can also select the sample images below.
        """
    )


    gr.Examples(
        examples=[
            [
                os.path.join(INPUT_FOLDER, "book (1).jpg"),
                os.path.join(INPUT_FOLDER, "book (2).jpg")
            ],
            [
                os.path.join(INPUT_FOLDER, "building (1).jpg"),
                os.path.join(INPUT_FOLDER, "building (2).jpg")
           ],
           [
                os.path.join(INPUT_FOLDER, "logo (1).jpg"),
                os.path.join(INPUT_FOLDER, "logo (2).jpg")
        ],
        [
                os.path.join(INPUT_FOLDER, "burj (1).jpg"),
                os.path.join(INPUT_FOLDER, "burj (2).jpg")
        ]
        ],
        inputs=[image_input1, image_input2],
        label="Book Image Pair"
    )


    # BUTTON EVENT

    match_button.click(
        fn=match_features,

        inputs=[image_input1, image_input2],
        outputs=[
            matched_output,
            result_information,
            keypoints_output1,
            keypoints_output2,
            good_matches_output
        ]
    )


# RUN APPLICATION
if __name__ == "__main__":

    app.launch()