// 기록·사진 동기화: GET ?name=data|slots → {value, updated_at}, PUT ?name= (본문 문자열). 헤더 x-read-key 필요
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "x-read-key, content-type",
  "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
};
let KEY: string | null = null;
async function readKey() {
  if (!KEY) { const { data } = await db.from("hc_config").select("value").eq("name", "read_key").single(); KEY = data?.value ?? ""; }
  return KEY;
}
const OK = ["data", "slots"];

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (req.headers.get("x-read-key") !== await readKey()) return new Response("unauthorized", { status: 401, headers: cors });
  const name = new URL(req.url).searchParams.get("name") ?? "";
  if (!OK.includes(name)) return new Response("bad name", { status: 400, headers: cors });
  if (req.method === "GET") {
    const { data, error } = await db.from("tk_sync").select("value, updated_at").eq("name", name).maybeSingle();
    if (error) return new Response("db error: " + error.message, { status: 500, headers: cors });
    return Response.json(data ?? { value: null, updated_at: null }, { headers: { ...cors, "Cache-Control": "no-store" } });
  }
  if (req.method === "PUT") {
    const value = await req.text();
    if (!value) return new Response("empty", { status: 400, headers: cors });
    const { data, error } = await db.from("tk_sync").upsert({ name, value, updated_at: new Date().toISOString() }).select("updated_at").single();
    if (error) return new Response("db error: " + error.message, { status: 500, headers: cors });
    return Response.json({ ok: true, updated_at: data.updated_at }, { headers: cors });
  }
  return new Response("method", { status: 405, headers: cors });
});
