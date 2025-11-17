import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit } from "lucide-react";

interface InterestSummaryProps {
  answers: Record<number, number>;
  questions: Array<{ index: number; area: string; text: string }>;
  onEdit: () => void;
  onContinue: () => void;
  onClear: () => void;
}

const getEmojiForRating = (rating: number) => {
  if (rating === 1) return "😞";
  if (rating === 2) return "😕";
  if (rating === 3) return "🤔";
  if (rating === 4) return "😊";
  return "🤩";
};


const getLabelForRating = (rating: number) => {
  if (rating === 1) return "Strongly Dislike";
  if (rating === 2) return "Dislike";
  if (rating === 3) return "Unsure";
  if (rating === 4) return "Like";
  return "Strongly Like";
};

const getBackgroundForRating = (rating: number) => {
  if (rating === 1) return "bg-red-100 dark:bg-red-950/30 border-red-300 dark:border-red-900/50";
  if (rating === 2) return "bg-rose-100 dark:bg-rosee-950/30 border-rose-300 dark:border-rose-900/50";
  if (rating === 3) return "bg-gray-200 dark:bg-gray-900/30 border-gray-300 dark:border-gray-800/50";
  if (rating === 4) return "bg-emerald-100 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-900/50";
  return "bg-cyan-100 dark:bg-cyan-950/30 border-cyan-300 dark:border-cyan-900/50";
};

const InterestSummary = ({ answers, questions, onEdit, onContinue, onClear }: InterestSummaryProps) => {
  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <Card className="shadow-lg">
        <CardHeader className="bg-gradient-to-r from-uh-green to-uh-green/80 text-white">
          <div className="flex justify-between items-center">
            <CardTitle className="text-3xl">Your Interest Assessment Summary</CardTitle>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={onEdit}
                className="bg-white/10 hover:bg-white/20 text-white border-white/30"
              >
                <Edit className="w-4 h-4 mr-2" />
                Edit Answers
              </Button>
              <Button
                variant="outline"
                onClick={onClear}
                className="bg-white/10 hover:bg-white/20 text-white border-white/30"
              >
                Clear All
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-8">
          <p className="text-muted-foreground mb-6">
            Review your responses before continuing. You can edit any answer by clicking the button above.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 mb-8 max-h-[500px] overflow-y-auto">
            {questions.map((question) => {
              const answer = answers[question.index - 1] ?? 3;
              return (
                <div
                  key={question.index}
                  className={`p-3 rounded-lg border transition-colors ${getBackgroundForRating(answer)}`}
                >
                  <div className="flex flex-col items-center gap-2 text-center">
                    <div className="text-3xl">{getEmojiForRating(answer)}</div>
                    <p className="font-medium text-foreground text-sm leading-tight">{question.text}</p>
                    <p className="text-xs text-muted-foreground">{getLabelForRating(answer)}</p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-end">
            <Button onClick={onContinue} size="lg" className="bg-primary hover:bg-primary/90">
              Continue to Results
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default InterestSummary;
