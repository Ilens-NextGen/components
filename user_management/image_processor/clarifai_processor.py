import asyncio
import cv2
import numpy as np
from PIL import Image
import imageio.v3 as iio
from typing import List, Optional, Tuple
from .env_clarifai import *
from io import BytesIO

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

class AsyncVideoProcessor:
    def __init__(self):
        # Initialize any required variables here
        pass

    async def process_video(self, video_bytes: bytes, max_frame: Optional[int]=4, grid=True) -> List[np.ndarray]:
        try:
            # Convert video bytes to frames
            frames, fps = await asyncio.to_thread(self._bytes_to_frames, video_bytes)
            resized_frames = await asyncio.to_thread(self._resize_frames, frames)
            selected_frames = await asyncio.to_thread(
                self._select_frames, resized_frames, fps, max_frame
            )
            if not grid:
                return selected_frames
            grid_image = await asyncio.to_thread(self._create_grid, selected_frames)
            
            return [grid_image]

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

    def convert_result_image_arrays_to_bytes(self, images: List[np.ndarray]) -> bytes:
        res = []
        for image in images:
            image_pil = Image.fromarray(image)
            with BytesIO() as buffer:
                image_pil.save(buffer, format="PNG")
                res.append(buffer.getvalue())
        return res

class AsyncClarifaiImageRecognition:
    def __init__(self):
        self.PAT = PAT
        self.USER_ID = USER_ID
        self.APP_ID = APP_ID
        self.MODEL_ID = MODEL_ID
        self.MODEL_VERSION_ID = MODEL_VERSION_ID
        self.channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(self.channel)
        self.metadata = ('authorization', 'Key ' + self.PAT),
        self.userDataObject = resources_pb2.UserAppIDSet(user_id=self.USER_ID, app_id=self.APP_ID)
        
    async def find_all_objects(self, file_bytes: List[bytes]):
        post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
                user_app_id=self.userDataObject,
                model_id=self.MODEL_ID,
                version_id=self.MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                base64=file_byte
                            )
                        )
                    ) for file_byte in file_bytes
                ]
            ),
            metadata=metadata
        )
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
            
        regions = post_model_outputs_response.outputs[0].data.regions

        for region in regions:
            # Accessing and rounding the bounding box values
            top_row = round(region.region_info.bounding_box.top_row, 3)
            left_col = round(region.region_info.bounding_box.left_col, 3)
            bottom_row = round(region.region_info.bounding_box.bottom_row, 3)
            right_col = round(region.region_info.bounding_box.right_col, 3)
            
            for concept in region.data.concepts:
                # Accessing and rounding the concept value
                name = concept.name
                value = round(concept.value, 4)
                print((f"{name}: {value} BBox: {top_row}, {left_col}, {bottom_row}, {right_col}"))
