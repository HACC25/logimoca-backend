import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { RIASECScores } from "@/pages/Assessment";
import { ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { highSchool40Skills, oneStop40Skills, TaskStatement } from "@/data/skillsData";

// Export for use in summary component - return appropriate dataset based on student type
export const getTaskStatements = (studentType: "high-school" | "professional"): TaskStatement[] => {
  return studentType === "high-school" ? highSchool40Skills : oneStop40Skills;
};

interface SkillsAssessmentProps {
  riasecScores: RIASECScores;
  studentType: "high-school" | "professional";
  onComplete: (selections: Record<string, boolean>) => void;
  initialSelections?: Record<string, boolean>;
  shownStatementIds?: string[];
  onClear?: () => void;
}

const SkillsAssessment = ({ 
  studentType, 
  onComplete, 
  initialSelections = {}, 
  shownStatementIds = [],
  onClear 
}: SkillsAssessmentProps) => {
  const [selections, setSelections] = useState<Record<string, boolean>>(initialSelections);
  const [visibleCount, setVisibleCount] = useState(12);
  const [currentStudentType, setCurrentStudentType] = useState(studentType);

  useEffect(() => {
    sessionStorage.setItem("skills-selections", JSON.stringify(selections));
  }, [selections]);

  // Sync local state when external selections change
  useEffect(() => {
    setSelections(initialSelections);
  }, [initialSelections]);

  // Reset visibleCount when student type changes (profile switch)
  useEffect(() => {
    if (currentStudentType !== studentType) {
      setCurrentStudentType(studentType);
      setVisibleCount(12);
    }
  }, [studentType, currentStudentType]);

  // Get all available statements for this student type
  const allStatements = getTaskStatements(studentType);
  
  // Track which unseen statements to show
  const unseenStatements = allStatements.filter(
    (s) => !shownStatementIds.includes(s.ElementId)
  );
  
  // Build currentTasks maintaining original order:
  // Show first N unseen statements OR already selected statements
  const unseenCount = Math.min(visibleCount, unseenStatements.length);
  const unseenIds = new Set(unseenStatements.slice(0, unseenCount).map(s => s.ElementId));
  
  const currentTasks = allStatements.filter((s) => 
    selections[s.ElementId] || unseenIds.has(s.ElementId)
  );
  
  const hasMoreToShow = unseenCount < unseenStatements.length;

  const handleToggle = (elementId: string) => {
    setSelections({
      ...selections,
      [elementId]: !selections[elementId],
    });
  };

  const selectedCount = Object.values(selections).filter(Boolean).length;

  const handleNext = () => {
    onComplete(selections);
  };

  const handleAddMore = () => {
    setVisibleCount((prev) => Math.min(prev + 12, unseenStatements.length));
  };

  const canProceed = selectedCount >= 3;

  return (
    <div className="max-w-5xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg bg-gradient-to-br from-background to-uh-green/5">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-uh-green to-primary bg-clip-text text-transparent">
              Skills Experience Check
            </h1>
            <Badge variant="secondary" className="text-sm">
              {studentType === "high-school" ? "High School Student" : "Returning Professional"}
            </Badge>
          </div>
          <p className="text-muted-foreground mb-4">
            Select the skills and experiences you have. Choose at least 3 to continue.
          </p>
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground mb-1">
              <span>Showing {currentTasks.length} statements</span>
              <span>{selectedCount} selected</span>
            </div>
          </div>
        </div>

        {/* Skill Pills - 3 columns for 12 items */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mb-8">
          {currentTasks.map((task) => {
            const isSelected = selections[task.ElementId];

            return (
              <Button
                key={task.ElementId}
                variant={isSelected ? "default" : "outline"}
                size="lg"
                onClick={() => handleToggle(task.ElementId)}
                className={`text-sm md:text-base py-4 px-4 h-auto whitespace-normal text-left transition-all ${
                  isSelected
                    ? "bg-uh-green hover:bg-uh-green/90 text-uh-green-foreground border-uh-green"
                    : "hover:bg-muted"
                }`}
              >
                {task.statement}
              </Button>
            );
          })}
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center gap-4">
          {onClear && (
            <Button
              variant="outline"
              onClick={onClear}
              size="lg"
            >
              Clear All
            </Button>
          )}
          {hasMoreToShow && (
            <Button
              variant="outline"
              onClick={handleAddMore}
              size="lg"
              className={!onClear ? "" : "ml-auto"}
            >
              Add More
            </Button>
          )}
          <Button
            onClick={handleNext}
            disabled={!canProceed}
            size="lg"
            className="bg-primary hover:bg-primary/90 group ml-auto"
          >
            Continue
            <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>

        {!canProceed && (
          <p className="text-sm text-muted-foreground text-center mt-4">Please select at least 3 skills to continue</p>
        )}
      </Card>
    </div>
  );
};

export default SkillsAssessment;
