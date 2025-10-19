/**
 * Video Player Component
 * Plays uploaded video with detection overlay
 */

'use client';

import { useEffect, useRef, forwardRef, useState } from 'react';
import { Play, Pause, SkipBack, SkipForward, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export interface VideoPlayerProps {
  videoId: string | null;
  isPlaying?: boolean;
  onPlay?: () => void;
  onPause?: () => void;
  onSeek?: (timestamp: number) => void;
  onSpeedChange?: (speed: number) => void;
  onTimeUpdate?: (currentTime: number) => void;
  className?: string;
}

export const VideoPlayer = forwardRef<HTMLVideoElement, VideoPlayerProps>(
  ({ videoId, isPlaying, onPlay, onPause, onSeek, onSpeedChange, onTimeUpdate, className = '' }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const internalRef = (ref as React.RefObject<HTMLVideoElement>) || videoRef;

    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
    const [videoUrl, setVideoUrl] = useState<string | null>(null);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    /**
     * Create video URL from backend stream
     */
    useEffect(() => {
      if (videoId) {
        const streamUrl = `${API_URL}/api/v1/video/${videoId}/stream`;
        setVideoUrl(streamUrl);

        // Load video metadata
        setTimeout(() => {
          if (internalRef.current) {
            internalRef.current.load();
          }
        }, 100);
      } else {
        setVideoUrl(null);
      }
    }, [videoId, API_URL]);

    /**
     * Handle isPlaying prop changes - sync video playback with external state
     */
    useEffect(() => {
      if (!internalRef.current || !videoUrl) return;

      const video = internalRef.current;

      // Auto-play when isPlaying becomes true
      if (isPlaying && video.paused) {
        video.play().catch((err) => {
          console.error('Failed to auto-play video:', err);
        });
      }
      // Auto-pause when isPlaying becomes false
      else if (!isPlaying && !video.paused) {
        video.pause();
      }
    }, [isPlaying, videoUrl]);

    /**
     * Handle video metadata loaded
     */
    const handleLoadedMetadata = () => {
      if (internalRef.current) {
        setDuration(internalRef.current.duration);
      }
    };

    /**
     * Handle time update
     */
    const handleTimeUpdate = () => {
      if (internalRef.current) {
        setCurrentTime(internalRef.current.currentTime);
        onTimeUpdate?.(internalRef.current.currentTime);
      }
    };

    /**
     * Handle play/pause
     */
    const togglePlayPause = () => {
      if (!internalRef.current) return;

      if (internalRef.current.paused) {
        internalRef.current.play();
        onPlay?.();
      } else {
        internalRef.current.pause();
        onPause?.();
      }
    };

    /**
     * Handle seek
     */
    const handleSeek = (value: number[]) => {
      if (!internalRef.current) return;

      const newTime = value[0];
      internalRef.current.currentTime = newTime;
      setCurrentTime(newTime);
      onSeek?.(newTime);
    };

    /**
     * Handle speed change
     */
    const handleSpeedChange = (speed: string) => {
      const speedValue = parseFloat(speed);
      if (!internalRef.current) return;

      internalRef.current.playbackRate = speedValue;
      setPlaybackSpeed(speedValue);
      onSpeedChange?.(speedValue);
    };

    /**
     * Skip forward/backward
     */
    const skip = (seconds: number) => {
      if (!internalRef.current) return;

      const newTime = Math.max(0, Math.min(duration, internalRef.current.currentTime + seconds));
      internalRef.current.currentTime = newTime;
      setCurrentTime(newTime);
      onSeek?.(newTime);
    };

    /**
     * Format time as MM:SS
     */
    const formatTime = (seconds: number): string => {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    if (!videoUrl) {
      return (
        <div className={`relative ${className}`}>
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 rounded-lg">
            <div className="text-center space-y-4">
              <AlertCircle className="w-16 h-16 mx-auto text-gray-600" />
              <p className="text-gray-400 text-sm">No video loaded</p>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className={`relative ${className}`}>
        {/* Video Element */}
        <video
          ref={internalRef}
          src={videoUrl}
          onLoadedMetadata={handleLoadedMetadata}
          onTimeUpdate={handleTimeUpdate}
          onError={() => {
            console.error('Video playback error:', internalRef.current?.error);
          }}
          preload="metadata"
          playsInline
          className="w-full h-full object-contain rounded-lg bg-black"
        />

        {/* Custom Controls */}
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4 rounded-b-lg">
          {/* Progress Bar */}
          <div className="mb-3">
            <Slider
              value={[currentTime]}
              min={0}
              max={duration || 100}
              step={0.1}
              onValueChange={handleSeek}
              className="cursor-pointer"
            />
          </div>

          {/* Controls Row */}
          <div className="flex items-center justify-between gap-4">
            {/* Playback Controls */}
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => skip(-10)}
                className="text-white hover:bg-white/20"
              >
                <SkipBack className="w-4 h-4" />
              </Button>

              <Button
                variant="ghost"
                size="sm"
                onClick={togglePlayPause}
                className="text-white hover:bg-white/20"
              >
                {isPlaying ? (
                  <Pause className="w-5 h-5" />
                ) : (
                  <Play className="w-5 h-5" />
                )}
              </Button>

              <Button
                variant="ghost"
                size="sm"
                onClick={() => skip(10)}
                className="text-white hover:bg-white/20"
              >
                <SkipForward className="w-4 h-4" />
              </Button>
            </div>

            {/* Time Display */}
            <div className="text-white text-sm font-medium">
              {formatTime(currentTime)} / {formatTime(duration)}
            </div>

            {/* Speed Control */}
            <Select value={playbackSpeed.toString()} onValueChange={handleSpeedChange}>
              <SelectTrigger className="w-20 h-8 text-white border-white/30 bg-black/20">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="0.5">0.5x</SelectItem>
                <SelectItem value="1">1x</SelectItem>
                <SelectItem value="1.5">1.5x</SelectItem>
                <SelectItem value="2">2x</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>
    );
  }
);

VideoPlayer.displayName = 'VideoPlayer';
