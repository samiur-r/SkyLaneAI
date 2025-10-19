/**
 * Video Upload Component
 * Drag-and-drop or click to upload video files
 */

'use client';

import { useCallback, useState } from 'react';
import { Upload, FileVideo, AlertCircle, CheckCircle2, X } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import type { VideoUploadMetadata } from '@repo/types';

export interface VideoUploadProps {
  onUploadComplete: (metadata: VideoUploadMetadata) => void;
  onUploadStart?: () => void;
  isUploading: boolean;
  uploadProgress: number;
  error: string | null;
  className?: string;
}

export function VideoUpload({
  onUploadComplete,
  onUploadStart,
  isUploading,
  uploadProgress,
  error,
  className = '',
}: VideoUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  /**
   * Handle file selection
   */
  const handleFileSelect = useCallback(
    (file: File) => {
      // Validate file type
      const allowedExtensions = ['.mp4', '.avi', '.mov', '.mkv'];
      const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

      if (!allowedExtensions.includes(fileExtension)) {
        return;
      }

      setSelectedFile(file);
      onUploadStart?.();
    },
    [onUploadStart]
  );

  /**
   * Handle file input change
   */
  const handleFileInputChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        handleFileSelect(file);
      }
    },
    [handleFileSelect]
  );

  /**
   * Handle drag over
   */
  const handleDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  }, []);

  /**
   * Handle drag leave
   */
  const handleDragLeave = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
  }, []);

  /**
   * Handle drop
   */
  const handleDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();
      setIsDragging(false);

      const file = event.dataTransfer.files?.[0];
      if (file) {
        handleFileSelect(file);
      }
    },
    [handleFileSelect]
  );

  /**
   * Clear selected file
   */
  const handleClear = useCallback(() => {
    setSelectedFile(null);
  }, []);

  /**
   * Format file size
   */
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className={className}>
      {/* Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-12 text-center
          transition-colors duration-200 cursor-pointer
          ${isDragging ? 'border-primary bg-primary/5' : 'border-gray-300 dark:border-gray-700'}
          ${isUploading ? 'pointer-events-none opacity-60' : 'hover:border-primary hover:bg-primary/5'}
        `}
        onClick={() => {
          if (!isUploading) {
            document.getElementById('video-upload-input')?.click();
          }
        }}
      >
        <input
          id="video-upload-input"
          type="file"
          accept="video/mp4,video/avi,video/mov,video/x-matroska,.mp4,.avi,.mov,.mkv"
          onChange={handleFileInputChange}
          className="hidden"
          disabled={isUploading}
        />

        <div className="space-y-4">
          {/* Upload Icon */}
          {isUploading ? (
            <FileVideo className="w-16 h-16 mx-auto text-primary animate-pulse" />
          ) : (
            <Upload className="w-16 h-16 mx-auto text-gray-400" />
          )}

          {/* Upload Text */}
          <div>
            <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
              {isUploading ? 'Uploading video...' : 'Drop video file here'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              or click to browse
            </p>
          </div>

          {/* Supported Formats */}
          <div className="text-xs text-gray-400">
            Supported formats: MP4, AVI, MOV, MKV
            <br />
            Maximum file size: 100 MB
          </div>

          {/* Selected File Info */}
          {selectedFile && !isUploading && (
            <Card className="max-w-md mx-auto p-4 bg-gray-50 dark:bg-gray-800">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3 flex-1 min-w-0">
                  <FileVideo className="w-5 h-5 flex-shrink-0 text-primary mt-0.5" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                      {selectedFile.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {formatFileSize(selectedFile.size)}
                    </p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleClear();
                  }}
                  className="flex-shrink-0"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </Card>
          )}

          {/* Upload Progress */}
          {isUploading && uploadProgress > 0 && (
            <div className="max-w-md mx-auto space-y-2">
              <Progress value={uploadProgress} className="h-2" />
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {uploadProgress}% complete
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mt-4">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Success Message */}
      {uploadProgress === 100 && !error && (
        <Alert className="mt-4 border-green-500 bg-green-50 dark:bg-green-950">
          <CheckCircle2 className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800 dark:text-green-200">
            Video uploaded successfully!
          </AlertDescription>
        </Alert>
      )}
    </div>
  );
}
