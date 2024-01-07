from datetime import datetime
import cv2
import numpy as np
def save_binary_to_file(binary: bytes, type: str) -> str:
    """Saves binary to file

    Args:
        binary (bytes): binary to save
        filename (str): filename to save binary to
    """
    # Convert binary data to numpy array
    nparr = np.frombuffer(binary, np.uint8)

    # Save as image
    if type == 'jpg':
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        filename = f"image-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.jpg"
        cv2.imwrite(filename, img)
    # Save as video
    elif type == 'mp4':
        # This assumes that the binary data is a full video
        filename = f"video-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.{type}"
        with open(filename, 'wb') as f:
            f.write(binary)
    else:
        raise ValueError(f"Unsupported file type: {type}")

    return filename