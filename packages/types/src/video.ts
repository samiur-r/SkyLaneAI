/**
 * Video stream and metadata types
 */

export type VideoStatus = 'idle' | 'streaming' | 'processing' | 'completed' | 'error';

export interface VideoMetadata {
  width: number;
  height: number;
  fps?: number;
  duration?: number;
  codec?: string;
}

export interface VideoStream {
  id: string;
  status: VideoStatus;
  metadata?: VideoMetadata;
  startedAt?: string;
  endedAt?: string;
}

export interface StreamConfig {
  maxFps?: number;
  resolution?: {
    width: number;
    height: number;
  };
  enableAudio?: boolean;
}
