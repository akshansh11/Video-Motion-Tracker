# Video Motion Tracker

Create stunning colorful trails that follow moving objects in videos! Perfect for creating eye-catching visual effects, dance videos, sports analysis, or adding visual flair to your footage.


![track (2) (1)](https://github.com/user-attachments/assets/2cc0b147-e5df-44f9-8512-ad197ad35584)

## Features

- **Multiple Tracking Methods**: Choose from contour-based or edge-based tracking
- **Vibrant Color Trails**: Rainbow-colored trails that fade over time
- **Smart Person Detection**: Filters out noise and focuses on human-sized objects
- **Real-time Processing**: Live preview while processing
- **Customizable Parameters**: Adjust trail length, colors, and sensitivity
- **Debug Mode**: Visual feedback to fine-tune detection settings

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/colorful-motion-tracker.git
cd colorful-motion-tracker

# Install dependencies
pip install opencv-python numpy
```

## Quick Start

```python
from colorful_tracker import SelectivePersonTracker

# Initialize tracker
tracker = SelectivePersonTracker(
    trail_length=15,        # How long trails last
    min_contour_area=3000   # Minimum size to track
)

# Process video
tracker.process_video("input_video.mp4", "output_video.mp4")
```

## Usage Examples

### Basic Person Tracking

```python
import cv2
from colorful_tracker import SelectivePersonTracker

# Create tracker with default settings
tracker = SelectivePersonTracker()

# Process video file
tracker.process_video(
    video_path="dance_video.mp4",
    output_path="dance_with_trails.mp4"
)
```

### Edge-Based Tracking

```python
from colorful_tracker import CleanEdgeTracker

# For more detailed edge tracking
tracker = CleanEdgeTracker(trail_length=20)
tracker.process_video("sports_video.mp4", "sports_tracked.mp4")
```

### Custom Configuration

```python
# High resolution video settings
tracker = SelectivePersonTracker(
    trail_length=25,        # Longer trails
    min_contour_area=5000   # Less sensitive for 4K videos
)

# Low resolution video settings  
tracker = SelectivePersonTracker(
    trail_length=10,        # Shorter trails
    min_contour_area=1500   # More sensitive for smaller videos
)
```

## Tracking Methods

### 1. Selective Person Tracker
- Best for tracking people in videos
- Uses background subtraction with intelligent filtering
- Focuses on human-sized objects with person-like proportions
- Recommended for most use cases

### 2. Clean Edge Tracker
- Tracks edges and contours of moving objects
- Creates more detailed, fine-grained trails
- Good for capturing intricate movements
- Better for objects with clear edges

## Parameters

### SelectivePersonTracker

| Parameter | Default | Description |
|-----------|---------|-------------|
| `trail_length` | 15 | Number of trail frames (higher = longer trails) |
| `min_contour_area` | 2000 | Minimum pixel area to track (higher = less sensitive) |

### CleanEdgeTracker

| Parameter | Default | Description |
|-----------|---------|-------------|
| `trail_length` | 20 | Number of trail frames |

## Troubleshooting

### Too Much Background Noise
- Increase `min_contour_area` (try 4000-8000)
- Let the background subtractor learn longer (increase learning frames)
- Use CleanEdgeTracker for cleaner results

### Not Detecting the Person
- Decrease `min_contour_area` (try 1000-2000)
- Check the debug window (top-left corner) to see what's being detected
- Ensure good contrast between person and background

### Performance Issues
- Reduce video resolution before processing
- Decrease `trail_length` for faster processing
- Process shorter video segments

## Advanced Usage

### Custom Colors

```python
# Modify the color palette
tracker = SelectivePersonTracker()
tracker.colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green  
    (0, 0, 255),    # Blue
    # Add more colors as needed
]
```

### Processing from Webcam

```python
# Use webcam input (0 = default camera)
tracker.process_video(0)  # No output file = live preview only
```

### Batch Processing

```python
import os
from colorful_tracker import SelectivePersonTracker

tracker = SelectivePersonTracker()

# Process all MP4 files in a directory
for filename in os.listdir("input_videos/"):
    if filename.endswith(".mp4"):
        input_path = f"input_videos/{filename}"
        output_path = f"output_videos/tracked_{filename}"
        tracker.process_video(input_path, output_path)
```

## Technical Details

### Algorithm Overview
1. **Background Subtraction**: Uses MOG2 algorithm to detect moving objects
2. **Noise Filtering**: Multiple morphological operations to clean detection
3. **Object Filtering**: Size and shape validation to focus on people
4. **Trail Generation**: Maintains history of object positions with color coding
5. **Rendering**: Blends colorful trails with original video using alpha compositing

### Dependencies
- OpenCV 4.x+ (cv2)
- NumPy 1.19+
- Python 3.7+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/yourusername/colorful-motion-tracker.git
cd colorful-motion-tracker
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with OpenCV computer vision library
- Inspired by motion tracking techniques in sports analysis
- Background subtraction using MOG2 algorithm

## Examples

### Input vs Output
| Original | With Colorful Trails |
|----------|---------------------|
| ![Original](examples/original.jpg) | ![Tracked](examples/tracked.jpg) |

### Different Tracking Methods
- **Contour Tracking**: Best for full-body movements
- **Edge Tracking**: Great for detailed motion capture
- **Custom Colors**: Match your brand or aesthetic

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Look at existing GitHub issues
3. Create a new issue with detailed description and sample video

---

**Made with Python and OpenCV**

