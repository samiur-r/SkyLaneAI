"use client";

import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  AlertCircle,
  AlertTriangle,
  Info,
  ChevronRight,
  ChevronDown,
  Clock,
  Target,
  Zap,
  TrendingUp
} from "lucide-react";
import type { TimeBasedAlert } from "@repo/types";

interface AlertTimelineProps {
  alerts: TimeBasedAlert[];
  currentTimestamp?: number;
  onSeekTo?: (timestamp: number) => void;
}

export function AlertTimeline({
  alerts,
  currentTimestamp = 0,
  onSeekTo
}: AlertTimelineProps) {
  const [expandedAlertId, setExpandedAlertId] = useState<string | null>(null);

  // Sort alerts by timestamp
  const sortedAlerts = [...alerts].sort((a, b) => a.timestamp - b.timestamp);

  // Get priority icon and color
  const getPriorityConfig = (level: string) => {
    switch (level.toLowerCase()) {
      case "critical":
        return {
          icon: AlertCircle,
          color: "text-red-500",
          bgColor: "bg-red-50 dark:bg-red-950",
          borderColor: "border-red-200 dark:border-red-800",
          badgeVariant: "destructive" as const,
        };
      case "high":
        return {
          icon: AlertTriangle,
          color: "text-orange-500",
          bgColor: "bg-orange-50 dark:bg-orange-950",
          borderColor: "border-orange-200 dark:border-orange-800",
          badgeVariant: "destructive" as const,
        };
      case "medium":
        return {
          icon: AlertTriangle,
          color: "text-yellow-500",
          bgColor: "bg-yellow-50 dark:bg-yellow-950",
          borderColor: "border-yellow-200 dark:border-yellow-800",
          badgeVariant: "outline" as const,
        };
      default:
        return {
          icon: Info,
          color: "text-blue-500",
          bgColor: "bg-blue-50 dark:bg-blue-950",
          borderColor: "border-blue-200 dark:border-blue-800",
          badgeVariant: "secondary" as const,
        };
    }
  };

  const formatTimestamp = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleToggleDetails = (alertId: string) => {
    setExpandedAlertId(expandedAlertId === alertId ? null : alertId);
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case 'immediate':
        return 'bg-red-500 text-white';
      case 'urgent':
        return 'bg-orange-500 text-white';
      case 'caution':
        return 'bg-yellow-500 text-white';
      case 'advisory':
        return 'bg-blue-500 text-white';
      default:
        return 'bg-gray-500 text-white';
    }
  };

  const handleSeek = (timestamp: number) => {
    if (onSeekTo) {
      onSeekTo(timestamp);
    }
  };

  if (alerts.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Alert Timeline
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Info className="w-12 h-12 mx-auto mb-2 opacity-20" />
            <p>No alerts generated yet</p>
            <p className="text-sm mt-1">Alerts will appear here as the video is processed</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Alert Timeline
            <Badge variant="secondary" className="ml-auto">
              {alerts.length} alert{alerts.length !== 1 ? 's' : ''}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <ScrollArea className="h-[400px]">
            <div className="space-y-2 p-4">
              {sortedAlerts.map((alert, index) => {
                const config = getPriorityConfig(alert.priorityLevel);
                const Icon = config.icon;
                const isCurrentAlert = currentTimestamp >= alert.timestamp &&
                  (index === sortedAlerts.length - 1 || currentTimestamp < sortedAlerts[index + 1].timestamp);
                const alertId = `${alert.second}-${index}`;
                const isExpanded = expandedAlertId === alertId;

                return (
                  <div
                    key={alertId}
                    className={`
                      p-4 rounded-lg border-2 transition-all
                      ${config.bgColor} ${config.borderColor}
                      ${isCurrentAlert ? 'ring-2 ring-primary' : ''}
                      hover:shadow-md
                    `}
                  >
                    <div className="flex items-start gap-3">
                      {/* Icon */}
                      <div className={`mt-1 ${config.color}`}>
                        <Icon className="w-5 h-5" />
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        {/* Header */}
                        <div className="flex items-center gap-2 mb-2">
                          <span className="font-mono text-sm font-medium">
                            {formatTimestamp(alert.timestamp)}
                          </span>
                          <Badge variant={config.badgeVariant} className="text-xs">
                            {alert.priorityLevel.toUpperCase()}
                          </Badge>
                          {isCurrentAlert && (
                            <Badge variant="default" className="text-xs">
                              CURRENT
                            </Badge>
                          )}
                        </div>

                        {/* Title */}
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-lg">{alert.emoji}</span>
                          <h4 className="font-semibold text-sm">
                            {alert.title}
                          </h4>
                        </div>

                        {/* Primary Action */}
                        <p className="text-sm text-muted-foreground mb-3">
                          {alert.primaryAction}
                        </p>

                        {/* Expandable Details */}
                        {isExpanded && (
                          <div className="mt-4 space-y-3 border-t pt-3">
                            {/* Priority Score Details */}
                            <div className="p-3 bg-background rounded-lg border">
                              <div className="flex items-center gap-2 mb-2">
                                <TrendingUp className="w-4 h-4 text-gray-500" />
                                <h5 className="font-semibold text-xs">Priority Analysis</h5>
                              </div>
                              <div className="text-center mb-2">
                                <div className="text-2xl font-bold">{alert.priorityScore.toFixed(1)}</div>
                                <div className="text-xs text-muted-foreground">Priority Score</div>
                              </div>
                              <div className="grid grid-cols-2 gap-2 text-xs">
                                {Object.entries(alert.fullAlert.priority.factors).map(([key, data]: [string, any]) => (
                                  <div key={key} className="flex justify-between">
                                    <span className="text-muted-foreground capitalize">{key.replace(/_/g, ' ')}:</span>
                                    <span className="font-medium">{data.value}</span>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Detection Context */}
                            <div className="p-3 bg-background rounded-lg border">
                              <div className="flex items-center gap-2 mb-2">
                                <Target className="w-4 h-4 text-gray-500" />
                                <h5 className="font-semibold text-xs">Detection Context</h5>
                              </div>
                              <div className="text-xs space-y-1">
                                <p><span className="text-muted-foreground">Size:</span> <span className="font-medium capitalize">{alert.fullAlert.context.estimated_size}</span></p>
                                <p><span className="text-muted-foreground">Position:</span> <span className="font-medium capitalize">{alert.fullAlert.context.screen_position}</span></p>
                                <p><span className="text-muted-foreground">Area:</span> <span className="font-medium">{alert.fullAlert.context.bbox_area_pixels.toLocaleString()} px²</span></p>
                                <p><span className="text-muted-foreground">Threat Level:</span> <span className="font-medium capitalize">{alert.fullAlert.context.threat_level_raw}</span></p>
                              </div>
                            </div>

                            {/* Action Recommendations */}
                            <div className="p-3 bg-background rounded-lg border">
                              <div className="flex items-center justify-between mb-2">
                                <div className="flex items-center gap-2">
                                  <Zap className="w-4 h-4 text-gray-500" />
                                  <h5 className="font-semibold text-xs">Recommended Actions</h5>
                                </div>
                                <Badge className={`text-xs ${getUrgencyColor(alert.fullAlert.action.urgency)}`}>
                                  {alert.fullAlert.action.urgency.toUpperCase()}
                                </Badge>
                              </div>
                              <div className="space-y-2">
                                <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800">
                                  <p className="text-xs text-blue-600 dark:text-blue-400 font-semibold mb-1">PRIMARY</p>
                                  <p className="text-xs">{alert.fullAlert.action.primary_action}</p>
                                </div>
                                <div className="p-2 bg-muted rounded border">
                                  <p className="text-xs text-muted-foreground font-semibold mb-1">SECONDARY</p>
                                  <p className="text-xs">{alert.fullAlert.action.secondary_action}</p>
                                </div>
                              </div>
                            </div>

                            {/* Message Body */}
                            <div className="p-3 bg-background rounded-lg border">
                              <h5 className="font-semibold text-xs mb-2">Full Message</h5>
                              <div className="text-xs prose prose-sm dark:prose-invert max-w-none">
                                <div
                                  dangerouslySetInnerHTML={{
                                    __html: alert.fullAlert.message.body
                                      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                      .replace(/^- /gm, '• ')
                                      .replace(/\n/g, '<br />'),
                                  }}
                                />
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Actions */}
                        <div className="flex gap-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleSeek(alert.timestamp)}
                            className="text-xs"
                          >
                            Jump to Time
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleToggleDetails(alertId)}
                            className="text-xs"
                          >
                            {isExpanded ? 'Hide Details' : 'View Details'}
                            {isExpanded ? (
                              <ChevronDown className="w-3 h-3 ml-1" />
                            ) : (
                              <ChevronRight className="w-3 h-3 ml-1" />
                            )}
                          </Button>
                        </div>
                      </div>

                      {/* Priority Score */}
                      <div className="text-right">
                        <div className="text-xs text-muted-foreground">Score</div>
                        <div className={`text-lg font-bold ${config.color}`}>
                          {alert.priorityScore.toFixed(0)}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </>
  );
}
