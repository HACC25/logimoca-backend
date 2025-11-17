import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { RIASECScores } from "@/pages/Assessment";
import { computeRiasecCode, submitRiasecCode } from "@/services/assessmentService";

// Back up RIASEC Questions from the uploaded JSON if query fails.
const questions = [
  { index: 1, area: "Realistic", text: "Build kitchen cabinets" },
  { index: 2, area: "Investigative", text: "Develop a new medicine" },
  { index: 3, area: "Artistic", text: "Write books or plays" },
  { index: 4, area: "Social", text: "Help people with personal or emotional problems" },
  { index: 5, area: "Enterprising", text: "Manage a department within a large company" },
  { index: 6, area: "Conventional", text: "Install software across computers on a large network" },
  { index: 7, area: "Realistic", text: "Repair household appliances" },
  { index: 8, area: "Investigative", text: "Study ways to reduce water pollution" },
  { index: 9, area: "Artistic", text: "Compose or arrange music" },
  { index: 10, area: "Social", text: "Give career guidance to people" },
  { index: 11, area: "Enterprising", text: "Start your own business" },
  { index: 12, area: "Conventional", text: "Operate a calculator" },
  { index: 13, area: "Realistic", text: "Assemble electronic parts" },
  { index: 14, area: "Investigative", text: "Conduct chemical experiments" },
  { index: 15, area: "Artistic", text: "Create special effects for movies" },
  { index: 16, area: "Social", text: "Teach an individual an exercise routine" },
  { index: 17, area: "Enterprising", text: "Sell merchandise at a department store" },
  { index: 18, area: "Conventional", text: "Compute and record statistical and other numerical data" },
  { index: 19, area: "Realistic", text: "Fix a broken faucet" },
  { index: 20, area: "Investigative", text: "Examine blood samples using a microscope" },
  { index: 21, area: "Artistic", text: "Create dance routines for a show" },
  { index: 22, area: "Social", text: "Help people who have problems with drugs or alcohol" },
  { index: 23, area: "Enterprising", text: "Manage a clothing store" },
  { index: 24, area: "Conventional", text: "Keep shipping and receiving records" },
  { index: 25, area: "Realistic", text: "Lay brick or tile" },
  { index: 26, area: "Investigative", text: "Investigate the cause of a fire" },
  { index: 27, area: "Artistic", text: "Edit movies" },
  { index: 28, area: "Social", text: "Perform rehabilitation therapy" },
  { index: 29, area: "Enterprising", text: "Operate a beauty salon or barber shop" },
  { index: 30, area: "Conventional", text: "Inventory supplies using a hand-held computer" },
];

const QUESTIONS_PER_PAGE = 6;

interface RIASECQuizProps {
  onComplete: (answers: Record<number, number>) => void;
  initialAnswers?: Record<number, number>;
  onClear?: () => void;
}

const emojis = ["😞", "🫤", "🤔", "😊", "🤩"];
const labels = ["Strongly Dislike", "Dislike", "Unsure", "Like", "Strongly Like"];

const getBackgroundForRating = (rating: number, isSelected: boolean) => {
  if (!isSelected) return "";
  if (rating === 1) return "bg-red-100 dark:bg-red-950/30 border-red-300 dark:border-red-900/50";
  if (rating === 2) return "bg-amber-100 dark:bg-amber-950/30 border-amber-300 dark:border-amber-900/50";
  if (rating === 3) return "bg-gray-200 dark:bg-gray-900/30 border-gray-300 dark:border-gray-800/50";
  if (rating === 4) return "bg-emerald-100 dark:bg-emerald-950/30 border-emerald-300 dark:border-emerald-900/50";
  return "bg-cyan-100 dark:bg-cyan-950/30 border-cyan-300 dark:border-cyan-900/50";
};

const RIASECQuiz = ({ onComplete, initialAnswers = {}, onClear }: RIASECQuizProps) => {
  const [currentPage, setCurrentPage] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>(initialAnswers);

  useEffect(() => {
    sessionStorage.setItem("riasec-answers", JSON.stringify(answers));
  }, [answers]);

  const totalPages = Math.ceil(questions.length / QUESTIONS_PER_PAGE);
  const progress = ((currentPage + 1) / totalPages) * 100;

  const startIndex = currentPage * QUESTIONS_PER_PAGE;
  const currentQuestions = questions.slice(startIndex, startIndex + QUESTIONS_PER_PAGE);

  const getAnswer = (questionIndex: number) => answers[questionIndex] ?? 3;

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    } else {
      // Compute 3-letter code and send to backend for baseline results
      try {
        const code = computeRiasecCode(answers, questions as any);
        // Persist answers for back/forward navigation
        sessionStorage.setItem("riasec-code", code);
        // Fire-and-forget to hydrate downstream results screens
        // Request more occupations to enrich the jobs map (e.g., 20 instead of 10)
        submitRiasecCode(code, 20)
          .then((result) => {
            sessionStorage.setItem("riasec-result", JSON.stringify(result));
          })
          .catch((err) => {
            console.error("RISEAC submit failed", err);
          });
      } catch (e) {
        console.error("Error computing/submitting RIASEC code", e);
      }
      onComplete(answers);
    }
  };

  const handlePrevious = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleEmojiClick = (questionIndex: number, value: number) => {
    setAnswers({ ...answers, [questionIndex]: value });
  };

  return (
    <div className="max-w-3xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg bg-gradient-to-br from-background via-background to-uh-green/5">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-uh-green to-primary bg-clip-text text-transparent mb-2">
            Interest Assessment
          </h1>
          <p className="text-muted-foreground mb-4">
            Rate your interest in each activity using the emoji buttons. There are no right or wrong answers.
          </p>

          {/* Emoji Guide */}
          <div className="mb-4 p-4 rounded-lg bg-muted/50 border border-border">
            <div className="flex justify-between items-center gap-2">
              {emojis.map((emoji, index) => (
                <div key={index} className="flex flex-col items-center flex-1">
                  <div className="text-2xl mb-1">{emoji}</div>
                  <div className="text-xs text-center text-muted-foreground">{labels[index]}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>
                Page {currentPage + 1} of {totalPages}
              </span>
              <span>{Math.round(progress)}% Complete</span>
            </div>
            <Progress value={progress} className="h-3 bg-secondary/50" />
          </div>
        </div>

        {/* Questions */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {currentQuestions.map((question) => {
            const answer = getAnswer(question.index - 1);

            return (
              <div
                key={question.index}
                className="p-4 rounded-lg border border-border/50 bg-gradient-to-br from-card to-uh-green/5 hover:border-uh-green/30 transition-all duration-200"
              >
                <h2 className="text-base font-medium text-foreground mb-3">{question.text}</h2>

                <div className="flex justify-between gap-2">
                  {emojis.map((emoji, index) => {
                    const value = index + 1;
                    const isSelected = answer === value;
                    return (
                      <button
                        key={value}
                        onClick={() => handleEmojiClick(question.index - 1, value)}
                        className={`flex-1 p-2 rounded-lg border transition-all duration-200 ${
                          isSelected
                            ? `scale-110 ${getBackgroundForRating(value, true)}`
                            : "border-border hover:border-uh-green/50 hover:bg-accent/5"
                        }`}
                      >
                        <div className="text-2xl">{emoji}</div>
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <div className="flex gap-2">
            <Button variant="outline" onClick={handlePrevious} disabled={currentPage === 0}>
              Previous
            </Button>
            {onClear && (
              <Button variant="outline" onClick={onClear}>
                Clear All
              </Button>
            )}
          </div>
          <Button onClick={handleNext} className="bg-primary hover:bg-primary/90">
            {currentPage < totalPages - 1 ? "Next" : "Complete"}
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default RIASECQuiz;
