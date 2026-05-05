import { motion } from 'framer-motion'

export default function Card({ children, className = '', ...props }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className={`glass p-6 rounded-2xl ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  )
}
