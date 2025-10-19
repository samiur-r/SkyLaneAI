/**
 * Video Detection Page
 * Upload and process videos with object detection
 */

'use client';

import { useEffect, useRef, useState } from 'react';
import { useVideoUpload } from '@/hooks/use-video-upload';
import { useVideoStream } from '@/hooks/use-video-stream';
import { useDetections } from '@/hooks/use-detections';
import { VideoUpload } from '@/components/video/video-upload';
import { VideoPlayer } from '@/components/video/video-player';
import { DetectionOverlay } from '@/components/video/detection-overlay';
import { DetectionStats } from '@/components/video/detection-stats';
import { DetectionSettings } from '@/components/controls/detection-settings';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Play, Pause, Trash2, Upload as UploadIcon } from 'lucide-react';
import type { VideoUploadMetadata, StreamSettings } from '@repo/types';

export default function VideoPage() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [videoMetadata, setVideoMetadata] = useState<VideoUploadMetadata | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [streamSettings, setStreamSettings] = useState<StreamSettings>({
    fps: 10,
    skipFrames: true,
    confidenceThreshold: 0.25,
  });

  // Video upload hook
  const {
    uploadVideo,
    deleteVideo,
    uploadProgress,
    isUploading,
    error: uploadError,
    clearError,
  } = useVideoUpload();

  // Detections hook
  const {
    detections,
    detectionCount,
    latestFrame,
    processingTimeMs,
    frameWidth,
    frameHeight,
    stats: detectionStats,
    addDetectionResult,
    clearDetections,
    setConfidenceFilter,
  } = useDetections({
    confidenceThreshold: streamSettings.confidenceThreshold,
  });

  // Video stream hook
  const {
    connectionStatus,
    isConnected,
    progress,
    connect,
    disconnect,
    play,
    pause,
    resume,
    updateSettings,
  } = useVideoStream({
    videoId: videoMetadata?.videoId || null,
    onDetection: (message) => {
      addDetectionResult(message);
    },
    onCompleted: () => {
      setIsProcessing(false);
      console.log('Video processing completed');
    },
    onError: (error) => {
      console.error('Video stream error:', error);
      setIsProcessing(false);
    },
  });

  /**
   * Handle video upload complete
   */
  const handleUploadComplete = async (file: File) => {
    try {
      const metadata = await uploadVideo(file);
      if (metadata) {
        setVideoMetadata(metadata);
        setVideoFile(file);
        console.log('Video uploaded:', metadata);
      }
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  /**
   * Handle start processing
   */
  const handleStartProcessing = async () => {
    if (!videoMetadata) return;

    try {
      // Connect to WebSocket
      await connect();

      // Wait a bit for connection to establish
      setTimeout(() => {
        // Start processing
        play(1.0);
        setIsProcessing(true);
      }, 500);
    } catch (error) {
      console.error('Failed to start processing:', error);
    }
  };

  /**
   * Handle pause/resume
   */
  const handleTogglePlayback = () => {
    if (isProcessing) {
      pause();
      setIsProcessing(false);
    } else {
      resume();
      setIsProcessing(true);
    }
  };

  /**
   * Handle delete video
   */
  const handleDeleteVideo = async () => {
    if (!videoMetadata) return;

    const confirmed = confirm('Are you sure you want to delete this video?');
    if (!confirmed) return;

    // Disconnect and cleanup
    disconnect();
    clearDetections();

    // Delete from server
    const success = await deleteVideo(videoMetadata.videoId);
    if (success) {
      setVideoMetadata(null);
      setVideoFile(null);
      setIsProcessing(false);
    }
  };

  /**
   * Handle settings change
   */
  const handleSettingsChange = (newSettings: Partial<StreamSettings>) => {
    const updatedSettings = { ...streamSettings, ...newSettings };
    setStreamSettings(updatedSettings);

    // Update confidence filter locally
    if (newSettings.confidenceThreshold !== undefined) {
      setConfidenceFilter(newSettings.confidenceThreshold);
    }

    // Send settings to backend if connected
    if (isConnected) {
      updateSettings({
        processFps: newSettings.fps,
        confidenceThreshold: newSettings.confidenceThreshold,
      });
    }
  };

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Video Detection</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Upload and analyze videos with YOLOv11 object detection
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Upload Mode */}
        {!videoMetadata && (
          <div className="max-w-3xl mx-auto">
            <VideoUpload
              onUploadComplete={(file) => {
                setVideoFile(file);
              }}
              onUploadStart={clearError}
              isUploading={isUploading}
              uploadProgress={uploadProgress}
              error={uploadError}
            />

            {/* Upload Button */}
            {videoFile && !isUploading && uploadProgress === 0 && (
              <div className="mt-6 flex justify-center">
                <Button
                  size="lg"
                  onClick={() => handleUploadComplete(videoFile)}
                  className="min-w-[200px]"
                >
                  <UploadIcon className="w-5 h-5 mr-2" />
                  Upload Video
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Playback Mode */}
        {videoMetadata && videoFile && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Video Player */}
            <div className="lg:col-span-2 space-y-6">
              {/* Video Container */}
              <div className="relative aspect-video bg-black rounded-lg overflow-hidden shadow-lg">
                <VideoPlayer
                  ref={videoRef}
                  videoFile={videoFile}
                  isPlaying={isProcessing}
                  onPlay={() => setIsProcessing(true)}
                  onPause={() => setIsProcessing(false)}
                  className="w-full h-full"
                />

                {/* Detection Overlay */}
                {videoRef.current && (
                  <DetectionOverlay
                    detections={detections}
                    videoRef={videoRef as React.RefObject<HTMLVideoElement>}
                    frameWidth={frameWidth}
                    frameHeight={frameHeight}
                  />
                )}
              </div>

              {/* Video Info Card */}
              <Card className="p-4">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-400">Duration</p>
                    <p className="text-sm font-medium">{videoMetadata.duration.toFixed(1)}s</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-400">Resolution</p>
                    <p className="text-sm font-medium">
                      {videoMetadata.width}x{videoMetadata.height}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-400">FPS</p>
                    <p className="text-sm font-medium">{videoMetadata.fps.toFixed(1)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 dark:text-gray-400">Size</p>
                    <p className="text-sm font-medium">{videoMetadata.sizeMb.toFixed(1)} MB</p>
                  </div>
                </div>
              </Card>

              {/* Processing Progress */}
              {progress && (
                <Card className="p-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Processing Progress</span>
                      <span className="font-medium">{Math.round(progress.percentage)}%</span>
                    </div>
                    <Progress value={progress.percentage} />
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Frame {progress.currentFrame} / {progress.totalFrames}
                    </div>
                  </div>
                </Card>
              )}

              {/* Detection Stats */}
              <DetectionStats
                stats={detectionStats}
                detectionCount={detectionCount}
                processingTimeMs={processingTimeMs}
                latestFrame={latestFrame}
              />
            </div>

            {/* Right Column - Controls */}
            <div className="space-y-6">
              {/* Connection Status */}
              <Card className="p-4">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status</span>
                    <Badge
                      variant={
                        connectionStatus === 'connected'
                          ? 'default'
                          : connectionStatus === 'error'
                          ? 'destructive'
                          : 'secondary'
                      }
                    >
                      {connectionStatus}
                    </Badge>
                  </div>

                  {/* Control Buttons */}
                  <div className="flex gap-2">
                    {!isConnected ? (
                      <Button onClick={handleStartProcessing} className="flex-1">
                        <Play className="w-4 h-4 mr-2" />
                        Start Processing
                      </Button>
                    ) : (
                      <Button onClick={handleTogglePlayback} className="flex-1">
                        {isProcessing ? (
                          <>
                            <Pause className="w-4 h-4 mr-2" />
                            Pause
                          </>
                        ) : (
                          <>
                            <Play className="w-4 h-4 mr-2" />
                            Resume
                          </>
                        )}
                      </Button>
                    )}

                    <Button variant="destructive" onClick={handleDeleteVideo}>
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </Card>

              {/* Detection Settings */}
              <DetectionSettings
                settings={streamSettings}
                onSettingsChange={handleSettingsChange}
                disabled={!isConnected}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
