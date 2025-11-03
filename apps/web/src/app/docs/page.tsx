import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { AlertCircle, Video, Zap, Eye } from "lucide-react";

export default function DocsPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <section className="mb-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">Documentation</h1>
        <p className="text-xl text-muted-foreground max-w-3xl">
          Learn about SkyLaneAI's capabilities and how it protects aerial vehicles from sky hazards.
        </p>
      </section>

      {/* Overview Section */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Overview</h2>
        <Card>
          <CardContent className="pt-6">
            <p className="text-lg leading-relaxed mb-4">
              SkyLaneAI is a safety-critical system designed to protect flying taxis and other aerial vehicles
              from sky hazards. Using advanced AI technology, it provides real-time detection and collision warnings
              for birds, drones, balloons, kites, and other airborne obstacles.
            </p>
            <p className="text-lg leading-relaxed">
              The system analyzes video feeds in real-time, calculates Time-to-Contact (TTC) for detected hazards,
              and provides graded collision warnings to help pilots and autonomous systems make informed decisions.
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
                <CardTitle>Real-time Detection</CardTitle>
              </div>
              <CardDescription>DETR-powered AI technology</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Advanced object detection using the latest DETR model, capable of identifying
                birds, drones, balloons, and kites with high accuracy and minimal latency.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Zap className="w-6 h-6 text-primary" />
                <CardTitle>Time-to-Contact (TTC)</CardTitle>
              </div>
              <CardDescription>Intelligent collision prediction</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Calculates the estimated time until potential collision with detected hazards,
                enabling proactive decision-making and early warning systems.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <AlertCircle className="w-6 h-6 text-primary" />
                <CardTitle>Graded Warnings</CardTitle>
              </div>
              <CardDescription>Color-coded alert system</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Four-level warning system (Green, Yellow, Orange, Red) based on TTC values,
                providing clear and intuitive risk assessment at a glance.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Video className="w-6 h-6 text-primary" />
                <CardTitle>Flexible Input Options</CardTitle>
              </div>
              <CardDescription>Live streams and video uploads</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Process live camera feeds for real-time monitoring or upload pre-recorded videos
                for detailed analysis and review.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">How It Works</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2">1. Video Capture</h3>
                <p className="text-muted-foreground">
                  The system ingests video feeds from onboard cameras or processes uploaded video files.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">2. Object Detection</h3>
                <p className="text-muted-foreground">
                  Each video frame is analyzed using our custom-trained DETR model to identify potential hazards
                  including birds, drones, balloons, and kites.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">3. TTC Calculation</h3>
                <p className="text-muted-foreground">
                  For each detected object, the system calculates Time-to-Contact by analyzing object size changes,
                  trajectory, and relative motion across consecutive frames.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">4. Warning Generation</h3>
                <p className="text-muted-foreground">
                  Based on TTC values, the system assigns color-coded warning levels and displays visual overlays
                  with bounding boxes around detected hazards.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2">5. Alert Notification</h3>
                <p className="text-muted-foreground">
                  Critical alerts are generated when hazards pose immediate danger, allowing pilots or autonomous
                  systems to take evasive action.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Warning Levels */}
      <section className="mb-12">
        <h2 className="text-3xl font-bold mb-6">Warning Levels</h2>
        <div className="space-y-4">
          <Card className="border-l-4 border-l-green-500">
            <CardHeader>
              <CardTitle className="text-green-600">Green - Safe</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Hazard detected at safe distance. No immediate action required. Continue monitoring.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader>
              <CardTitle className="text-yellow-600">Yellow - Caution</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Hazard approaching. Begin tracking and prepare for potential evasive action.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader>
              <CardTitle className="text-orange-600">Orange - Warning</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Hazard in proximity. Consider evasive maneuvers and alert crew/passengers.
              </p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-red-500">
            <CardHeader>
              <CardTitle className="text-red-600">Red - Critical</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Immediate collision risk. Execute evasive action now. Alert all systems.
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
                  <li>• DETR object detection</li>
                  <li>• OpenCV for video processing</li>
                  <li>• WebSocket for real-time data</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">AI/ML</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• DETR (Ultralytics)</li>
                  <li>• Custom-trained model</li>
                  <li>• GPU-accelerated inference</li>
                  <li>• Real-time TTC algorithms</li>
                </ul>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2">Infrastructure</h3>
                <ul className="space-y-1 text-muted-foreground">
                  <li>• Supabase (Database & Auth)</li>
                  <li>• Docker containerization</li>
                  <li>• Cloud deployment ready</li>
                  <li>• Scalable architecture</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
