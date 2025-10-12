import { Button } from "@/components/ui/button";
import { Play, Pause, RotateCcw, Zap } from "lucide-react";

interface SimulationControlsProps {
  isPlaying: boolean;
  onPlayPause: () => void;
  onReset: () => void;
  onInjectFault: () => void;
  canInjectFault: boolean;
}

export const SimulationControls = ({
  isPlaying,
  onPlayPause,
  onReset,
  onInjectFault,
  canInjectFault,
}: SimulationControlsProps) => {
  return (
    <div className="flex gap-3">
      <Button
        onClick={onPlayPause}
        size="lg"
        className="bg-primary hover:bg-primary/90 text-primary-foreground font-semibold"
      >
        {isPlaying ? (
          <>
            <Pause className="w-5 h-5 mr-2" />
            Pause
          </>
        ) : (
          <>
            <Play className="w-5 h-5 mr-2" />
            Start
          </>
        )}
      </Button>

      <Button
        onClick={onReset}
        size="lg"
        variant="outline"
        className="border-border hover:bg-muted"
      >
        <RotateCcw className="w-5 h-5 mr-2" />
        Reset
      </Button>

      <Button
        onClick={onInjectFault}
        size="lg"
        disabled={!canInjectFault}
        className="bg-fault hover:bg-fault/90 text-foreground font-semibold disabled:opacity-50"
      >
        <Zap className="w-5 h-5 mr-2" />
        Inject Fault
      </Button>
    </div>
  );
};
