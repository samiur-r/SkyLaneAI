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
    frameWidth: number;
    frameHeight: number;
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

// Time-based alert message (NEW)
export interface WSTimeBasedAlertMessage {
  type: 'time_based_alert';
  data: {
    second: number;
    timestamp: number;
    alert: {
      detection: {
        class_name: string;
        class_id: number;
        confidence: number;
        bbox: {
          x1: number;
          y1: number;
          x2: number;
          y2: number;
        };
      };
      context: {
        estimated_size: string;
        bbox_area_pixels: number;
        screen_position: string;
        threat_level_raw: string;
      };
      message: {
        title: string;
        emoji: string;
        body: string;
        sections: Record<string, string>;
      };
      action: {
        primary_action: string;
        secondary_action: string;
        reasoning: string;
        urgency: string;
      };
      priority: {
        overall_score: number;
        priority_level: string;
        factors: Record<string, {
          value: string | number;
          score: number;
          weight: number;
        }>;
      };
    };
  };
}

export type WSServerMessage =
  | WSAnswerMessage
  | WSDetectionMessage
  | WSStatsMessage
  | WSErrorMessage
  | WSPongMessage
  | WSTimeBasedAlertMessage;

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

// Time-based alert for timeline display
export interface TimeBasedAlert {
  second: number;
  timestamp: number;
  priorityLevel: 'critical' | 'high' | 'medium' | 'low';
  priorityScore: number;
  title: string;
  emoji: string;
  hazardType: string;
  primaryAction: string;
  urgency: 'immediate' | 'urgent' | 'caution' | 'advisory';
  fullAlert: WSTimeBasedAlertMessage['data']['alert'];
}
