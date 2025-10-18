/**
 * Detection Stats Component
 * Displays real-time detection statistics
 */

'use client';

import { Activity, Target, Zap, Timer } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { StreamStats } from '@skylane/types';

export interface DetectionStatsProps {
  stats: StreamStats | null;
  detectionCount: number;
  processingTimeMs: number;
  latestFrame: number | null;
  className?: string;
}

export function DetectionStats({
  stats,
  detectionCount,
  processingTimeMs,
  latestFrame,
  className = '',
}: DetectionStatsProps) {
  const calculateFPS = () => {
    if (!stats || stats.avgProcessingTime === 0) return 0;
    return Math.round(1000 / stats.avgProcessingTime);
  };

  const formatNumber = (num: number) => {
    return num.toLocaleString();
  };

  return (
    <Card className={className}>
      <CardContent className="p-6">
        <div className="space-y-4">
          {/* Title */}
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Detection Stats</h3>
            <Badge variant="outline" className="font-mono text-xs">
              Frame #{latestFrame || 0}
            </Badge>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            {/* Current Detections */}
            <div className="flex items-start space-x-3">
              <div className="p-2 bg-blue-500/10 rounded-lg">
                <Target className="w-5 h-5 text-blue-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Detections
                </p>
                <p className="text-2xl font-bold">{detectionCount}</p>
              </div>
            </div>

            {/* Processing Time */}
            <div className="flex items-start space-x-3">
              <div className="p-2 bg-green-500/10 rounded-lg">
                <Timer className="w-5 h-5 text-green-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Latency
                </p>
                <p className="text-2xl font-bold">
                  {processingTimeMs > 0 ? Math.round(processingTimeMs) : 0}
                  <span className="text-sm font-normal ml-1">ms</span>
                </p>
              </div>
            </div>

            {/* Processing FPS */}
            <div className="flex items-start space-x-3">
              <div className="p-2 bg-purple-500/10 rounded-lg">
                <Zap className="w-5 h-5 text-purple-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Processing FPS
                </p>
                <p className="text-2xl font-bold">
                  {calculateFPS()}
                  <span className="text-sm font-normal ml-1">fps</span>
                </p>
              </div>
            </div>

            {/* Total Detections */}
            <div className="flex items-start space-x-3">
              <div className="p-2 bg-amber-500/10 rounded-lg">
                <Activity className="w-5 h-5 text-amber-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Total Count
                </p>
                <p className="text-2xl font-bold">
                  {stats?.detectionsCount
                    ? formatNumber(stats.detectionsCount)
                    : 0}
                </p>
              </div>
            </div>
          </div>

          {/* Frame Stats */}
          {stats && (
            <div className="pt-4 border-t space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">
                  Frames Received
                </span>
                <span className="font-mono font-medium">
                  {formatNumber(stats.framesReceived)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">
                  Frames Processed
                </span>
                <span className="font-mono font-medium">
                  {formatNumber(stats.framesProcessed)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">
                  Frames Skipped
                </span>
                <span className="font-mono font-medium text-amber-600">
                  {formatNumber(stats.framesSkipped)}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500 dark:text-gray-400">
                  Avg Processing Time
                </span>
                <span className="font-mono font-medium">
                  {Math.round(stats.avgProcessingTime)}ms
                </span>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
