import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useThemeStore } from './store/themeStore'
import Landing from './pages/Landing'
import Hero from './pages/Hero'
import Dashboard from './pages/Dashboard'
import Perceptron from './pages/Perceptron'
import MLP from './pages/MLP'
import Visualizations from './pages/Visualizations'
import OpenCV from './pages/OpenCV'
import { useEffect } from 'react'

export default function App() {
  const { isDark, toggleTheme } = useThemeStore()

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDark])

  return (
    <BrowserRouter basename="/Neural-Network-Toolbox/">
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/hero" element={<Hero />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/perceptron" element={<Perceptron />} />
        <Route path="/mlp" element={<MLP />} />
        <Route path="/visualizations" element={<Visualizations />} />
        <Route path="/opencv" element={<OpenCV />} />
        <Route path="*" element={<Landing />} />
      </Routes>
    </BrowserRouter>
  )
}
