 "use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import Link from "next/link";
import { useAuth } from "@/store/useAuth";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

type QueueEntry = {
  id: number;
  patient: { full_name: string };
  symptom: string;
  status: string;
};

type Consultation = {
  id: number;
  patient: { full_name: string };
  symptom: string;
  anamnesis: string;
  prescription: string;
  certificate: string;
  declaration: string;
  room_name: string;
};

export default function DoctorPage() {
  const { accessToken } = useAuth();
  const [queue, setQueue] = useState<QueueEntry[]>([]);
  const [consultation, setConsultation] = useState<Consultation | null>(null);
  const [form, setForm] = useState({ anamnesis: "", prescription: "", certificate: "", declaration: "" });

  const headers = { Authorization: `Bearer ${accessToken}` };

  const loadQueue = async () => {
    const res = await axios.get(`${API}/doctor/queue/`, { headers });
    setQueue(res.data);
  };

  const startConsultation = async (queueId: number) => {
    const res = await axios.post(`${API}/doctor/queue/${queueId}/start/`, {}, { headers });
    setConsultation(res.data);
    setForm({
      anamnesis: res.data.anamnesis || "",
      prescription: res.data.prescription || "",
      certificate: res.data.certificate || "",
      declaration: res.data.declaration || "",
    });
  };

  const saveConsultation = async () => {
    if (!consultation) return;
    await axios.patch(`${API}/doctor/consultations/${consultation.id}/update/`, form, { headers });
  };

  const finishConsultation = async () => {
    if (!consultation) return;
    await axios.post(`${API}/doctor/consultations/${consultation.id}/finish/`, {}, { headers });
    setConsultation(null);
    await loadQueue();
  };

  const generateDocument = async (type: string) => {
    if (!consultation) return;
    await axios.post(
      `${API}/doctor/consultations/${consultation.id}/document/`,
      { doc_type: type },
      { headers }
    );
  };

  useEffect(() => {
    if (accessToken) loadQueue();
  }, [accessToken]);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-6xl mx-auto px-6 py-10 space-y-6">
        <h1 className="text-3xl font-bold">Painel do Médico</h1>
        <div className="grid md:grid-cols-3 gap-4">
          <Card className="space-y-3 md:col-span-1">
            <div className="font-semibold">Fila</div>
            <div className="space-y-2 text-sm">
              {queue.map((q) => (
                <div key={q.id} className="p-3 rounded-md glass flex justify-between items-center">
                  <div>
                    <div className="font-medium">{q.patient.full_name}</div>
                    <div className="text-white/70 text-xs">{q.symptom}</div>
                  </div>
                  <Button variant="outline" size="sm" onClick={() => startConsultation(q.id)}>
                    Atender
                  </Button>
                </div>
              ))}
            </div>
          </Card>
          <Card className="space-y-3 md:col-span-2">
            <div className="flex justify-between items-center">
              <div className="font-semibold">Consulta</div>
              {consultation && (
                <Link href={`/video/${consultation.id}`} className="text-brand underline">
                  Abrir sala de vídeo
                </Link>
              )}
            </div>
            {consultation ? (
              <div className="space-y-2">
                <div className="text-sm text-white/80">
                  Paciente: <strong>{consultation.patient.full_name}</strong>
                </div>
                <Textarea
                  placeholder="Anamnese"
                  value={form.anamnesis}
                  onChange={(e) => setForm({ ...form, anamnesis: e.target.value })}
                />
                <Textarea
                  placeholder="Receita"
                  value={form.prescription}
                  onChange={(e) => setForm({ ...form, prescription: e.target.value })}
                />
                <Textarea
                  placeholder="Atestado"
                  value={form.certificate}
                  onChange={(e) => setForm({ ...form, certificate: e.target.value })}
                />
                <Textarea
                  placeholder="Declaração"
                  value={form.declaration}
                  onChange={(e) => setForm({ ...form, declaration: e.target.value })}
                />
                <div className="flex gap-2">
                  <Button onClick={saveConsultation}>Salvar</Button>
                  <Button variant="outline" onClick={finishConsultation}>
                    Finalizar
                  </Button>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" onClick={() => generateDocument("prescription")}>
                    Gerar Receita
                  </Button>
                  <Button variant="outline" onClick={() => generateDocument("certificate")}>
                    Gerar Atestado
                  </Button>
                  <Button variant="outline" onClick={() => generateDocument("declaration")}>
                    Gerar Declaração
                  </Button>
                </div>
              </div>
            ) : (
              <div className="text-white/60">Selecione um paciente na fila para iniciar o atendimento.</div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
