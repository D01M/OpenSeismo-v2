/**
 * Stations Module - Seismic station data fetching and visualization
 */

let stationEntities = [];
let stationEntityLookup = new Map();

function formatStationTime(value) {
  if (!value) return "Unknown";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Unknown";
  return date.toLocaleString();
}

function getStationFilters() {
  const network = document.getElementById("stationNetworkFilter")?.value.trim();
  const status = document.getElementById("stationStatusFilter")?.value.trim();
  const channel = document.getElementById("stationChannelFilter")?.value.trim();
  const geo = document.getElementById("stationGeoFilter")?.value.trim();
  const tag = document.getElementById("stationTagFilter")?.value.trim();
  const activeRecent = document.getElementById("stationActiveRecentFilter")?.checked;
  const recentMinutes = Number(document.getElementById("stationRecentMinutesFilter")?.value || 30);

  const params = new URLSearchParams();
  if (network) params.set("network", network);
  if (status) params.set("status", status);
  if (channel) params.set("channel", channel);
  if (geo) {
    params.set("country", geo);
    params.set("region", geo);
  }
  if (tag) params.set("tag", tag);
  if (activeRecent) {
    params.set("active_recent", "1");
    params.set("recent_minutes", String(Number.isFinite(recentMinutes) && recentMinutes > 0 ? recentMinutes : 30));
  }

  const query = params.toString();
  return query ? `?${query}` : "";
}

/**
 * Noise level color mapping
 * @param {number} n - Noise level
 */
function noiseColor(n) {
  if (n < 20) return Cesium.Color.fromCssColorString("#00ffd1");
  if (n < 40) return Cesium.Color.fromCssColorString("#7dff5e");
  if (n < 65) return Cesium.Color.fromCssColorString("#ffd45e");
  return Cesium.Color.fromCssColorString("#ff3d5e");
}

function stationEntityId(station) {
  return station?.id || `${station?.network || ""}:${station?.code || station?.name || "station"}`;
}

function buildStationTelemetry(station) {
  const noise = Number(station.noise_level || 0);
  const status = String(station.status || station.health || "unknown").toLowerCase();
  const channels = Array.isArray(station.channels) ? station.channels.join(", ") : String(station.channels || "N/A");
  return `<b>${station.code}</b> · ${station.name}<br>Network: ${station.network}<br>Status: ${status}<br>Country: ${station.country || "N/A"}<br>Region: ${station.region || "N/A"}<br>Channels: ${channels}<br>Last seen: ${formatStationTime(station.last_seen)}<br>Noise: ${fmt(noise, 1)}/100 · ${station.signal_quality || "unknown"}<br>Provider: ${station.provider || station.source || "N/A"}<br>Coverage: ${station.coverage_radius_km || "N/A"} km<br>${
    station.arrival
      ? `Distance: ${station.arrival.distance_km} km (${station.arrival.distance_deg}°)<br>P: ${station.arrival.p_wave_seconds}s · S: ${station.arrival.s_wave_seconds}s · Surface: ${station.arrival.surface_wave_seconds}s`
      : "No linked M4.5+ event"
  }`;
}

function syncStationEntities(stations, visible) {
  const nextIds = new Set();
  const stationList = Array.isArray(stations) ? stations : [];

  stationList.forEach(station => {
    const stationId = stationEntityId(station);
    if (!stationId) return;
    nextIds.add(stationId);

    const existing = stationEntityLookup.get(stationId);
    const noise = Number(station.noise_level || 0);
    const status = String(station.status || station.health || "unknown").toLowerCase();
    const size = Math.max(7, Math.min(22, 6 + noise / 6));
    const color = stationColor(station, noise);
    const telemetry = buildStationTelemetry(station);

    if (existing) {
      existing.position = Cesium.Cartesian3.fromDegrees(Number(station.lon ?? station.longitude ?? 0), Number(station.lat ?? station.latitude ?? 0), 125000);
      existing.point.pixelSize = size;
      existing.point.color = color;
      existing.point.outlineColor = Cesium.Color.WHITE;
      existing.point.outlineWidth = 1;
      existing.point.scaleByDistance = new Cesium.NearFarScalar(1.5e6, 1.2, 2.8e7, 0.35);
      existing.show = visible;
      existing._telemetry = telemetry;
      return;
    }

    const entity = addPoint(
      Number(station.lon ?? station.longitude ?? 0),
      Number(station.lat ?? station.latitude ?? 0),
      125000,
      size,
      color,
      Cesium.Color.WHITE,
      telemetry,
      stationEntities,
      visible
    );
    entity._stationStatus = status;
    stationEntityLookup.set(stationId, entity);
  });

  for (const [id, entity] of stationEntityLookup.entries()) {
    if (!nextIds.has(id)) {
      try {
        viewer.entities.remove(entity);
      } catch (_) {}
      stationEntityLookup.delete(id);
      const index = stationEntities.indexOf(entity);
      if (index >= 0) stationEntities.splice(index, 1);
    }
  }
}

/**
 * Refresh station data from API
 */
async function refreshStations() {
  try {
    const data = await fetchJson(`/api/stations${getStationFilters()}`);
    const visible = document.getElementById("showStations").checked;
    const stations = data.stations || [];
    syncStationEntities(stations, visible);

    let total = 0;
    let rows = [];

    stations.forEach(s => {
      const noise = Number(s.noise_level || 0);
      const status = String(s.status || s.health || "unknown").toLowerCase();
      const channels = Array.isArray(s.channels) ? s.channels.join(", ") : String(s.channels || "N/A");
      total += noise;
      rows.push(
        `<div class="item"><b>${s.code}</b> ${s.name}<br>Status ${status} · Noise ${fmt(noise, 1)} · ${s.signal_quality || "unknown"}<br>${
          s.arrival
            ? `P ${s.arrival.p_wave_seconds}s / S ${s.arrival.s_wave_seconds}s`
            : "No linked event"
        }<br>Channels: ${channels}<br>Last seen: ${formatStationTime(s.last_seen)}</div>`
      );
    });

    if (window.openSeismoGlobeView) {
      window.openSeismoGlobeView.setStations(stations.map(s => ({
        id: s.id || `${s.network || ""}:${s.code || s.name}`,
        code: s.code,
        name: s.name,
        network: s.network,
        country: s.country,
        region: s.region,
        status: s.status || s.health,
        channels: s.channels || [],
        provider: s.provider || s.source,
        last_seen: s.last_seen,
        noise_level: s.noise_level,
        signal_quality: s.signal_quality,
        latitude: s.latitude ?? s.lat,
        longitude: s.longitude ?? s.lon,
        lat: s.latitude ?? s.lat,
        lon: s.longitude ?? s.lon,
        lastUpdated: s.last_seen || s.lastUpdated || null
      })));
    }

    document.getElementById("stationCount").textContent = stations.length || 0;
    document.getElementById("stationList").innerHTML = rows.join("") || "No stations.";
  } catch (e) {
    console.error(e);
    document.getElementById("stationList").innerHTML = `<span class="err">Station data failed: ${e.message}</span>`;
  }
}

function stationColor(station, noise) {
  const status = String(station.status || station.health || "unknown").toLowerCase();
  if (status === "offline") return Cesium.Color.fromCssColorString("#8b949e").withAlpha(0.35);
  if (status === "delayed") return Cesium.Color.fromCssColorString("#ffb347").withAlpha(0.88);
  if (status === "triggering") return Cesium.Color.fromCssColorString("#ff6b42").withAlpha(1.0);
  if (status === "unknown") return Cesium.Color.fromCssColorString("#aeb8c2").withAlpha(0.7);
  return noiseColor(noise).withAlpha(0.95);
}

/**
 * Get all station entities
 */
function getStationEntities() {
  return stationEntities;
}
