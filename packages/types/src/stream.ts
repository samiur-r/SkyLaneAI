/**
 * WebRTC and streaming types
 */

import { Detection } from './detection';

export type ConnectionStatus =
  | 'disconnected'
  | 'connecting'
  | 'connected'
  | 'reconnecting'
  | 'error';

export interface StreamStats {
  framesReceived: number;
  framesProcessed: number;
  framesSkipped: number;
  avgProcessingTime: number;
  detectionsCount?: number;
}

export interface StreamSettings {
  fps: number;
  skipFrames: boolean;
  confidenceThreshold?: number;
}

// WebSocket message types (Client -> Server)
export interface WSOfferMessage {
  type: 'offer';
  sdp: string;
}

export interface WSIceCandidateMessage {
  type: 'ice_candidate';
  candidate: string;
  sdpMid: string | null;
  sdpMLineIndex: number | null;
}

export interface WSSettingsMessage {
  type: 'settings';
  fps?: number;
  skipFrames?: boolean;
  confidenceThreshold?: number;
}

export interface WSGetStatsMessage {
  type: 'get_stats';
}

export interface WSPingMessage {
  type: 'ping';
}

export type WSClientMessage =
  | WSOfferMessage
  | WSIceCandidateMessage
  | WSSettingsMessage
  | WSGetStatsMessage
  | WSPingMessage;

// WebSocket message types (Server -> Client)
export interface WSAnswerMessage {
  type: 'answer';
  sdp: string;
}

export interface WSDetectionMessage {
  type: 'detection';
  data: {
    frameNumber: number;
    timestamp: number;
    detections: Array<{
      class_name: string;
      class_id: number;
      confidence: number;
      bbox: {
        x1: number;
        y1: number;
        x2: number;
        y2: number;
      };
    }>;
    processingTimeMs: number;
    stats: {
      frames_received: number;
      frames_processed: number;
      frames_skipped: number;
      avg_processing_time: number;
      detections_count: number;
    };
  };
}

export interface WSStatsMessage {
  type: 'stats';
  data: StreamStats;
}

export interface WSErrorMessage {
  type: 'error';
  message: string;
}

export interface WSPongMessage {
  type: 'pong';
}

export type WSServerMessage =
  | WSAnswerMessage
  | WSDetectionMessage
  | WSStatsMessage
  | WSErrorMessage
  | WSPongMessage;

// Camera device info
export interface CameraDevice {
  deviceId: string;
  label: string;
  groupId: string;
}

// Detection result with normalized data
export interface NormalizedDetection extends Detection {
  color: string;
}
