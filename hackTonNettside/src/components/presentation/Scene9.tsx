import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export const Scene9 = () => {
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setFadeIn(true), 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative w-full h-full bg-gradient-to-b from-background via-primary/5 to-secondary/10 overflow-hidden">
      {/* Network globe visualization */}
      <div className="absolute inset-0 flex items-center justify-center opacity-20">
        <div className="relative w-96 h-96">
          {[...Array(8)].map((_, i) => (
            <div
              key={i}
              className="absolute top-1/2 left-1/2 w-full h-full border-2 border-primary rounded-full"
              style={{
                transform: `translate(-50%, -50%) rotateY(${i * 45}deg)`,
                animation: `spin ${20 + i * 2}s linear infinite`,
              }}
            />
          ))}
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-primary rounded-full animate-pulse"
              style={{
                left: `${20 + Math.random() * 60}%`,
                top: `${20 + Math.random() * 60}%`,
                animationDelay: `${Math.random() * 2}s`,
              }}
            />
          ))}
        </div>
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8 text-center">
        <div
          className={cn(
            "space-y-12 max-w-5xl transition-all duration-1000",
            fadeIn ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
          )}
        >
          <div className="space-y-6">
            <p className="text-2xl md:text-3xl text-muted-foreground italic leading-relaxed">
              Inspired by biology — swarms, immune systems, and homeostasis —
            </p>
            <p className="text-2xl md:text-3xl text-foreground leading-relaxed">
              we're bringing intelligence to the beating heart of the digital world.
            </p>
          </div>

          <div className="space-y-8 pt-8">
            <div className="text-6xl md:text-7xl font-bold bg-gradient-to-r from-primary via-optimal to-secondary bg-clip-text text-transparent">
              Self-Healing Swarm AI
            </div>
            <div className="text-3xl md:text-4xl font-semibold text-foreground">
              Cooling System
            </div>
            <div className="flex items-center justify-center gap-8 text-xl md:text-2xl text-muted-foreground pt-4">
              <span className="px-4 py-2 rounded-full bg-optimal/20 text-optimal font-semibold">
                Autonomous
              </span>
              <span className="px-4 py-2 rounded-full bg-primary/20 text-primary font-semibold">
                Resilient
              </span>
              <span className="px-4 py-2 rounded-full bg-cooling/20 text-cooling font-semibold">
                Sustainable
              </span>
            </div>
          </div>

          <div className="text-lg text-muted-foreground pt-8 animate-pulse">
            Built by Patron Oslomet
          </div>
        </div>
      </div>
    </div>
  );
};
