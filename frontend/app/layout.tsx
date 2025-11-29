import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Telemed | Pronto-Socorro Online",
  description: "Atendimento médico online com fila em tempo real",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-br">
      <body>{children}</body>
    </html>
  );
}
