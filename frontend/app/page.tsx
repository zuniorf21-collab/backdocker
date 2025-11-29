import Link from "next/link";
import LandingHero from "@/components/landing-hero";
import Plans from "@/components/plans";
import AuthSection from "@/components/auth-section";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      <div className="max-w-6xl mx-auto px-6 py-12 space-y-12">
        <LandingHero />
        <Plans />
        <AuthSection />
        <div className="text-center">
          <Link
            href="/patient"
            className="inline-flex items-center rounded-full bg-brand px-6 py-3 font-semibold text-white hover:bg-brand-dark"
          >
            Iniciar consulta online agora
          </Link>
        </div>
      </div>
    </main>
  );
}
