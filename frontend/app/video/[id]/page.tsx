 "use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import axios from "axios";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/store/useAuth";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export default function VideoPage() {
  const { id } = useParams<{ id: string }>();
  const { accessToken } = useAuth();
  const [token, setToken] = useState<string | null>(null);
  const [room, setRoom] = useState<string | null>(null);

  const fetchToken = async () => {
    const res = await axios.post(
      `${API}/video/token/`,
      { consultation_id: id },
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );
    setToken(res.data.token);
    setRoom(res.data.room);
  };

  useEffect(() => {
    if (accessToken && id) {
      fetchToken();
    }
  }, [accessToken, id]);

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-6 py-10">
      <Card className="w-full max-w-2xl space-y-4 text-center">
        <h1 className="text-2xl font-bold">Sala de Vídeo</h1>
        {token ? (
          <div className="space-y-2">
            <div className="text-sm text-white/80">Room: {room}</div>
            <div className="text-xs text-white/60 break-all">
              Token (use no cliente Twilio Video): {token}
            </div>
            <Button onClick={fetchToken} variant="outline">
              Renovar token
            </Button>
          </div>
        ) : (
          <div className="text-white/60">Gerando token...</div>
        )}
      </Card>
    </div>
  );
}
