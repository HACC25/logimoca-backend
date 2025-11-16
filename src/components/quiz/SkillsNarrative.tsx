import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { SkillRating } from "@/pages/Assessment";
import { ChevronRight, Lightbulb } from "lucide-react";

interface SkillsNarrativeProps {
  topSkills: SkillRating[];
  onComplete: (narrative: string) => void;
}

const SkillsNarrative = ({ topSkills, onComplete }: SkillsNarrativeProps) => {
  const [narrative, setNarrative] = useState("");

  const skillNames = topSkills.map(s => s.ElementName).join(", ");

  const handleSubmit = () => {
    onComplete(narrative);
  };

  const handleSkip = () => {
    onComplete("");
  };

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg">
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-6 h-6 text-primary" />
            <h1 className="text-3xl font-bold text-foreground">Tell Us More</h1>
          </div>
          <p className="text-muted-foreground">
            Help us better understand your experience by sharing a specific example.
          </p>
        </div>

        <div className="bg-secondary/20 border border-border rounded-lg p-6 mb-6">
          <h2 className="text-lg font-semibold text-foreground mb-3">
            Based on your responses, your strongest skills appear to be:
          </h2>
          <div className="flex flex-wrap gap-2 mb-4">
            {topSkills.map((skill) => (
              <span 
                key={skill.ElementId}
                className="px-4 py-2 bg-primary/10 text-primary border border-primary/20 rounded-lg font-medium"
              >
                {skill.ElementName}
              </span>
            ))}
          </div>
          <p className="text-foreground font-medium mt-4">
            Can you share a specific example where you used these skills?
          </p>
          <p className="text-sm text-muted-foreground mt-2">
            Describe the situation, what you did, and what the result was. This helps us refine your matches.
          </p>
        </div>

        <div className="mb-6">
          <Textarea
            placeholder={`For example: "I led our school's fundraiser for a local charity. I created a budget, coordinated with team members, and presented our plan to the principal. We ended up raising $2,000, which was double our goal."`}
            value={narrative}
            onChange={(e) => setNarrative(e.target.value)}
            className="min-h-[200px] resize-none text-base"
            maxLength={500}
          />
          <div className="flex justify-between items-center mt-2">
            <p className="text-sm text-muted-foreground">
              300-500 characters recommended
            </p>
            <p className="text-sm text-muted-foreground">
              {narrative.length} / 500
            </p>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <Button
            variant="ghost"
            onClick={handleSkip}
            className="text-muted-foreground"
          >
            Skip this step
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={narrative.length < 50}
            size="lg"
            className="bg-primary hover:bg-primary/90 group"
          >
            Find My Matches
            <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default SkillsNarrative;
