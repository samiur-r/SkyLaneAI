"""WebSocket routes for video streaming"""
import json
import logging
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.webrtc_handler import WebRTCConnectionHandler
from app.services.video_stream import VideoStreamProcessor

logger = logging.getLogger(__name__)

router = APIRouter()

# Store active connections (in production, use Redis or similar)
active_connections: Dict[str, dict] = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for WebRTC signaling and detection results

    Flow:
    1. Client connects and sends WebRTC offer
    2. Server responds with WebRTC answer
    3. WebRTC connection established, video frames flow
    4. Server processes frames and sends detection results back via WebSocket
    """
    await websocket.accept()
    connection_id = id(websocket)
    logger.info(f"WebSocket connection accepted: {connection_id}")

    # Create WebRTC handler and video processor
    webrtc_handler = WebRTCConnectionHandler()
    video_processor = VideoStreamProcessor(
        process_fps=10,  # Process 10 frames per second
        skip_frames=True
    )

    # Set up callback to send detections back to client
    async def send_detection_result(result: dict):
        """Send detection results to client via WebSocket"""
        try:
            await websocket.send_json({
                "type": "detection",
                "data": result
            })
        except Exception as e:
            logger.error(f"Error sending detection: {e}")

    # Set up callback for frame processing
    async def on_frame(frame, frame_number):
        """Called when a frame is received from WebRTC"""
        await video_processor.on_frame_received(frame, frame_number)

    # Configure callbacks
    video_processor.set_detection_callback(send_detection_result)
    webrtc_handler.set_frame_callback(on_frame)

    # Store connection
    active_connections[str(connection_id)] = {
        "websocket": websocket,
        "webrtc": webrtc_handler,
        "processor": video_processor
    }

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            message_type = message.get("type")

            logger.info(f"Received message type: {message_type}")

            if message_type == "offer":
                # Handle WebRTC offer from client
                offer_sdp = message.get("sdp")
                offer_type = message.get("offer_type", "offer")

                answer = await webrtc_handler.handle_offer(offer_sdp, offer_type)

                # Send answer back to client
                await websocket.send_json({
                    "type": "answer",
                    "sdp": answer["sdp"],
                    "answer_type": answer["type"]
                })

                # Start processing video frames
                await video_processor.start_processing()

                logger.info("WebRTC negotiation completed")

            elif message_type == "ice_candidate":
                # Handle ICE candidate
                candidate = message.get("candidate")
                await webrtc_handler.handle_ice_candidate(candidate)

            elif message_type == "settings":
                # Update processing settings
                settings = message.get("data", {})
                process_fps = settings.get("process_fps")
                skip_frames = settings.get("skip_frames")

                video_processor.update_settings(
                    process_fps=process_fps,
                    skip_frames=skip_frames
                )

                await websocket.send_json({
                    "type": "settings_updated",
                    "data": settings
                })

            elif message_type == "get_stats":
                # Send current statistics
                stats = video_processor.get_stats()
                await websocket.send_json({
                    "type": "stats",
                    "data": stats
                })

            elif message_type == "ping":
                # Respond to ping
                await websocket.send_json({
                    "type": "pong"
                })

            else:
                logger.warning(f"Unknown message type: {message_type}")

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        # Cleanup
        await video_processor.stop_processing()
        await webrtc_handler.close()

        # Remove from active connections
        if str(connection_id) in active_connections:
            del active_connections[str(connection_id)]

        logger.info(f"Connection cleaned up: {connection_id}")


@router.get("/connections")
async def get_active_connections():
    """Get count of active WebSocket connections"""
    return {
        "active_connections": len(active_connections),
        "connections": [
            {
                "id": conn_id,
                "state": conn_data["webrtc"].get_connection_state(),
                "stats": conn_data["processor"].get_stats()
            }
            for conn_id, conn_data in active_connections.items()
        ]
    }
