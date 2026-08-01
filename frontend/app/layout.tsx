import "./globals.css";

export const metadata = {
  title: "Clip Generator",
  description: "Gere clipes verticais a partir de VODs com IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-neutral-950 text-neutral-100">{children}</body>
    </html>
  );
}
