 "use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { useAuth } from "@/store/useAuth";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

type QueueEntry = {
  id: number;
  symptom: string;
  status: string;
  created_at: string;
};

type DocumentItem = {
  id: number;
  doc_type: string;
};

export default function PatientPage() {
  const { accessToken, profile } = useAuth();
  const [symptom, setSymptom] = useState("");
  const [queue, setQueue] = useState<QueueEntry[]>([]);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);

  const loadQueue = async () => {
    const res = await axios.get(`${API}/patient/queue/status/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    setQueue(res.data);
  };

  const loadDocuments = async () => {
    const res = await axios.get(`${API}/patient/documents/`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    setDocuments(res.data);
  };

  useEffect(() => {
    if (accessToken) {
      loadQueue();
      loadDocuments();
    }
  }, [accessToken]);

  const enterQueue = async () => {
    await axios.post(
      `${API}/patient/queue/`,
      { symptom },
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
    setSymptom("");
    await loadQueue();
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        <h1 className="text-3xl font-bold">Painel do Paciente</h1>
        <Card className="space-y-3">
          <div className="text-lg font-semibold">Entrar na fila</div>
          <Textarea placeholder="Descreva seu sintoma" value={symptom} onChange={(e) => setSymptom(e.target.value)} />
          <Button onClick={enterQueue} disabled={!symptom}>
            Entrar agora
          </Button>
        </Card>

        <Card className="space-y-3">
          <div className="text-lg font-semibold">Minha fila</div>
          <div className="space-y-2 text-sm">
            {queue.map((q) => (
              <div key={q.id} className="flex justify-between glass p-3 rounded-md">
                <div>
                  <div className="font-medium">{q.symptom}</div>
                  <div className="text-white/70">{new Date(q.created_at).toLocaleString()}</div>
                </div>
                <span className="uppercase text-xs">{q.status}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card className="space-y-3">
          <div className="text-lg font-semibold">Documentos</div>
          <div className="flex flex-col gap-2">
            {documents.map((d) => (
              <a
                key={d.id}
                href={`${API}/documents/${d.id}/download/`}
                target="_blank"
                className="text-brand hover:underline"
              >
                Baixar {d.doc_type} #{d.id}
              </a>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}
