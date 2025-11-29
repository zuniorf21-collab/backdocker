import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Consulta Avulsa",
    price: "R$ 89",
    perks: ["Fila imediata", "Receita e atestado em PDF", "Envio por WhatsApp"],
  },
  {
    name: "Plano Família",
    price: "R$ 159/mês",
    perks: ["Até 4 dependentes", "Histórico compartilhado", "Fila prioritária"],
  },
  {
    name: "Empresas",
    price: "Fale com vendas",
    perks: ["Cobertura nacional", "Relatórios mensais", "Médicos dedicados"],
  },
];

export default function Plans() {
  return (
    <section className="space-y-6">
      <h2 className="text-2xl font-semibold">Planos de Telemedicina</h2>
      <div className="grid gap-6 md:grid-cols-3">
        {plans.map((plan) => (
          <Card key={plan.name} className="flex flex-col gap-4">
            <div className="text-lg font-semibold">{plan.name}</div>
            <div className="text-3xl font-bold text-brand">{plan.price}</div>
            <ul className="space-y-2 text-sm text-white/80">
              {plan.perks.map((perk) => (
                <li key={perk} className="flex items-center gap-2">
                  <Check className="text-brand" size={16} /> {perk}
                </li>
              ))}
            </ul>
            <Button className="mt-auto" variant="outline">
              Escolher plano
            </Button>
          </Card>
        ))}
      </div>
    </section>
  );
}
