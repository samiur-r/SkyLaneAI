/**
 * Stream Controls Component
 * Controls for starting/stopping stream and selecting camera
 */

'use client';

import { Play, Square, Camera, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { ConnectionStatus, CameraDevice } from '@skylane/types';

export interface StreamControlsProps {
  isStreaming: boolean;
  isLoading: boolean;
  connectionStatus: ConnectionStatus;
  devices: CameraDevice[];
  selectedDevice: string | null;
  onStart: () => void;
  onStop: () => void;
  onDeviceChange: (deviceId: string) => void;
  className?: string;
}

export function StreamControls({
  isStreaming,
  isLoading,
  connectionStatus,
  devices,
  selectedDevice,
  onStart,
  onStop,
  onDeviceChange,
  className = '',
}: StreamControlsProps) {
  const getStatusBadge = () => {
    const variants: Record<
      ConnectionStatus,
      { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }
    > = {
      disconnected: { label: 'Disconnected', variant: 'secondary' },
      connecting: { label: 'Connecting...', variant: 'outline' },
      connected: { label: 'Connected', variant: 'default' },
      reconnecting: { label: 'Reconnecting...', variant: 'outline' },
      error: { label: 'Error', variant: 'destructive' },
    };

    const { label, variant } = variants[connectionStatus];

    return (
      <Badge variant={variant} className="ml-auto">
        {connectionStatus === 'connecting' || connectionStatus === 'reconnecting' ? (
          <Loader2 className="w-3 h-3 mr-1 animate-spin" />
        ) : null}
        {label}
      </Badge>
    );
  };

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Stream Controls</CardTitle>
          {getStatusBadge()}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Camera Selection */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Camera Device
          </label>
          <Select
            value={selectedDevice || undefined}
            onValueChange={onDeviceChange}
            disabled={isStreaming || devices.length === 0}
          >
            <SelectTrigger>
              <Camera className="w-4 h-4 mr-2" />
              <SelectValue placeholder="Select camera" />
            </SelectTrigger>
            <SelectContent>
              {devices.length === 0 ? (
                <SelectItem value="none" disabled>
                  No cameras found
                </SelectItem>
              ) : (
                devices.map((device) => (
                  <SelectItem key={device.deviceId} value={device.deviceId}>
                    {device.label}
                  </SelectItem>
                ))
              )}
            </SelectContent>
          </Select>
        </div>

        {/* Start/Stop Buttons */}
        <div className="flex gap-2">
          {!isStreaming ? (
            <Button
              onClick={onStart}
              disabled={isLoading || !selectedDevice}
              className="flex-1"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Starting...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Start Stream
                </>
              )}
            </Button>
          ) : (
            <Button
              onClick={onStop}
              variant="destructive"
              className="flex-1"
              size="lg"
            >
              <Square className="w-4 h-4 mr-2" />
              Stop Stream
            </Button>
          )}
        </div>

        {/* Info Text */}
        {!isStreaming && (
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            {devices.length === 0
              ? 'No camera detected. Please connect a camera.'
              : !selectedDevice
              ? 'Please select a camera to start streaming.'
              : 'Ready to start streaming. Click "Start Stream" to begin.'}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
