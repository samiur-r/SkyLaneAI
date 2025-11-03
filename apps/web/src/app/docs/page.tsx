import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Video, Brain, Eye, Network } from "lucide-react";

export default function DocsPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <section className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Documentation</h1>
        <p className="text-xl text-muted-foreground max-w-3xl">
          Learn about SkyLaneAI's multi-agent AI system and how it protects aerial vehicles from sky hazards.
        </p>
      </section>

      {/* Overview Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Overview</h2>
        <Card>
          <CardContent className="pt-6">
            <p className="text-lg leading-relaxed mb-4">
              SkyLaneAI is a safety-critical system designed to protect flying taxis and other aerial vehicles
              from sky hazards. Using advanced AI technology, it detects birds, drones, balloons, and kites in
              video feeds and provides intelligent, context-aware alerts.
            </p>
            <p className="text-lg leading-relaxed">
              The system employs a sophisticated multi-agent AI architecture powered by LangGraph and OpenAI,
              where specialized agents work together to analyze detections, assess threats, and generate
              actionable recommendations for pilots.
            </p>
          </CardContent>
        </Card>
      </section>

      {/* Key Features */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Key Features</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Eye className="w-6 h-6 text-primary" />
                <CardTitle>YOLOv11 Detection</CardTitle>
              </div>
              <CardDescription>Real-time object detection</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Advanced object detection using YOLOv11, capable of identifying
                birds, drones (detected as airplanes), kites, and balloons (detected as sports balls)
                with high accuracy and minimal latency.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Network className="w-6 h-6 text-primary" />
                <CardTitle>Multi-Agent AI System</CardTitle>
              </div>
              <CardDescription>LangGraph-powered intelligence</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Four specialized agents work together: Context Agent analyzes patterns, Action Agent
                recommends pilot actions, Message Agent crafts alerts, and Priority Agent ranks threats
                by urgency.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Brain className="w-6 h-6 text-primary" />
                <CardTitle>Context-Aware Alerts</CardTitle>
              </div>
              <CardDescription>Intelligent message generation</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                AI-generated natural language alerts that include threat assessment, detection details,
                and actionable pilot recommendations based on aviation safety protocols.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Video className="w-6 h-6 text-primary" />
                <CardTitle>Video Analysis</CardTitle>
              </div>
              <CardDescription>Upload and analyze recordings</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Upload pre-recorded videos for detailed analysis with interactive timeline,
                detection filtering, and comprehensive alert review capabilities.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Multi-Agent System */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Multi-Agent System Architecture</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">1. Context Agent (Rule-based)</h3>
                <p className="text-muted-foreground mb-2">
                  Analyzes detection data to enrich context with size estimation, screen position,
                  and initial threat level calculation. Fast and deterministic with no API costs.
                </p>
                <ul className="list-disc list-inside text-muted-foreground ml-4">
                  <li>Calculates bounding box area and size category (small, medium, large)</li>
                  <li>Determines screen position (upper-left, center, lower-right, etc.)</li>
                  <li>Computes threat level (low, moderate, high, critical)</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">2. Action Agent (LLM-powered)</h3>
                <p className="text-muted-foreground mb-2">
                  Uses OpenAI GPT to generate actionable pilot recommendations following aviation safety protocols.
                </p>
                <ul className="list-disc list-inside text-muted-foreground ml-4">
                  <li>PRIMARY ACTION: Most critical immediate action</li>
                  <li>SECONDARY ACTION: Follow-up or alternative action</li>
                  <li>REASONING: Brief explanation of recommendations</li>
                  <li>URGENCY: Advisory, caution, urgent, or immediate</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">3. Message Agent (LLM-powered)</h3>
                <p className="text-muted-foreground mb-2">
                  Generates natural language alert messages with professional, aviation-focused tone.
                </p>
                <ul className="list-disc list-inside text-muted-foreground ml-4">
                  <li>Creates structured alerts with title and emoji</li>
                  <li>Includes Detection Details and Threat Assessment sections</li>
                  <li>Provides scannable, actionable information for pilots</li>
                  <li>Fallback to rule-based messages if LLM fails</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">4. Priority Agent (Rule-based)</h3>
                <p className="text-muted-foreground mb-2">
                  Scores and ranks alerts using a weighted system to help pilots focus on critical threats first.
                </p>
                <ul className="list-disc list-inside text-muted-foreground ml-4">
                  <li>Threat level (40% weight)</li>
                  <li>Action urgency (30% weight)</li>
                  <li>Detection confidence (20% weight)</li>
                  <li>Object size (10% weight)</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* How It Works */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">How It Works</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">1. Video Upload</h3>
                <p className="text-muted-foreground">
                  Upload a video file through the web interface. Supported formats include MP4, AVI, MOV, and MKV.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">2. Object Detection</h3>
                <p className="text-muted-foreground">
                  Each video frame is analyzed using YOLOv11 to identify potential sky hazards including
                  birds, kites, airplanes (drones), and sports balls (balloons).
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">3. Multi-Agent Analysis</h3>
                <p className="text-muted-foreground">
                  Detected hazards flow through the multi-agent pipeline: Context Agent enriches data,
                  Action Agent recommends pilot actions, Message Agent crafts alerts, and Priority Agent
                  ranks threats by urgency.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">4. Interactive Results</h3>
                <p className="text-muted-foreground">
                  View detections with bounding box overlays on the video player, explore the interactive
                  timeline, filter by hazard type, and review AI-generated alerts with actionable recommendations.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Threat Levels */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Threat Levels (Context Agent)</h2>
        <div className="space-y-4">
          <Card className="border-l-4 border-l-red-500">
            <CardHeader>
              <CardTitle className="text-red-600">Critical</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Large hazard with high confidence, significant screen coverage. Requires immediate action.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader>
              <CardTitle className="text-orange-600">High</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Hazard detected with good confidence and considerable size. Urgent monitoring and potential evasive action.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader>
              <CardTitle className="text-yellow-600">Moderate</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Hazard present with reasonable confidence. Continue monitoring and be prepared for course adjustment.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader>
              <CardTitle className="text-green-600">Low</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Small or distant hazard. Maintain awareness but no immediate action required.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Technology Stack */}
      <section>
        <h2 className="text-3xl font-bold mb-6">Technology Stack</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-lg font-semibold mb-2">Frontend</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Next.js with App Router</li>
                  <li>• React with TypeScript</li>
                  <li>• Tailwind CSS</li>
                  <li>• shadcn/ui components</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Backend</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• FastAPI (Python)</li>
                  <li>• YOLOv11 object detection</li>
                  <li>• OpenCV for video processing</li>
                  <li>• File-based storage (temporary)</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">AI Multi-Agent System</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• LangGraph for agent orchestration</li>
                  <li>• OpenAI GPT (gpt-4o-mini)</li>
                  <li>• 4 specialized agents (2 LLM, 2 rule-based)</li>
                  <li>• Fallback logic for reliability</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Coming Soon</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Live camera streaming (WebRTC)</li>
                  <li>• Time-to-Contact (TTC) calculation</li>
                  <li>• Persistent database storage</li>
                  <li>• Multi-camera support</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
