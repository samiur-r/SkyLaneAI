/**
 * Hook for managing video WebSocket connection and detection streaming
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import type {
  WSDetectionMessage,
  WSVideoServerMessage,
  VideoProcessingProgress
} from '@repo/types';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

export interface UseVideoStreamOptions {
  videoId: string | null;
  onDetection?: (message: WSDetectionMessage) => void;
  onProgress?: (progress: VideoProcessingProgress) => void;
  onCompleted?: () => void;
  onError?: (error: string) => void;
}

export type VideoConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'error';

export interface UseVideoStreamReturn {
  connectionStatus: VideoConnectionStatus;
  isConnected: boolean;
  progress: VideoProcessingProgress | null;
  connect: () => Promise<void>;
  disconnect: () => void;
  play: (speed?: number) => void;
  pause: () => void;
  resume: () => void;
  stop: () => void;
  seek: (options: { frameNumber?: number; timestamp?: number }) => void;
  updateSettings: (settings: {
    processFps?: number;
    confidenceThreshold?: number;
    playbackSpeed?: number;
  }) => void;
}

export function useVideoStream(options: UseVideoStreamOptions): UseVideoStreamReturn {
  const { videoId, onDetection, onProgress, onCompleted, onError } = options;

  const [connectionStatus, setConnectionStatus] = useState<VideoConnectionStatus>('disconnected');
  const [progress, setProgress] = useState<VideoProcessingProgress | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const isConnected = connectionStatus === 'connected';

  /**
   * Send message to WebSocket server
   */
  const sendMessage = useCallback((message: object) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket not connected, message not sent:', message);
    }
  }, []);

  /**
   * Connect to WebSocket
   */
  const connect = useCallback(async () => {
    if (!videoId) {
      console.error('Cannot connect: videoId is null');
      return;
    }

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      console.log('Already connected');
      return;
    }

    try {
      setConnectionStatus('connecting');

      const wsUrl = `${WS_URL}/api/v1/video/ws/${videoId}`;
      console.log('Connecting to video WebSocket:', wsUrl);

      const ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        console.log('Video WebSocket connected');
        setConnectionStatus('connected');
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WSVideoServerMessage | WSDetectionMessage;

          switch (message.type) {
            case 'detection':
              onDetection?.(message as WSDetectionMessage);
              break;

            case 'progress':
              const progressData = (message as any).data;
              setProgress(progressData);
              onProgress?.(progressData);
              break;

            case 'completed':
              console.log('Video processing completed');
              onCompleted?.();
              break;

            case 'started':
            case 'paused':
            case 'resumed':
            case 'stopped':
            case 'seeked':
              console.log('Video state:', message.type);
              break;

            case 'error':
              const errorMsg = (message as any).message || 'Unknown error';
              console.error('Video WebSocket error:', errorMsg);
              onError?.(errorMsg);
              break;

            default:
              console.log('Unknown message type:', (message as any).type);
          }
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      ws.onerror = (error) => {
        console.error('Video WebSocket error:', error);
        setConnectionStatus('error');
        onError?.('WebSocket connection error');
      };

      ws.onclose = () => {
        console.log('Video WebSocket disconnected');
        setConnectionStatus('disconnected');
        wsRef.current = null;
      };

      wsRef.current = ws;
    } catch (err) {
      console.error('Failed to connect:', err);
      setConnectionStatus('error');
      onError?.(err instanceof Error ? err.message : 'Connection failed');
    }
  }, [videoId, onDetection, onProgress, onCompleted, onError]);

  /**
   * Disconnect from WebSocket
   */
  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setConnectionStatus('disconnected');
    setProgress(null);
  }, []);

  /**
   * Start video processing
   */
  const play = useCallback((speed: number = 1.0) => {
    sendMessage({ type: 'start', speed });
  }, [sendMessage]);

  /**
   * Pause video processing
   */
  const pause = useCallback(() => {
    sendMessage({ type: 'pause' });
  }, [sendMessage]);

  /**
   * Resume video processing
   */
  const resume = useCallback(() => {
    sendMessage({ type: 'resume' });
  }, [sendMessage]);

  /**
   * Stop video processing
   */
  const stop = useCallback(() => {
    sendMessage({ type: 'stop' });
  }, [sendMessage]);

  /**
   * Seek to frame or timestamp
   */
  const seek = useCallback((options: { frameNumber?: number; timestamp?: number }) => {
    sendMessage({
      type: 'seek',
      frame_number: options.frameNumber,
      timestamp: options.timestamp,
    });
  }, [sendMessage]);

  /**
   * Update processing settings
   */
  const updateSettings = useCallback((settings: {
    processFps?: number;
    confidenceThreshold?: number;
    playbackSpeed?: number;
  }) => {
    sendMessage({
      type: 'settings',
      data: {
        process_fps: settings.processFps,
        confidence_threshold: settings.confidenceThreshold,
        playback_speed: settings.playbackSpeed,
      },
    });
  }, [sendMessage]);

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    connectionStatus,
    isConnected,
    progress,
    connect,
    disconnect,
    play,
    pause,
    resume,
    stop,
    seek,
    updateSettings,
  };
}
