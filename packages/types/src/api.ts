/**
 * API request and response types
 */

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  message: string;
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
}
