import asyncio
import cv2
import numpy as np
from PIL import Image
import imageio.v3 as iio
from typing import List, Optional, Tuple

class AsyncVideoProcessor:
    def __init__(self):
        # Initialize any required variables here
        pass

    async def process_video(self, video_bytes: bytes, max_frame: Optional[int]=None):
        try:
            # Convert video bytes to frames
            frames, fps = await asyncio.to_thread(self._bytes_to_frames, video_bytes)
            resized_frames = await asyncio.to_thread(self._resize_frames, frames)
            selected_frames = await asyncio.to_thread(
                self._select_frames, resized_frames, fps, max_frame
            )
            grid_image = await asyncio.to_thread(self._create_grid, selected_frames)
            
            # use pil to display the image
            pil_image = Image.fromarray(grid_image)
            pil_image.show()
            return grid_image

        except Exception as e:
            print(f"Error processing video: {e}")
            return None

    def _bytes_to_frames(self, video_bytes: bytes) -> Tuple[List[np.ndarray], int]:
        frames = iio.imread(video_bytes, index=None, format_hint=".mp4")
        return frames, len(frames)
            
    def _resize_frames(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        return [cv2.resize(frame, (0, 0), fx=0.9, fy=0.9) for frame in frames]

    def _select_frames(self, frames: List[np.ndarray], fps: int, max_frame: int) -> List[np.ndarray]:
        if max_frame:
            total_frames = len(frames)
            duration = total_frames / fps
            step = int(total_frames / (duration * max_frame))
            return frames[::step] if len(frames) <= max_frame else frames[-max_frame:]
        else:
            return frames

    def _create_grid(self, frames: List[np.ndarray]) -> np.ndarray:
        """Create a grid of 2 by 2 frames. I expect exactly four frames and
        so I've calculated it and hardcoded it as such
        Args:
            frames (List[np.ndarray]): a list of frames
        Returns:
            np.ndarray: the composite image
        """
        # Assuming frames are of the same size
        height, width, _ = frames[0].shape
        grid_image = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)
        for i, frame in enumerate(frames):
            row = i // 2
            col = i % 2
            grid_image[row * height:(row + 1) * height, col * width:(col + 1) * width] = frame
        return grid_image
