"use client";

import { useEffect, useState } from "react";
import { clipDownloadUrl, getProject, Project } from "../../../lib/api";

export default function ProjectPage({ params }: { params: { id: string } }) {
  const [project, setProject] = useState<Project | null>(null);

  useEffect(() => {
    async function refresh() {
      setProject(await getProject(params.id));
    }
    refresh();
    const interval = setInterval(refresh, 4000);
    return () => clearInterval(interval);
  }, [params.id]);

  if (!project) return <main className="p-8">Carregando...</main>;

  return (
    <main className="mx-auto max-w-2xl p-8">
      <h1 className="mb-2 truncate text-xl font-semibold">{project.source_url}</h1>
      <p className="mb-6 text-neutral-400">status: {project.status}</p>

      <h2 className="mb-2 font-medium">Etapas</h2>
      <ul className="mb-6 space-y-1 text-sm">
        {project.jobs.map((job) => (
          <li key={job.id}>
            {job.stage}: {job.status} {job.error ? `(${job.error})` : ""}
          </li>
        ))}
      </ul>

      <h2 className="mb-2 font-medium">Clipes</h2>
      <ul className="space-y-3">
        {project.clips.map((clip) => (
          <li key={clip.id} className="rounded border border-neutral-800 p-4">
            <p className="text-sm text-neutral-400">
              {clip.start_seconds.toFixed(0)}s - {clip.end_seconds.toFixed(0)}s
            </p>
            {clip.reason && <p className="mb-2 text-sm">{clip.reason}</p>}
            <a href={clipDownloadUrl(clip.id)} className="text-indigo-400 hover:underline">
              Baixar clipe
            </a>
          </li>
        ))}
      </ul>
    </main>
  );
}
