// HC Webhook(삼성 헬스 → Health Connect) 데이터를 받아 hc_records 에 저장
// 앱에서 헤더 x-api-key 에 hc_config.webhook_key 값을 넣어야 받아줌
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const KEEP = [
  "steps", "distance", "active_calories", "total_calories", "heart_rate", "resting_heart_rate",
  "sleep", "exercise", "weight", "oxygen_saturation", "heart_rate_variability", "body_fat",
];

let KEYS: Record<string, string> | null = null;
async function key(name: string) {
  if (!KEYS) { const { data } = await db.from("hc_config").select("name,value"); KEYS = Object.fromEntries((data ?? []).map((r) => [r.name, r.value])); }
  return KEYS[name];
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("ok", { status: 200 });
  if (req.headers.get("x-api-key") !== await key("webhook_key")) {
    return new Response("unauthorized", { status: 401 });
  }
  let body: Record<string, unknown>;
  try { body = await req.json(); } catch { return new Response("bad json", { status: 400 }); }

  const rows: Record<string, unknown>[] = [];
  const counts: Record<string, number> = {};
  for (const type of KEEP) {
    const arr = body[type];
    if (!Array.isArray(arr)) continue;
    counts[type] = arr.length;
    for (const rec of arr as Record<string, any>[]) {
      const start = rec.start_time ?? rec.time ??
        (rec.session_end_time && rec.duration_seconds
          ? new Date(Date.parse(rec.session_end_time) - rec.duration_seconds * 1000).toISOString() : null);
      if (!start) continue;
      const end = rec.end_time ?? rec.session_end_time ?? null;
      const { metadata, ...v } = rec;
      // 원본 기록은 Health Connect id, 묶음(집계) 값은 종류+시작 시각으로 덮어쓰기
      const id = metadata?.id && !("avg" in rec) ? `${type}:${metadata.id}` : `${type}@${new Date(start).toISOString()}`;
      if (metadata?.data_origin) v.origin = metadata.data_origin;
      rows.push({ id, type, t_start: start, t_end: end, v, received_at: new Date().toISOString() });
    }
  }
  for (let i = 0; i < rows.length; i += 500) {
    const { error } = await db.from("hc_records").upsert(rows.slice(i, i + 500));
    if (error) return new Response("db error: " + error.message, { status: 500 });
  }
  const del = Array.isArray(body.deleted) ? (body.deleted as { type: string; id: string }[]) : [];
  if (del.length) await db.from("hc_records").delete().in("id", del.map((d) => `${d.type}:${d.id}`));
  await db.from("hc_payloads").insert({ app_version: body.app_version ?? null, counts: { ...counts, deleted: del.length } });

  return Response.json({ ok: true, saved: rows.length, deleted: del.length });
});
