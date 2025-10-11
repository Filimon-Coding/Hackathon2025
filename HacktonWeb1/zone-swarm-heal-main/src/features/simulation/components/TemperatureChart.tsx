import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Card } from "@/components/ui/card";

interface TemperatureChartProps {
  data: { time: number; [key: string]: number }[];
  agentCount: number;
}

const AGENT_COLORS = [
  "hsl(var(--chart-1))",
  "hsl(var(--chart-2))",
  "hsl(var(--chart-3))",
  "hsl(var(--chart-4))",
  "hsl(var(--chart-5))",
  "hsl(var(--primary))",
];

export const TemperatureChart = ({ data, agentCount }: TemperatureChartProps) => {
  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Temperature History</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis 
            dataKey="time" 
            stroke="hsl(var(--muted-foreground))"
            label={{ value: "Time Steps", position: "insideBottom", offset: -5 }}
          />
          <YAxis 
            stroke="hsl(var(--muted-foreground))"
            label={{ value: "Temperature (°C)", angle: -90, position: "insideLeft" }}
            domain={[18, 40]}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "var(--radius)",
            }}
          />
          <Legend />
          {Array.from({ length: agentCount }).map((_, i) => (
            <Line
              key={`agent${i}`}
              type="monotone"
              dataKey={`agent${i}`}
              stroke={AGENT_COLORS[i % AGENT_COLORS.length]}
              strokeWidth={2}
              dot={false}
              name={`Agent ${i}`}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
};
