# Image Alignment and Timestamping Script

This script is designed for aligning multiple images taken from the same location over time. The initial idea was to capture photos from a fixed viewpoint and observe seasonal changes—how snow accumulates in winter, how trees regain their leaves in spring, and how the landscape transforms through summer and autumn.

To ensure smooth visual transitions, the script automatically aligns images to a reference photo using feature matching and homography transformation. This process corrects small shifts in camera positioning, ensuring all images are perfectly overlaid for a seamless comparison or time-lapse video.

Additionally, the script can optionally overlay timestamps extracted from EXIF metadata, marking the date each photo was taken. This feature helps track seasonal changes over time in an organized and visually clear way.

## Features  
✅ **Aligns images** to a reference photo for consistency.  
✅ **Optional timestamp overlay** (e.g., "January 20").  
✅ **EXIF metadata extraction** for accurate dates.  
✅ **Automatic folder management** for organized output.  
✅ **Customizable settings** (font, timestamp position, etc.).  

## Usage  

### 1. Install Dependencies  
Ensure you have Python installed, then install the required libraries:  
```bash
pip install opencv-python numpy pillow
```

### 2. Configure Settings  
Modify the **top section** of the script:  
```python
BASE_IMAGE_PATH = "path/to/reference.jpg"  # Set your reference image  
INPUT_FOLDER = "path/to/input_images"  # Folder containing images  
OUTPUT_FOLDER = "path/to/output_images"  # Where results will be saved  

ADD_TIMESTAMP = True  # Set False to disable date overlay  
TIMESTAMP_POSITION = "bottom"  # Options: 'bottom' or 'top'  
FONT_PATH = "arial.ttf"  # Ensure the font is available  
FONT_SIZE = 100  # Adjust for visibility  
```

### 3. Run the Script  
```bash
python script.py
```

### 4. Output Structure  
The script automatically creates folders:  
```
output_images/
│── aligned/         # Aligned images without timestamps  
│── dated/           # Aligned images with timestamps (if enabled)  
```

## Example Use Case  
This script was designed to align **year-round images from a fixed window view** at **my work place**, allowing smooth transitions for a time-lapse video showing seasonal changes.
