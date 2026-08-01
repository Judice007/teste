const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Job = {
  id: string;
  stage: string;
  status: string;
  error: string | null;
};

export type Clip = {
  id: string;
  start_seconds: number;
  end_seconds: number;
  reason: string | null;
  video_path: string | null;
};

export type Project = {
  id: string;
  source_url: string | null;
  status: string;
  created_at: string;
  jobs: Job[];
  clips: Clip[];
};

export async function createProject(sourceUrl: string): Promise<Project> {
  const res = await fetch(`${API_URL}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_url: sourceUrl }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function listProjects(): Promise<Project[]> {
  const res = await fetch(`${API_URL}/projects`, { cache: "no-store" });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getProject(id: string): Promise<Project> {
  const res = await fetch(`${API_URL}/projects/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export function clipDownloadUrl(clipId: string): string {
  return `${API_URL}/clips/${clipId}/download`;
}
