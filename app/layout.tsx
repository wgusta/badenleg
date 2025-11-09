import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "badenleg",
  description: "A new Next.js project",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="de">
      <body>{children}</body>
    </html>
  );
}

