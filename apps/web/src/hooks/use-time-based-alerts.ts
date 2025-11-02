"use client";

import { useState, useCallback, useEffect } from "react";
import { TimeBasedAlert, WSTimeBasedAlertMessage } from "@repo/types/stream";

export function useTimeBasedAlerts() {
  const [alerts, setAlerts] = useState<TimeBasedAlert[]>([]);
  const [isReceivingAlerts, setIsReceivingAlerts] = useState(false);

  // Add a new alert from WebSocket message
  const addAlert = useCallback((message: WSTimeBasedAlertMessage) => {
    const alert: TimeBasedAlert = {
      second: message.data.second,
      timestamp: message.data.timestamp,
      priorityLevel: message.data.alert.priority.priority_level as any,
      priorityScore: message.data.alert.priority.overall_score,
      title: message.data.alert.message.title,
      emoji: message.data.alert.message.emoji,
      hazardType: message.data.alert.detection.class_name,
      primaryAction: message.data.alert.action.primary_action,
      urgency: message.data.alert.action.urgency as any,
      fullAlert: message.data.alert,
    };

    setAlerts((prev) => {
      // Check if alert for this second already exists
      const existingIndex = prev.findIndex((a) => a.second === alert.second);
      if (existingIndex >= 0) {
        // Replace existing alert (in case of reprocessing)
        const newAlerts = [...prev];
        newAlerts[existingIndex] = alert;
        return newAlerts;
      } else {
        // Add new alert
        return [...prev, alert].sort((a, b) => a.second - b.second);
      }
    });

    setIsReceivingAlerts(true);
  }, []);

  // Clear all alerts
  const clearAlerts = useCallback(() => {
    setAlerts([]);
    setIsReceivingAlerts(false);
  }, []);

  // Get alert at specific timestamp
  const getAlertAtTimestamp = useCallback(
    (timestamp: number): TimeBasedAlert | null => {
      const second = Math.floor(timestamp);
      return alerts.find((a) => a.second === second) || null;
    },
    [alerts]
  );

  // Get statistics
  const getStatistics = useCallback(() => {
    const priorityCounts = {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
    };

    const urgencyCounts = {
      immediate: 0,
      urgent: 0,
      caution: 0,
      advisory: 0,
    };

    const hazardCounts: Record<string, number> = {};

    alerts.forEach((alert) => {
      // Count by priority
      priorityCounts[alert.priorityLevel] =
        (priorityCounts[alert.priorityLevel] || 0) + 1;

      // Count by urgency
      urgencyCounts[alert.urgency] = (urgencyCounts[alert.urgency] || 0) + 1;

      // Count by hazard type
      hazardCounts[alert.hazardType] =
        (hazardCounts[alert.hazardType] || 0) + 1;
    });

    const averagePriorityScore =
      alerts.length > 0
        ? alerts.reduce((sum, a) => sum + a.priorityScore, 0) / alerts.length
        : 0;

    return {
      totalAlerts: alerts.length,
      priorityCounts,
      urgencyCounts,
      hazardCounts,
      averagePriorityScore,
      highestPriorityAlert:
        alerts.length > 0
          ? [...alerts].sort((a, b) => b.priorityScore - a.priorityScore)[0]
          : null,
    };
  }, [alerts]);

  return {
    alerts,
    isReceivingAlerts,
    addAlert,
    clearAlerts,
    getAlertAtTimestamp,
    getStatistics,
  };
}
