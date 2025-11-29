import { create } from "zustand";
import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

type UserProfile = {
  id: number;
  role: "patient" | "doctor" | "admin";
  patient?: any;
  doctor?: any;
};

type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  profile: UserProfile | null;
  setTokens: (access: string, refresh: string) => void;
  loadProfile: () => Promise<void>;
  logout: () => void;
};

export const useAuth = create<AuthState>((set, get) => ({
  accessToken: null,
  refreshToken: null,
  profile: null,
  setTokens: (access, refresh) => set({ accessToken: access, refreshToken: refresh }),
  logout: () => set({ accessToken: null, refreshToken: null, profile: null }),
  loadProfile: async () => {
    const token = get().accessToken;
    if (!token) return;
    const res = await axios.get(`${API_BASE}/profile/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    set({ profile: res.data });
  },
}));
