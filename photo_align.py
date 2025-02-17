import os
import cv2
import numpy as np
import logging
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from datetime import datetime

# ---- USER CONFIGURATION ----
BASE_IMAGE_PATH = r"BASE_IMAGE_PATH "
INPUT_FOLDER = r"INPUT_FOLDER"
OUTPUT_FOLDER = r"OUTPUT_FOLDER"
FONT_PATH = "arial.ttf"  # Set to None for default font
FONT_SIZE = 100  # Adjust as needed
ADD_TIMESTAMP = True  # Set to False to skip adding a timestamp
TIMESTAMP_POSITION = "bottom"  # Options: 'bottom', 'top'

# ---- CONFIGURE LOGGING ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_date_taken(image_path):
    """Extract the 'DateTimeOriginal' field from EXIF data."""
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return value
    except Exception as e:
        logging.warning(f"Error reading EXIF data from {image_path}: {e}")
    return None

def load_font(font_path, size):
    """Load the specified font or fallback to default."""
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        logging.warning(f"Font not found at {font_path}. Using default font.")
        return ImageFont.load_default()

def align_images(base_img, target_img):
    """Align target image to the base image using feature matching."""
    try:
        base_gray = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT_create()
        keypoints_base, descriptors_base = sift.detectAndCompute(base_gray, None)
        keypoints_target, descriptors_target = sift.detectAndCompute(target_gray, None)

        flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
        matches = flann.knnMatch(descriptors_base, descriptors_target, k=2)

        good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

        if len(good_matches) > 10:
            points_base = np.float32([keypoints_base[m.queryIdx].pt for m in good_matches])
            points_target = np.float32([keypoints_target[m.trainIdx].pt for m in good_matches])

            h, _ = cv2.findHomography(points_target, points_base, cv2.RANSAC)
            height, width, _ = base_img.shape
            return cv2.warpPerspective(target_img, h, (width, height))
        else:
            logging.warning("Not enough matches to align images.")
            return None
    except Exception as e:
        logging.error(f"Error aligning images: {e}")
        return None

def add_timestamp(image, timestamp, font, position="bottom"):
    """Overlay a timestamp onto the image."""
    try:
        draw = ImageDraw.Draw(image)
        text_bbox = draw.textbbox((0, 0), timestamp, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        x_position = (image.width - text_width) // 2
        y_position = 50 if position == "top" else image.height - text_height - 100

        draw.rectangle(
            [(x_position - 10, y_position - 10), (x_position + text_width + 10, y_position + text_height + 10)],
            fill="black"
        )
        draw.text((x_position, y_position), timestamp, fill="white", font=font)
    except Exception as e:
        logging.error(f"Error adding timestamp: {e}")

def process_images(base_image_path, input_folder, output_folder, font_path, font_size, add_timestamp_flag, timestamp_position):
    """Process images: align them and optionally overlay timestamps."""
    aligned_folder = os.path.join(output_folder, "aligned")
    dated_folder = os.path.join(aligned_folder, "dated")
    os.makedirs(dated_folder, exist_ok=True)

    base_img = cv2.imread(base_image_path, cv2.IMREAD_COLOR)
    if base_img is None:
        logging.error(f"Error loading base image: {base_image_path}")
        return

    font = load_font(font_path, font_size)

    for file_name in sorted(os.listdir(input_folder)):
        if not file_name.lower().endswith(('jpg', 'jpeg', 'png')):
            continue

        image_path = os.path.join(input_folder, file_name)
        date_taken = get_date_taken(image_path)
        timestamp = datetime.strptime(date_taken, "%Y:%m:%d %H:%M:%S").strftime("%B %d") if date_taken else datetime.now().strftime("%B %d")

        aligned_image_path = os.path.join(aligned_folder, file_name)
        dated_image_path = os.path.join(dated_folder, file_name)

        target_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if target_img is None:
            logging.warning(f"Error loading image: {image_path}")
            continue

        aligned_img = align_images(base_img, target_img)
        if aligned_img is None:
            logging.warning(f"Skipping alignment for {file_name}")
            continue

        cv2.imwrite(aligned_image_path, aligned_img)
        logging.info(f"Aligned image saved: {aligned_image_path}")

        pil_img = Image.fromarray(cv2.cvtColor(aligned_img, cv2.COLOR_BGR2RGB))

        if add_timestamp_flag:
            add_timestamp(pil_img, timestamp, font, timestamp_position)
            pil_img.save(dated_image_path, format="JPEG")
            logging.info(f"Dated image saved: {dated_image_path}")
        else:
            pil_img.save(aligned_image_path, format="JPEG")
            logging.info(f"Saved aligned image without timestamp: {aligned_image_path}")

# ---- RUN SCRIPT ----
if __name__ == "__main__":
    process_images(
        BASE_IMAGE_PATH, 
        INPUT_FOLDER, 
        OUTPUT_FOLDER, 
        FONT_PATH, 
        FONT_SIZE, 
        ADD_TIMESTAMP, 
        TIMESTAMP_POSITION
    )
