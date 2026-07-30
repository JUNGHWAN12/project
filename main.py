import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Focus Timer",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit is used only as the host. The timer itself runs in the browser so it
# remains smooth without rerunning the Python script every second.
st.markdown(
    """
    <style>
        #MainMenu, footer, header { visibility: hidden; }
        .stApp { background: #0b0d12; }
        .block-container { max-width: 1180px; padding: 1.25rem 1rem 0; }
        iframe { border: 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(
    r"""
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    * { box-sizing: border-box; }
    :root {
      --bg: #0b0d12;
      --panel: rgba(23, 26, 34, .86);
      --line: rgba(255, 255, 255, .09);
      --text: #f7f8fa;
      --muted: #8d93a1;
      --accent: #b8f34a;
      --accent-dark: #18220a;
      --danger: #ff6b6b;
    }
    html, body { margin: 0; min-height: 100%; background: var(--bg); color: var(--text); }
    body {
      font-family: Inter, Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    button, input { font: inherit; }
    button { -webkit-tap-highlight-color: transparent; }
    .app { width: min(100%, 1100px); margin: 0 auto; padding: 10px 8px 30px; }
    header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
    .brand { display: flex; gap: 10px; align-items: center; font-size: 15px; font-weight: 750; letter-spacing: -.02em; }
    .brand-mark { width: 27px; height: 27px; display: grid; place-items: center; border-radius: 8px; background: var(--accent); color: #111; }
    .status { display: flex; gap: 7px; align-items: center; color: var(--muted); font-size: 12px; }
    .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #59606e; transition: .2s; }
    .status-dot.on { background: var(--accent); box-shadow: 0 0 12px rgba(184,243,74,.65); }
    .panel {
      position: relative; overflow: hidden; border: 1px solid var(--line); border-radius: 26px;
      background: var(--panel); box-shadow: 0 30px 80px rgba(0,0,0,.28); padding: clamp(22px, 5vw, 54px);
    }
    .panel::before {
      content: ""; position: absolute; width: 280px; height: 280px; right: -140px; top: -160px;
      border-radius: 50%; background: rgba(184,243,74,.08); filter: blur(8px); pointer-events: none;
    }
    .tabs { display: inline-flex; padding: 4px; gap: 3px; border: 1px solid var(--line); border-radius: 12px; background: rgba(0,0,0,.18); }
    .tab { border: 0; border-radius: 8px; background: transparent; color: var(--muted); padding: 8px 14px; cursor: pointer; font-size: 13px; font-weight: 650; }
    .tab.active { background: #2a2e38; color: var(--text); }
    .timer-wrap { text-align: center; padding: clamp(30px, 6vw, 62px) 0 clamp(26px, 5vw, 48px); }
    .eyebrow { color: var(--muted); text-transform: uppercase; letter-spacing: .16em; font-weight: 700; font-size: 11px; margin-bottom: 10px; }
    .time {
      font-variant-numeric: tabular-nums; font-size: clamp(66px, 14vw, 154px); font-weight: 760;
      letter-spacing: -.075em; line-height: .95; white-space: nowrap; margin-left: -.07em;
    }
    .milliseconds { display: inline-block; width: 1.9em; color: var(--muted); font-size: .32em; letter-spacing: -.04em; text-align: left; margin-left: .12em; }
    .progress { height: 3px; max-width: 610px; margin: 25px auto 0; border-radius: 4px; overflow: hidden; background: #2b2e36; }
    .progress-bar { width: 0; height: 100%; background: var(--accent); transition: width .15s linear; }
    .controls { display: flex; justify-content: center; align-items: center; gap: 10px; }
    .control { border: 1px solid var(--line); color: var(--text); background: #23262e; height: 52px; padding: 0 20px; border-radius: 15px; font-weight: 720; cursor: pointer; transition: transform .15s, background .15s; }
    .control:hover { background: #2c3039; }
    .control:active { transform: scale(.97); }
    .control.primary { min-width: 132px; border-color: var(--accent); background: var(--accent); color: #11150b; }
    .control.primary:hover { background: #c6ff58; }
    .control.icon { width: 52px; padding: 0; font-size: 19px; }
    .settings { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 22px; margin-top: 40px; padding-top: 22px; border-top: 1px solid var(--line); }
    .setting-label { color: var(--muted); font-size: 11px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 9px; }
    .presets { display: flex; flex-wrap: wrap; gap: 7px; }
    .preset { border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; color: #c9ccd3; background: transparent; font-size: 12px; cursor: pointer; }
    .preset:hover, .preset.active { color: var(--accent); border-color: rgba(184,243,74,.45); background: rgba(184,243,74,.06); }
    .custom { display: flex; align-items: center; gap: 7px; }
    .custom input { width: 74px; height: 34px; border: 1px solid var(--line); border-radius: 9px; outline: 0; background: #101218; color: var(--text); text-align: center; }
    .custom input:focus { border-color: rgba(184,243,74,.65); }
    .custom span { color: var(--muted); font-size: 12px; }
    .hint { margin-top: 13px; color: #656b78; font-size: 11px; text-align: center; }
    @media (max-width: 640px) {
      .app { padding: 5px 2px 24px; }
      header { margin: 0 8px 13px; }
      .panel { border-radius: 20px; padding: 19px 15px 23px; }
      .timer-wrap { padding: 42px 0 35px; }
      .time { font-size: clamp(58px, 20vw, 92px); }
      .milliseconds { display: block; width: auto; text-align: center; margin: 12px 0 0; font-size: 16px; letter-spacing: .04em; }
      .settings { grid-template-columns: 1fr; align-items: start; gap: 20px; margin-top: 34px; }
      .custom input { width: 68px; }
      .control { height: 49px; padding: 0 16px; }
      .control.primary { min-width: 120px; }
      .hint { display: none; }
    }
  </style>
</head>
<body>
  <main class="app">
    <header>
      <div class="brand"><span class="brand-mark">◷</span> Focus Timer</div>
      <div class="status"><span id="statusDot" class="status-dot"></span><span id="statusText">준비됨</span></div>
    </header>
    <section class="panel">
      <div class="tabs" role="tablist" aria-label="타이머 모드">
        <button class="tab active" data-mode="timer" role="tab">타이머</button>
        <button class="tab" data-mode="stopwatch" role="tab">스톱워치</button>
      </div>
      <div class="timer-wrap" aria-live="polite">
        <div id="eyebrow" class="eyebrow">Focus session</div>
        <div class="time"><span id="clock">25:00</span><span id="ms" class="milliseconds">.00</span></div>
        <div class="progress"><div id="progress" class="progress-bar"></div></div>
      </div>
      <div class="controls">
        <button id="reset" class="control icon" aria-label="초기화" title="초기화">↺</button>
        <button id="toggle" class="control primary">시작</button>
        <button id="add" class="control" title="1분 추가">+ 1분</button>
      </div>
      <div id="settings" class="settings">
        <div>
          <div class="setting-label">빠른 설정</div>
          <div class="presets">
            <button class="preset" data-min="5">5분</button>
            <button class="preset" data-min="10">10분</button>
            <button class="preset active" data-min="25">25분</button>
            <button class="preset" data-min="45">45분</button>
            <button class="preset" data-min="60">60분</button>
          </div>
        </div>
        <div>
          <div class="setting-label">직접 입력</div>
          <div class="custom"><input id="customMin" type="number" min="1" max="999" value="25" aria-label="분 입력"/><span>분</span></div>
        </div>
      </div>
      <div class="hint">Space 시작·일시정지 &nbsp; R 초기화</div>
    </section>
  </main>
  <script>
    const el = id => document.getElementById(id);
    const clock = el('clock'), ms = el('ms'), toggle = el('toggle'), reset = el('reset'), add = el('add');
    const progress = el('progress'), statusText = el('statusText'), statusDot = el('statusDot');
    const settings = el('settings'), customMin = el('customMin'), eyebrow = el('eyebrow');
    let mode = 'timer', duration = 25 * 60 * 1000, elapsed = 0, running = false, startedAt = 0, frame = null;

    function currentElapsed() { return elapsed + (running ? performance.now() - startedAt : 0); }
    function visibleMs() { return mode === 'timer' ? Math.max(0, duration - currentElapsed()) : currentElapsed(); }
    function format(value) {
      const totalSeconds = Math.floor(value / 1000), minutes = Math.floor(totalSeconds / 60), seconds = totalSeconds % 60;
      return `${String(minutes).padStart(2,'0')}:${String(seconds).padStart(2,'0')}`;
    }
    function render() {
      const value = visibleMs();
      clock.textContent = format(value);
      ms.textContent = '.' + String(Math.floor((value % 1000) / 10)).padStart(2, '0');
      progress.style.width = mode === 'timer' ? `${Math.min(100, currentElapsed() / duration * 100)}%` : '0%';
      document.title = `${format(value)} · Focus Timer`;
      if (running && mode === 'timer' && value <= 0) { finish(); return; }
      if (running) frame = requestAnimationFrame(render);
    }
    function setStatus(text, on=false) { statusText.textContent = text; statusDot.classList.toggle('on', on); }
    function startPause() {
      if (running) {
        elapsed = currentElapsed(); running = false; cancelAnimationFrame(frame);
        toggle.textContent = '계속'; setStatus('일시정지');
      } else {
        if (mode === 'timer' && elapsed >= duration) elapsed = 0;
        startedAt = performance.now(); running = true; toggle.textContent = '일시정지'; setStatus('집중 중', true); render();
      }
    }
    function finish() {
      elapsed = duration; running = false; cancelAnimationFrame(frame); toggle.textContent = '다시 시작'; setStatus('완료'); render();
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        [0, .18].forEach(delay => { const osc=ctx.createOscillator(), gain=ctx.createGain(); osc.connect(gain); gain.connect(ctx.destination); osc.frequency.value=740; gain.gain.setValueAtTime(.12,ctx.currentTime+delay); gain.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+delay+.14); osc.start(ctx.currentTime+delay); osc.stop(ctx.currentTime+delay+.15); });
      } catch (_) {}
    }
    function resetTimer() { running=false; cancelAnimationFrame(frame); elapsed=0; toggle.textContent='시작'; setStatus('준비됨'); render(); }
    function setDuration(minutes) {
      const safe = Math.max(1, Math.min(999, Number(minutes) || 1)); duration=safe*60000; customMin.value=safe; resetTimer();
      document.querySelectorAll('.preset').forEach(p => p.classList.toggle('active', Number(p.dataset.min)===safe));
    }
    function setMode(next) {
      mode=next; resetTimer();
      document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.mode===mode));
      settings.style.display = mode==='timer' ? '' : 'none'; add.style.display = mode==='timer' ? '' : 'none';
      eyebrow.textContent = mode==='timer' ? 'Focus session' : 'Elapsed time'; render();
    }
    toggle.addEventListener('click', startPause);
    reset.addEventListener('click', resetTimer);
    add.addEventListener('click', () => { duration += 60000; customMin.value=Math.round(duration/60000); render(); });
    customMin.addEventListener('change', () => setDuration(customMin.value));
    document.querySelectorAll('.preset').forEach(p => p.addEventListener('click', () => setDuration(p.dataset.min)));
    document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => setMode(t.dataset.mode)));
    document.addEventListener('keydown', e => {
      if (e.target.tagName==='INPUT') return;
      if (e.code==='Space') { e.preventDefault(); startPause(); }
      if (e.key.toLowerCase()==='r') resetTimer();
    });
    render();
  </script>
</body>
</html>
    """,
    height=760,
    scrolling=False,
)
