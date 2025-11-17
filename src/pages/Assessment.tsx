import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import RIASECQuiz from "@/components/quiz/RIASECQuiz";
import RIASECResults from "@/components/quiz/RIASECResults";
import SkillsAssessment, { getTaskStatements } from "@/components/quiz/SkillsAssessment";
import SkillsNarrative from "@/components/quiz/SkillsNarrative";
import OccupationResults from "@/components/quiz/OccupationResults";
import OccupationDetails from "@/components/quiz/OccupationDetails";
import InterestSummary from "@/components/quiz/InterestSummary";
import SkillsSummary from "@/components/quiz/SkillsSummary";
import StudentTypeSelection from "@/components/quiz/StudentTypeSelection";

export type AssessmentStage = 
  | "student-type"
  | "riasec" 
  | "riasec-summary"
  | "riasec-results" 
  | "skills" 
  | "skills-summary"
  | "skills-narrative"
  | "occupation-results" 
  | "occupation-detail";

export interface RIASECScores {
  Realistic: number;
  Investigative: number;
  Artistic: number;
  Social: number;
  Enterprising: number;
  Conventional: number;
}

export interface SkillRating {
  ElementId: string;
  ElementName: string;
  rating: number;
}

export interface OccupationMatch {
  onetCode: string;
  title: string;
  matchScore: number;
  medianSalary: number;
  growthOutlook: string;
  topSkills: string[];
  trainingDuration: string;
  description: string;
}

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

const Assessment = () => {
  const [stage, setStage] = useState<AssessmentStage>("student-type");
  const [studentType, setStudentType] = useState<"high-school" | "professional" | null>(null);
  const [riasecAnswers, setRiasecAnswers] = useState<Record<number, number>>({});
  const [riasecScores, setRiasecScores] = useState<RIASECScores | null>(null);
  const [skillSelections, setSkillSelections] = useState<Record<string, boolean>>({});
  const [skillRatings, setSkillRatings] = useState<SkillRating[]>([]);
  const [shownStatementIds, setShownStatementIds] = useState<string[]>([]);
  const [skillNarrative, setSkillNarrative] = useState<string>("");
  const [occupations, setOccupations] = useState<OccupationMatch[]>([]);
  const [selectedOccupation, setSelectedOccupation] = useState<OccupationMatch | null>(null);

  // Load from session storage on mount
  useEffect(() => {
    const savedRiasecAnswers = sessionStorage.getItem('riasec-answers');
    const savedSkillSelections = sessionStorage.getItem('skills-selections');
    
    if (savedRiasecAnswers) {
      setRiasecAnswers(JSON.parse(savedRiasecAnswers));
    }
    if (savedSkillSelections) {
      setSkillSelections(JSON.parse(savedSkillSelections));
    }
  }, []);

  const calculateScores = (answers: Record<number, number>): RIASECScores => {
    const scores: RIASECScores = {
      Realistic: 0,
      Investigative: 0,
      Artistic: 0,
      Social: 0,
      Enterprising: 0,
      Conventional: 0,
    };

    Object.entries(answers).forEach(([index, score]) => {
      const area = questions[parseInt(index)].area as keyof RIASECScores;
      scores[area] += score;
    });

    return scores;
  };

  const convertSelectionsToRatings = (selections: Record<string, boolean>): SkillRating[] => {
    const ratings: SkillRating[] = [];
    
    if (!studentType) return ratings;
    
    const taskStatements = getTaskStatements(studentType);
    taskStatements.forEach(task => {
      const isSelected = selections[task.ElementId];
      const rating = isSelected ? 5 : 1;
      ratings.push({
        ElementId: task.ElementId,
        ElementName: task.ElementName,
        rating,
      });
    });
    
    return ratings;
  };

  const handleStudentTypeSelect = (type: "high-school" | "professional") => {
    const isChanging = studentType !== null && studentType !== type;
    setStudentType(type);

    if (isChanging) {
      // Reset skills only; keep interests intact
      setSkillSelections({});
      setSkillRatings([]);
      setShownStatementIds([]);
      sessionStorage.removeItem("skills-selections");
    }

    setStage("riasec");
  };

  const handleRIASECComplete = (answers: Record<number, number>) => {
    setRiasecAnswers(answers);
    setStage("riasec-summary");
  };

  const handleInterestSummaryEdit = () => {
    setStage("riasec");
  };

  const handleInterestSummaryContinue = () => {
    const scores = calculateScores(riasecAnswers);
    setRiasecScores(scores);
    setStage("riasec-results");
  };

  const handleContinueToSkills = () => {
    // Load occupations from API data stored in sessionStorage
    const storedResult = sessionStorage.getItem("riasec-result");
    if (storedResult) {
      try {
        const riasecResult = JSON.parse(storedResult);
        // Transform API's OccupationLite to OccupationMatch format
        const transformedOccupations: OccupationMatch[] = riasecResult.top10_jobs.map((job: any, index: number) => ({
          onetCode: job.onet_code,
          title: job.title,
          matchScore: 95 - index * 2, // Descending scores from 95
          medianSalary: 0, // Placeholder - will need backend enhancement
          growthOutlook: "Data pending", // Placeholder
          topSkills: [], // Placeholder
          trainingDuration: "Varies by occupation", // Placeholder
          description: "Occupation details will be added soon." // Placeholder
        }));
        setOccupations(transformedOccupations);
      } catch (error) {
        console.error("Failed to parse RIASEC result from sessionStorage:", error);
      }
    }
    setStage("skills");
  };

  const handleSkillsComplete = (newSelections: Record<string, boolean>) => {
    const allSelections = { ...skillSelections, ...newSelections };
    setSkillSelections(allSelections);
    
    // Track all statements that have selections (either selected or explicitly not selected)
    const allStatements = getTaskStatements(studentType!);
    const statementsWithSelections = allStatements
      .filter(s => newSelections.hasOwnProperty(s.ElementId))
      .map(s => s.ElementId);
    
    // Merge with existing shown IDs
    const updatedShownIds = Array.from(new Set([...shownStatementIds, ...statementsWithSelections]));
    setShownStatementIds(updatedShownIds);
    
    setStage("skills-summary");
  };

  const handleSkillsSummaryEdit = () => {
    setStage("skills");
  };

  const handleSkillsSummaryAnswerMore = () => {
    setStage("skills");
  };

  const handleSkillsSummaryContinue = () => {
    const ratings = convertSelectionsToRatings(skillSelections);
    setSkillRatings(ratings);
    setStage("skills-narrative");
  };

  const handleNarrativeComplete = (narrative: string) => {
    setSkillNarrative(narrative);
    // Occupations already loaded from API in handleContinueToSkills
    setStage("occupation-results");
  };

  const handleOccupationSelect = (occupation: OccupationMatch) => {
    setSelectedOccupation(occupation);
    setStage("occupation-detail");
  };

  const handleBackToResults = () => {
    setStage("occupation-results");
  };

  const handleViewInterestSummary = () => {
    setStage("riasec-summary");
  };

  const handleViewSkillsSummary = () => {
    setStage("skills-summary");
  };

  const handleBackToSkillsFromResults = () => {
    setStage("skills-summary");
  };

  const handleBackToInterestsFromResults = () => {
    setStage("riasec-results");
  };

  const handleClearInterests = () => {
    setRiasecAnswers({});
    setRiasecScores(null);
    sessionStorage.removeItem('riasec-answers');
    setStage("riasec");
  };

  const handleClearSkills = () => {
    setSkillSelections({});
    setSkillRatings([]);
    setShownStatementIds([]);
    sessionStorage.removeItem('skills-selections');
    setStage("skills");
  };

  const generateMockOccupations = () => {
    const mockOccupations: OccupationMatch[] = [
      {
        onetCode: "15-1252.00",
        title: "Software Developers",
        matchScore: 92,
        medianSalary: 110140,
        growthOutlook: "Much faster than average",
        topSkills: ["Programming", "Problem Solving", "Critical Thinking"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Design, develop, and test computer applications or systems."
      },
      {
        onetCode: "29-1141.00",
        title: "Registered Nurses",
        matchScore: 88,
        medianSalary: 75330,
        growthOutlook: "Faster than average",
        topSkills: ["Active Listening", "Critical Thinking", "Service Orientation"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Assess patient health problems and needs, develop and implement nursing care plans."
      },
      {
        onetCode: "27-3031.00",
        title: "Public Relations Specialists",
        matchScore: 85,
        medianSalary: 62810,
        growthOutlook: "Average",
        topSkills: ["Writing", "Speaking", "Active Listening"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Promote or create an intended public image for individuals, groups, or organizations."
      },
      {
        onetCode: "19-3033.00",
        title: "Clinical Psychologists",
        matchScore: 84,
        medianSalary: 81040,
        growthOutlook: "Faster than average",
        topSkills: ["Active Listening", "Social Perceptiveness", "Critical Thinking"],
        trainingDuration: "Doctoral degree (8+ years)",
        description: "Diagnose or evaluate mental and emotional disorders and administer programs of treatment."
      },
      {
        onetCode: "13-1161.00",
        title: "Market Research Analysts",
        matchScore: 82,
        medianSalary: 63790,
        growthOutlook: "Much faster than average",
        topSkills: ["Critical Thinking", "Reading Comprehension", "Active Listening"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Research market conditions to examine potential sales of products or services."
      },
      {
        onetCode: "25-2021.00",
        title: "Elementary School Teachers",
        matchScore: 80,
        medianSalary: 60660,
        growthOutlook: "Average",
        topSkills: ["Instructing", "Learning Strategies", "Speaking"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Teach students in elementary school subjects like math, reading, and science."
      },
      {
        onetCode: "13-2011.00",
        title: "Accountants",
        matchScore: 78,
        medianSalary: 73560,
        growthOutlook: "Average",
        topSkills: ["Mathematics", "Critical Thinking", "Active Listening"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Prepare and examine financial records for accuracy and compliance."
      },
      {
        onetCode: "27-1024.00",
        title: "Graphic Designers",
        matchScore: 77,
        medianSalary: 53380,
        growthOutlook: "Average",
        topSkills: ["Originality", "Active Listening", "Critical Thinking"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Design visual concepts using computer software or by hand."
      },
      {
        onetCode: "11-2021.00",
        title: "Marketing Managers",
        matchScore: 76,
        medianSalary: 135900,
        growthOutlook: "Faster than average",
        topSkills: ["Management", "Speaking", "Active Listening"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Plan programs to generate interest in products or services."
      },
      {
        onetCode: "15-1244.00",
        title: "Network Administrators",
        matchScore: 75,
        medianSalary: 84810,
        growthOutlook: "Average",
        topSkills: ["Computers and Electronics", "Troubleshooting", "Critical Thinking"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Install, configure, and maintain computer networks and systems."
      },
      {
        onetCode: "21-1093.00",
        title: "Social Workers",
        matchScore: 74,
        medianSalary: 51760,
        growthOutlook: "Faster than average",
        topSkills: ["Active Listening", "Social Perceptiveness", "Service Orientation"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Help people solve and cope with problems in their everyday lives."
      },
      {
        onetCode: "19-2041.00",
        title: "Environmental Scientists",
        matchScore: 73,
        medianSalary: 73230,
        growthOutlook: "Average",
        topSkills: ["Science", "Critical Thinking", "Reading Comprehension"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Conduct research to identify and eliminate environmental hazards."
      },
      {
        onetCode: "41-3099.00",
        title: "Sales Representatives",
        matchScore: 72,
        medianSalary: 62890,
        growthOutlook: "Average",
        topSkills: ["Persuasion", "Active Listening", "Speaking"],
        trainingDuration: "High school diploma + training",
        description: "Sell goods and services to businesses and individuals."
      },
      {
        onetCode: "17-2051.00",
        title: "Civil Engineers",
        matchScore: 71,
        medianSalary: 88570,
        growthOutlook: "Average",
        topSkills: ["Mathematics", "Critical Thinking", "Complex Problem Solving"],
        trainingDuration: "Bachelor's degree (4 years)",
        description: "Design and oversee construction of infrastructure projects."
      },
      {
        onetCode: "29-1171.00",
        title: "Nurse Practitioners",
        matchScore: 70,
        medianSalary: 111680,
        growthOutlook: "Much faster than average",
        topSkills: ["Medicine and Dentistry", "Active Listening", "Critical Thinking"],
        trainingDuration: "Master's degree (6+ years)",
        description: "Diagnose and treat acute and chronic illnesses in patients."
      }
    ];
    setOccupations(mockOccupations);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        {stage === "student-type" && (
          <StudentTypeSelection onSelect={handleStudentTypeSelect} />
        )}

        {stage === "riasec" && (
          <RIASECQuiz 
            onComplete={handleRIASECComplete}
            initialAnswers={riasecAnswers}
            onClear={handleClearInterests}
          />
        )}
        
        {stage === "riasec-summary" && (
          <InterestSummary
            answers={riasecAnswers}
            questions={questions}
            onEdit={handleInterestSummaryEdit}
            onContinue={handleInterestSummaryContinue}
            onClear={handleClearInterests}
          />
        )}
        
        {stage === "riasec-results" && riasecScores && (
          <RIASECResults 
            riasecScores={riasecScores} 
            onContinue={handleContinueToSkills}
            onBack={handleViewInterestSummary}
            onClear={handleClearInterests}
          />
        )}
        
        {stage === "skills" && riasecScores && studentType && (
          <SkillsAssessment 
            riasecScores={riasecScores}
            studentType={studentType}
            onComplete={handleSkillsComplete}
            initialSelections={skillSelections}
            shownStatementIds={shownStatementIds}
            onClear={handleClearSkills}
          />
        )}
        
        {stage === "skills-summary" && studentType && (
          <SkillsSummary
            selections={skillSelections}
            taskStatements={getTaskStatements(studentType)}
            onEdit={handleSkillsSummaryEdit}
            onContinue={handleSkillsSummaryContinue}
            onAnswerMore={handleSkillsSummaryAnswerMore}
            onClear={handleClearSkills}
          />
        )}
        
        {stage === "skills-narrative" && (
          <SkillsNarrative
            topSkills={skillRatings.slice(0, 3)}
            onComplete={handleNarrativeComplete}
          />
        )}
        
        {stage === "occupation-results" && (
          <OccupationResults 
            occupations={occupations}
            riasecScores={riasecScores!}
            onOccupationSelect={handleOccupationSelect}
            onBackToSkills={handleBackToSkillsFromResults}
            onBackToInterests={handleBackToInterestsFromResults}
          />
        )}
        
        {stage === "occupation-detail" && selectedOccupation && (
          <OccupationDetails 
            occupation={selectedOccupation}
            onBack={handleBackToResults}
          />
        )}
      </div>
    </div>
  );
};

export default Assessment;
