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

// Video Upload Types
export interface VideoUploadMetadata {
  videoId: string;
  filename: string;
  duration: number;
  fps: number;
  totalFrames: number;
  width: number;
  height: number;
  sizeMb: number;
  codec: string;
}

export interface VideoProcessingProgress {
  currentFrame: number;
  totalFrames: number;
  percentage: number;
}

export interface VideoPlaybackState {
  isPlaying: boolean;
  isPaused: boolean;
  currentTime: number;
  speed: number;
}

// Video WebSocket Message Types (Client -> Server)
export interface WSVideoStartMessage {
  type: 'start';
  speed?: number;
}

export interface WSVideoPauseMessage {
  type: 'pause';
}

export interface WSVideoResumeMessage {
  type: 'resume';
}

export interface WSVideoStopMessage {
  type: 'stop';
}

export interface WSVideoSeekMessage {
  type: 'seek';
  frame_number?: number;
  timestamp?: number;
}

export interface WSVideoSettingsMessage {
  type: 'settings';
  data: {
    process_fps?: number;
    confidence_threshold?: number;
    playback_speed?: number;
  };
}

export type WSVideoClientMessage =
  | WSVideoStartMessage
  | WSVideoPauseMessage
  | WSVideoResumeMessage
  | WSVideoStopMessage
  | WSVideoSeekMessage
  | WSVideoSettingsMessage;

// Video WebSocket Message Types (Server -> Client)
export interface WSVideoProgressMessage {
  type: 'progress';
  data: VideoProcessingProgress;
}

export interface WSVideoCompletedMessage {
  type: 'completed';
}

export interface WSVideoStartedMessage {
  type: 'started';
}

export interface WSVideoPausedMessage {
  type: 'paused';
}

export interface WSVideoResumedMessage {
  type: 'resumed';
}

export interface WSVideoStoppedMessage {
  type: 'stopped';
}

export interface WSVideoSeekedMessage {
  type: 'seeked';
  frame_number: number;
}

export type WSVideoServerMessage =
  | WSVideoProgressMessage
  | WSVideoCompletedMessage
  | WSVideoStartedMessage
  | WSVideoPausedMessage
  | WSVideoResumedMessage
  | WSVideoStoppedMessage
  | WSVideoSeekedMessage;
