"""WebRTC connection handler for video streaming"""
import asyncio
import json
import logging
from typing import Optional, Callable
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaRelay
import av
import numpy as np

logger = logging.getLogger(__name__)


class VideoTransformTrack(VideoStreamTrack):
    """
    Video track that receives frames from the client
    and makes them available for processing
    """

    def __init__(self, track: VideoStreamTrack, on_frame: Optional[Callable] = None):
        super().__init__()
        self.track = track
        self.on_frame = on_frame
        self.frame_count = 0

    async def recv(self):
        """Receive and process video frame"""
        frame = await self.track.recv()
        self.frame_count += 1

        # Convert frame to numpy array for YOLO processing
        if self.on_frame:
            try:
                # Convert frame to numpy array (BGR format for OpenCV/YOLO)
                img = frame.to_ndarray(format="bgr24")
                await self.on_frame(img, self.frame_count)
            except Exception as e:
                logger.error(f"Error processing frame: {e}")

        return frame


class WebRTCConnectionHandler:
    """Handles WebRTC peer connections and video streaming"""

    def __init__(self):
        self.pc: Optional[RTCPeerConnection] = None
        self.relay = MediaRelay()
        self.video_track: Optional[VideoTransformTrack] = None
        self.on_frame_callback: Optional[Callable] = None

    def set_frame_callback(self, callback: Callable):
        """Set callback function to be called when a frame is received"""
        self.on_frame_callback = callback

    async def create_peer_connection(self) -> RTCPeerConnection:
        """Create a new RTCPeerConnection"""
        self.pc = RTCPeerConnection()

        @self.pc.on("track")
        async def on_track(track):
            """Handle incoming video track"""
            logger.info(f"Track received: {track.kind}")

            if track.kind == "video":
                # Create video transform track with frame callback
                self.video_track = VideoTransformTrack(
                    self.relay.subscribe(track),
                    on_frame=self.on_frame_callback
                )

                # Keep the track alive
                @track.on("ended")
                async def on_ended():
                    logger.info("Video track ended")

        @self.pc.on("connectionstatechange")
        async def on_connectionstatechange():
            """Handle connection state changes"""
            logger.info(f"Connection state: {self.pc.connectionState}")
            if self.pc.connectionState == "failed":
                await self.close()

        return self.pc

    async def handle_offer(self, offer_sdp: str, offer_type: str = "offer") -> dict:
        """
        Handle WebRTC offer from client

        Args:
            offer_sdp: SDP offer from client
            offer_type: Type of offer (default: "offer")

        Returns:
            Dictionary containing answer SDP
        """
        try:
            # Create peer connection if not exists
            if not self.pc:
                await self.create_peer_connection()

            # Set remote description (client's offer)
            offer = RTCSessionDescription(sdp=offer_sdp, type=offer_type)
            await self.pc.setRemoteDescription(offer)
            logger.info("Remote description set")

            # Create answer
            answer = await self.pc.createAnswer()
            await self.pc.setLocalDescription(answer)
            logger.info("Local description set")

            return {
                "type": self.pc.localDescription.type,
                "sdp": self.pc.localDescription.sdp
            }

        except Exception as e:
            logger.error(f"Error handling offer: {e}")
            raise

    async def handle_ice_candidate(self, candidate: dict):
        """
        Handle ICE candidate from client

        Args:
            candidate: ICE candidate data
        """
        try:
            if self.pc:
                # Note: aiortc handles ICE candidates automatically
                # This is here for future expansion if needed
                logger.info(f"ICE candidate received: {candidate}")
        except Exception as e:
            logger.error(f"Error handling ICE candidate: {e}")

    async def close(self):
        """Close the peer connection"""
        if self.pc:
            await self.pc.close()
            logger.info("Peer connection closed")
            self.pc = None
            self.video_track = None

    def get_connection_state(self) -> str:
        """Get current connection state"""
        if self.pc:
            return self.pc.connectionState
        return "closed"
