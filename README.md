# Image Alignment and Timestamping Script

This script aligns images in a folder based on a reference image using **feature matching** and **homography transformation**. Optionally, it can overlay a timestamp extracted from EXIF metadata.

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

## License  
This project is licensed under the **GNU General Public License v3.0 (GPL v3)**, ensuring that any modifications or redistributions remain open-source.  

## Uploading to GitHub  
1. **Initialize Git**:  
   ```bash
   git init
   git add script.py README.md
   git commit -m "Added image alignment script with optional timestamps"
   ```
2. **Connect to GitHub**:  
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
