(() => {
  const startEffects = () => {
  const isMobile = window.matchMedia("(max-width: 560px)").matches;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const field = document.createElement("div");
  const count = reduceMotion ? 0 : isMobile ? 96 : 180;
  let seed = 0x7f4a7c15;

  const random = () => {
    seed += 0x6d2b79f5;
    let value = seed;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };

  field.className = "star-field";
  field.setAttribute("aria-hidden", "true");

  for (let index = 0; index < count; index += 1) {
    const star = document.createElement("i");
    const size = index % 19 === 0
      ? 13 + random() * 9
      : 2.3 + random() * 8.2;
    const duration = 4.8 + random() * 8.4;
    const classes = ["screen-star"];

    if (index % 3 === 0 || index % 7 === 0) classes.push("is-white");
    if (index % 5 === 0) classes.push("is-cross");

    star.className = classes.join(" ");
    star.style.cssText = [
      `--x:${(random() * 100).toFixed(2)}%`,
      `--y:${(random() * 100).toFixed(2)}%`,
      `--size:${size.toFixed(1)}px`,
      `--opacity:${(.24 + random() * .7).toFixed(2)}`,
      `--duration:${duration.toFixed(2)}s`,
      `--delay:${(-random() * duration).toFixed(2)}s`,
      `--dx:${(-54 + random() * 108).toFixed(1)}px`,
      `--dy:${(-66 + random() * 132).toFixed(1)}px`,
      `--dx2:${(-62 + random() * 124).toFixed(1)}px`,
      `--dy2:${(-74 + random() * 148).toFixed(1)}px`,
    ].join(";");
    field.append(star);
  }

  if (count > 0) document.body.prepend(field);

  const glass = document.querySelector(".hero-art");

  if (glass && !reduceMotion) {
    const overlay = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    overlay.classList.add("glass-edge-overlay");
    overlay.setAttribute("viewBox", "0 0 1254 1254");
    overlay.setAttribute("aria-hidden", "true");
    overlay.innerHTML = `
      <defs>
        <linearGradient id="glass-edge-sheen" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#fff" stop-opacity=".35"/>
          <stop offset=".23" stop-color="#fff" stop-opacity="1"/>
          <stop offset=".45" stop-color="#ffd3e7" stop-opacity=".8"/>
          <stop offset=".7" stop-color="#fff" stop-opacity="1"/>
          <stop offset="1" stop-color="#f59bc5" stop-opacity=".35"/>
        </linearGradient>
      </defs>
      <path class="glass-edge-line" d="M229 491 L644 976 Q674 1002 706 977 L1111 491"/>
      <path class="glass-edge-line is-inner" d="M294 536 L651 950 Q675 971 699 952 L1045 536"/>
      <path class="glass-edge-line is-rim" d="M231 491 Q370 519 505 501 M835 502 Q978 519 1110 491"/>
      <path class="glass-edge-line is-stem" d="M644 983 L642 1108 M705 981 L708 1108"/>
      <ellipse class="glass-edge-line is-base" cx="676" cy="1129" rx="225" ry="33"/>
      <path class="glass-edge-glint" style="--edge-delay:-.5s" d="M0-20 L6-6 L20 0 L6 6 L0 20 L-6 6 L-20 0 L-6-6Z" transform="translate(355 641)"/>
      <path class="glass-edge-glint is-soft" style="--edge-delay:-2.1s" d="M0-18 L5-5 L18 0 L5 5 L0 18 L-5 5 L-18 0 L-5-5Z" transform="translate(981 643)"/>
      <path class="glass-edge-glint" style="--edge-delay:-1.35s" d="M0-16 L5-5 L16 0 L5 5 L0 16 L-5 5 L-16 0 L-5-5Z" transform="translate(675 975)"/>
      <path class="glass-edge-glint is-soft" style="--edge-delay:-3.2s" d="M0-15 L4-4 L15 0 L4 4 L0 15 L-4 4 L-15 0 L-4-4Z" transform="translate(522 1128)"/>
      <path class="glass-edge-glint" style="--edge-delay:-2.65s" d="M0-14 L4-4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4-4Z" transform="translate(827 1129)"/>
    `;
    glass.append(overlay);
  }
  };

  const scheduleEffects = () => {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(startEffects, { timeout: 1200 });
    } else {
      window.setTimeout(startEffects, 180);
    }
  };

  if (document.readyState === "complete") {
    scheduleEffects();
  } else {
    window.addEventListener("load", scheduleEffects, { once: true });
  }
})();
