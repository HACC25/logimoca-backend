import React, { useState, useEffect } from 'react';
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Skeleton } from "@/components/ui/skeleton";
import { ProgramCard } from "@/components/ProgramCard";
import { getOccupationPrograms } from "@/services/occupationService";
import { GraduationCap, ArrowRight, Briefcase, AlertCircle } from "lucide-react";
import type { Program } from "@/services/occupationService";

interface OccupationPathwayMapProps {
  onetCode: string;
  occupationTitle?: string;
}

interface GroupedPrograms {
  certificates: Program[];
  associates: Program[];
  bachelors: Program[];
}

const OccupationPathwayMap: React.FC<OccupationPathwayMapProps> = ({
  onetCode,
  occupationTitle
}) => {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPrograms = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getOccupationPrograms(onetCode);
        setPrograms(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load programs');
      } finally {
        setLoading(false);
      }
    };

    if (onetCode) {
      fetchPrograms();
    }
  }, [onetCode]);

  // Group programs by degree type
  const groupPrograms = (programs: Program[]): GroupedPrograms => {
    return programs.reduce(
      (acc, program) => {
        const degreeType = program.degree_type?.toLowerCase() || '';
        
        if (degreeType.includes('certificate') || degreeType.includes('competence')) {
          acc.certificates.push(program);
        } else if (degreeType.includes('associate')) {
          acc.associates.push(program);
        } else if (degreeType.includes('bachelor')) {
          acc.bachelors.push(program);
        } else {
          // Default to associates if unknown
          acc.associates.push(program);
        }
        
        return acc;
      },
      { certificates: [], associates: [], bachelors: [] } as GroupedPrograms
    );
  };

  if (loading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          Failed to load education pathways. Please try again later.
        </AlertDescription>
      </Alert>
    );
  }

  if (programs.length === 0) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No education programs found for {occupationTitle || 'this occupation'}. Check back soon as we add more programs!
        </AlertDescription>
      </Alert>
    );
  }

  const grouped = groupPrograms(programs);
  const hasAnyPrograms = grouped.certificates.length > 0 || grouped.associates.length > 0 || grouped.bachelors.length > 0;

  if (!hasAnyPrograms) {
    return (
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>
          No programs available at this time.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-8">
      {/* Legend */}
      <Card className="p-4 bg-gradient-to-r from-secondary/20 to-muted/20">
        <div className="flex flex-wrap items-center gap-4 md:gap-6 justify-center">
          <p className="font-semibold text-sm">Your Pathway to {occupationTitle}:</p>
          {grouped.certificates.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gradient-to-br from-amber-500 to-amber-600"></div>
              <span className="text-xs md:text-sm">Certificates ({grouped.certificates.length})</span>
            </div>
          )}
          {grouped.associates.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gradient-to-br from-emerald-500 to-emerald-600"></div>
              <span className="text-xs md:text-sm">Associate Degrees ({grouped.associates.length})</span>
            </div>
          )}
          {grouped.bachelors.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gradient-to-br from-blue-500 to-blue-600"></div>
              <span className="text-xs md:text-sm">Bachelor's Degrees ({grouped.bachelors.length})</span>
            </div>
          )}
        </div>
      </Card>

      {/* Desktop: Horizontal pathway flow */}
      <div className="hidden md:block">
        <div className="flex items-start gap-4 lg:gap-6">
          {/* Certificates Track */}
          {grouped.certificates.length > 0 && (
            <>
              <div className="flex-1 min-w-0">
                <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/10 rounded-lg p-4 border-2 border-amber-500/30 h-full">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="bg-amber-500/20 p-2 rounded-lg">
                      <GraduationCap className="w-5 h-5 text-amber-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-foreground">Training & Certificates</h3>
                      <p className="text-xs text-muted-foreground">6 months - 1 year</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {grouped.certificates.map((program) => (
                      <ProgramCard key={program.id} program={program} compact={true} />
                    ))}
                  </div>
                </div>
              </div>
              {(grouped.associates.length > 0 || grouped.bachelors.length > 0) && (
                <div className="flex items-center justify-center py-8">
                  <ArrowRight className="w-6 h-6 text-muted-foreground" />
                </div>
              )}
            </>
          )}

          {/* Associates Track */}
          {grouped.associates.length > 0 && (
            <>
              <div className="flex-1 min-w-0">
                <div className="bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 rounded-lg p-4 border-2 border-emerald-500/30 h-full">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="bg-emerald-500/20 p-2 rounded-lg">
                      <GraduationCap className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-foreground">Community College</h3>
                      <p className="text-xs text-muted-foreground">2-year programs</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {grouped.associates.slice(0, 3).map((program) => (
                      <ProgramCard key={program.id} program={program} compact={true} />
                    ))}
                    {grouped.associates.length > 3 && (
                      <p className="text-xs text-center text-muted-foreground pt-2">
                        +{grouped.associates.length - 3} more programs
                      </p>
                    )}
                  </div>
                </div>
              </div>
              {grouped.bachelors.length > 0 && (
                <div className="flex items-center justify-center py-8">
                  <ArrowRight className="w-6 h-6 text-muted-foreground" />
                </div>
              )}
            </>
          )}

          {/* Bachelor's Track */}
          {grouped.bachelors.length > 0 && (
            <>
              <div className="flex-1 min-w-0">
                <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-lg p-4 border-2 border-blue-500/30 h-full">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="bg-blue-500/20 p-2 rounded-lg">
                      <GraduationCap className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-bold text-base text-foreground">University</h3>
                      <p className="text-xs text-muted-foreground">4-year programs</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {grouped.bachelors.slice(0, 3).map((program) => (
                      <ProgramCard key={program.id} program={program} compact={true} />
                    ))}
                    {grouped.bachelors.length > 3 && (
                      <p className="text-xs text-center text-muted-foreground pt-2">
                        +{grouped.bachelors.length - 3} more programs
                      </p>
                    )}
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-center py-8">
                <ArrowRight className="w-6 h-6 text-muted-foreground" />
              </div>
            </>
          )}

          {/* Career destination */}
          <div className="flex-shrink-0" style={{ width: '180px' }}>
            <div className="bg-gradient-to-br from-primary/20 to-primary/10 rounded-lg p-4 border-2 border-primary/30 h-full flex flex-col items-center justify-center text-center">
              <div className="bg-primary/20 p-3 rounded-full mb-3">
                <Briefcase className="w-8 h-8 text-primary" />
              </div>
              <h3 className="font-bold text-base mb-2">Career</h3>
              <p className="text-xs text-muted-foreground mb-2">{occupationTitle}</p>
              <Badge className="bg-emerald-500/20 text-emerald-700 border-emerald-500/40 text-xs">
                Your Goal
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile: Vertical pathway flow */}
      <div className="md:hidden space-y-4">
        {grouped.certificates.length > 0 && (
          <>
            <div className="bg-gradient-to-br from-amber-500/20 to-amber-600/10 rounded-lg p-4 border-2 border-amber-500/30">
              <div className="flex items-center gap-2 mb-3">
                <div className="bg-amber-500/20 p-2 rounded-lg">
                  <GraduationCap className="w-4 h-4 text-amber-600" />
                </div>
                <div>
                  <h3 className="font-bold text-sm">Training & Certificates</h3>
                  <p className="text-xs text-muted-foreground">6 months - 1 year</p>
                </div>
              </div>
              <div className="space-y-2">
                {grouped.certificates.map((program) => (
                  <ProgramCard key={program.id} program={program} compact={true} />
                ))}
              </div>
            </div>
            <div className="flex justify-center">
              <ArrowRight className="w-5 h-5 text-muted-foreground rotate-90" />
            </div>
          </>
        )}

        {grouped.associates.length > 0 && (
          <>
            <div className="bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 rounded-lg p-4 border-2 border-emerald-500/30">
              <div className="flex items-center gap-2 mb-3">
                <div className="bg-emerald-500/20 p-2 rounded-lg">
                  <GraduationCap className="w-4 h-4 text-emerald-600" />
                </div>
                <div>
                  <h3 className="font-bold text-sm">Community College</h3>
                  <p className="text-xs text-muted-foreground">2-year programs</p>
                </div>
              </div>
              <div className="space-y-2">
                {grouped.associates.map((program) => (
                  <ProgramCard key={program.id} program={program} compact={true} />
                ))}
              </div>
            </div>
            {grouped.bachelors.length > 0 && (
              <div className="flex justify-center">
                <ArrowRight className="w-5 h-5 text-muted-foreground rotate-90" />
              </div>
            )}
          </>
        )}

        {grouped.bachelors.length > 0 && (
          <>
            <div className="bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-lg p-4 border-2 border-blue-500/30">
              <div className="flex items-center gap-2 mb-3">
                <div className="bg-blue-500/20 p-2 rounded-lg">
                  <GraduationCap className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-bold text-sm">University</h3>
                  <p className="text-xs text-muted-foreground">4-year programs</p>
                </div>
              </div>
              <div className="space-y-2">
                {grouped.bachelors.map((program) => (
                  <ProgramCard key={program.id} program={program} compact={true} />
                ))}
              </div>
            </div>
            <div className="flex justify-center">
              <ArrowRight className="w-5 h-5 text-muted-foreground rotate-90" />
            </div>
          </>
        )}

        {/* Career destination mobile */}
        <div className="bg-gradient-to-br from-primary/20 to-primary/10 rounded-lg p-6 border-2 border-primary/30 flex flex-col items-center text-center">
          <div className="bg-primary/20 p-3 rounded-full mb-3">
            <Briefcase className="w-8 h-8 text-primary" />
          </div>
          <h3 className="font-bold text-lg mb-2">Career Goal</h3>
          <p className="text-sm text-muted-foreground mb-3">{occupationTitle}</p>
          <Badge className="bg-emerald-500/20 text-emerald-700 border-emerald-500/40">
            Your Destination
          </Badge>
        </div>
      </div>
    </div>
  );
};

export default OccupationPathwayMap;
