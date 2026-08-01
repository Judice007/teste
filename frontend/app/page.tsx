"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { createProject, listProjects, Project } from "../lib/api";

export default function Home() {
  const [url, setUrl] = useState("");
  const [projects, setProjects] = useState<Project[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      setProjects(await listProjects());
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, 4000);
    return () => clearInterval(interval);
  }, []);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await createProject(url);
      setUrl("");
      await refresh();
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="mb-6 text-2xl font-semibold">Clip Generator</h1>

      <form onSubmit={handleSubmit} className="mb-8 flex gap-2">
        <input
          type="url"
          required
          placeholder="URL do VOD (Twitch, YouTube, Kick)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="flex-1 rounded border border-neutral-800 bg-neutral-900 px-3 py-2"
        />
        <button
          type="submit"
          disabled={submitting}
          className="rounded bg-indigo-600 px-4 py-2 disabled:opacity-50"
        >
          {submitting ? "Enviando..." : "Gerar clipes"}
        </button>
      </form>

      {error && <p className="mb-4 text-red-400">{error}</p>}

      <ul className="space-y-3">
        {projects.map((p) => (
          <li key={p.id} className="rounded border border-neutral-800 p-4">
            <Link href={`/projects/${p.id}`} className="hover:underline">
              <p className="truncate">{p.source_url}</p>
              <p className="text-sm text-neutral-400">
                status: {p.status} · {p.clips.length} clipe(s)
              </p>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
