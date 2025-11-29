'use client';

import { useState } from "react";
import axios from "axios";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import { useAuth } from "@/store/useAuth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

export default function AuthSection() {
  const [registerData, setRegisterData] = useState({
    full_name: "",
    cpf: "",
    email: "",
    phone: "",
    birth_date: "",
    address: "",
    symptom_initial: "",
    password: "",
  });
  const [loginData, setLoginData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const { setTokens, loadProfile } = useAuth();

  const handleRegister = async () => {
    setMessage("");
    await axios.post(`${API_BASE}/register/patient/`, registerData);
    setMessage("Cadastro concluído! Faça login para acessar o painel.");
  };

  const handleLogin = async () => {
    setMessage("");
    const res = await axios.post(`${API_BASE}/auth/token/`, {
      username: loginData.username,
      password: loginData.password,
    });
    setTokens(res.data.access, res.data.refresh);
    await loadProfile();
    setMessage("Login efetuado! Acesse o painel do paciente ou médico.");
  };

  return (
    <section className="grid gap-6 md:grid-cols-2">
      <div className="glass p-6 rounded-2xl">
        <h3 className="text-xl font-semibold mb-3">Cadastro de Paciente</h3>
        <div className="grid gap-3">
          <Input placeholder="Nome completo" value={registerData.full_name} onChange={(e) => setRegisterData({ ...registerData, full_name: e.target.value })} />
          <Input placeholder="CPF" value={registerData.cpf} onChange={(e) => setRegisterData({ ...registerData, cpf: e.target.value })} />
          <Input placeholder="E-mail" value={registerData.email} onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })} />
          <Input placeholder="Telefone" value={registerData.phone} onChange={(e) => setRegisterData({ ...registerData, phone: e.target.value })} />
          <Input type="date" value={registerData.birth_date} onChange={(e) => setRegisterData({ ...registerData, birth_date: e.target.value })} />
          <Input placeholder="Endereço completo" value={registerData.address} onChange={(e) => setRegisterData({ ...registerData, address: e.target.value })} />
          <Textarea placeholder="Sintoma inicial" value={registerData.symptom_initial} onChange={(e) => setRegisterData({ ...registerData, symptom_initial: e.target.value })} />
          <Input type="password" placeholder="Senha" value={registerData.password} onChange={(e) => setRegisterData({ ...registerData, password: e.target.value })} />
          <Button onClick={handleRegister}>Cadastrar</Button>
        </div>
      </div>
      <div className="glass p-6 rounded-2xl">
        <h3 className="text-xl font-semibold mb-3">Login</h3>
        <div className="grid gap-3">
          <Input placeholder="E-mail" value={loginData.username} onChange={(e) => setLoginData({ ...loginData, username: e.target.value })} />
          <Input type="password" placeholder="Senha" value={loginData.password} onChange={(e) => setLoginData({ ...loginData, password: e.target.value })} />
          <Button onClick={handleLogin}>Entrar</Button>
          {message && <p className="text-sm text-brand">{message}</p>}
        </div>
      </div>
    </section>
  );
}
