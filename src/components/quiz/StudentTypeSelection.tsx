import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { GraduationCap, Briefcase } from "lucide-react";

interface StudentTypeSelectionProps {
  onSelect: (type: "high-school" | "professional") => void;
}

const StudentTypeSelection = ({ onSelect }: StudentTypeSelectionProps) => {
  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <Card className="p-8 shadow-lg bg-gradient-to-br from-background to-uh-green/5">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-uh-green to-primary bg-clip-text text-transparent mb-2">
            Welcome to Your Career Assessment
          </h1>
          <p className="text-muted-foreground">
            Let's start by understanding your background
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <button
            onClick={() => onSelect("high-school")}
            className="group relative overflow-hidden rounded-lg border-2 border-border hover:border-uh-green transition-all duration-300 p-8 text-left bg-card hover:shadow-lg"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="p-4 rounded-full bg-uh-green/10 group-hover:bg-uh-green/20 transition-colors">
                <GraduationCap className="h-12 w-12 text-uh-green" />
              </div>
              <div>
                <h2 className="text-xl font-bold mb-2">High School Student</h2>
                <p className="text-muted-foreground text-sm">
                  I'm currently in high school or recently graduated with limited work experience
                </p>
              </div>
            </div>
          </button>

          <button
            onClick={() => onSelect("professional")}
            className="group relative overflow-hidden rounded-lg border-2 border-border hover:border-primary transition-all duration-300 p-8 text-left bg-card hover:shadow-lg"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className="p-4 rounded-full bg-primary/10 group-hover:bg-primary/20 transition-colors">
                <Briefcase className="h-12 w-12 text-primary" />
              </div>
              <div>
                <h2 className="text-xl font-bold mb-2">Returning Professional</h2>
                <p className="text-muted-foreground text-sm">
                  I have prior work experience and am exploring new career opportunities
                </p>
              </div>
            </div>
          </button>
        </div>
      </Card>
    </div>
  );
};

export default StudentTypeSelection;
