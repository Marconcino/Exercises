<template>
  <canvas ref = "canvasEl" class = "bee-bg" aria-hidden = "true"></canvas>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const canvasEl = ref(null);

let ctx;
let rafId = null;

const state = {
  dpr: 1,
  w: 0,
  h: 0,
  bees: [],
  lastTs: 0,
  reducedMotion: false,
};

// Simple “bee” particle with a tiny state machine: fly -> cook -> eat -> fly
function makeBee(w, h) {
  const x = Math.random() * w;
  const y = Math.random() * h;
  return {
    x,
    y,
    vx: (Math.random() * 2 - 1) * 40,
    vy: (Math.random() * 2 - 1) * 25,
    size: 10 + Math.random() * 10,
    phase: Math.random() * Math.PI * 2,
    mode: "fly", // fly | cook | eat
    modeT: 1 + Math.random() * 3,
  };
}

function resize() {
  const c = canvasEl.value;
  if (!c) return;

  state.dpr = Math.max(1, window.devicePixelRatio || 1);

  const rect = c.getBoundingClientRect();
  state.w = Math.floor(rect.width);
  state.h = Math.floor(rect.height);

  c.width = Math.floor(state.w * state.dpr);
  c.height = Math.floor(state.h * state.dpr);

  ctx = c.getContext("2d");
  ctx.setTransform(state.dpr, 0, 0, state.dpr, 0, 0);

  // keep bees count proportional
  const target = Math.min(28, Math.max(10, Math.floor(state.w / 60)));
  while (state.bees.length < target) state.bees.push(makeBee(state.w, state.h));
  while (state.bees.length > target) state.bees.pop();
}

function step(ts) {
  if (!ctx) return;
  const dt = Math.min(0.05, (ts - state.lastTs) / 1000 || 0);
  state.lastTs = ts;

  ctx.clearRect(0, 0, state.w, state.h);

  // soft “paper” overlay vibe
  ctx.globalAlpha = 0.06;
  for (let i = 0; i < 180; i++) {
    const x = Math.random() * state.w;
    const y = Math.random() * state.h;
    ctx.fillRect(x, y, 1, 1);
  }
  ctx.globalAlpha = 1;

  // Draw a few “stations”: oven + pizza table
  const oven = { x: state.w * 0.18, y: state.h * 0.72 };
  const table = { x: state.w * 0.78, y: state.h * 0.28 };

  drawStation(oven.x, oven.y, "oven");
  drawStation(table.x, table.y, "pizza");

  for (const b of state.bees) {
    if (!state.reducedMotion) {
      // mode timer
      b.modeT -= dt;
      if (b.modeT <= 0) {
        if (b.mode === "fly") b.mode = Math.random() < 0.5 ? "cook" : "eat";
        else b.mode = "fly";
        b.modeT = b.mode === "fly" ? 1 + Math.random() * 3 : 1 + Math.random() * 2;
      }

      // target attraction
      let tx = b.x, ty = b.y;
      if (b.mode === "cook") { tx = oven.x; ty = oven.y; }
      if (b.mode === "eat") { tx = table.x; ty = table.y; }

      const ax = (tx - b.x) * 0.15;
      const ay = (ty - b.y) * 0.15;

      b.vx += ax * dt * 30;
      b.vy += ay * dt * 30;

      // damping + clamp
      b.vx *= 0.98;
      b.vy *= 0.98;

      b.x += b.vx * dt;
      b.y += b.vy * dt;

      // wrap edges
      if (b.x < -20) b.x = state.w + 20;
      if (b.x > state.w + 20) b.x = -20;
      if (b.y < -20) b.y = state.h + 20;
      if (b.y > state.h + 20) b.y = -20;
    }

    b.phase += dt * 8;
    drawBee(b);
  }

  rafId = requestAnimationFrame(step);
}

function drawStation(x, y, type) {
  ctx.save();
  ctx.translate(x, y);

  ctx.globalAlpha = 0.25;
  ctx.beginPath();
  ctx.arc(0, 0, 26, 0, Math.PI * 2);
  ctx.fill();

  ctx.globalAlpha = 0.9;
  ctx.lineWidth = 2;

  if (type === "oven") {
    // tiny oven icon
    ctx.strokeRect(-16, -12, 32, 24);
    ctx.beginPath();
    ctx.arc(0, 0, 6, 0, Math.PI * 2);
    ctx.stroke();
  } else {
    // tiny pizza slice icon
    ctx.beginPath();
    ctx.moveTo(-10, -12);
    ctx.lineTo(12, 0);
    ctx.lineTo(-10, 12);
    ctx.closePath();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(-4, -4, 1.8, 0, Math.PI * 2);
    ctx.arc(0, 0, 1.8, 0, Math.PI * 2);
    ctx.arc(-4, 4, 1.8, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.restore();
}

function drawBee(b) {
  ctx.save();
  ctx.translate(b.x, b.y);

  // wing flutter
  const wing = Math.sin(b.phase) * 6;

  // body
  ctx.globalAlpha = 0.85;
  ctx.beginPath();
  ctx.ellipse(0, 0, b.size * 0.9, b.size * 0.6, 0, 0, Math.PI * 2);
  ctx.fill();

  // stripes
  ctx.globalAlpha = 0.35;
  for (let i = -2; i <= 2; i++) {
    ctx.fillRect(i * 4, -b.size * 0.55, 2, b.size * 1.1);
  }

  // wings
  ctx.globalAlpha = 0.28;
  ctx.beginPath();
  ctx.ellipse(-b.size * 0.3, -b.size * 0.8, b.size * 0.45, b.size * 0.25, wing * 0.02, 0, Math.PI * 2);
  ctx.ellipse(b.size * 0.2, -b.size * 0.8, b.size * 0.45, b.size * 0.25, -wing * 0.02, 0, Math.PI * 2);
  ctx.fill();

  // tiny “action” indicator
  ctx.globalAlpha = 0.9;
  ctx.font = "12px system-ui, -apple-system, Segoe UI, Roboto, Arial";
  if (b.mode === "cook") ctx.fillText("🍕🔥", b.size * 0.9, -b.size * 0.9);
  if (b.mode === "eat") ctx.fillText("😋🍕", b.size * 0.9, -b.size * 0.9);

  ctx.restore();
}

onMounted(() => {
  state.reducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches ?? false;

  resize();
  window.addEventListener("resize", resize, { passive: true });

  rafId = requestAnimationFrame(step);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resize);
  if (rafId) cancelAnimationFrame(rafId);
});
</script>

<style scoped>
.bee-bg {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  pointer-events: none;
}
</style>
