// 사이트가 날짜별 건강 기록 요약을 읽어가는 주소 (헤더 x-read-key 필요)
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "x-read-key, content-type",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};
const isDate = (s: string | null) => !!s && /^\d{4}-\d{2}-\d{2}$/.test(s);

let KEYS: Record<string, string> | null = null;
async function key(name: string) {
  if (!KEYS) { const { data } = await db.from("hc_config").select("name,value"); KEYS = Object.fromEntries((data ?? []).map((r) => [r.name, r.value])); }
  return KEYS[name];
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (req.headers.get("x-read-key") !== await key("read_key")) {
    return new Response("unauthorized", { status: 401, headers: cors });
  }
  const u = new URL(req.url);
  const from = u.searchParams.get("from"), to = u.searchParams.get("to");
  if (!isDate(from) || !isDate(to)) return new Response("from/to 필요", { status: 400, headers: cors });

  const [{ data: days, error }, { data: last }] = await Promise.all([
    db.rpc("hc_daily", { d_from: from, d_to: to }),
    db.from("hc_payloads").select("received_at, counts").order("id", { ascending: false }).limit(1),
  ]);
  if (error) return new Response("db error: " + error.message, { status: 500, headers: cors });
  return Response.json({ days, last: last?.[0] ?? null }, { headers: { ...cors, "Cache-Control": "no-store" } });
});
