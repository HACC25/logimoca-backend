// src/services/assessmentService.ts
import apiClient from '@/lib/apiClient';

// --- Types aligned to FastAPI Pydantic models ---

export interface OccupationLite {
  onet_code: string;
  title: string;
}

export interface SkillDefinition {
  element_id: string;
  name: string;
  question: string;
  easy_read_description: string;
  anchor_first: string;
  anchor_third: string;
  anchor_last: string;
  data_point_20: number;
  data_point_35: number;
  data_point_50: number;
  data_point_65: number;
  data_point_80: number;
}

export interface RiasecResult {
  riasec_code: string;
  occupation_pool: string[];
  top10_jobs: OccupationLite[];
  skills_panel: SkillDefinition[];
}

export interface SkillRatingsSubmission {
  riasec_code: string;
  ratings: Record<string, number>; // element_id -> user rating
}

export interface SkillWeighted {
  element_id: string;
  raw_rating: number;
  normalized_score: number;
  adjusted_weight: number;
}

export interface SkillWeightsResponse {
  riasec_code: string;
  weighted_skills: SkillWeighted[];
  category_weights: Record<string, number>;
}

// --- Helper: compute 3-letter RIASEC from answers ---

const AREA_TO_CODE: Record<string, string> = {
  Realistic: 'R',
  Investigative: 'I',
  Artistic: 'A',
  Social: 'S',
  Enterprising: 'E',
  Conventional: 'C',
};

export interface RiasecAnswerMap {
  [questionIndex: number]: number; // 0-based index -> rating 1..5
}

export interface RiasecQuestion {
  index: number; // 1..30
  area: keyof typeof AREA_TO_CODE;
  text: string;
}

export function computeRiasecCode(
  answers: RiasecAnswerMap,
  questions: RiasecQuestion[],
): string {
  const areaScores: Record<string, number> = {
    Realistic: 0,
    Investigative: 0,
    Artistic: 0,
    Social: 0,
    Enterprising: 0,
    Conventional: 0,
  };
  for (const q of questions) {
    const idx = q.index - 1; // stored 0-based in state
    const val = answers[idx] ?? 3; // default mid if unanswered
    areaScores[q.area] += val;
  }
  const sorted = Object.entries(areaScores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([area]) => AREA_TO_CODE[area]);
  return sorted.join('');
}

// --- API functions ---

export const submitRiasecCode = async (riasecCode: string, limit: number = 10): Promise<RiasecResult> => {
  const response = await apiClient.post<RiasecResult>('/assessment/riasec', { riasec_code: riasecCode, limit });
  return response.data;
};

export const submitSkillWeights = async (
  submission: SkillRatingsSubmission,
): Promise<SkillWeightsResponse> => {
  const response = await apiClient.post<SkillWeightsResponse>('/assessment/skills/weights', submission);
  return response.data;
};

export const getOccupationDetails = async (onetCode: string) => {
  const response = await apiClient.get(`/occupations/${onetCode}`);
  return response.data;
};