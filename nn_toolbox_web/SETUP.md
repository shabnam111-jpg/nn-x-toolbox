# Quick Setup Guide

## Step-by-Step Installation

### 1. Prerequisites Check
Ensure you have Node.js installed:
```bash
node --version  # Should be v16 or higher
npm --version
```

If not installed, download from: https://nodejs.org/

### 2. Navigate to Project
```bash
cd c:\Users\ARSH\OneDrive\Desktop\TOOLBOX\nn_toolbox_web
```

### 3. Install Dependencies
```bash
npm install
```

This will install:
- React 18
- Vite (build tool)
- Tailwind CSS
- Framer Motion
- Recharts
- React Router
- Zustand
- React Icons

### 4. Start Development Server
```bash
npm run dev
```

The app will automatically open at: `http://localhost:5173`

### 5. Start Coding
- Make changes to files in `src/`
- Hot reload is enabled (auto-refresh)
- Changes appear in browser instantly

## Project Structure Explained

### Components (`src/components/`)
- **Button.jsx** - Animated button with variants
- **Card.jsx** - Glass-morphism card component
- **Navbar.jsx** - Top navigation bar
- **Sidebar.jsx** - Side navigation (collapsible on mobile)
- **GraphContainer.jsx** - Chart wrapper
- **GradientBorder.jsx** - Gradient border effect

### Pages (`src/pages/`)
- **Landing.jsx** - Homepage with hero section
- **Dashboard.jsx** - Overview with charts
- **Perceptron.jsx** - Perceptron training UI
- **MLP.jsx** - Multi-layer perceptron UI
- **Visualizations.jsx** - Analytics dashboard
- **OpenCV.jsx** - Object detection UI

### State Management (`src/store/`)
- **themeStore.js** - Dark/light theme toggle
- **appStore.js** - Global app state

### Styling
- **index.css** - Global styles + animations
- **tailwind.config.js** - Tailwind configuration
- Custom CSS classes:
  - `.glass` - Glassmorphism effect
  - `.gradient-text` - Gradient text
  - `.gradient-border` - Gradient border

## Key Features

✅ **Fully Responsive**
- Mobile: Single column layout
- Tablet: 2-column layout with collapsible sidebar
- Desktop: Full 3-column layout

✅ **Dark Mode**
- Toggle in navbar
- Persistent (saved in localStorage)
- System preference detection

✅ **Smooth Animations**
- Page transitions
- Hover effects
- Chart animations
- Loading states

✅ **Production Ready**
- No console errors
- Clean code structure
- Reusable components
- Performance optimized

## Common Commands

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Add new package
npm install package-name
```

## Customization Examples

### Change Primary Color
Edit `tailwind.config.js`:
```js
colors: {
  primary: "#4F46E5",  // Change this
  secondary: "#06B6D4",
  // ...
}
```

### Add New Page
1. Create file: `src/pages/NewPage.jsx`
2. Add route in `App.jsx`
3. Add menu item in `Sidebar.jsx`

### Modify Animations
Edit component files (e.g., `Button.jsx`):
```jsx
<motion.button
  whileHover={{ scale: 1.05 }}  // Adjust these
  whileTap={{ scale: 0.98 }}
>
```

## Deployment

### Build for Production
```bash
npm run build
```

Creates optimized `dist/` folder.

### Deploy to Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to Netlify
Drag-and-drop `dist/` folder or use Netlify CLI.

## Troubleshooting

**Port already in use?**
```bash
npm run dev -- --port 3000
```

**Clear cache and reinstall:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Vite not starting?**
```bash
npm run dev -- --host
```

## Resources

- Vite Docs: https://vitejs.dev
- React Docs: https://react.dev
- Tailwind CSS: https://tailwindcss.com
- Framer Motion: https://www.framer.com/motion
- Recharts: https://recharts.org

## Support

For issues:
1. Check browser console (F12)
2. Verify Node version
3. Reinstall dependencies
4. Clear browser cache

Happy coding! 🚀
