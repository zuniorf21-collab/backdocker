import { cn } from "@/lib/utils";
import React from "react";

export const Card = ({ className, children }: { className?: string; children: React.ReactNode }) => (
  <div className={cn("glass p-6 shadow-lg", className)}>{children}</div>
);
