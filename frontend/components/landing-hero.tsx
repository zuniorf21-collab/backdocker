import { Button } from "./ui/button";
import { HeartPulse, ShieldCheck, Video } from "lucide-react";
import Link from "next/link";

export default function LandingHero() {
  return (
    <section className="grid gap-8 md:grid-cols-2 items-center">
      <div className="space-y-4">
        <div className="inline-flex items-center gap-2 rounded-full border border-white/20 px-3 py-1 text-xs uppercase tracking-[0.2em] text-white/80">
          <Video size={16} /> Pronto-Socorro Online
        </div>
        <h1 className="text-4xl md:text-5xl font-bold leading-tight">
          Consulta médica imediata, com fila em tempo real e sala de vídeo segura.
        </h1>
        <p className="text-white/80 text-lg">
          Cadastre-se, entre na fila e fale com um médico sem sair de casa. Documentos gerados em PDF e enviados
          direto no seu WhatsApp.
        </p>
        <div className="flex gap-4">
          <Link href="/patient">
            <Button size="lg">Iniciar agora</Button>
          </Link>
          <Link href="/doctor">
            <Button size="lg" variant="outline">
              Sou médico
            </Button>
          </Link>
        </div>
        <div className="flex items-center gap-6 text-white/70">
          <div className="flex items-center gap-2">
            <HeartPulse className="text-brand" size={20} /> Fila online
          </div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="text-brand" size={20} /> Dados auditáveis
          </div>
        </div>
      </div>
      <div className="glass p-6 rounded-2xl shadow-xl border border-white/10">
        <div className="text-sm text-white/70">Fluxo em 3 passos</div>
        <ol className="space-y-4 mt-4 text-white">
          <li className="flex gap-3">
            <span className="h-8 w-8 flex items-center justify-center rounded-full bg-brand text-white font-bold">1</span>
            Cadastre seus dados e sintomas iniciais.
          </li>
          <li className="flex gap-3">
            <span className="h-8 w-8 flex items-center justify-center rounded-full bg-brand text-white font-bold">2</span>
            Entre na fila online e acompanhe seu status.
          </li>
          <li className="flex gap-3">
            <span className="h-8 w-8 flex items-center justify-center rounded-full bg-brand text-white font-bold">3</span>
            Abra a sala de vídeo, receba receita e documentos em PDF/WhatsApp.
          </li>
        </ol>
      </div>
    </section>
  );
}
