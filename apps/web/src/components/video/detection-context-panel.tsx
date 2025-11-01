/**
 * Detection Context Panel Component
 * Displays enriched context information from the Context Enrichment Agent
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle, Target, MapPin, Ruler } from 'lucide-react';
import type { NormalizedDetection } from '@repo/types';

export interface DetectionContextPanelProps {
  detections: NormalizedDetection[];
  className?: string;
}

export function DetectionContextPanel({
  detections,
  className = '',
}: DetectionContextPanelProps) {
  // Filter detections that have context
  const detectionsWithContext = detections.filter(d => d.context);

  if (detectionsWithContext.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="text-lg">Detection Context</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            No detections with context available.
            Process a video to see enriched context information.
          </p>
        </CardContent>
      </Card>
    );
  }

  const getThreatColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      case 'high':
        return 'bg-orange-500/10 text-orange-500 border-orange-500/20';
      case 'moderate':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
      case 'low':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  const getSizeColor = (size: string) => {
    switch (size.toLowerCase()) {
      case 'large':
        return 'bg-red-500';
      case 'medium':
        return 'bg-orange-500';
      case 'small':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  const formatAreaPixels = (pixels: number) => {
    return pixels.toLocaleString() + ' px²';
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Target className="w-5 h-5" />
          Detection Context
          <Badge variant="secondary" className="ml-auto">
            {detectionsWithContext.length} object{detectionsWithContext.length !== 1 ? 's' : ''}
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 max-h-[400px] overflow-y-auto">
          {detectionsWithContext.map((detection, index) => {
            const context = detection.context!;

            return (
              <div
                key={detection.id || index}
                className="p-4 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="font-semibold text-sm capitalize">
                      {detection.className}
                    </h4>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Confidence: {(detection.confidence * 100).toFixed(0)}%
                    </p>
                  </div>
                  <Badge
                    variant="outline"
                    className={`${getThreatColor(context.threat_level_raw)} border font-semibold`}
                  >
                    {context.threat_level_raw.toUpperCase()}
                  </Badge>
                </div>

                {/* Context Details */}
                <div className="grid grid-cols-3 gap-3">
                  {/* Size */}
                  <div className="flex items-start gap-2">
                    <div className={`p-1.5 ${getSizeColor(context.estimated_size)}/10 rounded`}>
                      <Ruler className={`w-4 h-4 ${getSizeColor(context.estimated_size).replace('bg-', 'text-')}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Size
                      </p>
                      <p className="text-sm font-medium capitalize">
                        {context.estimated_size}
                      </p>
                    </div>
                  </div>

                  {/* Position */}
                  <div className="flex items-start gap-2">
                    <div className="p-1.5 bg-purple-500/10 rounded">
                      <MapPin className="w-4 h-4 text-purple-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Position
                      </p>
                      <p className="text-sm font-medium capitalize">
                        {context.screen_position}
                      </p>
                    </div>
                  </div>

                  {/* Area */}
                  <div className="flex items-start gap-2">
                    <div className="p-1.5 bg-blue-500/10 rounded">
                      <Target className="w-4 h-4 text-blue-500" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Area
                      </p>
                      <p className="text-xs font-medium font-mono">
                        {formatAreaPixels(context.bbox_area_pixels)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
