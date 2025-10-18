/**
 * Hook for managing camera/media stream access
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import type { CameraDevice } from '@repo/types';

export interface UseMediaStreamOptions {
  video?: boolean | MediaTrackConstraints;
  audio?: boolean | MediaTrackConstraints;
  deviceId?: string;
}

export interface UseMediaStreamReturn {
  stream: MediaStream | null;
  devices: CameraDevice[];
  selectedDevice: string | null;
  isLoading: boolean;
  error: string | null;
  requestStream: () => Promise<void>;
  stopStream: () => void;
  switchDevice: (deviceId: string) => Promise<void>;
  refreshDevices: () => Promise<void>;
}

export function useMediaStream(
  options: UseMediaStreamOptions = { video: true, audio: false }
): UseMediaStreamReturn {
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [devices, setDevices] = useState<CameraDevice[]>([]);
  const [selectedDevice, setSelectedDevice] = useState<string | null>(options.deviceId || null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  /**
   * Get list of available camera devices
   */
  const refreshDevices = useCallback(async () => {
    try {
      // Check if mediaDevices API is available
      if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
        console.error('Media Devices API not supported');
        setDevices([]);
        return;
      }

      const deviceList = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = deviceList
        .filter((device) => device.kind === 'videoinput')
        .filter((device) => device.deviceId !== '') // Filter out empty device IDs
        .map((device) => ({
          deviceId: device.deviceId,
          label: device.label || `Camera ${device.deviceId.slice(0, 5)}`,
          groupId: device.groupId,
        }));

      setDevices(videoDevices);

      // Select first device if none selected
      if (!selectedDevice && videoDevices.length > 0) {
        setSelectedDevice(videoDevices[0].deviceId);
      }
    } catch (err) {
      console.error('Failed to enumerate devices:', err);
      // Don't set error here - devices might populate after permission is granted
      setDevices([]);
    }
  }, [selectedDevice]);

  /**
   * Request camera access
   */
  const requestStream = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Stop existing stream
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }

      // Build constraints
      const constraints: MediaStreamConstraints = {
        audio: options.audio || false,
        video: options.video
          ? typeof options.video === 'boolean'
            ? {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                frameRate: { ideal: 30 },
                ...(selectedDevice && { deviceId: { exact: selectedDevice } }),
              }
            : {
                ...options.video,
                ...(selectedDevice && { deviceId: { exact: selectedDevice } }),
              }
          : false,
      };

      // Request media stream
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = mediaStream;
      setStream(mediaStream);

      // Refresh device list (labels will now be available)
      await refreshDevices();

      setIsLoading(false);
    } catch (err) {
      console.error('Failed to get media stream:', err);

      let errorMessage = 'Failed to access camera';
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError') {
          errorMessage = 'Camera access denied. Please grant camera permissions.';
        } else if (err.name === 'NotFoundError') {
          errorMessage = 'No camera found. Please connect a camera.';
        } else if (err.name === 'NotReadableError') {
          errorMessage = 'Camera is already in use by another application.';
        } else if (err.name === 'OverconstrainedError') {
          errorMessage = 'Camera does not support the requested settings.';
        } else {
          errorMessage = err.message;
        }
      }

      setError(errorMessage);
      setIsLoading(false);
      streamRef.current = null;
      setStream(null);
    }
  }, [options.audio, options.video, selectedDevice, refreshDevices]);

  /**
   * Stop current stream
   */
  const stopStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });
      streamRef.current = null;
      setStream(null);
    }
  }, []);

  /**
   * Switch to different camera device
   */
  const switchDevice = useCallback(
    async (deviceId: string) => {
      // Ignore empty strings
      if (!deviceId || deviceId.trim() === '') {
        return;
      }
      setSelectedDevice(deviceId);
      if (streamRef.current) {
        // Re-request stream with new device
        await requestStream();
      }
    },
    [requestStream]
  );

  /**
   * Cleanup on unmount
   */
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  /**
   * Refresh devices on mount
   */
  useEffect(() => {
    refreshDevices();
  }, [refreshDevices]);

  return {
    stream,
    devices,
    selectedDevice,
    isLoading,
    error,
    requestStream,
    stopStream,
    switchDevice,
    refreshDevices,
  };
}
