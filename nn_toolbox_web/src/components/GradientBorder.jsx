import { motion } from 'framer-motion'

export default function GradientBorder({ children, className = '' }) {
  return (
    <motion.div
      className={`gradient-border relative ${className}`}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      {children}
    </motion.div>
  )
}
