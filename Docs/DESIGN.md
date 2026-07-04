---
name: Crave AI
colors:
  surface: '#121222'
  surface-dim: '#121222'
  surface-bright: '#38374a'
  surface-container-lowest: '#0c0c1d'
  surface-container-low: '#1a1a2b'
  surface-container: '#1e1e2f'
  surface-container-high: '#29283a'
  surface-container-highest: '#333345'
  on-surface: '#e3e0f8'
  on-surface-variant: '#e4bebc'
  inverse-surface: '#e3e0f8'
  inverse-on-surface: '#2f2f40'
  outline: '#ab8987'
  outline-variant: '#5b403f'
  surface-tint: '#ffb3b1'
  primary: '#ffb3b1'
  on-primary: '#680011'
  primary-container: '#ff535a'
  on-primary-container: '#5b000e'
  inverse-primary: '#bb162c'
  secondary: '#c0c1ff'
  on-secondary: '#1000a9'
  secondary-container: '#3131c0'
  on-secondary-container: '#b0b2ff'
  tertiary: '#f9bd22'
  on-tertiary: '#402d00'
  tertiary-container: '#b88900'
  on-tertiary-container: '#372700'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#e1e0ff'
  secondary-fixed-dim: '#c0c1ff'
  on-secondary-fixed: '#07006c'
  on-secondary-fixed-variant: '#2f2ebe'
  tertiary-fixed: '#ffdf9f'
  tertiary-fixed-dim: '#f9bd22'
  on-tertiary-fixed: '#261a00'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#121222'
  on-background: '#e3e0f8'
  surface-variant: '#333345'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Outfit
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Outfit
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 64px
  container-max: 1280px
---

## Brand & Style

The design system is engineered for an elite, AI-driven gastronomic experience. It blends the high-energy utility of modern food tech with the sophisticated aesthetics of premium hardware interfaces. The brand personality is intelligent, exclusive, and forward-looking.

The design style is **Modern Glassmorphism**. It relies on depth created through semi-transparent surfaces, deep background blurs, and luminous accents. High-fidelity textures are achieved through razor-thin borders and subtle glow effects, evoking a "glass-cockpit" feel for a high-end concierge service.

## Colors

The palette is anchored in a cinematic "Deep Night" spectrum.
- **Primary (Zomato Red):** Reserved for high-intent actions, critical brand moments, and live statuses.
- **Secondary (Indigo Glow):** Used for AI-related accents and shimmering gradients, differentiating machine-learning features from standard interactions.
- **Backgrounds:** Utilize a vertical linear gradient from `#0A0A1A` to `#12122A`. 
- **Typography:** Pure White (`#FFFFFF`) for primary content; Muted Silver (`#94A3B8`) for secondary metadata and descriptions.
- **AI Accents:** Utilize a "Sparkle Gradient" (Primary Red to Secondary Indigo) for ranking badges and AI-generated insight panels.

## Typography

The typography strategy pairs a technical, geometric display face with a soft, approachable body face. 
- **Space Grotesk** handles all headings. Its wide stance and "tech-forward" terminals reinforce the AI-driven nature of the app.
- **Outfit** is used for body text and labels. Its high legibility and circular forms provide a premium, balanced feel that contrasts well with the sharp headers.
- Use `headline-lg-mobile` for all top-level screen titles on devices narrower than 768px to ensure readability without crowding the glass containers.

## Layout & Spacing

The layout follows a strict 8px rhythmic grid to maintain architectural precision.
- **Mobile:** Single column layout with 20px side margins. Elements use full-width glass containers with internal padding of 16px or 24px.
- **Desktop:** 12-column fluid grid. Restaurant cards typically span 4 columns (3-up display). 
- **AI Recommendation Engine:** Featured AI-curated content should break the grid occasionally with slightly larger margins or offset positioning to draw the eye.
- **Transitions:** Use staggered "fade-up" animations (20px vertical travel) when loading lists of restaurant cards.

## Elevation & Depth

Depth is achieved through layering rather than traditional drop shadows.
- **Level 0 (Base):** Deep Navy gradient background.
- **Level 1 (Cards):** Surface Glass (5% white/blue opacity) with a `backdrop-filter: blur(12px)`.
- **Level 2 (Active/Hover):** Increase surface opacity to 10% and add a subtle 1px inner border (`rgba(255,255,255,0.1)`).
- **AI Highlight:** Elements curated by AI feature a soft, 20px outer glow using the primary red at 15% opacity to simulate a "breathing" light effect.

## Shapes

The design uses a modern "Rounded" language.
- **Cards & Containers:** 16px (`rounded-lg`) is the standard for restaurant and insight cards.
- **Action Buttons & Chips:** 100px (`pill-shaped`) for cuisine tags, budget toggles, and primary CTAs to create a friendly, tactile feel.
- **Borders:** Always use 1px width. Borders on glass elements should be semi-transparent to allow background colors to bleed through slightly at the edges.

## Components

- **Buttons:** Primary buttons use a solid Zomato Red fill. Secondary buttons use a glass background with a white stroke. Hover states trigger a subtle `scale(1.02)` and increased glow intensity.
- **AI "Crave" Cards:** These cards feature a gradient border (Red to Indigo) and include the ✨ emoji in the top right. 
- **Cuisine Chips:** Pill-shaped, high-contrast labels. When active, they glow with a subtle primary-color shadow.
- **Input Fields:** Search bars are ultra-minimal glass containers with "Search for a craving..." in muted silver text.
- **Rank Badges:** Circular or pill-shaped badges with a vibrant gradient background and bold white typography to denote restaurant ranking (e.g., "#1 in Sushi").
- **List Items:** Use generous vertical padding (16px+) and separators made of 1px lines with a 10% white opacity.