# Neural Network Toolbox - Web UI

A premium, industry-level React + Vite web interface for the Neural Network Toolbox platform.

## Features

✨ **Premium Design**
- Glassmorphism effects with gradient borders
- Dark/Light theme toggle
- Smooth animations with Framer Motion
- Responsive design (mobile, tablet, desktop)

🎨 **Component Library**
- Reusable UI components (Button, Card, Navbar, Sidebar)
- Interactive graphs and charts (Recharts)
- Gradient text and borders
- Micro-interactions on hover

📊 **Pages**
- **Landing**: Hero section, features, CTA
- **Dashboard**: Overview with charts and stats
- **Perceptron**: Model training and visualization
- **MLP**: Multi-layer perceptron configuration
- **Visualizations**: Advanced analytics and metrics
- **OpenCV**: Object detection interface

🚀 **Tech Stack**
- React 18
- Vite (fast build tool)
- Tailwind CSS (utility-first styling)
- Framer Motion (animations)
- Recharts (data visualization)
- React Router (navigation)
- Zustand (state management)
- React Icons (icon library)

## Installation

### Prerequisites
- Node.js (v16+)
- npm or yarn

### Steps

1. Navigate to the project directory:
```bash
cd nn_toolbox_web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and go to:
```
http://localhost:5173
```

## Project Structure

```
nn_toolbox_web/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page components
│   ├── store/           # Zustand state management
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Utility functions
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS config
├── postcss.config.js    # PostCSS config
└── package.json         # Dependencies
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Customization

### Colors
Edit `tailwind.config.js` to modify the color palette.

### Typography
Fonts are configured in `index.html` (Inter via Google Fonts).

### Animations
Framer Motion animations are in component files. Adjust `initial`, `animate`, and `whilehover` props.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

MIT - Feel free to use this UI for your projects!

## Credits

Built with React, Framer Motion, Tailwind CSS, and passion for AI education.
