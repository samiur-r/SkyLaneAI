/**
 * Detection Debug Component
 * Shows raw detection data for debugging
 */

'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Bug } from 'lucide-react';
import type { NormalizedDetection } from '@repo/types';

export interface DetectionDebugProps {
  detections: NormalizedDetection[];
  className?: string;
}

export function DetectionDebug({
  detections,
  className = '',
}: DetectionDebugProps) {
  if (detections.length === 0) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Bug className="w-5 h-5" />
            Debug: No Detections
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-gray-500">
            No detections received yet. Upload and process a video to see detection data.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Take first 3 detections as sample
  const sampleDetections = detections.slice(0, 3);
  const detectionsWithContext = detections.filter(d => d.context);

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Bug className="w-5 h-5" />
          Debug: Detection Data
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="text-sm space-y-2">
          <p>
            <strong>Total Detections:</strong> {detections.length}
          </p>
          <p>
            <strong>Detections with Context:</strong> {detectionsWithContext.length}
          </p>
          <p className={detectionsWithContext.length > 0 ? 'text-green-600' : 'text-red-600'}>
            <strong>Status:</strong> {detectionsWithContext.length > 0
              ? '✓ Context data is being received'
              : '✗ Context data is NOT being received'}
          </p>
        </div>

        <div className="space-y-3">
          <p className="text-sm font-semibold">Sample Detections (first 3):</p>
          {sampleDetections.map((detection, index) => (
            <div key={detection.id || index} className="p-3 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono">
              <pre className="whitespace-pre-wrap overflow-auto max-h-40">
                {JSON.stringify({
                  id: detection.id,
                  className: detection.className,
                  confidence: detection.confidence,
                  hasContext: !!detection.context,
                  context: detection.context || 'NO CONTEXT',
                }, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
