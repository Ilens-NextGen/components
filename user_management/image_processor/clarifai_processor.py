from datetime import datetime
import cv2
import numpy as np
from typing import Tuple, List, Union, Optional


class AsyncImageProcessor:
    """This is an asynchronous implementation of an image processor.
    This makes use of clarifai's models, keras opencv, and other models in order to
    process and detect stuff in images"""

    async def calculate_grid_positions(
        self, num_frames: int, frame_width: int, frame_height: int
    ) -> Tuple[int, int]:
        """Calculate the grid positions for overlaying the frames
        Args:
            num_frames (int): the number of frames
            frame_width (int): the width of a frame
            frame_height (int): the height of a frame
        Returns:
            Tuple[int, int]: the rows - column value
        """
        root = sqrt(num_frames)
        if frame_width > frame_height:  # Landscape orientation
            rows = 2
            cols = num_frames / 2
        else:  # Portrait orientation
            rows = num_frames / 2
            cols = 2

        # Adjust if necessary
        while rows * cols < num_frames:
            if frame_width > frame_height:  # Landscape orientation
                cols += 1
            else:  # Portrait orientation
                rows += 1

        return int(rows), int(cols)

    async def convert_image_list_to_frames(
        self, images: List[str] | List[UploadedFile] = []
    ):
        """Converts a list of images to frames"""
        frames = []
        if all(isinstance(image, str) for image in images):
            for image in images:
                frame = cv2.imread(image)
                frames.append(frame)
        else:  # Images are straight from fileStorage
            for file in images:
                data = file.read()
                # file.seek(0) Incase we would like to use this for anything else
                frame = np.asarray(bytearray(data), dtype="uint8")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                frames.append(frame)
        return frames

    async def save_image_grid(self, image, output_path: str, show=True, save=False):
        output_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_name = f"output/grid-{output_timestamp}.jpg"
        output_path = os.path.abspath(output_name)
        print(f"Saving image grid to {output_path}")
        if show:
            cv2.imshow("Image Grid", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        if save:
            cv2.imwrite(output_name, image)
        return output_name

    async def video_to_grid(self, video, show, max_frames=4):
        frames, width, height = await self.convert_videos_to_frames(video, max_frames)
        rows, cols = await self.calculate_grid_positions(len(frames), width, height)
        image_grid = await self.convert_frames_to_grid(frames, rows, cols)
        return await self.save_image_grid(image_grid, show)

    async def open_video_to_cv(
        self, bytes_data: bytes, type: str, max_frames: Optional[int] = 4
    ) -> Tuple[List[np.ndarray], int, int]:
        nparr = np.frombuffer(bytes_data, np.uint8)
        cap = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(num_frames / max_frames) if max_frames else int(cap.get(cv2.CAP_PROP_FPS))
        time_in_s = max_frames or int(num_frames / fps)
        f_width, f_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ff_width, ff_height = int(f_width * 0.8), int(f_height * 0.8)

        frames = []
        count = 1

        for i in range(num_frames):
            if count > time_in_s:
                break
            ret, frame = cap.read()
            if not ret:
                break
            if i == (count * fps):
                print(f"Adding frame {i}")
                frame = cv2.resize(frame, (ff_width, ff_height))
                frames.append(frame)
                count += 1

        return frames, ff_width, ff_height


    async def convert_frames_to_grid(self, frames: List[np.ndarray], rows: int, cols: int) -> np.ndarray:
        grid = [frames[i:i + cols] for i in range(0, len(frames), cols)]

        final_image = np.vstack([np.hstack(row_frames) for row_frames in grid])

        return final_image