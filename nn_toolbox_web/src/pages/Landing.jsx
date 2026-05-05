import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { FiArrowRight, FiExternalLink } from 'react-icons/fi'
import { FaGithub } from 'react-icons/fa'
import Button from '../components/Button'
import Card from '../components/Card'
import Navbar from '../components/Navbar'
import PixelBlast from '../components/PixelBlast'

const features = [
  {
    title: 'Perceptron Training',
    description: 'Build and train perceptrons from scratch with interactive controls.',
    icon: '⚡'
  },
  {
    title: 'MLP Playground',
    description: 'Experiment with multi-layer networks and visualize decision boundaries.',
    icon: '🧠'
  },
  {
    title: 'Propagation Visualizer',
    description: 'Understand forward and backpropagation step-by-step.',
    icon: '🔄'
  },
  {
    title: 'OpenCV Detection',
    description: 'Real-time computer vision with face and object detection.',
    icon: '👁️'
  }
]

export default function Landing() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.3 }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white overflow-x-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div style={{ width: '100%', height: '100dvh', position: 'relative', opacity: 0.75 }}>
          <PixelBlast
            variant="square"
            pixelSize={1}
            color="#B19EEF"
            patternScale={2}
            patternDensity={1}
            pixelSizeJitter={0.75}
            enableRipples
            rippleSpeed={0.4}
            rippleThickness={0.12}
            rippleIntensityScale={1.5}
            liquid={false}
            liquidStrength={0.12}
            liquidRadius={1.2}
            liquidWobbleSpeed={5}
            speed={2.75}
            edgeFade={0.25}
            transparent
          />
        </div>
        <div className="absolute top-20 left-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Navbar />

        {/* Hero Section */}
        <motion.section
          className="max-w-6xl mx-auto px-6 py-20 text-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <h1 className="text-5xl md:text-7xl font-bold mb-6 gradient-text leading-tight">
              Neural Network Toolbox
            </h1>
          </motion.div>

          <motion.div variants={itemVariants}>
            <p className="text-xl md:text-2xl text-slate-300 mb-8 max-w-2xl mx-auto">
              Learn, visualize, and experiment with AI models in real-time. A powerful platform for understanding deep learning.
            </p>
          </motion.div>

          <motion.div
            variants={itemVariants}
            className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
          >
            <Link to="/dashboard">
              <Button size="lg" className="w-full sm:w-auto">
                Get Started <FiArrowRight className="inline ml-2" />
              </Button>
            </Link>
            <Button
              variant="secondary"
              size="lg"
              className="w-full sm:w-auto"
              onClick={() => window.open('http://localhost:8504', '_blank', 'noopener,noreferrer')}
            >
              Attendance vision
            </Button>
          </motion.div>
        </motion.section>

        {/* Features Section */}
        <motion.section
          className="max-w-6xl mx-auto px-6 py-20"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
        >
          <h2 className="text-4xl font-bold text-center mb-12 gradient-text">
            Powerful Features
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                variants={itemVariants}
                whileHover={{ y: -8 }}
              >
                <Card>
                  <div className="text-3xl mb-3">{feature.icon}</div>
                  <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                  <p className="text-slate-300">{feature.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* How It Works */}
        <motion.section
          className="max-w-6xl mx-auto px-6 py-20"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
        >
          <h2 className="text-4xl font-bold text-center mb-12 gradient-text">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: 1, title: 'Choose Model', desc: 'Select from various neural network architectures' },
              { step: 2, title: 'Configure Params', desc: 'Set learning rate, epochs, and layer sizes' },
              { step: 3, title: 'Train & Visualize', desc: 'Watch your model learn in real-time' }
            ].map((item, i) => (
              <motion.div
                key={i}
                variants={itemVariants}
                className="text-center"
              >
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 flex items-center justify-center mx-auto mb-4 text-2xl font-bold"
                >
                  {item.step}
                </motion.div>
                <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                <p className="text-slate-400">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* CTA Section */}
        <motion.section
          className="max-w-4xl mx-auto px-6 py-20 text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
        >
          <Card className="bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30">
            <h2 className="text-3xl font-bold mb-4">Ready to Learn?</h2>
            <p className="text-slate-300 mb-6">Start experimenting with neural networks today.</p>
            <Link to="/dashboard">
              <Button size="lg" className="mx-auto">
                Launch Dashboard
              </Button>
            </Link>
          </Card>
        </motion.section>

        {/* Footer */}
        <footer className="border-t border-slate-700/30 py-12 px-6 text-center text-slate-400">
          <div className="max-w-6xl mx-auto">
            <p className="mb-4">Built with React, Framer Motion & Tailwind CSS</p>
            <div className="flex justify-center gap-4">
              <a href="#" className="hover:text-white transition">
                <FaGithub size={20} />
              </a>
              <a href="#" className="hover:text-white transition">
                <FiExternalLink size={20} />
              </a>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
