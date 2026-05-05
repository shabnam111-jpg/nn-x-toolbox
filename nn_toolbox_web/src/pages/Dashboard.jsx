import { motion } from 'framer-motion'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import Card from '../components/Card'
import GraphContainer from '../components/GraphContainer'
import Button from '../components/Button'

const mockData = [
  { epoch: 1, loss: 2.3, accuracy: 0.45 },
  { epoch: 2, loss: 2.1, accuracy: 0.52 },
  { epoch: 3, loss: 1.9, accuracy: 0.58 },
  { epoch: 4, loss: 1.6, accuracy: 0.68 },
  { epoch: 5, loss: 1.3, accuracy: 0.75 },
  { epoch: 6, loss: 0.9, accuracy: 0.82 },
  { epoch: 7, loss: 0.6, accuracy: 0.88 },
  { epoch: 8, loss: 0.4, accuracy: 0.92 }
]

export default function Dashboard() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1 }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-6 md:p-8">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="max-w-7xl mx-auto"
          >
            {/* Header */}
            <motion.div variants={itemVariants} className="mb-8">
              <h1 className="text-4xl font-bold gradient-text mb-2">Dashboard</h1>
              <p className="text-slate-400">Welcome back! Here's your training overview.</p>
            </motion.div>

            {/* Stats Cards */}
            <motion.div
              variants={itemVariants}
              className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8"
            >
              {[
                { label: 'Models Trained', value: '12', change: '+2' },
                { label: 'Avg Accuracy', value: '92%', change: '+5%' },
                { label: 'Total Epochs', value: '2.5K', change: '+300' },
                { label: 'Training Time', value: '4.2h', change: '-0.5h' }
              ].map((stat, i) => (
                <motion.div
                  key={i}
                  whileHover={{ y: -4 }}
                  className="glass p-6 rounded-2xl"
                >
                  <p className="text-slate-400 text-sm font-medium mb-2">{stat.label}</p>
                  <div className="flex items-end justify-between">
                    <span className="text-3xl font-bold">{stat.value}</span>
                    <span className="text-green-400 text-sm">{stat.change}</span>
                  </div>
                </motion.div>
              ))}
            </motion.div>

            {/* Charts */}
            <motion.div
              variants={itemVariants}
              className="grid md:grid-cols-2 gap-6 mb-8"
            >
              <GraphContainer title="Training Loss">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={mockData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="epoch" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                      labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Line
                      type="monotone"
                      dataKey="loss"
                      stroke="#0ea5e9"
                      strokeWidth={2}
                      dot={{ fill: '#0ea5e9', r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </GraphContainer>

              <GraphContainer title="Accuracy Progress">
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={mockData}>
                    <defs>
                      <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="epoch" stroke="#94a3b8" />
                    <YAxis stroke="#94a3b8" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                      labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Area
                      type="monotone"
                      dataKey="accuracy"
                      stroke="#06b6d4"
                      fill="url(#colorAcc)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </GraphContainer>
            </motion.div>

            {/* Recent Models */}
            <motion.div variants={itemVariants}>
              <Card>
                <h3 className="text-xl font-bold mb-4 gradient-text">Recent Models</h3>
                <div className="space-y-3">
                  {[
                    { name: 'Perceptron Model', acc: 85, time: '2m ago' },
                    { name: 'MLP Classifier', acc: 92, time: '15m ago' },
                    { name: 'Deep Network', acc: 88, time: '1h ago' }
                  ].map((model, i) => (
                    <motion.div
                      key={i}
                      whileHover={{ x: 4 }}
                      className="flex justify-between items-center p-3 hover:bg-white/10 rounded-lg transition"
                    >
                      <div>
                        <p className="font-semibold">{model.name}</p>
                        <p className="text-sm text-slate-400">{model.time}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-green-400">{model.acc}%</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </Card>
            </motion.div>
          </motion.div>
        </main>
      </div>
    </div>
  )
}
