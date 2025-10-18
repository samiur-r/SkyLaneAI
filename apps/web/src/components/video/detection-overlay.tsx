/**
 * Detection Overlay Component
 * Draws bounding boxes and labels on canvas over video
 */

'use client';

import { useEffect, useRef } from 'react';
import type { NormalizedDetection } from '@skylane/types';

export interface DetectionOverlayProps {
  detections: NormalizedDetection[];
  videoRef: React.RefObject<HTMLVideoElement>;
  className?: string;
}

export function DetectionOverlay({
  detections,
  videoRef,
  className = '',
}: DetectionOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    const video = videoRef.current;

    if (!canvas || !video) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Update canvas size to match video
    const updateCanvasSize = () => {
      if (video.videoWidth && video.videoHeight) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.style.width = `${video.clientWidth}px`;
        canvas.style.height = `${video.clientHeight}px`;
      }
    };

    // Draw detections on canvas
    const drawDetections = () => {
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update canvas size if video dimensions changed
      if (
        canvas.width !== video.videoWidth ||
        canvas.height !== video.videoHeight
      ) {
        updateCanvasSize();
      }

      // Draw each detection
      detections.forEach((detection) => {
        const { bbox, className, confidence, color } = detection;

        // Calculate box dimensions
        const boxWidth = bbox.x2 - bbox.x1;
        const boxHeight = bbox.y2 - bbox.y1;

        // Draw bounding box
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.strokeRect(bbox.x1, bbox.y1, boxWidth, boxHeight);

        // Draw filled background for label
        const label = `${className} ${(confidence * 100).toFixed(0)}%`;
        ctx.font = '16px Inter, sans-serif';
        const textMetrics = ctx.measureText(label);
        const textWidth = textMetrics.width + 12;
        const textHeight = 24;

        // Position label above box, or below if too close to top
        const labelY = bbox.y1 > 30 ? bbox.y1 - textHeight : bbox.y1 + boxHeight;

        // Draw label background
        ctx.fillStyle = color;
        ctx.fillRect(bbox.x1, labelY, textWidth, textHeight);

        // Draw label text
        ctx.fillStyle = '#ffffff';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, bbox.x1 + 6, labelY + textHeight / 2);
      });

      // Continue animation loop
      animationFrameRef.current = requestAnimationFrame(drawDetections);
    };

    // Start drawing when video is playing
    const handleVideoPlay = () => {
      updateCanvasSize();
      drawDetections();
    };

    // Listen for video events
    video.addEventListener('loadedmetadata', updateCanvasSize);
    video.addEventListener('play', handleVideoPlay);

    // Start drawing if video is already playing
    if (!video.paused && video.videoWidth) {
      handleVideoPlay();
    }

    // Handle window resize
    const handleResize = () => {
      updateCanvasSize();
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      video.removeEventListener('loadedmetadata', updateCanvasSize);
      video.removeEventListener('play', handleVideoPlay);
      window.removeEventListener('resize', handleResize);
    };
  }, [detections, videoRef]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{
        width: '100%',
        height: '100%',
      }}
    />
  );
}
