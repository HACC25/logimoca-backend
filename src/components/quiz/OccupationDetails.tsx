import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { OccupationMatch } from "@/pages/Assessment";
import OccupationPathwayMap from "@/components/OccupationPathwayMap";
import { 
  ArrowLeft, 
  DollarSign, 
  TrendingUp, 
  GraduationCap, 
  MapPin, 
  ExternalLink,
  School,
  Clock,
  BookOpen,
  ArrowRight,
  Briefcase
} from "lucide-react";

interface OccupationDetailsProps {
  occupation: OccupationMatch;
  onBack: () => void;
}

// Mock Hawaii was used for testing
const mockHawaiiPrograms = {
  training: [
    {
      id: "1",
      name: "Web Development Bootcamp",
      institution: "Honolulu CC",
      campus: "Honolulu, Oʻahu",
      type: "Certificate",
      duration: "6 months",
      credits: "15 credits",
      costPerCredit: "$135",
      estimatedTotalCost: "$2,025",
      deliveryMode: ["Online", "Evening"],
      description: "Intensive bootcamp covering HTML, CSS, JavaScript, and React framework.",
      programUrl: "https://www.honolulu.hawaii.edu/",
      icon: "🚀"
    },
    {
      id: "2",
      name: "IT Support Certificate",
      institution: "Kauaʻi CC",
      campus: "Līhuʻe, Kauaʻi",
      type: "Certificate",
      duration: "1 year",
      credits: "24 credits",
      costPerCredit: "$135",
      estimatedTotalCost: "$3,240",
      deliveryMode: ["Hybrid"],
      description: "Fast-track program for technical support and troubleshooting skills.",
      programUrl: "https://www.kauai.hawaii.edu/",
      icon: "⚡"
    }
  ],
  communityCollege: [
    {
      id: "3",
      name: "AS - Information Technology",
      institution: "Leeward CC",
      campus: "Pearl City, Oʻahu",
      type: "Associate Degree",
      duration: "2 years",
      credits: "60 credits",
      costPerCredit: "$135",
      estimatedTotalCost: "$8,100",
      deliveryMode: ["In-person", "Online"],
      description: "Foundational IT program with networking, databases, and web development.",
      programUrl: "https://www.leeward.hawaii.edu/",
      icon: "💻"
    },
    {
      id: "4",
      name: "AAS - Computer Science",
      institution: "Windward CC",
      campus: "Kāneʻohe, Oʻahu",
      type: "Associate Degree",
      duration: "2 years",
      credits: "62 credits",
      costPerCredit: "$135",
      estimatedTotalCost: "$8,370",
      deliveryMode: ["In-person"],
      description: "Applied science degree with programming and systems focus.",
      programUrl: "https://www.windward.hawaii.edu/",
      icon: "🖥️"
    },
    {
      id: "5",
      name: "AS - Engineering Technology",
      institution: "Honolulu CC",
      campus: "Honolulu, Oʻahu",
      type: "Associate Degree",
      duration: "2 years",
      credits: "64 credits",
      costPerCredit: "$135",
      estimatedTotalCost: "$8,640",
      deliveryMode: ["In-person", "Hybrid"],
      description: "Technical foundation with pathways to engineering programs.",
      programUrl: "https://www.honolulu.hawaii.edu/",
      icon: "⚙️"
    }
  ],
  university: [
    {
      id: "6",
      name: "BS - Computer Science",
      institution: "UH Mānoa",
      campus: "Mānoa, Oʻahu",
      type: "Bachelor's Degree",
      duration: "4 years",
      credits: "124 credits",
      costPerCredit: "$348",
      estimatedTotalCost: "$43,152",
      deliveryMode: ["In-person", "Hybrid"],
      description: "Comprehensive CS program covering software, algorithms, and systems.",
      programUrl: "https://www.hawaii.edu/ics/",
      icon: "🎓"
    },
    {
      id: "7",
      name: "BS - Information & Computer Science",
      institution: "UH Hilo",
      campus: "Hilo, Hawaiʻi Island",
      type: "Bachelor's Degree",
      duration: "4 years",
      credits: "120 credits",
      costPerCredit: "$348",
      estimatedTotalCost: "$41,760",
      deliveryMode: ["In-person"],
      description: "Bachelor's program with focus on practical application and systems.",
      programUrl: "https://hilo.hawaii.edu/",
      icon: "🎯"
    },
    {
      id: "8",
      name: "BS - Computer Engineering",
      institution: "UH Mānoa",
      campus: "Mānoa, Oʻahu",
      type: "Bachelor's Degree",
      duration: "4 years",
      credits: "128 credits",
      costPerCredit: "$348",
      estimatedTotalCost: "$44,544",
      deliveryMode: ["In-person"],
      description: "Engineering program combining hardware and software expertise.",
      programUrl: "https://www.hawaii.edu/coe/",
      icon: "🔧"
    }
  ]
};

const OccupationDetails = ({ occupation, onBack }: OccupationDetailsProps) => {
  const formatSalary = (salary: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0
    }).format(salary);
  };

  const ProgramCard = ({ program, color }: { program: any; color: string }) => (
    <HoverCard>
      <HoverCardTrigger asChild>
        <div 
          className={`
            p-4 rounded-lg cursor-pointer transition-all duration-300
            hover:scale-105 hover:shadow-xl border-2
            ${color}
          `}
        >
          <div className="text-2xl mb-2">{program.icon}</div>
          <h4 className="font-bold text-sm mb-1 text-card-foreground">{program.name}</h4>
          <p className="text-xs text-muted-foreground italic">{program.institution}</p>
        </div>
      </HoverCardTrigger>
      <HoverCardContent className="w-96 p-6" side="top">
        <div className="space-y-4">
          <div>
            <h4 className="font-bold text-lg mb-2 flex items-center gap-2">
              {program.icon} {program.name}
            </h4>
            <p className="text-sm text-muted-foreground">{program.description}</p>
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            <div className="flex items-start gap-2">
              <Clock className="w-4 h-4 text-accent mt-0.5" />
              <div>
                <p className="text-xs text-muted-foreground">Duration</p>
                <p className="text-sm font-semibold">{program.duration}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-2">
              <BookOpen className="w-4 h-4 text-accent mt-0.5" />
              <div>
                <p className="text-xs text-muted-foreground">Credits</p>
                <p className="text-sm font-semibold">{program.credits}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-2">
              <DollarSign className="w-4 h-4 text-accent mt-0.5" />
              <div>
                <p className="text-xs text-muted-foreground">Total Cost</p>
                <p className="text-sm font-semibold">{program.estimatedTotalCost}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-2">
              <MapPin className="w-4 h-4 text-accent mt-0.5" />
              <div>
                <p className="text-xs text-muted-foreground">Campus</p>
                <p className="text-sm font-semibold">{program.campus}</p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {program.deliveryMode.map((mode: string) => (
              <Badge key={mode} variant="outline" className="text-xs">
                {mode}
              </Badge>
            ))}
          </div>

          <Button 
            className="w-full"
            onClick={() => window.open(program.programUrl, '_blank')}
          >
            View Program Details
            <ExternalLink className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </HoverCardContent>
    </HoverCard>
  );

  return (
    <div className="w-full animate-fade-in pb-12">
      <div className="max-w-7xl mx-auto px-4">
        <Button 
          variant="ghost" 
          onClick={onBack}
          className="mb-6 hover:bg-secondary"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Results
        </Button>

        {/* Occupation Header */}
        <Card className="p-6 md:p-8 mb-8 bg-gradient-to-r from-primary/5 via-accent/5 to-secondary/5 border border-border/50">
          <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-3">{occupation.title}</h1>
          <p className="text-base text-muted-foreground mb-6">{occupation.description}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-uh-green/20 rounded-lg">
                <DollarSign className="w-6 h-6 text-uh-green" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Median Salary</p>
                <p className="text-xl font-bold text-foreground">{formatSalary(occupation.medianSalary)}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="p-2 bg-accent/20 rounded-lg">
                <TrendingUp className="w-6 h-6 text-accent" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Job Outlook</p>
                <p className="text-lg font-semibold text-foreground">{occupation.growthOutlook}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="p-2 bg-primary/20 rounded-lg">
                <GraduationCap className="w-6 h-6 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Education</p>
                <p className="text-lg font-semibold text-foreground">{occupation.trainingDuration}</p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="p-2 bg-uh-gold/20 rounded-lg">
                <MapPin className="w-6 h-6 text-uh-gold" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Location</p>
                <p className="text-lg font-semibold text-foreground">Hawaiʻi</p>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <p className="text-sm font-medium text-foreground mb-3">Key Skills Required:</p>
            <div className="flex flex-wrap gap-2">
              {occupation.topSkills.map((skill) => (
                <Badge key={skill} className="bg-primary/10 text-primary border-primary/20">
                  {skill}
                </Badge>
              ))}
            </div>
          </div>
        </Card>

        {/* Education Pathway Map Section */}
        <div className="mb-8">
          <div className="mb-6 text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <School className="w-6 h-6 text-primary" />
              <h2 className="text-xl md:text-2xl font-bold text-foreground">Your Education Pathway</h2>
            </div>
            <p className="text-sm text-muted-foreground max-w-2xl mx-auto">
              See how different education paths can lead you to a career as {occupation.title}.
            </p>
          </div>

          <OccupationPathwayMap 
            onetCode={occupation.onetCode}
            occupationTitle={occupation.title}
          />
        </div>

        {/* Pathway Map Section - Legacy mock data preserved for reference */}
        <div className="mb-8 hidden">
          {/* This section with mockHawaiiPrograms is preserved but hidden */}
          {/* Legend */}
          <Card className="p-4 mb-6 bg-gradient-to-r from-secondary/20 to-muted/20">
            <div className="flex flex-wrap items-center gap-4 md:gap-6">
              <p className="font-semibold text-sm">Program Types:</p>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gradient-to-br from-destructive to-destructive/60"></div>
                <span className="text-xs md:text-sm">Training (&lt;1 Year)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gradient-to-br from-uh-green to-uh-green/60"></div>
                <span className="text-xs md:text-sm">Community College (2 Years)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gradient-to-br from-accent to-accent/60"></div>
                <span className="text-xs md:text-sm">University (4 Years)</span>
              </div>
            </div>
          </Card>

          {/* Pathway Flow - Tree Structure */}
          <div className="relative">
            {/* Desktop/Tablet: Horizontal Tree */}
            <div className="hidden md:flex items-start gap-6 lg:gap-8 justify-center pb-4">
              {/* Column 1: Training Programs */}
              <div className="relative flex-shrink-0 w-56 lg:w-64">
                {/* Connecting lines to center */}
                <svg className="absolute top-0 left-full w-6 lg:w-8 h-full pointer-events-none" style={{ zIndex: 0 }}>
                  <line x1="0" y1="50%" x2="100%" y2="50%" stroke="hsl(var(--border))" strokeWidth="2" strokeDasharray="4,4" />
                </svg>
                <div className="relative bg-gradient-to-br from-destructive/20 to-destructive/10 rounded-lg p-3 lg:p-4 border-2 border-destructive/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-destructive/20 p-1.5 rounded-lg">
                      <Clock className="w-4 h-4 text-destructive" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">Training</h3>
                      <p className="text-xs text-muted-foreground">&lt;1 Year</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.training.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-destructive/30 to-destructive/10 border-destructive/40 hover:border-destructive"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Column 2: Community College */}
              <div className="relative flex-shrink-0 w-56 lg:w-64">
                {/* Connecting lines */}
                <svg className="absolute top-0 left-full w-6 lg:w-8 h-full pointer-events-none" style={{ zIndex: 0 }}>
                  <line x1="0" y1="50%" x2="100%" y2="50%" stroke="hsl(var(--border))" strokeWidth="2" strokeDasharray="4,4" />
                </svg>
                <div className="relative bg-gradient-to-br from-uh-green/20 to-uh-green/10 rounded-lg p-3 lg:p-4 border-2 border-uh-green/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-uh-green/20 p-1.5 rounded-lg">
                      <School className="w-4 h-4 text-uh-green" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">Community College</h3>
                      <p className="text-xs text-muted-foreground">2 Years</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.communityCollege.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-uh-green/30 to-uh-green/10 border-uh-green/40 hover:border-uh-green"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Column 3: University Track */}
              <div className="relative flex-shrink-0 w-56 lg:w-64">
                {/* Connecting lines */}
                <svg className="absolute top-0 left-full w-6 lg:w-8 h-full pointer-events-none" style={{ zIndex: 0 }}>
                  <line x1="0" y1="50%" x2="100%" y2="50%" stroke="hsl(var(--border))" strokeWidth="2" strokeDasharray="4,4" />
                </svg>
                <div className="relative bg-gradient-to-br from-accent/20 to-accent/10 rounded-lg p-3 lg:p-4 border-2 border-accent/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-accent/20 p-1.5 rounded-lg">
                      <GraduationCap className="w-4 h-4 text-accent" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">University</h3>
                      <p className="text-xs text-muted-foreground">4 Years</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.university.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-accent/30 to-accent/10 border-accent/40 hover:border-accent"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Final: Career */}
              <div className="relative flex-shrink-0 w-48 lg:w-56">
                <div className="bg-gradient-to-br from-primary/20 to-primary/10 rounded-lg p-4 lg:p-6 border-2 border-primary/30 h-full flex flex-col items-center justify-center">
                  <div className="bg-primary/20 p-3 rounded-full mb-3">
                    <Briefcase className="w-8 h-8 lg:w-10 lg:h-10 text-primary" />
                  </div>
                  <h3 className="font-bold text-base lg:text-lg text-center mb-2">Career</h3>
                  <p className="text-xs lg:text-sm text-center text-muted-foreground mb-2">{occupation.title}</p>
                  <Badge className="bg-uh-green/20 text-uh-green border-uh-green/40 text-xs">
                    {formatSalary(occupation.medianSalary)}
                  </Badge>
                </div>
              </div>
            </div>

            {/* Mobile: Vertical Tree */}
            <div className="md:hidden flex flex-col items-center gap-6">
              {/* Training Programs */}
              <div className="w-full max-w-sm">
                <div className="bg-gradient-to-br from-destructive/20 to-destructive/10 rounded-lg p-4 border-2 border-destructive/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-destructive/20 p-1.5 rounded-lg">
                      <Clock className="w-4 h-4 text-destructive" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">Training Programs</h3>
                      <p className="text-xs text-muted-foreground">&lt;1 Year</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.training.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-destructive/30 to-destructive/10 border-destructive/40 hover:border-destructive"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Arrow Down */}
              <div className="flex items-center justify-center">
                <div className="w-0.5 h-8 bg-border" />
              </div>

              {/* Community College */}
              <div className="w-full max-w-sm">
                <div className="bg-gradient-to-br from-uh-green/20 to-uh-green/10 rounded-lg p-4 border-2 border-uh-green/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-uh-green/20 p-1.5 rounded-lg">
                      <School className="w-4 h-4 text-uh-green" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">Community College</h3>
                      <p className="text-xs text-muted-foreground">2-Year Track</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.communityCollege.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-uh-green/30 to-uh-green/10 border-uh-green/40 hover:border-uh-green"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Arrow Down */}
              <div className="flex items-center justify-center">
                <div className="w-0.5 h-8 bg-border" />
              </div>

              {/* University Track */}
              <div className="w-full max-w-sm">
                <div className="bg-gradient-to-br from-accent/20 to-accent/10 rounded-lg p-4 border-2 border-accent/30">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="bg-accent/20 p-1.5 rounded-lg">
                      <GraduationCap className="w-4 h-4 text-accent" />
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-foreground">University Track</h3>
                      <p className="text-xs text-muted-foreground">4-Year Programs</p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    {mockHawaiiPrograms.university.map((program) => (
                      <ProgramCard 
                        key={program.id} 
                        program={program} 
                        color="bg-gradient-to-br from-accent/30 to-accent/10 border-accent/40 hover:border-accent"
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Arrow Down */}
              <div className="flex items-center justify-center">
                <div className="w-0.5 h-8 bg-border" />
              </div>

              {/* Final: Career */}
              <div className="w-full max-w-sm">
                <div className="bg-gradient-to-br from-primary/20 to-primary/10 rounded-lg p-6 border-2 border-primary/30 flex flex-col items-center justify-center">
                  <div className="bg-primary/20 p-3 rounded-full mb-3">
                    <Briefcase className="w-10 h-10 text-primary" />
                  </div>
                  <h3 className="font-bold text-lg text-center mb-2">Career</h3>
                  <p className="text-sm text-center text-muted-foreground mb-3">{occupation.title}</p>
                  <Badge className="bg-uh-green/20 text-uh-green border-uh-green/40">
                    {formatSalary(occupation.medianSalary)}
                  </Badge>
                </div>
              </div>
            </div>
          </div>
          {/* End of hidden legacy section */}
        </div>
      </div>
    </div>
  );
};

export default OccupationDetails;
