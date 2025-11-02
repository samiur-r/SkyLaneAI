export function Header() {
  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-primary">
              SkyLaneAI
            </div>
            <span className="text-sm text-muted-foreground">v2.0</span>
          </div>
          <nav className="flex items-center space-x-6">
            <a href="/" className="text-sm font-medium hover:text-primary transition-colors">
              Home
            </a>
            <a href="/docs" className="text-sm font-medium hover:text-primary transition-colors">
              Docs
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}
