# Design Spec: cammseb UI Redesign (Elegant Pastel Cute Luxe)

**Date**: 2026-03-26
**Topic**: UI/UX Overhaul for cammseb Beauty Center App

## 1. Goal Description
Transform the current `nicegui` application from a basic functional tool into a premium, "Elegant Pastel Cute Luxe" experience for a beauty spa. The redesign aims to blend the original lavender/purple identity with a luxurious cream/gold palette, using soft "cute" elements like rounded corners and delicate animations.

## 2. Aesthetic Direction: "Soft Elegance"
*   **Persona**: Professional, high-end, yet warm and approachable (cute).
*   **Colors**:
    *   `background`: `linear-gradient(135deg, #FFFDF5 0%, #FFF0F5 100%)` (Cream to Blush Pink)
    *   `primary`: `#E6E6FA` (Soft Lavender)
    *   `secondary`: `#FFF0F5` (Blush Pink)
    *   `accent`: `#F0E68C` (Soft Gold)
    *   `text_primary`: `#4A148C` (Muted Deep Purple)
    *   `text_secondary`: `#6B4FBB` (Lighter Purple)
*   **Typography**:
    *   Headers: `Playfair Display` (Serif) - imported from Google Fonts.
    *   Body/Labels: `Quicksand` (Rounded Sans-Serif) - imported from Google Fonts.
*   **Shapes**: `border-radius: 32px` for cards and major container elements.
*   **Effects**: Soft box-shadows (`rgba(147, 112, 219, 0.15)`), Glassmorphism for header.

## 3. Key Components & Features
### 3.1 App Structure
*   **Sticky Header**: Transparent header with a blur effect (`backdrop-filter: blur(12px)`), containing the branding "🌸 cammseb 🌸".
*   **Navigation Tabs**: Centered tabs with icons, using pastel purple for active states and soft hover animations.
*   **Enhanced Calendar**: Inclusion of a visual date picker (`ui.date`) directly in the "Citas" tab to allow a more intuitive booking experience.

### 3.2 Feature Enhancements
*   **Interactive "Bubble" Cards**: Forms for "Diagnóstico" and "Calculadora" will be contained in cards with a high border-radius and soft glows.
*   **Polished Tables**: Data tables with rounded corners, custom headers, and row-hover highlighting in soft lavender.
*   **Dialogs**: Refined edit dialogs with better margin/padding and matching aesthetic.

## 4. Architecture & Data Flow
*   **Framework**: NiceGUI (Python).
*   **Database**: SQLite (SQLAlchemy).
*   **State Management**: `state` dict for cross-tab suggestions remains.

## 5. Verification Plan
*   **Visual Regression**: Match the implementation with the approved "Elegant Pastel Cute Luxe" mockup.
*   **Responsive Flow**: Test window resizing to ensure centered tabs and bubble cards maintain visual balance.
*   **CRUD Checks**: Verify all DB operations (create, read, update) work correctly in the new UI.
