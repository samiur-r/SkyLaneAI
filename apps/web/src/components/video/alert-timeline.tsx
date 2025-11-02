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
  Clock
} from "lucide-react";
import { TimeBasedAlert } from "@repo/types/stream";
import { AlertDetailModal } from "./alert-detail-modal";

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
  const [selectedAlert, setSelectedAlert] = useState<TimeBasedAlert | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

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

  const handleViewDetails = (alert: TimeBasedAlert) => {
    setSelectedAlert(alert);
    setIsModalOpen(true);
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

                return (
                  <div
                    key={`${alert.second}-${index}`}
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
                            onClick={() => handleViewDetails(alert)}
                            className="text-xs"
                          >
                            View Details
                            <ChevronRight className="w-3 h-3 ml-1" />
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

      {/* Alert Detail Modal */}
      {selectedAlert && (
        <AlertDetailModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setSelectedAlert(null);
          }}
          alert={{
            detection: {
              id: `alert-${selectedAlert.second}`,
              className: selectedAlert.hazardType,
              confidence: 0, // Not available in timeline data
              bbox: selectedAlert.fullAlert.detection.bbox,
            },
            context: selectedAlert.fullAlert.context,
          }}
          preloadedAlert={{
            detection: selectedAlert.fullAlert.detection,
            context: selectedAlert.fullAlert.context,
            message: selectedAlert.fullAlert.message,
            action: selectedAlert.fullAlert.action,
            priority: selectedAlert.fullAlert.priority,
          }}
        />
      )}
    </>
  );
}
