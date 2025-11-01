/**
 * Hook for managing detection results and visualization
 */

import { useState, useCallback, useRef } from 'react';
import type { WSDetectionMessage, NormalizedDetection } from '@repo/types';

export interface UseDetectionsOptions {
  confidenceThreshold?: number;
  maxDetections?: number;
}

export interface UseDetectionsReturn {
  detections: NormalizedDetection[];
  detectionCount: number;
  latestFrame: number | null;
  latestTimestamp: number | null;
  processingTimeMs: number;
  frameWidth: number | null;
  frameHeight: number | null;
  stats: {
    framesReceived: number;
    framesProcessed: number;
    framesSkipped: number;
    avgProcessingTime: number;
    detectionsCount: number;
  } | null;
  addDetectionResult: (message: WSDetectionMessage) => void;
  clearDetections: () => void;
  setConfidenceFilter: (threshold: number) => void;
}

// Color mapping for different object classes
const CLASS_COLORS: Record<string, string> = {
  bird: '#ef4444', // red
  drone: '#f59e0b', // amber
  aircraft: '#3b82f6', // blue
  person: '#10b981', // green
  car: '#8b5cf6', // purple
  balloon: '#ec4899', // pink
  kite: '#14b8a6', // teal
  default: '#6b7280', // gray
};

function getColorForClass(className: string): string {
  const lowerClassName = className.toLowerCase();
  return CLASS_COLORS[lowerClassName] || CLASS_COLORS.default;
}

export function useDetections(
  options: UseDetectionsOptions = {}
): UseDetectionsReturn {
  const [detections, setDetections] = useState<NormalizedDetection[]>([]);
  const [detectionCount, setDetectionCount] = useState(0);
  const [latestFrame, setLatestFrame] = useState<number | null>(null);
  const [latestTimestamp, setLatestTimestamp] = useState<number | null>(null);
  const [processingTimeMs, setProcessingTimeMs] = useState(0);
  const [frameWidth, setFrameWidth] = useState<number | null>(null);
  const [frameHeight, setFrameHeight] = useState<number | null>(null);
  const [stats, setStats] = useState<{
    framesReceived: number;
    framesProcessed: number;
    framesSkipped: number;
    avgProcessingTime: number;
    detectionsCount: number;
  } | null>(null);
  const confidenceThreshold = useRef(options.confidenceThreshold || 0.25);

  /**
   * Add new detection result
   */
  const addDetectionResult = useCallback(
    (message: WSDetectionMessage) => {
      const { data } = message;

      // Update frame info
      setLatestFrame(data.frameNumber);
      setLatestTimestamp(data.timestamp);
      setProcessingTimeMs(data.processingTimeMs);

      // Update frame dimensions
      setFrameWidth((data as any).frameWidth);
      setFrameHeight((data as any).frameHeight);

      // Update stats if available
      if (data.stats) {
        setStats({
          framesReceived: data.stats.frames_received,
          framesProcessed: data.stats.frames_processed,
          framesSkipped: data.stats.frames_skipped,
          avgProcessingTime: data.stats.avg_processing_time,
          detectionsCount: data.stats.detections_count,
        });
      }

      // Filter and normalize detections
      const normalizedDetections: NormalizedDetection[] = data.detections
        .filter((detection: any) => detection.confidence >= confidenceThreshold.current)
        .slice(0, options.maxDetections || 100)
        .map((detection: any, index: number) => ({
          id: `${data.frameNumber}-${index}`,
          className: detection.class_name,
          classId: detection.class_id,
          confidence: detection.confidence,
          bbox: {
            x1: detection.bbox.x1,
            y1: detection.bbox.y1,
            x2: detection.bbox.x2,
            y2: detection.bbox.y2,
          },
          timestamp: data.timestamp,
          frameNumber: data.frameNumber,
          color: getColorForClass(detection.class_name),
          // Include enriched context from Context Enrichment Agent
          context: detection.context ? {
            estimated_size: detection.context.estimated_size,
            bbox_area_pixels: detection.context.bbox_area_pixels,
            screen_position: detection.context.screen_position,
            threat_level_raw: detection.context.threat_level_raw,
          } : undefined,
        }));

      setDetections(normalizedDetections);
      setDetectionCount(normalizedDetections.length);
    },
    [options.maxDetections]
  );

  /**
   * Clear all detections
   */
  const clearDetections = useCallback(() => {
    setDetections([]);
    setDetectionCount(0);
    setLatestFrame(null);
    setLatestTimestamp(null);
    setProcessingTimeMs(0);
    setFrameWidth(null);
    setFrameHeight(null);
    setStats(null);
  }, []);

  /**
   * Update confidence threshold filter
   */
  const setConfidenceFilter = useCallback((threshold: number) => {
    confidenceThreshold.current = threshold;
  }, []);

  return {
    detections,
    detectionCount,
    latestFrame,
    latestTimestamp,
    processingTimeMs,
    frameWidth,
    frameHeight,
    stats,
    addDetectionResult,
    clearDetections,
    setConfidenceFilter,
  };
}
