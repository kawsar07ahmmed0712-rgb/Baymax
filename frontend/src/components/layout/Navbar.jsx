import { Bot, Github } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-500">
            <Bot size={22} />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white">Baymax</h1>
            <p className="text-xs text-slate-400">AI-vs-AI Chess Arena</p>
          </div>
        </div>

        <div className="hidden items-center gap-2 text-sm text-slate-400 sm:flex">
          <Github size={16} />
          <span>Local-first · Deploy-ready</span>
        </div>
      </div>
    </header>
  );
}
