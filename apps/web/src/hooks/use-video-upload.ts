/**
 * Hook for managing video file uploads
 */

import { useState, useCallback } from 'react';
import type { VideoUploadMetadata } from '@repo/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface UseVideoUploadReturn {
  uploadVideo: (file: File) => Promise<VideoUploadMetadata | null>;
  deleteVideo: (videoId: string) => Promise<boolean>;
  uploadProgress: number;
  videoMetadata: VideoUploadMetadata | null;
  isUploading: boolean;
  error: string | null;
  clearError: () => void;
}

export function useVideoUpload(): UseVideoUploadReturn {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [videoMetadata, setVideoMetadata] = useState<VideoUploadMetadata | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Upload a video file
   */
  const uploadVideo = useCallback(async (file: File): Promise<VideoUploadMetadata | null> => {
    try {
      setIsUploading(true);
      setError(null);
      setUploadProgress(0);

      // Validate file type
      const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/x-matroska', 'video/quicktime'];
      if (!allowedTypes.includes(file.type) && !file.name.match(/\.(mp4|avi|mov|mkv)$/i)) {
        throw new Error('Invalid file type. Allowed formats: MP4, AVI, MOV, MKV');
      }

      // Validate file size (100MB max)
      const maxSizeMB = 100;
      const fileSizeMB = file.size / (1024 * 1024);
      if (fileSizeMB > maxSizeMB) {
        throw new Error(`File too large. Maximum size: ${maxSizeMB}MB`);
      }

      // Create form data
      const formData = new FormData();
      formData.append('file', file);

      // Upload with progress tracking
      const response = await fetch(`${API_URL}/api/v1/video/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
      }

      const metadata: VideoUploadMetadata = await response.json();

      // Map snake_case to camelCase
      const normalizedMetadata: VideoUploadMetadata = {
        videoId: metadata.video_id || (metadata as any).videoId,
        filename: metadata.filename,
        duration: metadata.duration,
        fps: metadata.fps,
        totalFrames: metadata.total_frames || (metadata as any).totalFrames,
        width: metadata.width,
        height: metadata.height,
        sizeMb: metadata.size_mb || (metadata as any).sizeMb,
        codec: metadata.codec,
      };

      setVideoMetadata(normalizedMetadata);
      setUploadProgress(100);

      return normalizedMetadata;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to upload video';
      setError(errorMessage);
      console.error('Upload error:', err);
      return null;
    } finally {
      setIsUploading(false);
    }
  }, []);

  /**
   * Delete an uploaded video
   */
  const deleteVideo = useCallback(async (videoId: string): Promise<boolean> => {
    try {
      setError(null);

      const response = await fetch(`${API_URL}/api/v1/video/${videoId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Delete failed' }));
        throw new Error(errorData.detail || `Delete failed: ${response.statusText}`);
      }

      // Clear metadata if this was the current video
      if (videoMetadata?.videoId === videoId) {
        setVideoMetadata(null);
        setUploadProgress(0);
      }

      return true;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete video';
      setError(errorMessage);
      console.error('Delete error:', err);
      return false;
    }
  }, [videoMetadata]);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    uploadVideo,
    deleteVideo,
    uploadProgress,
    videoMetadata,
    isUploading,
    error,
    clearError,
  };
}
