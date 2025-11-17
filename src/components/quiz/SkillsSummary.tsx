import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Edit } from "lucide-react";

interface SkillsSummaryProps {
  selections: Record<string, boolean>;
  taskStatements: Array<{
    ElementId: string;
    ElementName: string;
    statement: string;
  }>;
  onEdit: () => void;
  onContinue: () => void;
  onAnswerMore: () => void;
  onClear: () => void;
}

const SkillsSummary = ({
  selections,
  taskStatements,
  onEdit,
  onContinue,
  onAnswerMore,
  onClear,
}: SkillsSummaryProps) => {
  const selectedSkills = taskStatements.filter(
    (task) => selections[task.ElementId]
  );
  const selectedCount = selectedSkills.length;

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg bg-gradient-to-br from-background to-uh-green/5">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-uh-green to-primary bg-clip-text text-transparent">
              Your Skills Summary
            </h1>
            <div className="flex gap-2">
              <Button variant="outline" onClick={onEdit} size="sm">
                <Edit className="w-4 h-4 mr-2" />
                Edit Answers
              </Button>
              <Button variant="outline" onClick={onClear} size="sm">
                Clear All
              </Button>
            </div>
          </div>
          <p className="text-muted-foreground">
            Review the skills you selected before continuing to your career matches.
          </p>
        </div>

        {/* Selected Skills Display */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4 text-center">
            You selected {selectedCount} skill{selectedCount !== 1 ? 's' : ''}
          </h2>
          <div className="flex flex-wrap gap-2 justify-center">
            {selectedSkills.map((task) => (
              <Badge
                key={task.ElementId}
                variant="default"
                className="bg-uh-green text-uh-green-foreground text-sm py-2 px-4"
              >
                {task.ElementName}
              </Badge>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-between items-center">
          <Button onClick={onAnswerMore} variant="outline" size="lg">
            Add More
          </Button>
          <Button
            onClick={onContinue}
            size="lg"
            className="bg-primary hover:bg-primary/90"
          >
            Continue to Career Matches
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default SkillsSummary;
