/**
 * Hook for managing WebRTC connection
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { WebRTCClient } from '@/lib/webrtc-client';
import type {
  ConnectionStatus,
  WSDetectionMessage,
  StreamStats,
  StreamSettings,
} from '@repo/types';

export interface UseWebRTCOptions {
  wsUrl: string;
  onDetection?: (message: WSDetectionMessage) => void;
  onError?: (error: string) => void;
  autoConnect?: boolean;
}

export interface UseWebRTCReturn {
  client: WebRTCClient | null;
  connectionStatus: ConnectionStatus;
  stats: StreamStats | null;
  isConnected: boolean;
  connect: () => Promise<void>;
  disconnect: () => void;
  addVideoStream: (stream: MediaStream) => Promise<void>;
  updateSettings: (settings: Partial<StreamSettings>) => void;
  requestStats: () => void;
}

export function useWebRTC(options: UseWebRTCOptions): UseWebRTCReturn {
  const [client, setClient] = useState<WebRTCClient | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
  const [stats, setStats] = useState<StreamStats | null>(null);
  const clientRef = useRef<WebRTCClient | null>(null);
  const isConnecting = useRef(false);

  /**
   * Initialize WebRTC client
   */
  const initializeClient = useCallback(() => {
    if (clientRef.current) {
      return clientRef.current;
    }

    const newClient = new WebRTCClient({
      wsUrl: options.wsUrl,
      onConnectionStatusChange: (status) => {
        setConnectionStatus(status);
      },
      onDetection: (message) => {
        // Update stats from detection message
        if (message.data.stats) {
          setStats({
            framesReceived: message.data.stats.frames_received,
            framesProcessed: message.data.stats.frames_processed,
            framesSkipped: message.data.stats.frames_skipped,
            avgProcessingTime: message.data.stats.avg_processing_time,
            detectionsCount: message.data.stats.detections_count,
          });
        }
        options.onDetection?.(message);
      },
      onStats: (statsData) => {
        setStats(statsData);
      },
      onError: (error) => {
        console.error('WebRTC error:', error);
        options.onError?.(error);
      },
    });

    clientRef.current = newClient;
    setClient(newClient);
    return newClient;
  }, [options]);

  /**
   * Connect to WebRTC server
   */
  const connect = useCallback(async () => {
    if (isConnecting.current) {
      console.warn('Already connecting...');
      return;
    }

    isConnecting.current = true;

    try {
      const rtcClient = initializeClient();
      await rtcClient.connect();
    } catch (error) {
      console.error('Failed to connect:', error);
      throw error;
    } finally {
      isConnecting.current = false;
    }
  }, [initializeClient]);

  /**
   * Disconnect from WebRTC server
   */
  const disconnect = useCallback(() => {
    if (clientRef.current) {
      clientRef.current.disconnect();
      clientRef.current = null;
      setClient(null);
      setStats(null);
    }
  }, []);

  /**
   * Add video stream to connection
   */
  const addVideoStream = useCallback(
    async (stream: MediaStream) => {
      if (!clientRef.current) {
        throw new Error('WebRTC client not initialized. Call connect() first.');
      }

      try {
        await clientRef.current.addVideoTrack(stream);
      } catch (error) {
        console.error('Failed to add video stream:', error);
        throw error;
      }
    },
    []
  );

  /**
   * Update stream settings
   */
  const updateSettings = useCallback((settings: Partial<StreamSettings>) => {
    if (clientRef.current) {
      clientRef.current.updateSettings(settings);
    }
  }, []);

  /**
   * Request current statistics
   */
  const requestStats = useCallback(() => {
    if (clientRef.current) {
      clientRef.current.requestStats();
    }
  }, []);

  /**
   * Auto-connect on mount if enabled
   */
  useEffect(() => {
    if (options.autoConnect) {
      connect().catch((error) => {
        console.error('Auto-connect failed:', error);
      });
    }

    // Cleanup on unmount
    return () => {
      if (clientRef.current) {
        clientRef.current.disconnect();
      }
    };
  }, []); // Only run on mount/unmount

  const isConnected = connectionStatus === 'connected';

  return {
    client,
    connectionStatus,
    stats,
    isConnected,
    connect,
    disconnect,
    addVideoStream,
    updateSettings,
    requestStats,
  };
}
