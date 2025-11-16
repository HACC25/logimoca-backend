import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ArrowRight, Target, Sparkles, Map, GraduationCap } from "lucide-react";
import Navigation from "@/components/Navigation";

const Index = () => {
  const features = [
    {
      icon: Target,
      title: "Interest Assessment",
      description: "Discover your career interests with the RIASEC Holland personality assessment.",
    },
    {
      icon: Sparkles,
      title: "Skills Evaluation",
      description: "Identify your strengths across 40 skill dimensions with an interactive assessment.",
    },
    {
      icon: Map,
      title: "Career Matching",
      description: "Get personalized occupation recommendations based on your unique profile.",
    },
    {
      icon: GraduationCap,
      title: "Hawaiʻi Programs",
      description: "Connect with local educational pathways across the UH system.",
    },
  ];

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-primary text-primary-foreground">
        <div className="absolute inset-0 bg-gradient-to-br from-primary via-primary to-primary/90" />
        <div className="container mx-auto px-4 py-20 md:py-32 relative">
          <div className="max-w-4xl mx-auto text-center animate-fade-in">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Discover Your Path at the University of Hawaiʻi
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-foreground/90">
              AI-powered career guidance connecting your interests, skills, and goals with Hawaiʻi educational pathways
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/assessment">
                <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2 text-lg px-8">
                  Start Assessment
                  <ArrowRight className="w-5 h-5" />
                </Button>
              </Link>
              <Link to="/about">
                <Button size="lg" variant="outline" className="bg-primary-foreground/10 border-primary-foreground/20 hover:bg-primary-foreground/20 text-lg px-8">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 animate-slide-up">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              How UH Pathfinder AI Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              A simple, personalized approach to discovering your ideal career path
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="p-6 hover:shadow-xl transition-all duration-300 animate-scale-in"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-accent" />
                </div>
                <h3 className="text-xl font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground">
                  {feature.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-secondary">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto text-center">
            <div className="animate-fade-in">
              <div className="text-4xl md:text-5xl font-bold text-accent mb-2">10</div>
              <div className="text-foreground font-medium">UH Campuses</div>
            </div>
            <div className="animate-fade-in" style={{ animationDelay: "0.1s" }}>
              <div className="text-4xl md:text-5xl font-bold text-accent mb-2">1000+</div>
              <div className="text-foreground font-medium">Programs Available</div>
            </div>
            <div className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
              <div className="text-4xl md:text-5xl font-bold text-accent mb-2">5-10</div>
              <div className="text-foreground font-medium">Minutes to Complete</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <Card className="max-w-4xl mx-auto p-12 text-center bg-primary text-primary-foreground shadow-2xl">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Find Your Path?
            </h2>
            <p className="text-xl mb-8 text-primary-foreground/90">
              Take the first step toward discovering careers that match your unique interests and skills.
            </p>
            <Link to="/assessment">
              <Button size="lg" className="bg-accent hover:bg-accent/90 text-accent-foreground gap-2 text-lg px-8">
                Begin Your Journey
                <ArrowRight className="w-5 h-5" />
              </Button>
            </Link>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;
