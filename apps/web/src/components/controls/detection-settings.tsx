/**
 * Detection Settings Component
 * Controls for configuring detection parameters
 */

'use client';

import { useState } from 'react';
import { Settings, Zap, Target } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import type { StreamSettings } from '@repo/types';

export interface DetectionSettingsProps {
  settings: StreamSettings;
  onSettingsChange: (settings: Partial<StreamSettings>) => void;
  disabled?: boolean;
  className?: string;
}

export function DetectionSettings({
  settings,
  onSettingsChange,
  disabled = false,
  className = '',
}: DetectionSettingsProps) {
  const [localConfidence, setLocalConfidence] = useState(
    settings.confidenceThreshold || 0.25
  );

  const handleConfidenceChange = (value: number[]) => {
    const newValue = value[0];
    setLocalConfidence(newValue);
  };

  const handleConfidenceCommit = (value: number[]) => {
    onSettingsChange({ confidenceThreshold: value[0] });
  };

  const handleFpsChange = (value: string) => {
    onSettingsChange({ fps: parseInt(value, 10) });
  };

  const handleSkipFramesChange = (checked: boolean) => {
    onSettingsChange({ skipFrames: checked });
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Settings className="w-5 h-5" />
          Detection Settings
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Confidence Threshold */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Label className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              Confidence Threshold
            </Label>
            <span className="text-sm font-mono font-semibold">
              {(localConfidence * 100).toFixed(0)}%
            </span>
          </div>
          <Slider
            value={[localConfidence]}
            onValueChange={handleConfidenceChange}
            onValueCommit={handleConfidenceCommit}
            min={0.1}
            max={1.0}
            step={0.05}
            disabled={disabled}
            className="w-full"
          />
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Only show detections with confidence above this threshold
          </p>
        </div>

        {/* Processing FPS */}
        <div className="space-y-3">
          <Label className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Processing FPS
          </Label>
          <Select
            value={settings.fps.toString()}
            onValueChange={handleFpsChange}
            disabled={disabled}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="5">5 FPS (Low CPU)</SelectItem>
              <SelectItem value="10">10 FPS (Recommended)</SelectItem>
              <SelectItem value="15">15 FPS (Balanced)</SelectItem>
              <SelectItem value="20">20 FPS (High)</SelectItem>
              <SelectItem value="30">30 FPS (Maximum)</SelectItem>
            </SelectContent>
          </Select>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Higher FPS = more detections but higher CPU usage
          </p>
        </div>

        {/* Frame Skipping */}
        <div className="flex items-center justify-between space-x-2">
          <div className="flex-1">
            <Label htmlFor="skip-frames" className="text-sm font-medium">
              Enable Frame Skipping
            </Label>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Skip frames when processing is slow to reduce latency
            </p>
          </div>
          <Switch
            id="skip-frames"
            checked={settings.skipFrames}
            onCheckedChange={handleSkipFramesChange}
            disabled={disabled}
          />
        </div>

        {/* Info Section */}
        <div className="pt-4 border-t">
          <div className="bg-blue-50 dark:bg-blue-950/20 p-3 rounded-lg">
            <p className="text-xs text-blue-900 dark:text-blue-100">
              <strong>Tip:</strong> For best performance, use 10 FPS with frame
              skipping enabled. Increase FPS for smoother detection if your device
              can handle it.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
