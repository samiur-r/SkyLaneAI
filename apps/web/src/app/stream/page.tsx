/**
 * Live Stream Page
 * Main page for real-time video streaming and object detection
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { useMediaStream } from '@/hooks/use-media-stream';
import { useWebRTC } from '@/hooks/use-webrtc';
import { useDetections } from '@/hooks/use-detections';
import { VideoCapture } from '@/components/video/video-capture';
import { DetectionOverlay } from '@/components/video/detection-overlay';
import { DetectionStats } from '@/components/video/detection-stats';
import { StreamControls } from '@/components/controls/stream-controls';
import { DetectionSettings } from '@/components/controls/detection-settings';
import type { StreamSettings } from '@repo/types';

const WS_URL =
  process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/api/v1/stream/ws';

export default function StreamPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamSettings, setStreamSettings] = useState<StreamSettings>({
    fps: 10,
    skipFrames: true,
    confidenceThreshold: 0.25,
  });

  // Media stream hook
  const {
    stream,
    devices,
    selectedDevice,
    isLoading: isCameraLoading,
    error: cameraError,
    requestStream,
    stopStream,
    switchDevice,
  } = useMediaStream({
    video: {
      width: { ideal: 1280 },
      height: { ideal: 720 },
      frameRate: { ideal: 30 },
    },
  });

  // Detections hook
  const {
    detections,
    detectionCount,
    latestFrame,
    processingTimeMs,
    stats: detectionStats,
    addDetectionResult,
    clearDetections,
    setConfidenceFilter,
  } = useDetections({
    confidenceThreshold: streamSettings.confidenceThreshold,
  });

  // WebRTC hook
  const {
    connectionStatus,
    stats: webrtcStats,
    isConnected,
    connect,
    disconnect,
    addVideoStream,
    updateSettings,
  } = useWebRTC({
    wsUrl: WS_URL,
    onDetection: (message) => {
      addDetectionResult(message);
    },
    onError: (error) => {
      console.error('WebRTC error:', error);
    },
  });

  /**
   * Start streaming
   */
  const handleStart = async () => {
    try {
      // Step 1: Request camera access
      await requestStream();
      setIsStreaming(true);
    } catch (error) {
      console.error('Failed to start stream:', error);
      setIsStreaming(false);
    }
  };

  /**
   * Stop streaming
   */
  const handleStop = () => {
    // Stop camera
    stopStream();

    // Disconnect WebRTC
    disconnect();

    // Clear detections
    clearDetections();

    setIsStreaming(false);
  };

  /**
   * When stream is available, connect to WebRTC
   */
  useEffect(() => {
    if (!stream || !isStreaming || isConnected) {
      return;
    }

    let isMounted = true;

    const setupWebRTC = async () => {
      if (!isMounted) return;

      try {
        console.log('Setting up WebRTC connection...');

        // Connect to WebRTC server
        await connect();

        if (!isMounted) return;

        // Small delay to ensure connection is ready
        await new Promise(resolve => setTimeout(resolve, 100));

        if (!isMounted) return;

        // Add video stream to connection
        await addVideoStream(stream);

        console.log('WebRTC connected and streaming');
      } catch (error) {
        console.error('Failed to setup WebRTC:', error);
        if (isMounted) {
          setIsStreaming(false);
        }
      }
    };

    setupWebRTC();

    return () => {
      isMounted = false;
    };
  }, [stream, isStreaming, isConnected, connect, addVideoStream]);

  /**
   * Update settings
   */
  const handleSettingsChange = (newSettings: Partial<StreamSettings>) => {
    const updatedSettings = { ...streamSettings, ...newSettings };
    setStreamSettings(updatedSettings);

    // Update confidence filter locally
    if (newSettings.confidenceThreshold !== undefined) {
      setConfidenceFilter(newSettings.confidenceThreshold);
    }

    // Send settings to backend
    if (isConnected) {
      updateSettings(newSettings);
    }
  };

  // Combine stats from detections and WebRTC
  const combinedStats = webrtcStats || detectionStats;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Live Detection Stream</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Real-time object detection with YOLOv11
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Video Stream */}
          <div className="lg:col-span-2 space-y-6">
            {/* Video Container */}
            <div className="relative aspect-video bg-black rounded-lg overflow-hidden shadow-lg">
              <VideoCapture
                ref={videoRef}
                stream={stream}
                isLoading={isCameraLoading}
                error={cameraError}
                className="w-full h-full"
              />

              {/* Detection Overlay */}
              {stream && videoRef.current && (
                <DetectionOverlay
                  detections={detections}
                  videoRef={videoRef as React.RefObject<HTMLVideoElement>}
                />
              )}
            </div>

            {/* Detection Stats */}
            <DetectionStats
              stats={combinedStats}
              detectionCount={detectionCount}
              processingTimeMs={processingTimeMs}
              latestFrame={latestFrame}
            />
          </div>

          {/* Right Column - Controls */}
          <div className="space-y-6">
            {/* Stream Controls */}
            <StreamControls
              isStreaming={isStreaming}
              isLoading={isCameraLoading}
              connectionStatus={connectionStatus}
              devices={devices}
              selectedDevice={selectedDevice}
              onStart={handleStart}
              onStop={handleStop}
              onDeviceChange={switchDevice}
            />

            {/* Detection Settings */}
            <DetectionSettings
              settings={streamSettings}
              onSettingsChange={handleSettingsChange}
              disabled={!isConnected}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
