// src/services/occupationService.ts
import apiClient from '@/lib/apiClient';

// --- Types for Occupation and Program data ---

export interface Occupation {
  onet_code: string;
  title: string;
  description: string;
  median_annual_wage: number | null;
  employment_outlook: string;
  job_zone: number;
  interest_codes: string[];
  interest_scores: Record<string, number>;
  onet_url: string;
}

export interface Program {
  id: string;
  name: string;
  description: string;
  pathway_id: string;
  institution_id: string;
  degree_type: string;
  duration_years: number;
  total_credits: number;
  cost_per_credit: number;
  program_url: string;
  program_links: string[];
  prerequisites: string[];
  delivery_modes: string[];
}

export interface OccupationWithPrograms {
  occupation: Occupation;
  programs: Program[];
  program_count: number;
}

// --- API Functions ---

/**
 * Get detailed information about a specific occupation by O*NET code.
 * 
 * @param onetCode - The O*NET SOC code (e.g., '51-4041.00')
 * @returns Occupation details
 */
export const getOccupation = async (onetCode: string): Promise<Occupation> => {
  const response = await apiClient.get<Occupation>(`/occupations/${onetCode}`);
  return response.data;
};

/**
 * Get an occupation along with all its associated programs.
 * 
 * Programs are matched through semantic similarity analysis that maps
 * occupations to relevant University of Hawaii programs via career pathways.
 * 
 * @param onetCode - The O*NET SOC code (e.g., '51-4041.00')
 * @returns Occupation details with associated programs
 */
export const getOccupationWithPrograms = async (
  onetCode: string
): Promise<OccupationWithPrograms> => {
  const response = await apiClient.get<OccupationWithPrograms>(
    `/occupations/${onetCode}/programs`
  );
  return response.data;
};

/**
 * Get just the programs associated with an occupation (lightweight).
 * 
 * @param onetCode - The O*NET SOC code
 * @returns Array of programs
 */
export const getOccupationPrograms = async (onetCode: string): Promise<Program[]> => {
  const response = await apiClient.get<Program[]>(
    `/occupations/${onetCode}/programs/summary`
  );
  return response.data;
};

/**
 * Get programs for multiple occupations in batch.
 * Useful for loading programs for all occupation recommendations at once.
 * 
 * @param onetCodes - Array of O*NET SOC codes
 * @returns Map of onet_code to programs
 */
export const getMultipleOccupationPrograms = async (
  onetCodes: string[]
): Promise<Record<string, Program[]>> => {
  // Fetch all programs in parallel
  const results = await Promise.allSettled(
    onetCodes.map(code => getOccupationPrograms(code))
  );
  
  // Build result map
  const programsMap: Record<string, Program[]> = {};
  results.forEach((result, index) => {
    const code = onetCodes[index];
    if (result.status === 'fulfilled') {
      programsMap[code] = result.value;
    } else {
      // If fetch failed, return empty array for this occupation
      console.warn(`Failed to fetch programs for ${code}:`, result.reason);
      programsMap[code] = [];
    }
  });
  
  return programsMap;
};

/**
 * Calculate total estimated cost for a program.
 * 
 * @param program - Program object
 * @returns Estimated total cost
 */
export const calculateProgramCost = (program: Program): number => {
  return program.total_credits * program.cost_per_credit;
};

/**
 * Format program duration in human-readable form.
 * 
 * @param durationYears - Duration in years
 * @returns Formatted string (e.g., "2 years", "1.5 years")
 */
export const formatProgramDuration = (durationYears: number): string => {
  if (durationYears === 1) return '1 year';
  return `${durationYears} years`;
};
