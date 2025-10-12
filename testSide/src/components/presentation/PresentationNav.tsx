import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface PresentationNavProps {
  scenes: { id: number; name: string }[];
  activeScene: number;
  onNavigate: (sceneId: number) => void;
}

export const PresentationNav = ({
  scenes,
  activeScene,
  onNavigate,
}: PresentationNavProps) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          <div className="text-sm font-semibold text-primary">
            Self-Healing Swarm AI
          </div>
          <div className="flex items-center gap-2 overflow-x-auto">
            {scenes.map((scene) => (
              <Button
                key={scene.id}
                variant="ghost"
                size="sm"
                onClick={() => onNavigate(scene.id)}
                className={cn(
                  "text-xs whitespace-nowrap transition-colors",
                  activeScene === scene.id
                    ? "text-primary font-semibold bg-primary/10"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {scene.name}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};
