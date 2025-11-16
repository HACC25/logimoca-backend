import { CheckCircle, Target, Users, Sparkles } from "lucide-react";
import Navigation from "@/components/Navigation";
import { Card } from "@/components/ui/card";

const About = () => {
  const features = [
    {
      icon: Target,
      title: "Personalized Guidance",
      description: "RIASEC interest assessment and skills matching to find careers that truly fit you.",
    },
    {
      icon: Users,
      title: "Hawaiʻi-Focused",
      description: "Connect with local training programs and educational pathways across the UH system.",
    },
    {
      icon: Sparkles,
      title: "AI-Powered Insights",
      description: "Advanced LLM technology provides accurate, personalized career recommendations.",
    },
    {
      icon: CheckCircle,
      title: "Quick & Easy",
      description: "Complete your assessment in just 5-10 minutes and get immediate results.",
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="max-w-3xl mx-auto text-center mb-16 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold text-foreground mb-4">
            About UH Pathfinder AI
          </h1>
          <p className="text-xl text-muted-foreground">
            Helping Hawaiʻi students discover personalized educational pathways
          </p>
        </div>

        {/* Mission Section */}
        <div className="max-w-4xl mx-auto mb-16 animate-slide-up">
          <Card className="p-8 bg-card shadow-lg">
            <h2 className="text-2xl font-bold text-foreground mb-4">Our Mission</h2>
            <p className="text-foreground/80 mb-4">
              UH Pathfinder AI helps Hawaiʻi students discover personalized educational pathways by 
              connecting their interests, skills, and career goals with local training programs and 
              national occupational data.
            </p>
            <p className="text-foreground/80">
              Unlike generic career tools, UH Pathfinder specifically maps Hawaiʻi-based training 
              programs to career pathways, addressing the unique needs of island students navigating 
              the 10 UH campuses and thousands of program options.
            </p>
          </Card>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-foreground text-center mb-12">
            How It Works
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="p-6 hover:shadow-xl transition-shadow duration-300 animate-scale-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center">
                      <feature.icon className="w-6 h-6 text-accent" />
                    </div>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-foreground mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Assessment Process */}
        <div className="max-w-4xl mx-auto">
          <Card className="p-8 bg-primary text-primary-foreground shadow-lg">
            <h2 className="text-2xl font-bold mb-6">The Assessment Process</h2>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center font-bold">
                  1
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Interest Assessment</h3>
                  <p className="text-primary-foreground/80">
                    Complete the RIASEC quiz to identify your career interests across 6 personality types.
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center font-bold">
                  2
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Skills Evaluation</h3>
                  <p className="text-primary-foreground/80">
                    Assess your abilities across 40 skill dimensions using an interactive, adaptive interface.
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center font-bold">
                  3
                </div>
                <div>
                  <h3 className="font-semibold mb-1">Get Matched</h3>
                  <p className="text-primary-foreground/80">
                    Receive personalized career recommendations and discover relevant Hawaiʻi training programs.
                  </p>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;
