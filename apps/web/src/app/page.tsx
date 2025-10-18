import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function Home() {
  return (
    <div className="py-12">
      {/* Hero Section */}
      <section className="text-center mb-16">
        <h1 className="text-4xl md:text-6xl font-bold mb-4">SkyLaneAI</h1>
        <p className="text-xl md:text-2xl text-muted-foreground mb-8">
          Advanced Sky Hazard Detection for Flying Taxis
        </p>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
          Real-time detection of birds, drones, and airborne hazards using
          state-of-the-art YOLOv11 technology
        </p>
        <div className="flex gap-4 justify-center">
          <Button size="lg">Get Started</Button>
          <Button size="lg" variant="outline">
            Learn More
          </Button>
        </div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-6 mb-16">
        <Card>
          <CardHeader>
            <CardTitle>Real-time Detection</CardTitle>
            <CardDescription>YOLOv11-powered object detection</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Detect birds, drones, and other airborne hazards in real-time with
              high accuracy and low latency.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Live Video Streaming</CardTitle>
            <CardDescription>WebRTC-based video processing</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Stream live video from cameras with real-time object detection
              overlays and annotations.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Multi-hazard Support</CardTitle>
            <CardDescription>Comprehensive hazard detection</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Detect multiple hazard types including birds, drones, debris, and
              weather-related obstacles.
            </p>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
