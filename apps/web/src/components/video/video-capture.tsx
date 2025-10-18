/**
 * Video Capture Component
 * Displays live camera feed
 */

'use client';

import { useEffect, useRef, forwardRef } from 'react';
import { AlertCircle, Camera } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

export interface VideoCaptureProps {
  stream: MediaStream | null;
  isLoading?: boolean;
  error?: string | null;
  className?: string;
  onVideoReady?: (video: HTMLVideoElement) => void;
}

export const VideoCapture = forwardRef<HTMLVideoElement, VideoCaptureProps>(
  ({ stream, isLoading, error, className = '', onVideoReady }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const internalRef = (ref as React.RefObject<HTMLVideoElement>) || videoRef;

    useEffect(() => {
      const video = internalRef.current;
      if (!video) return;

      if (stream) {
        // Set stream to video element
        video.srcObject = stream;

        // Play video when metadata is loaded
        video.onloadedmetadata = () => {
          video
            .play()
            .then(() => {
              console.log('Video playback started');
              onVideoReady?.(video);
            })
            .catch((err) => {
              console.error('Failed to play video:', err);
            });
        };
      } else {
        // Clear video when stream is removed
        video.srcObject = null;
      }

      return () => {
        if (video) {
          video.srcObject = null;
        }
      };
    }, [stream, internalRef, onVideoReady]);

    return (
      <div className={`relative ${className}`}>
        {/* Video Element */}
        <video
          ref={internalRef}
          autoPlay
          playsInline
          muted
          className={`w-full h-full object-cover rounded-lg bg-black ${
            !stream ? 'hidden' : ''
          }`}
        />

        {/* Loading State */}
        {isLoading && !stream && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/80 rounded-lg">
            <div className="text-center space-y-4">
              <Camera className="w-16 h-16 mx-auto text-gray-400 animate-pulse" />
              <p className="text-gray-300 text-sm">Accessing camera...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && !stream && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/90 rounded-lg p-6">
            <Alert variant="destructive" className="max-w-md">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </div>
        )}

        {/* No Stream Placeholder */}
        {!stream && !isLoading && !error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-900 rounded-lg">
            <div className="text-center space-y-4">
              <Camera className="w-16 h-16 mx-auto text-gray-600" />
              <p className="text-gray-400 text-sm">Camera not active</p>
            </div>
          </div>
        )}
      </div>
    );
  }
);

VideoCapture.displayName = 'VideoCapture';
