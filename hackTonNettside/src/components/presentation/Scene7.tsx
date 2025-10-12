import { Card } from "@/components/ui/card";
import { Leaf, Cog, DollarSign, Globe } from "lucide-react";

export const Scene7 = () => {
  const impacts = [
    {
      icon: Leaf,
      title: "Energy Efficiency",
      description: "Savings in cooling costs",
      color: "text-optimal",
      bgColor: "bg-optimal/10",
      borderColor: "border-optimal/30",
    },
    {
      icon: Cog,
      title: "Fault Resilience",
      description: "Predictive AI prevents overheating",
      color: "text-primary",
      bgColor: "bg-primary/10",
      borderColor: "border-primary/30",
    },
    {
      icon: DollarSign,
      title: "Cost Reduction",
      description: "Fewer failures, lower maintenance",
      color: "text-warning",
      bgColor: "bg-warning/10",
      borderColor: "border-warning/30",
    },
    {
      icon: Globe,
      title: "Sustainability",
      description: "Smarter cooling for a greener planet",
      color: "text-cooling",
      bgColor: "bg-cooling/10",
      borderColor: "border-cooling/30",
    },
  ];

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-optimal/5 via-background to-cooling/5 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(16,185,129,0.1)_0%,transparent_50%),radial-gradient(circle_at_bottom_left,rgba(79,209,197,0.1)_0%,transparent_50%)]" />
      
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8">
        <div className="max-w-6xl space-y-12">
          <div className="text-center space-y-4 animate-fade-in">
            <h2 className="text-5xl md:text-6xl font-bold text-foreground">
              Real-World Impact
            </h2>
            <p className="text-xl text-muted-foreground">
              Transforming data center operations through AI innovation
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {impacts.map((impact, idx) => (
              <Card
                key={idx}
                className={`p-8 ${impact.bgColor} ${impact.borderColor} backdrop-blur-sm hover:scale-105 transition-all duration-300 animate-scale-in`}
                style={{ animationDelay: `${idx * 0.15}s` }}
              >
                <impact.icon className={`w-16 h-16 mb-4 ${impact.color}`} />
                <h3 className="text-2xl font-bold text-foreground mb-2">
                  {impact.title}
                </h3>
                <p className="text-lg text-muted-foreground">
                  {impact.description}
                </p>
              </Card>
            ))}
          </div>

          <Card className="p-8 bg-gradient-to-r from-primary/10 via-optimal/10 to-cooling/10 border-primary/30 animate-fade-in" style={{ animationDelay: "0.8s" }}>
            <p className="text-center text-2xl md:text-3xl text-foreground font-semibold">
              AI transforms reactive cooling into adaptive intelligence
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
