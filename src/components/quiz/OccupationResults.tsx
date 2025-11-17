import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { OccupationMatch, RIASECScores } from "@/pages/Assessment";
import { HoverCard, HoverCardContent, HoverCardTrigger } from "@/components/ui/hover-card";
import { DollarSign, TrendingUp, Clock } from "lucide-react";

interface OccupationResultsProps {
  occupations: OccupationMatch[];
  riasecScores: RIASECScores;
  onOccupationSelect: (occupation: OccupationMatch) => void;
  onBackToSkills: () => void;
  onBackToInterests: () => void;
}

const OccupationResults = ({ occupations, onOccupationSelect, onBackToSkills, onBackToInterests }: OccupationResultsProps) => {
  // Create 3 orbital rings with staggered positions for 20 occupations
  // Inner ring: 6 positions at radius 25%
  // Middle ring: 7 positions at radius 33%
  // Outer ring: 7 positions at radius 41%
  const generateOrbitPositions = () => {
    const positions = [];
    
    // Inner orbit - 6 positions, starting offset 0°
    const innerCount = 6;
    const innerRadius = 25;
    for (let i = 0; i < innerCount; i++) {
      const angle = (i * 360 / innerCount) - 90;
      const radians = (angle * Math.PI) / 180;
      positions.push({
        x: Math.round((50 + innerRadius * Math.cos(radians)) * 10) / 10,
        y: Math.round((50 + innerRadius * Math.sin(radians)) * 10) / 10
      });
    }
    
    // Middle orbit - 7 positions, offset by half interval for stagger
    const middleCount = 7;
    const middleRadius = 33;
    const middleOffset = 360 / (middleCount * 2); // Half interval offset
    for (let i = 0; i < middleCount; i++) {
      const angle = (i * 360 / middleCount) + middleOffset - 90;
      const radians = (angle * Math.PI) / 180;
      positions.push({
        x: Math.round((50 + middleRadius * Math.cos(radians)) * 10) / 10,
        y: Math.round((50 + middleRadius * Math.sin(radians)) * 10) / 10
      });
    }
    
    // Outer orbit - 7 positions, offset differently for more stagger
    const outerCount = 7;
    const outerRadius = 41;
    const outerOffset = 360 / (outerCount * 3); // Different offset
    for (let i = 0; i < outerCount; i++) {
      const angle = (i * 360 / outerCount) + outerOffset - 90;
      const radians = (angle * Math.PI) / 180;
      positions.push({
        x: Math.round((50 + outerRadius * Math.cos(radians)) * 10) / 10,
        y: Math.round((50 + outerRadius * Math.sin(radians)) * 10) / 10
      });
    }
    
    return positions;
  };

  // Desktop/tablet positions - 20 results in 3 orbits (6 + 7 + 7)
  const desktopPositions = generateOrbitPositions();

  // Mobile positions - 8 results in 2 orbits (4 inner + 4 outer)
  const generateMobilePositions = () => {
    const positions = [];
    
    // Inner orbit - 4 positions
    for (let i = 0; i < 4; i++) {
      const angle = (i * 90) - 90; // 90° apart
      const radians = (angle * Math.PI) / 180;
      positions.push({
        x: Math.round((50 + 28 * Math.cos(radians)) * 10) / 10,
        y: Math.round((50 + 28 * Math.sin(radians)) * 10) / 10
      });
    }
    
    // Outer orbit - 4 positions, offset by 45° for stagger
    for (let i = 0; i < 4; i++) {
      const angle = (i * 90) + 45 - 90; // Offset by 45°
      const radians = (angle * Math.PI) / 180;
      positions.push({
        x: Math.round((50 + 38 * Math.cos(radians)) * 10) / 10,
        y: Math.round((50 + 38 * Math.sin(radians)) * 10) / 10
      });
    }
    
    return positions;
  };

  const mobilePositions = generateMobilePositions();

  // Color variants for different occupations
  const getColor = (index: number) => {
    const colors = [
      "hsl(var(--uh-green))",
      "hsl(var(--accent))",
      "hsl(var(--primary))",
    ];
    return colors[index % colors.length];
  };

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      <Card className="p-4 md:p-8 shadow-lg bg-gradient-to-br from-background to-uh-green/5">
        {/* Navigation */}
        <div className="flex gap-2 mb-6">
          <Button 
            variant="outline" 
            onClick={onBackToInterests}
            className="text-sm"
          >
            ← Back to Interests
          </Button>
          <Button 
            variant="outline" 
            onClick={onBackToSkills}
            className="text-sm"
          >
            ← Back to Skills
          </Button>
        </div>

        {/* Header */}
        <div className="text-center mb-8 md:mb-12">
          <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-uh-green to-primary bg-clip-text text-transparent mb-4">
            Your Career Possibilities
          </h1>
          <p className="text-base md:text-lg text-muted-foreground max-w-2xl mx-auto">
            Explore careers based on your interests and skills. Hover over each career to learn more.
          </p>
        </div>

        {/* Career Map */}
        <div className="relative w-full h-[500px] md:h-[600px] bg-gradient-to-br from-muted/20 to-muted/5 rounded-xl border-2 border-border/50 mb-8 overflow-hidden">
          {/* Center Circle */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-uh-green/30 to-primary/30 rounded-full blur-3xl" />
              <Card className="relative w-32 h-32 md:w-48 md:h-48 rounded-full flex items-center justify-center border-4 border-border/50 bg-background/95 shadow-xl">
                <div className="text-center px-2 md:px-4">
                  <p className="text-xs md:text-sm font-medium text-muted-foreground mb-1">
                    Explore paths
                  </p>
                  <p className="text-[10px] md:text-xs text-muted-foreground">based on...</p>
                  <div className="mt-1 md:mt-2 text-xl md:text-2xl">
                    🎯 💪
                  </div>
                </div>
              </Card>
            </div>
          </div>

          {/* Career Dots - Desktop (15 results) */}
          <div className="hidden md:block">
            {occupations.map((occupation, index) => {
              const pos = desktopPositions[index] || { x: 50, y: 50 };
              const color = getColor(index);

              return (
                <HoverCard key={occupation.onetCode} openDelay={200}>
                  <HoverCardTrigger asChild>
                    <button
                      className="absolute group cursor-pointer animate-[float_3s_ease-in-out_infinite]"
                      style={{
                        left: `${pos.x}%`,
                        top: `${pos.y}%`,
                        transform: 'translate(-50%, -50%)',
                        animationDelay: `${index * 0.2}s`,
                      }}
                      onClick={() => onOccupationSelect(occupation)}
                    >
                      {/* Glow effect */}
                      <div
                        className="absolute inset-0 rounded-full blur-xl opacity-40 group-hover:opacity-70 transition-opacity"
                        style={{ backgroundColor: color }}
                      />
                      
                      {/* Dot */}
                      <div
                        className="relative w-3 h-3 rounded-full transition-transform group-hover:scale-150"
                        style={{ backgroundColor: color }}
                      />
                      
                      {/* Label - always visible */}
                      <div className="absolute top-5 left-1/2 -translate-x-1/2 whitespace-nowrap">
                        <p className="text-xs font-medium text-foreground bg-background/95 px-2 py-1 rounded-md shadow-lg border border-border">
                          {occupation.title}
                        </p>
                      </div>
                    </button>
                  </HoverCardTrigger>
                  <HoverCardContent className="w-80" side="top">
                    <div className="space-y-3">
                      <div>
                        <h3 className="font-bold text-lg mb-1">{occupation.title}</h3>
                        <p className="text-sm text-muted-foreground">{occupation.description}</p>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                          <DollarSign className="w-4 h-4 text-uh-green" />
                          <span className="font-medium">
                            ${(occupation.medianSalary / 1000).toFixed(0)}k
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="w-4 h-4 text-accent" />
                          <span className="text-xs">{occupation.growthOutlook}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-1 text-sm">
                        <Clock className="w-4 h-4 text-primary" />
                        <span className="text-xs">{occupation.trainingDuration}</span>
                      </div>

                      <div>
                        <p className="text-xs font-semibold mb-2">Top Skills:</p>
                        <div className="flex flex-wrap gap-1">
                          {occupation.topSkills.map((skill) => (
                            <span
                              key={skill}
                              className="text-xs bg-muted px-2 py-1 rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>

                      <Button
                        size="sm"
                        className="w-full bg-uh-green hover:bg-uh-green/90"
                        onClick={() => onOccupationSelect(occupation)}
                      >
                        Explore Programs
                      </Button>
                    </div>
                  </HoverCardContent>
                </HoverCard>
              );
            })}
          </div>

          {/* Career Dots - Mobile (8 results) */}
          <div className="md:hidden">
            {occupations.slice(0, 8).map((occupation, index) => {
              const pos = mobilePositions[index] || { x: 50, y: 50 };
              const color = getColor(index);

              return (
                <HoverCard key={occupation.onetCode} openDelay={200}>
                  <HoverCardTrigger asChild>
                    <button
                      className="absolute group cursor-pointer animate-[float_3s_ease-in-out_infinite]"
                      style={{
                        left: `${pos.x}%`,
                        top: `${pos.y}%`,
                        transform: 'translate(-50%, -50%)',
                        animationDelay: `${index * 0.2}s`,
                      }}
                      onClick={() => onOccupationSelect(occupation)}
                    >
                      {/* Glow effect */}
                      <div
                        className="absolute inset-0 rounded-full blur-xl opacity-40 group-hover:opacity-70 transition-opacity"
                        style={{ backgroundColor: color }}
                      />
                      
                      {/* Dot */}
                      <div
                        className="relative w-3 h-3 rounded-full transition-transform group-hover:scale-150"
                        style={{ backgroundColor: color }}
                      />
                      
                      {/* Label - always visible */}
                      <div className="absolute top-5 left-1/2 -translate-x-1/2 whitespace-nowrap">
                        <p className="text-[10px] font-medium text-foreground bg-background/95 px-2 py-1 rounded-md shadow-lg border border-border">
                          {occupation.title}
                        </p>
                      </div>
                    </button>
                  </HoverCardTrigger>
                  <HoverCardContent className="w-80" side="top">
                    <div className="space-y-3">
                      <div>
                        <h3 className="font-bold text-lg mb-1">{occupation.title}</h3>
                        <p className="text-sm text-muted-foreground">{occupation.description}</p>
                      </div>
                      
                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                          <DollarSign className="w-4 h-4 text-uh-green" />
                          <span className="font-medium">
                            ${(occupation.medianSalary / 1000).toFixed(0)}k
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <TrendingUp className="w-4 h-4 text-accent" />
                          <span className="text-xs">{occupation.growthOutlook}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-1 text-sm">
                        <Clock className="w-4 h-4 text-primary" />
                        <span className="text-xs">{occupation.trainingDuration}</span>
                      </div>

                      <div>
                        <p className="text-xs font-semibold mb-2">Top Skills:</p>
                        <div className="flex flex-wrap gap-1">
                          {occupation.topSkills.map((skill) => (
                            <span
                              key={skill}
                              className="text-xs bg-muted px-2 py-1 rounded-full"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>

                      <Button
                        size="sm"
                        className="w-full bg-uh-green hover:bg-uh-green/90"
                        onClick={() => onOccupationSelect(occupation)}
                      >
                        Explore Programs
                      </Button>
                    </div>
                  </HoverCardContent>
                </HoverCard>
              );
            })}
          </div>
        </div>

        {/* Instructions */}
        <div className="text-center text-sm text-muted-foreground">
          <p>Click on any career to explore education programs and pathways</p>
        </div>
      </Card>
    </div>
  );
};

export default OccupationResults;
