/**
 * WebRTC Client for video streaming
 * Handles peer connection, signaling, and video track management
 */

import type {
  ConnectionStatus,
  WSClientMessage,
  WSServerMessage,
  WSDetectionMessage,
  StreamStats,
  StreamSettings,
} from '@skylane/types';

export interface WebRTCClientConfig {
  wsUrl: string;
  iceServers?: RTCIceServer[];
  onConnectionStatusChange?: (status: ConnectionStatus) => void;
  onDetection?: (message: WSDetectionMessage) => void;
  onStats?: (stats: StreamStats) => void;
  onError?: (error: string) => void;
}

export class WebRTCClient {
  private peerConnection: RTCPeerConnection | null = null;
  private websocket: WebSocket | null = null;
  private config: WebRTCClientConfig;
  private connectionStatus: ConnectionStatus = 'disconnected';
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;

  constructor(config: WebRTCClientConfig) {
    this.config = {
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }],
      ...config,
    };
  }

  /**
   * Connect to the WebRTC server
   */
  async connect(): Promise<void> {
    if (this.connectionStatus === 'connected' || this.connectionStatus === 'connecting') {
      console.warn('Already connected or connecting');
      return;
    }

    this.updateConnectionStatus('connecting');

    try {
      // Create WebSocket connection
      await this.connectWebSocket();

      // Create RTCPeerConnection
      this.createPeerConnection();

      console.log('WebRTC client connected');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('Failed to connect:', errorMessage);
      this.updateConnectionStatus('error');
      this.config.onError?.(errorMessage);
      throw error;
    }
  }

  /**
   * Create WebSocket connection
   */
  private connectWebSocket(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.websocket = new WebSocket(this.config.wsUrl);

        this.websocket.onopen = () => {
          console.log('WebSocket connected');
          this.reconnectAttempts = 0;
          this.startPingInterval();
          resolve();
        };

        this.websocket.onmessage = (event) => {
          this.handleWebSocketMessage(event);
        };

        this.websocket.onerror = (error) => {
          console.error('WebSocket error:', error);
          reject(new Error('WebSocket connection failed'));
        };

        this.websocket.onclose = () => {
          console.log('WebSocket closed');
          this.handleWebSocketClose();
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Create RTCPeerConnection
   */
  private createPeerConnection(): void {
    this.peerConnection = new RTCPeerConnection({
      iceServers: this.config.iceServers,
    });

    // Handle ICE candidates
    this.peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        this.sendMessage({
          type: 'ice_candidate',
          candidate: event.candidate.candidate,
          sdpMid: event.candidate.sdpMid,
          sdpMLineIndex: event.candidate.sdpMLineIndex,
        });
      }
    };

    // Handle connection state changes
    this.peerConnection.onconnectionstatechange = () => {
      const state = this.peerConnection?.connectionState;
      console.log('Connection state:', state);

      if (state === 'connected') {
        this.updateConnectionStatus('connected');
      } else if (state === 'disconnected' || state === 'failed') {
        this.updateConnectionStatus('error');
        this.attemptReconnect();
      }
    };

    // Handle ICE connection state changes
    this.peerConnection.oniceconnectionstatechange = () => {
      const state = this.peerConnection?.iceConnectionState;
      console.log('ICE connection state:', state);
    };
  }

  /**
   * Add local video track to peer connection
   */
  async addVideoTrack(stream: MediaStream): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    const videoTrack = stream.getVideoTracks()[0];
    if (!videoTrack) {
      throw new Error('No video track found in stream');
    }

    // Add track to peer connection
    this.peerConnection.addTrack(videoTrack, stream);
    console.log('Video track added to peer connection');

    // Create and send offer
    await this.createAndSendOffer();
  }

  /**
   * Create WebRTC offer and send to server
   */
  private async createAndSendOffer(): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    try {
      // Create offer
      const offer = await this.peerConnection.createOffer({
        offerToReceiveVideo: false,
        offerToReceiveAudio: false,
      });

      // Set local description
      await this.peerConnection.setLocalDescription(offer);

      // Send offer to server
      this.sendMessage({
        type: 'offer',
        sdp: offer.sdp!,
      });

      console.log('Offer sent to server');
    } catch (error) {
      console.error('Failed to create offer:', error);
      throw error;
    }
  }

  /**
   * Handle incoming WebSocket messages
   */
  private async handleWebSocketMessage(event: MessageEvent): Promise<void> {
    try {
      const message: WSServerMessage = JSON.parse(event.data);

      switch (message.type) {
        case 'answer':
          await this.handleAnswer(message.sdp);
          break;

        case 'detection':
          this.config.onDetection?.(message);
          break;

        case 'stats':
          this.config.onStats?.(message.data);
          break;

        case 'error':
          console.error('Server error:', message.message);
          this.config.onError?.(message.message);
          break;

        case 'pong':
          // Keep-alive response
          break;

        default:
          console.warn('Unknown message type:', message);
      }
    } catch (error) {
      console.error('Failed to handle message:', error);
    }
  }

  /**
   * Handle WebRTC answer from server
   */
  private async handleAnswer(sdp: string): Promise<void> {
    if (!this.peerConnection) {
      throw new Error('Peer connection not initialized');
    }

    try {
      const answer: RTCSessionDescriptionInit = {
        type: 'answer',
        sdp,
      };

      await this.peerConnection.setRemoteDescription(answer);
      console.log('Remote description set');
    } catch (error) {
      console.error('Failed to set remote description:', error);
      throw error;
    }
  }

  /**
   * Update stream settings
   */
  updateSettings(settings: Partial<StreamSettings>): void {
    this.sendMessage({
      type: 'settings',
      ...settings,
    });
  }

  /**
   * Request current statistics
   */
  requestStats(): void {
    this.sendMessage({
      type: 'get_stats',
    });
  }

  /**
   * Send message via WebSocket
   */
  private sendMessage(message: WSClientMessage): void {
    if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket not connected, cannot send message');
      return;
    }

    this.websocket.send(JSON.stringify(message));
  }

  /**
   * Start ping interval to keep connection alive
   */
  private startPingInterval(): void {
    this.stopPingInterval();
    this.pingInterval = setInterval(() => {
      this.sendMessage({ type: 'ping' });
    }, 30000); // Ping every 30 seconds
  }

  /**
   * Stop ping interval
   */
  private stopPingInterval(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  /**
   * Handle WebSocket close
   */
  private handleWebSocketClose(): void {
    this.stopPingInterval();
    if (this.connectionStatus === 'connected') {
      this.updateConnectionStatus('disconnected');
      this.attemptReconnect();
    }
  }

  /**
   * Attempt to reconnect
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      this.updateConnectionStatus('error');
      return;
    }

    if (this.reconnectTimeout) {
      return; // Already attempting to reconnect
    }

    this.reconnectAttempts++;
    this.updateConnectionStatus('reconnecting');

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectTimeout = null;
      this.connect().catch((error) => {
        console.error('Reconnection failed:', error);
      });
    }, delay);
  }

  /**
   * Update connection status
   */
  private updateConnectionStatus(status: ConnectionStatus): void {
    if (this.connectionStatus !== status) {
      this.connectionStatus = status;
      this.config.onConnectionStatusChange?.(status);
    }
  }

  /**
   * Get current connection status
   */
  getConnectionStatus(): ConnectionStatus {
    return this.connectionStatus;
  }

  /**
   * Disconnect and clean up
   */
  disconnect(): void {
    console.log('Disconnecting WebRTC client');

    // Stop ping interval
    this.stopPingInterval();

    // Clear reconnect timeout
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    // Close peer connection
    if (this.peerConnection) {
      this.peerConnection.close();
      this.peerConnection = null;
    }

    // Close WebSocket
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }

    this.updateConnectionStatus('disconnected');
    this.reconnectAttempts = 0;
  }
}
