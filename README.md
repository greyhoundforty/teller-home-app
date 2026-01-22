# Teller Home App

A beautiful, full-featured financial management application that securely connects to your bank accounts via Teller Connect, providing real-time balance tracking, transaction history, bill payment scheduling, and weekly financial forecasts.

## 🚀 Quick Start

```bash
# Start the application
mise run dev

# Open Teller Connect to link your bank
open http://localhost:5001/static/teller-connect.html
```

## ✨ Features

### Core Functionality
- 🏦 **Teller Connect Integration** - Securely connect multiple bank accounts
- 💰 **Real-time Balance Tracking** - View current balances across all accounts
- 📊 **Transaction History** - Automatic sync and categorization
- 📅 **Bill Payment Calendar** - Schedule and track recurring payments
- 📈 **Weekly Financial Forecast** - Projected balances based on upcoming bills
- 🔄 **Automatic Sync** - Twice-daily data updates from Teller
- 📱 **Beautiful UI** - Responsive, modern design

### Technical Features
- ✅ Complete REST API with 11+ endpoints
- ✅ Dual database support (PostgreSQL/SQLite)
- ✅ Docker containerization
- ✅ Mock data for development
- ✅ Comprehensive test coverage
- ✅ Production-ready deployment

## 🏗️ Tech Stack

- **Backend**: Python 3.12, Flask 3.0.0
- **Database**: PostgreSQL 15 (production) / SQLite (development)
- **API**: Teller Connect (Financial Data)
- **ORM**: SQLAlchemy 2.0.23
- **Task Runner**: Mise
- **Containerization**: Docker & Docker Compose
- **Visualization**: Plotly 5.18.0, Dash 2.14.2
- **Scheduling**: APScheduler 3.10.4
- **WSGI Server**: Gunicorn 21.2.0

## Design Thinking

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Agents are capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
