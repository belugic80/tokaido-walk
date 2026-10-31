// 폰 GPS 위치 로거(OwnTracks / GPSLogger 등)가 백그라운드로 보내는 위치를 hc_loc 에 저장
// 주소 뒤에 ?k=<hc_config.loc_key> 가 있어야 받아줌
import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
let KEY: string | null = null;
async function locKey() {
  if (!KEY) { const { data } = await db.from("hc_config").select("value").eq("name", "loc_key").single(); KEY = data?.value ?? ""; }
  return KEY;
}
const num = (v: unknown) => (v === undefined || v === null || v === "" ? NaN : Number(v));

Deno.serve(async (req) => {
  const u = new URL(req.url);
  if (u.searchParams.get("k") !== await locKey()) return new Response("unauthorized", { status: 401 });
  let p: Record<string, unknown> = Object.fromEntries(u.searchParams);
  if (req.method === "POST") {
    const raw = await req.text();
    try { p = { ...p, ...JSON.parse(raw) }; } catch { try { p = { ...p, ...Object.fromEntries(new URLSearchParams(raw)) }; } catch { /* ignore */ } }
  }
  // OwnTracks는 위치 외 메시지(_type: lwt 등)도 보냄 → 무시하고 정상 응답
  if (p._type && p._type !== "location") return Response.json([]);
  const lat = num(p.lat), lon = num(p.lon ?? p.lng ?? p.long);
  if (!isFinite(lat) || !isFinite(lon) || Math.abs(lat) > 90 || Math.abs(lon) > 180) return Response.json([]);
  let ms = NaN;
  const ts = num(p.tst ?? p.ts ?? p.timestamp ?? p.epoch);
  if (isFinite(ts)) ms = ts > 1e12 ? ts : ts * 1000;
  else if (p.time) ms = Date.parse(String(p.time));
  if (!isFinite(ms) || Math.abs(ms - Date.now()) > 7 * 864e5) ms = Date.now();
  const at = new Date(ms);
  const day = new Date(ms + 9 * 3600e3).toISOString().slice(0, 10); // 한국·일본 모두 UTC+9
  const acc = num(p.acc ?? p.accuracy);
  const { error } = await db.from("hc_loc").upsert(
    { day, at: at.toISOString(), lat, lon, acc: isFinite(acc) ? acc : null, src: String(p.src ?? "phone") },
    { onConflict: "at,src", ignoreDuplicates: true },
  );
  if (error) { console.error("loc-webhook", error.message); return new Response("error", { status: 500 }); }
  return Response.json([]); // OwnTracks가 기대하는 응답 형식
});
