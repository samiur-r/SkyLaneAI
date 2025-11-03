/**
 * MJPEG Video Player Component
 * Displays annotated video stream from backend with detections already rendered
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { AlertCircle } from 'lucide-react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface MjpegPlayerProps {
  videoId: string;
  className?: string;
  onError?: (error: Error) => void;
  onLoad?: () => void;
  onEnded?: () => void;
  streamKey?: number;
}

export function MjpegPlayer({
  videoId,
  className = '',
  onError,
  onLoad,
  onEnded,
  streamKey = 0,
}: MjpegPlayerProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const imgRef = useRef<HTMLImageElement>(null);
  const hasStreamEndedRef = useRef(false);

  // Use streamKey from parent, combined with retry count for error retries
  const urlKey = streamKey * 1000 + retryCount;
  const streamUrl = `${API_URL}/api/v1/video/${videoId}/mjpeg?t=${urlKey}`;

  const handleLoad = () => {
    setIsLoading(false);
    setError(null);
    hasStreamEndedRef.current = false;
    onLoad?.();
  };

  const handleError = () => {
    // MJPEG streams end by closing the connection, which triggers an error
    // If we've already loaded successfully, this is likely the stream ending
    if (!isLoading && !error) {
      hasStreamEndedRef.current = true;
      onEnded?.();
      return;
    }

    const err = new Error('Failed to load MJPEG stream. Make sure processing has started.');
    setError(err);
    setIsLoading(false);
    onError?.(err);
  };

  const retry = () => {
    setIsLoading(true);
    setError(null);
    setRetryCount((prev) => prev + 1);
  };

  // Reset state when streamKey changes (for replay)
  useEffect(() => {
    setIsLoading(true);
    setError(null);
    setRetryCount(0);
    hasStreamEndedRef.current = false;
  }, [streamKey]);

  if (error) {
    return (
      <div className={`p-4 ${className}`}>
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error.message}</AlertDescription>
        </Alert>
        <Button onClick={retry} variant="outline" className="mt-4 w-full">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
          <div className="text-center space-y-4">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent" />
            <p className="text-sm text-gray-400">Loading MJPEG stream...</p>
          </div>
        </div>
      )}
      <img
        ref={imgRef}
        src={streamUrl}
        alt="MJPEG Video Stream with Detections"
        className="w-full h-auto bg-black"
        onLoad={handleLoad}
        onError={handleError}
      />
    </div>
  );
}
