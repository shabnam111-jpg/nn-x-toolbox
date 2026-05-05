import { useEffect, useRef, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiMoon, FiSun, FiMenu, FiChevronRight, FiArrowLeft } from 'react-icons/fi'
import { useThemeStore } from '../store/themeStore'
import { useAppStore } from '../store/appStore'

const featureLinks = [
  { label: 'Home', path: '/' },
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Perceptron', path: '/perceptron' },
  { label: 'MLP', path: '/mlp' },
  { label: 'Visualizations', path: '/visualizations' },
  { label: 'OpenCV', path: '/opencv' }
]

export default function Navbar() {
  const location = useLocation()
  const { isDark, toggleTheme } = useThemeStore()
  const { toggleSidebar } = useAppStore()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    setMenuOpen(false)
  }, [location.pathname])

  useEffect(() => {
    const onClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', onClickOutside)
    return () => document.removeEventListener('mousedown', onClickOutside)
  }, [])

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="glass sticky top-0 z-50 px-6 py-4 flex justify-between items-center relative"
    >
      <Link to="/" className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold">NN</span>
        </div>
        <span className="gradient-text font-bold text-xl hidden sm:block">Neural Toolbox</span>
      </Link>

      <div className="flex items-center gap-4">
        {location.pathname !== '/' && (
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.history.back()}
            className="p-2 border border-slate-500 hover:bg-white/10 rounded-lg transition flex items-center gap-2"
            title="Go back"
          >
            <FiArrowLeft size={20} />
          </motion.button>
        )}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleTheme}
          className="p-2 hover:bg-white/10 rounded-lg transition"
        >
          {isDark ? <FiSun size={20} /> : <FiMoon size={20} />}
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setMenuOpen((prev) => !prev)}
          className="p-2 hover:bg-white/10 rounded-lg transition"
          aria-label="Open feature menu"
        >
          <FiMenu size={20} />
        </motion.button>
      </div>

      {menuOpen && (
        <motion.div
          ref={menuRef}
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute right-6 top-16 w-64 glass border border-slate-700/40 rounded-xl p-3 shadow-2xl"
        >
          <p className="text-xs uppercase tracking-wide text-slate-400 px-2 py-1">Features</p>

          <div className="mt-1 space-y-1">
            {featureLinks.map((item) => {
              const isActive = location.pathname === item.path

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center justify-between px-3 py-2 rounded-lg transition ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-cyan-300'
                      : 'text-slate-200 hover:bg-white/10'
                  }`}
                >
                  <span>{item.label}</span>
                  <FiChevronRight size={14} />
                </Link>
              )
            })}
          </div>

          <button
            onClick={toggleSidebar}
            className="mt-3 w-full text-left px-3 py-2 rounded-lg text-slate-300 hover:bg-white/10 transition"
            type="button"
          >
            Toggle Side Panel
          </button>
        </motion.div>
      )}
    </motion.nav>
  )
}
