import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Play, Pause, RotateCcw } from "lucide-react";

interface ControlPanelProps {
  isRunning: boolean;
  onToggle: () => void;
  onReset: () => void;
  time: number;
}

export const ControlPanel = ({ isRunning, onToggle, onReset, time }: ControlPanelProps) => {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold mb-1">Simulation Control</h2>
          <p className="text-sm text-muted-foreground">
            Time Step: <span className="data-value text-primary">{time}</span>
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={onToggle}
            variant={isRunning ? "secondary" : "default"}
            size="lg"
          >
            {isRunning ? (
              <>
                <Pause className="mr-2 h-5 w-5" />
                Pause
              </>
            ) : (
              <>
                <Play className="mr-2 h-5 w-5" />
                Start
              </>
            )}
          </Button>
          <Button onClick={onReset} variant="outline" size="lg">
            <RotateCcw className="mr-2 h-5 w-5" />
            Reset
          </Button>
        </div>
      </div>
    </Card>
  );
};
