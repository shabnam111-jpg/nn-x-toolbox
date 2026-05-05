import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { FiHome, FiZap, FiLayers, FiEye, FiCamera, FiSettings, FiX } from 'react-icons/fi'
import { useAppStore } from '../store/appStore'

const menuItems = [
  { label: 'Home', path: '/dashboard', icon: FiHome },
  { label: 'Perceptron', path: '/perceptron', icon: FiZap },
  { label: 'MLP', path: '/mlp', icon: FiLayers },
  { label: 'Visualizations', path: '/visualizations', icon: FiEye },
  { label: 'OpenCV', path: '/opencv', icon: FiCamera },
  { label: 'Settings', path: '#', icon: FiSettings }
]

export default function Sidebar() {
  const location = useLocation()
  const { sidebarOpen, setSidebarOpen } = useAppStore()

  return (
    <>
      {/* Mobile Overlay */}
      {sidebarOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: sidebarOpen ? 0 : -300 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        className="fixed left-0 top-16 w-64 h-[calc(100vh-4rem)] glass p-4 overflow-y-auto md:static md:translate-x-0 z-40"
      >
        <div className="flex justify-between items-center mb-6 md:hidden">
          <h3 className="text-lg font-bold gradient-text">Menu</h3>
          <button onClick={() => setSidebarOpen(false)}>
            <FiX size={24} />
          </button>
        </div>

        <nav className="space-y-2">
          {menuItems.map(({ label, path, icon: Icon }) => (
            <Link key={path} to={path} onClick={() => setSidebarOpen(false)}>
              <motion.div
                whileHover={{ x: 4 }}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  location.pathname === path
                    ? 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-500/50 text-cyan-300'
                    : 'text-slate-300 hover:bg-white/10'
                }`}
              >
                <Icon size={18} />
                <span className="font-medium">{label}</span>
              </motion.div>
            </Link>
          ))}
        </nav>

        {/* Footer Branding */}
        <div className="mt-8 pt-8 border-t border-slate-700/50">
          <p className="text-xs text-slate-500">
            Neural Network Toolbox v1.0
          </p>
          <p className="text-xs text-slate-600 mt-2">
            Powered by React + Framer Motion
          </p>
        </div>
      </motion.aside>
    </>
  )
}
