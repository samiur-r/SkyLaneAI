/**
 * Alert Detail Modal Component
 * Displays complete natural language alert from all 4 agents
 */

'use client';

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Loader2, AlertTriangle, Target, Zap, TrendingUp, X } from 'lucide-react';
import type { NormalizedDetection } from '@repo/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface NaturalLanguageAlert {
  detection: any;
  context: any;
  message: {
    title: string;
    emoji: string;
    body: string;
    sections: Record<string, string>;
  };
  action: {
    primary_action: string;
    secondary_action: string;
    reasoning: string;
    urgency: string;
  };
  priority: {
    overall_score: number;
    priority_level: string;
    factors: Record<string, any>;
  };
}

export interface AlertDetailModalProps {
  detection?: NormalizedDetection | null;
  videoWidth?: number;
  videoHeight?: number;
  isOpen: boolean;
  onClose: () => void;
  preloadedAlert?: NaturalLanguageAlert; // NEW: Allow passing pre-generated alerts
  alert?: any; // NEW: Alternative alert structure from timeline
}

export function AlertDetailModal({
  detection,
  videoWidth,
  videoHeight,
  isOpen,
  onClose,
  preloadedAlert,
  alert: timelineAlert,
}: AlertDetailModalProps) {
  const [alert, setAlert] = useState<NaturalLanguageAlert | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch complete alert when modal opens (or use preloaded)
  useEffect(() => {
    if (isOpen) {
      if (preloadedAlert) {
        // Use preloaded alert (from timeline)
        setAlert(preloadedAlert);
        setIsLoading(false);
      } else if (timelineAlert) {
        // Use alert structure from timeline
        setAlert({
          detection: timelineAlert.detection,
          context: timelineAlert.context,
          message: timelineAlert.message || {},
          action: timelineAlert.action || {},
          priority: timelineAlert.priority || {},
        });
        setIsLoading(false);
      } else if (detection) {
        // Fetch alert from API
        fetchCompleteAlert();
      }
    } else {
      // Reset state when modal closes
      setAlert(null);
      setError(null);
    }
  }, [isOpen, detection, preloadedAlert, timelineAlert]);

  const fetchCompleteAlert = async () => {
    if (!detection) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/alerts/generate-complete?image_width=${videoWidth || 1920}&image_height=${videoHeight || 1080}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            class_name: detection.className,
            class_id: detection.classId,
            confidence: detection.confidence,
            bbox: detection.bbox,
            frame_number: detection.frameNumber,
            timestamp: detection.timestamp,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Failed to generate alert: ${response.statusText}`);
      }

      const data = await response.json();
      setAlert(data);
    } catch (err) {
      console.error('Error fetching alert:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate alert');
    } finally {
      setIsLoading(false);
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'immediate':
        return 'bg-red-500';
      case 'urgent':
        return 'bg-orange-500';
      case 'caution':
        return 'bg-yellow-500';
      case 'advisory':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getPriorityColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'critical':
        return 'text-red-500 border-red-500/20 bg-red-500/10';
      case 'high':
        return 'text-orange-500 border-orange-500/20 bg-orange-500/10';
      case 'medium':
        return 'text-yellow-500 border-yellow-500/20 bg-yellow-500/10';
      case 'low':
        return 'text-green-500 border-green-500/20 bg-green-500/10';
      default:
        return 'text-gray-500 border-gray-500/20 bg-gray-500/10';
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-12 h-12 animate-spin text-blue-500 mb-4" />
            <p className="text-sm text-gray-500">Generating complete alert...</p>
            <p className="text-xs text-gray-400 mt-1">Running all 4 agents...</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center py-12">
            <AlertTriangle className="w-12 h-12 text-red-500 mb-4" />
            <p className="text-sm text-red-600 font-medium">Error</p>
            <p className="text-xs text-gray-500 mt-1">{error}</p>
            <Button onClick={fetchCompleteAlert} className="mt-4" size="sm">
              Retry
            </Button>
          </div>
        ) : alert ? (
          <>
            <DialogHeader>
              <DialogTitle className="text-2xl flex items-center gap-2">
                <span>{alert.message.emoji}</span>
                {alert.message.title}
              </DialogTitle>
              <DialogDescription>
                Natural language alert generated by 4-agent pipeline
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-6">
              {/* Priority Score */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-gray-500" />
                      <h3 className="font-semibold">Priority Score</h3>
                    </div>
                    <Badge
                      variant="outline"
                      className={`${getPriorityColor(alert.priority.priority_level)} border font-semibold`}
                    >
                      {alert.priority.priority_level.toUpperCase()}
                    </Badge>
                  </div>
                  <div className="text-center mb-4">
                    <div className="text-4xl font-bold">{alert.priority.overall_score.toFixed(1)}</div>
                    <div className="text-sm text-gray-500">out of 100</div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {Object.entries(alert.priority.factors).map(([key, data]: [string, any]) => (
                      <div key={key} className="flex justify-between">
                        <span className="text-gray-600 capitalize">{key.replace(/_/g, ' ')}:</span>
                        <span className="font-medium">{data.value}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Message */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center gap-2 mb-4">
                    <Target className="w-5 h-5 text-gray-500" />
                    <h3 className="font-semibold">Detection Details</h3>
                  </div>
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <div
                      className="text-sm"
                      dangerouslySetInnerHTML={{
                        __html: alert.message.body
                          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                          .replace(/^- /gm, '• ')
                          .replace(/\n/g, '<br />'),
                      }}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Action Recommendations */}
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Zap className="w-5 h-5 text-gray-500" />
                      <h3 className="font-semibold">Recommended Actions</h3>
                    </div>
                    <Badge className={`${getUrgencyColor(alert.action.urgency)} text-white`}>
                      {alert.action.urgency.toUpperCase()}
                    </Badge>
                  </div>

                  <div className="space-y-4">
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                      <p className="text-xs text-blue-600 dark:text-blue-400 font-semibold mb-1">
                        PRIMARY ACTION
                      </p>
                      <p className="text-sm font-medium">{alert.action.primary_action}</p>
                    </div>

                    <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border">
                      <p className="text-xs text-gray-600 dark:text-gray-400 font-semibold mb-1">
                        SECONDARY ACTION
                      </p>
                      <p className="text-sm">{alert.action.secondary_action}</p>
                    </div>

                    <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <p className="text-xs text-gray-600 dark:text-gray-400 font-semibold mb-1">
                        REASONING
                      </p>
                      <p className="text-sm italic text-gray-700 dark:text-gray-300">
                        {alert.action.reasoning}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Close Button */}
              <div className="flex justify-end">
                <Button onClick={onClose} variant="outline">
                  <X className="w-4 h-4 mr-2" />
                  Close
                </Button>
              </div>
            </div>
          </>
        ) : null}
      </DialogContent>
    </Dialog>
  );
}
