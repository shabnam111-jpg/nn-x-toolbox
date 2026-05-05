import { motion } from 'framer-motion'

export default function GraphContainer({ title, children }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass p-6 rounded-2xl"
    >
      <h3 className="text-lg font-semibold mb-4 gradient-text">{title}</h3>
      {children}
    </motion.div>
  )
}
