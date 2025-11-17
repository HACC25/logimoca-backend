import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RIASECScores } from "@/pages/Assessment";
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from "recharts";
import { ChevronRight, ExternalLink } from "lucide-react";
import { useState } from "react";
import realisticImg from "@/assets/riasec-realistic.jpg";
import investigativeImg from "@/assets/riasec-investigative.jpg";
import artisticImg from "@/assets/riasec-artistic.jpg";
import socialImg from "@/assets/riasec-social.jpg";
import enterprisingImg from "@/assets/riasec-enterprising.jpg";
import conventionalImg from "@/assets/riasec-conventional.jpg";

interface RIASECResultsProps {
  riasecScores: RIASECScores;
  onContinue: () => void;
  onBack: () => void;
  onClear: () => void;
}

const riasecInfo = {
  Realistic: {
    color: "hsl(var(--uh-navy))",
    description: "People with Realistic interests like work that includes practical, hands-on problems and answers.",
    careers: ["Electrician", "Mechanical Engineer", "Chef", "Carpenter"],
    image: realisticImg
  },
  Investigative: {
    color: "hsl(var(--uh-green))",
    description: "People with Investigative interests like work that has to do with ideas and thinking.",
    careers: ["Biologist", "Software Developer", "Data Analyst", "Chemist"],
    image: investigativeImg
  },
  Artistic: {
    color: "hsl(142 71% 45%)",
    description: "People with Artistic interests like work that deals with the artistic side of things.",
    careers: ["Graphic Designer", "Musician", "Writer", "Interior Designer"],
    image: artisticImg
  },
  Social: {
    color: "hsl(25 95% 53%)",
    description: "People with Social interests like working with others to help them learn and grow.",
    careers: ["Teacher", "Counselor", "Social Worker", "Nurse"],
    image: socialImg
  },
  Enterprising: {
    color: "hsl(0 84% 60%)",
    description: "People with Enterprising interests like work that has to do with starting up and carrying out business projects.",
    careers: ["Sales Manager", "Marketing Director", "Entrepreneur", "Lawyer"],
    image: enterprisingImg
  },
  Conventional: {
    color: "hsl(221 83% 53%)",
    description: "People with Conventional interests like work that follows set procedures and routines.",
    careers: ["Accountant", "Administrative Assistant", "Database Administrator", "Financial Analyst"],
    image: conventionalImg
  }
};

const RIASECResults = ({ riasecScores, onContinue, onBack, onClear }: RIASECResultsProps) => {
  const [showAllAreas, setShowAllAreas] = useState(false);
  
  // Prepare data for radar chart
  const chartData = Object.entries(riasecScores).map(([key, value]) => ({
    subject: key,
    score: value,
    fullName: key,
    fill: riasecInfo[key as keyof typeof riasecInfo].color
  }));

  // Get top 3 interests and remaining
  const sortedScores = Object.entries(riasecScores)
    .sort(([, a], [, b]) => b - a);
  
  const top3Interests = sortedScores.slice(0, 3);
  const remainingInterests = sortedScores.slice(3);

  const topInterests = top3Interests.map(([key]) => key.charAt(0)).join("");

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">Your Interest Profile</h1>
          <p className="text-lg text-muted-foreground mb-4">
            Your RIASEC Code: <span className="font-bold text-primary text-2xl">{topInterests}</span>
          </p>
          <p className="text-muted-foreground">
            This profile helps match you with careers that align with your interests.
          </p>
        </div>

        {/* Radar Chart */}
        <div className="mb-8 bg-secondary/20 rounded-lg p-6">
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={chartData}>
              <PolarGrid stroke="hsl(var(--border))" />
              <PolarAngleAxis 
                dataKey="fullName" 
                tick={({ x, y, payload }) => {
                  const info = riasecInfo[payload.value as keyof typeof riasecInfo];
                  return (
                    <text 
                      x={x} 
                      y={y} 
                      textAnchor="middle" 
                      fill={info.color}
                      fontSize={12}
                      fontWeight={600}
                    >
                      {payload.value}
                    </text>
                  );
                }}
              />
              <PolarRadiusAxis angle={90} domain={[0, 25]} tick={{ fill: 'hsl(var(--muted-foreground))' }} />
              <Radar 
                name="Your Scores" 
                dataKey="score" 
                stroke="hsl(var(--primary))" 
                fill="hsl(var(--primary))" 
                fillOpacity={0.3}
                strokeWidth={2}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Top 3 Interest Areas */}
        <div className="mb-8">
          <h2 className="text-2xl font-semibold text-foreground mb-6">Your Top Interest Areas</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {top3Interests.map(([domain, score], index) => {
              const info = riasecInfo[domain as keyof typeof riasecInfo];
              const percentage = (score / 25) * 100;
              
              return (
                <Card key={domain} className="overflow-hidden border-2 hover:shadow-lg transition-shadow" style={{ borderColor: info.color }}>
                  <div className="relative h-48 overflow-hidden">
                    <img 
                      src={info.image} 
                      alt={domain}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute top-4 right-4 bg-background/90 backdrop-blur-sm px-3 py-1 rounded-full">
                      <span className="text-lg font-bold" style={{ color: info.color }}>#{index + 1}</span>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="text-xl font-semibold text-foreground">{domain}</h3>
                      <div className="text-right ml-2">
                        <div className="text-2xl font-bold" style={{ color: info.color }}>{score}</div>
                        <div className="text-sm text-muted-foreground">{Math.round(percentage)}%</div>
                      </div>
                    </div>
                    
                    <p className="text-sm text-muted-foreground mb-4">{info.description}</p>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-secondary rounded-full h-2 mb-4">
                      <div 
                        className="h-2 rounded-full transition-all duration-500"
                        style={{ 
                          width: `${percentage}%`,
                          backgroundColor: info.color
                        }}
                      />
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium text-foreground mb-2">Example Careers:</p>
                      <div className="flex flex-wrap gap-2">
                        {info.careers.map((career) => (
                          <span 
                            key={career} 
                            className="px-2 py-1 bg-secondary text-secondary-foreground rounded-full text-xs"
                          >
                            {career}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Remaining Areas Footer */}
        <Card className="p-6 bg-secondary/30 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground">Other Interest Areas</h3>
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => setShowAllAreas(!showAllAreas)}
              className="text-primary hover:text-primary/80"
            >
              {showAllAreas ? "Show Less" : "Read About All 6 Areas"}
              <ExternalLink className="ml-2 h-4 w-4" />
            </Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {remainingInterests.map(([domain, score]) => {
              const info = riasecInfo[domain as keyof typeof riasecInfo];
              const percentage = (score / 25) * 100;
              
              return (
                <div key={domain} className="flex items-center justify-between p-4 bg-background rounded-lg border">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-12 rounded-full" style={{ backgroundColor: info.color }} />
                    <div>
                      <h4 className="font-semibold text-foreground">{domain}</h4>
                      <p className="text-sm text-muted-foreground">Score: {score} ({Math.round(percentage)}%)</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          
          {showAllAreas && (
            <div className="mt-6 pt-6 border-t space-y-4">
              {remainingInterests.map(([domain]) => {
                const info = riasecInfo[domain as keyof typeof riasecInfo];
                
                return (
                  <div key={domain} className="p-4 bg-background rounded-lg">
                    <h4 className="font-semibold text-foreground mb-2" style={{ color: info.color }}>{domain}</h4>
                    <p className="text-sm text-muted-foreground mb-3">{info.description}</p>
                    <div>
                      <p className="text-xs font-medium text-foreground mb-2">Example Careers:</p>
                      <div className="flex flex-wrap gap-2">
                        {info.careers.map((career) => (
                          <span 
                            key={career} 
                            className="px-2 py-1 bg-secondary text-secondary-foreground rounded-full text-xs"
                          >
                            {career}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>

        {/* Continue Button */}
        <div className="flex justify-between items-center">
          <div className="flex gap-2">
            <Button 
              onClick={onBack}
              variant="outline"
              size="lg"
            >
              Back to Summary
            </Button>
            <Button 
              onClick={onClear}
              variant="outline"
              size="lg"
            >
              Clear All
            </Button>
          </div>
          <Button 
            onClick={onContinue}
            size="lg"
            className="bg-primary hover:bg-primary/90 text-primary-foreground group"
          >
            Continue to Skills Assessment
            <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default RIASECResults;
