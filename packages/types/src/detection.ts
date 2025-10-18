/**
 * Detection and hazard types
 */

export type HazardType = 'bird' | 'drone' | 'balloon' | 'kite' | 'debris' | 'unknown';

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Detection {
  id: string;
  className: string;
  classId: number;
  confidence: number;
  bbox: BoundingBox;
  timestamp?: number;
  frameNumber?: number;
}

export interface DetectionResult {
  detections: Detection[];
  processingTimeMs: number;
  frameCount?: number;
  videoId?: string;
}
