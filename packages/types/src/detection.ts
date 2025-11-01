/**
 * Detection and hazard types
 */

export type HazardType = 'bird' | 'drone' | 'balloon' | 'kite' | 'debris' | 'unknown';

export interface BoundingBox {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
}

export interface EnrichedContext {
  estimated_size: string;  // "small", "medium", "large"
  bbox_area_pixels: number;
  screen_position: string;  // e.g., "upper-left", "center", etc.
  threat_level_raw: string; // "low", "moderate", "high", "critical"
}

export interface Detection {
  id: string;
  className: string;
  classId: number;
  confidence: number;
  bbox: BoundingBox;
  timestamp?: number;
  frameNumber?: number;
  context?: EnrichedContext;  // Added context from Context Enrichment Agent
}

export interface DetectionResult {
  detections: Detection[];
  processingTimeMs: number;
  frameCount?: number;
  videoId?: string;
}
