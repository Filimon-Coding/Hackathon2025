import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export const Scene1 = () => {
  const [fadeIn, setFadeIn] = useState(false);
  const [showLogo, setShowLogo] = useState(false);

  useEffect(() => {
    const timer1 = setTimeout(() => setFadeIn(true), 500);
    const timer2 = setTimeout(() => setShowLogo(true), 3000);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  return (
    <div className="relative w-full h-full bg-gradient-to-b from-background via-background/95 to-background/90 overflow-hidden">
      {/* Animated particles background */}
      <div className="absolute inset-0 opacity-30">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-primary rounded-full animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${2 + Math.random() * 3}s`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8 text-center">
        {!showLogo ? (
          <div
            className={cn(
              "space-y-8 transition-all duration-1000",
              fadeIn ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
            )}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-4">
              Can a Data Center Think?
            </h1>
            <div className="space-y-6 text-xl md:text-2xl text-muted-foreground max-w-4xl">
              <p className="animate-fade-in" style={{ animationDelay: "0.5s" }}>
                Every minute, data centers consume gigawatts just to stay cool.
              </p>
              <p className="animate-fade-in" style={{ animationDelay: "1.5s" }}>
                What if they could think collectively — and heal themselves?
              </p>
            </div>
          </div>
        ) : (
          <div
            className={cn(
              "space-y-6 transition-all duration-1000",
              "animate-fade-in"
            )}
          >
            <div className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent animate-scale-in">
              Self-Healing Swarm AI
            </div>
            <div className="text-3xl md:text-4xl font-semibold text-foreground">
              Cooling System
            </div>
            <div className="text-xl text-muted-foreground pt-4">
              Built by Patron Oslomet
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
