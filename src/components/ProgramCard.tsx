// src/components/ProgramCard.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ExternalLink, Clock, DollarSign, GraduationCap } from 'lucide-react';
import { Program, calculateProgramCost, formatProgramDuration } from '@/services/occupationService';

interface ProgramCardProps {
  program: Program;
  compact?: boolean;
}

export const ProgramCard = ({ program, compact = false }: ProgramCardProps) => {
  const totalCost = calculateProgramCost(program);
  const duration = formatProgramDuration(program.duration_years);

  if (compact) {
    return (
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="text-base line-clamp-2">{program.name}</CardTitle>
            <Badge variant="secondary" className="shrink-0">
              {program.degree_type}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Clock className="h-4 w-4" />
              <span>{duration}</span>
            </div>
            <div className="flex items-center gap-1">
              <DollarSign className="h-4 w-4" />
              <span>${totalCost.toLocaleString()}</span>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            className="w-full"
            asChild
          >
            <a href={program.program_url} target="_blank" rel="noopener noreferrer">
              View Program <ExternalLink className="ml-2 h-3 w-3" />
            </a>
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2 flex-1">
            <CardTitle className="text-xl">{program.name}</CardTitle>
            <CardDescription className="line-clamp-3">
              {program.description}
            </CardDescription>
          </div>
          <Badge variant="secondary" className="shrink-0">
            {program.degree_type}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Program Details */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2">
            <Clock className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">Duration</p>
              <p className="text-sm text-muted-foreground">{duration}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">Est. Total Cost</p>
              <p className="text-sm text-muted-foreground">
                ${totalCost.toLocaleString()}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <GraduationCap className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">Credits</p>
              <p className="text-sm text-muted-foreground">
                {program.total_credits} credits
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <DollarSign className="h-5 w-5 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">Per Credit</p>
              <p className="text-sm text-muted-foreground">
                ${program.cost_per_credit}
              </p>
            </div>
          </div>
        </div>

        {/* Prerequisites */}
        {program.prerequisites && program.prerequisites.length > 0 && (
          <div>
            <p className="text-sm font-medium mb-2">Prerequisites:</p>
            <ul className="text-sm text-muted-foreground list-disc list-inside">
              {program.prerequisites.map((prereq, idx) => (
                <li key={idx}>{prereq}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Delivery Modes */}
        {program.delivery_modes && program.delivery_modes.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {program.delivery_modes.map((mode, idx) => (
              <Badge key={idx} variant="outline">
                {mode}
              </Badge>
            ))}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-2 pt-2">
          <Button asChild className="flex-1">
            <a href={program.program_url} target="_blank" rel="noopener noreferrer">
              View Program <ExternalLink className="ml-2 h-4 w-4" />
            </a>
          </Button>
          {program.program_links && program.program_links.length > 0 && (
            <Button variant="outline" asChild>
              <a href={program.program_links[0]} target="_blank" rel="noopener noreferrer">
                More Info <ExternalLink className="ml-2 h-4 w-4" />
              </a>
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
