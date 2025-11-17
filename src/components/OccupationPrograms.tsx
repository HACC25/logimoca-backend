// src/components/OccupationPrograms.tsx
import { useEffect, useState } from 'react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { ProgramCard } from '@/components/ProgramCard';
import { Program, getOccupationPrograms } from '@/services/occupationService';
import { BookOpen, AlertCircle } from 'lucide-react';

interface OccupationProgramsProps {
  onetCode: string;
  occupationTitle?: string;
  compact?: boolean;
  maxPrograms?: number;
}

export const OccupationPrograms = ({
  onetCode,
  occupationTitle,
  compact = false,
  maxPrograms
}: OccupationProgramsProps) => {
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
        console.error('Failed to fetch programs:', err);
        setError('Unable to load related programs. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchPrograms();
  }, [onetCode]);

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-4">
          <BookOpen className="h-5 w-5" />
          <h3 className="text-lg font-semibold">Related Programs</h3>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (programs.length === 0) {
    return (
      <Alert>
        <BookOpen className="h-4 w-4" />
        <AlertDescription>
          No related programs found for {occupationTitle || 'this occupation'} at this time.
          Check back later as we continue to expand our program database.
        </AlertDescription>
      </Alert>
    );
  }

  const displayPrograms = maxPrograms ? programs.slice(0, maxPrograms) : programs;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BookOpen className="h-5 w-5" />
          <h3 className="text-lg font-semibold">
            Related Programs
            {occupationTitle && (
              <span className="text-muted-foreground font-normal ml-2">
                for {occupationTitle}
              </span>
            )}
          </h3>
        </div>
        <span className="text-sm text-muted-foreground">
          {programs.length} {programs.length === 1 ? 'program' : 'programs'} found
        </span>
      </div>

      <div className={`grid gap-4 ${compact ? 'md:grid-cols-2 lg:grid-cols-3' : 'lg:grid-cols-2'}`}>
        {displayPrograms.map((program) => (
          <ProgramCard key={program.id} program={program} compact={compact} />
        ))}
      </div>

      {maxPrograms && programs.length > maxPrograms && (
        <p className="text-sm text-muted-foreground text-center">
          Showing {maxPrograms} of {programs.length} programs
        </p>
      )}
    </div>
  );
};
