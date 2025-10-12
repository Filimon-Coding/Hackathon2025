#  Self-Healing Swarm AI Cooling System – Web Simulation

Dette prosjektet er en **interaktiv nettside** som simulerer et selvhelbredende AI-basert kjølesystem for datasentre.  
Nettsiden viser hvordan flere smarte agenter samarbeider for å stabilisere temperaturen når en feil oppstår.

---

##  Funksjoner

- Dynamisk **simulering** av AI-agenter som reagerer på varme og feil  
- **Start**- og **Reset**-knapper for å kontrollere simuleringen  
- Visuell fremstilling av hvordan svermen balanserer varme og energi  
- Responsivt og moderne brukergrensesnitt med Tailwind CSS  
- Bygget for rask lasting og enkel utvidelse  

---

##  Teknologistack

| Teknologi | Bruksområde |
|------------|-------------|
| **React + TypeScript** | Frontend og logikk |
| **Vite** | Rask utviklingsserver og byggverktøy |
| **Tailwind CSS** | Styling og layout |
| **shadcn/ui** | Ferdige UI-komponenter |
| **React Router DOM** | Navigasjon mellom sider |
| **React Query** | Tilstandshåndtering og datalagring |

---

##  Prosjektstruktur

```
src/
 ├── components/        # Gjenbrukbare UI-komponenter
 ├── hooks/             # Egendefinerte React-hooks
 ├── lib/               # Hjelpefunksjoner og utils
 ├── pages/             # Hovedsider (Index, Presentation, NotFound)
 ├── App.tsx            # Ruter og hovedstruktur
 ├── main.tsx           # Inngangspunkt for React
 └── index.css          # Globale stiler
```

---

##  Installasjon og kjøring lokalt

###  Klon repoet
```bash
git clone <repo-url>
cd dual-play-sim
```

###  Installer avhengigheter
```bash
npm install
```

###  Start utviklingsserver
```bash
npm run dev
```

Deretter åpner du:
```
http://localhost:5173
```

---

## Hvordan det fungerer

Når du trykker **Start**, aktiveres en simulert sverm av AI-agenter.  
De oppdager endringer i varme, samarbeider om kjøling og balanserer temperaturen i sanntid.  
**Reset** stopper simuleringen og nullstiller systemet.

---

## 🧰 Tilpasning

- Logo og tittel kan endres i `public/index.html`  
- Farger og tema styres via `tailwind.config.ts`  
- Nye sider kan legges til i `src/pages/` og registreres i `App.tsx`  

---

##  Bygg for produksjon
```bash
npm run build
```
Ferdige filer legges i mappen `/dist` og kan distribueres hvor som helst.

---


---

##  Lisens
Dette prosjektet er utviklet for hackathon-bruk og er åpent for videreutvikling.  
Fri bruk for læring, demonstrasjon og forskning.

---

© 2025 Self-Healing Swarm AI Cooling System Team