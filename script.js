const targetDate = new Date("2026-09-11T19:00:00+03:00").getTime();

const guests = {
  mama: "Дорогая мамочка",
  "ekaterina-vladimir-varvara": "Екатерина, Владимир и Варвара",
  "artem-inna-lyubov": "Артём, Инна и Любовь",
  "mama-svetlana-dmitriy": "Мама Светлана и Дмитрий",
  "babushka-galina": "Бабушка Галина",
  "sergey-oksana-anastasia-alisa": "Сергей, Оксана, Анастасия и Алиса",
  "vladimir-anastasia": "Владимир и Анастасия",
  andrey: "Андрей",
  arnold: "Арнольд",
  vladislav: "Владислав",
  nikita: "Никита",
  "arina-maria": "Арина и Мария",
  anna: "Анна",
  alina: "Алина",
  elizaveta: "Елизавета",
  "polina-maxim": "Полина и Максим",
  nigina: "Нигина",
};

const params = new URLSearchParams(window.location.search);
const guestKey = params.get("guest") || params.get("to");
const guestGreeting = document.querySelector("[data-guest-greeting]");

if (guestGreeting && guestKey && guests[guestKey]) {
  guestGreeting.textContent = `${guests[guestKey]}!`;
  guestGreeting.hidden = false;
}

const countdown = {
  days: document.querySelector("[data-days]"),
  hours: document.querySelector("[data-hours]"),
  minutes: document.querySelector("[data-minutes]"),
  seconds: document.querySelector("[data-seconds]"),
};

function pad(value) {
  return String(value).padStart(2, "0");
}

function updateCountdown() {
  if (!countdown.days) return;

  const distance = Math.max(0, targetDate - Date.now());
  const day = 24 * 60 * 60 * 1000;
  const hour = 60 * 60 * 1000;
  const minute = 60 * 1000;

  countdown.days.textContent = pad(Math.floor(distance / day));
  countdown.hours.textContent = pad(Math.floor((distance % day) / hour));
  countdown.minutes.textContent = pad(Math.floor((distance % hour) / minute));
  countdown.seconds.textContent = pad(Math.floor((distance % minute) / 1000));
}

updateCountdown();
window.setInterval(updateCountdown, 1000);

const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 },
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}
