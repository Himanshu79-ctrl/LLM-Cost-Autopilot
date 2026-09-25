import Hero from "../../components/landing/Hero";
import PromptPreview from "../../components/landing/PromptPreview";
import WhyRouteMind from "../../components/landing/WhyRouteMind";
import HowItWorks from "../../components/landing/HowItWorks";
import ModelRouting from "../../components/landing/ModelRouting";
import CostQuality from "../../components/landing/CostQuality";
import FinalCTA from "../../components/landing/FinalCTA";
import Footer from "../../components/common/Footer";

function LandingPage() {
  return (
    <main>
      <Hero />

      <PromptPreview />

      <WhyRouteMind />

      <HowItWorks />

      <ModelRouting />

      <CostQuality />

      <FinalCTA />

      <Footer />
    </main>
  );
}

export default LandingPage;