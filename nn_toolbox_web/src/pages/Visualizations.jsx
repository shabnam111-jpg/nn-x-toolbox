import { motion } from 'framer-motion'
import { useState } from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import Card from '../components/Card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import GraphContainer from '../components/GraphContainer'
import Button from '../components/Button'

function sigmoid(value) {
  return 1 / (1 + Math.exp(-value))
}

function relu(value) {
  return Math.max(0, value)
}

function reluDerivative(value) {
  return value > 0 ? 1 : 0
}

function randomWeight(scale = 1) {
  return (Math.random() * 2 - 1) * scale
}

function evaluateLogicGate(gate, a, b) {
  switch (gate) {
    case 'AND':
      return a & b
    case 'OR':
      return a | b
    case 'NAND':
      return Number(!(a & b))
    case 'NOR':
      return Number(!(a | b))
    case 'XOR':
      return a ^ b
    case 'XNOR':
      return Number(!(a ^ b))
    case 'NOT':
      return Number(!a)
    case 'BUFFER':
      return a
    default:
      return a & b
  }
}

function generateLogicGateDataset(gate, size = 240) {
  const truthTable = [
    { a: 0, b: 0, x1: 0.12, x2: 0.12 },
    { a: 0, b: 1, x1: 0.12, x2: 0.88 },
    { a: 1, b: 0, x1: 0.88, x2: 0.12 },
    { a: 1, b: 1, x1: 0.88, x2: 0.88 }
  ]

  return Array.from({ length: size }, () => {
    const base = truthTable[Math.floor(Math.random() * truthTable.length)]
    const jitter = 0.08
    return {
      x1: Math.min(1, Math.max(0, base.x1 + (Math.random() - 0.5) * jitter)),
      x2: Math.min(1, Math.max(0, base.x2 + (Math.random() - 0.5) * jitter)),
      label: evaluateLogicGate(gate, base.a, base.b)
    }
  })
}

function generateDataset(datasetType = 'Linearly Separable', size = 240) {
  if (datasetType.startsWith('Logic Gate: ')) {
    const gate = datasetType.replace('Logic Gate: ', '')
    return generateLogicGateDataset(gate, size)
  }

  return Array.from({ length: size }, () => {
    const x1 = Math.random()
    const x2 = Math.random()
    const jitter = (Math.random() - 0.5) * 0.16

    if (datasetType === 'XOR') {
      return {
        x1,
        x2,
        label: (x1 > 0.5) !== (x2 > 0.5) ? 1 : 0
      }
    }

    if (datasetType === 'Noisy Ring') {
      const dx = x1 - 0.5
      const dy = x2 - 0.5
      const radius = Math.sqrt(dx * dx + dy * dy)
      return {
        x1,
        x2,
        label: radius + jitter > 0.28 && radius + jitter < 0.43 ? 1 : 0
      }
    }

    return {
      x1,
      x2,
      label: x1 + x2 + jitter > 1 ? 1 : 0
    }
  })
}

function runAnalysis(samples, epochs, learningRate) {
  let w1 = [randomWeight(0.4), randomWeight(0.4)]
  let b1 = randomWeight(0.2)
  let w2 = [randomWeight(0.4), randomWeight(0.4)]
  let b2 = randomWeight(0.2)

  const gradientHistory = []

  for (let epoch = 1; epoch <= epochs; epoch += 1) {
    let gradW1Abs = 0
    let gradW2Abs = 0
    let gradBAbs = 0

    for (let i = 0; i < samples.length; i += 1) {
      const sample = samples[i]
      const z1 = w1[0] * sample.x1 + w1[1] * sample.x2 + b1
      const h1 = relu(z1)

      const z2a = w2[0] * h1 + b2
      const z2b = w2[1] * h1 - b2
      const yHat = sigmoid(z2a - z2b)

      const error = yHat - sample.label
      const dz2 = error

      const gradW2_0 = dz2 * h1
      const gradW2_1 = -dz2 * h1
      const gradB2 = dz2

      const dh = dz2 * (w2[0] - w2[1])
      const dz1 = dh * reluDerivative(z1)
      const gradW1_0 = dz1 * sample.x1
      const gradW1_1 = dz1 * sample.x2
      const gradB1 = dz1

      w2[0] -= learningRate * gradW2_0
      w2[1] -= learningRate * gradW2_1
      b2 -= learningRate * gradB2

      w1[0] -= learningRate * gradW1_0
      w1[1] -= learningRate * gradW1_1
      b1 -= learningRate * gradB1

      gradW2Abs += Math.abs(gradW2_0) + Math.abs(gradW2_1)
      gradW1Abs += Math.abs(gradW1_0) + Math.abs(gradW1_1)
      gradBAbs += Math.abs(gradB1) + Math.abs(gradB2)
    }

    gradientHistory.push({
      epoch,
      g1: gradW1Abs / samples.length,
      g2: gradW2Abs / samples.length,
      gb: gradBAbs / samples.length
    })
  }

  let tp = 0
  let fp = 0
  let fn = 0
  let tn = 0

  for (let i = 0; i < samples.length; i += 1) {
    const sample = samples[i]
    const z1 = w1[0] * sample.x1 + w1[1] * sample.x2 + b1
    const h1 = relu(z1)
    const yHat = sigmoid((w2[0] * h1 + b2) - (w2[1] * h1 - b2))
    const pred = yHat >= 0.5 ? 1 : 0

    if (pred === 1 && sample.label === 1) tp += 1
    if (pred === 1 && sample.label === 0) fp += 1
    if (pred === 0 && sample.label === 1) fn += 1
    if (pred === 0 && sample.label === 0) tn += 1
  }

  const safe = (value) => Math.max(0, Math.min(1, value))
  const latest = gradientHistory[gradientHistory.length - 1]

  const gradientFlow = [
    { name: 'Input->Hidden', grad: safe(latest.g1 * 5) },
    { name: 'Hidden Act', grad: safe((latest.g1 + latest.g2) * 2.5) },
    { name: 'Hidden->Output', grad: safe(latest.g2 * 5) },
    { name: 'Bias Terms', grad: safe(latest.gb * 5) }
  ]

  const wX1 = Math.abs(w1[0])
  const wX2 = Math.abs(w1[1])
  const cross = Math.abs(w1[0] * w1[1])
  const diff = Math.abs(w1[0] - w1[1])
  const total = wX1 + wX2 + cross + diff + 1e-8

  const featureImportance = [
    { name: 'Input 1', value: Math.round((wX1 / total) * 100) },
    { name: 'Input 2', value: Math.round((wX2 / total) * 100) },
    { name: 'Cross x1*x2', value: Math.round((cross / total) * 100) },
    { name: '|x1-x2|', value: Math.round((diff / total) * 100) }
  ]

  const accuracy = (tp + tn) / Math.max(1, samples.length)

  return {
    gradientFlow,
    featureImportance,
    confusion: { tp, fp, fn, tn },
    accuracy
  }
}

export default function Visualizations() {
  const [datasetType, setDatasetType] = useState('Linearly Separable')
  const [epochs, setEpochs] = useState(100)
  const [learningRate, setLearningRate] = useState(0.03)
  const [isRunning, setIsRunning] = useState(false)
  const [status, setStatus] = useState('Choose settings and run analysis.')
  const [analysis, setAnalysis] = useState({
    gradientFlow: [
      { name: 'Input->Hidden', grad: 0.3 },
      { name: 'Hidden Act', grad: 0.22 },
      { name: 'Hidden->Output', grad: 0.28 },
      { name: 'Bias Terms', grad: 0.17 }
    ],
    featureImportance: [
      { name: 'Input 1', value: 35 },
      { name: 'Input 2', value: 31 },
      { name: 'Cross x1*x2', value: 19 },
      { name: '|x1-x2|', value: 15 }
    ],
    confusion: { tp: 0, fp: 0, fn: 0, tn: 0 },
    accuracy: 0
  })

  const handleRunAnalysis = () => {
    setIsRunning(true)
    setStatus('Analyzing gradients and feature importances...')

    const clippedEpochs = Math.min(250, Math.max(10, Number(epochs) || 10))
    const clippedLr = Math.min(0.2, Math.max(0.001, Number(learningRate) || 0.01))
    setEpochs(clippedEpochs)
    setLearningRate(clippedLr)

    const samples = generateDataset(datasetType, 240)
    const result = runAnalysis(samples, clippedEpochs, clippedLr)
    setAnalysis(result)
    setStatus(
      `Analysis complete. Accuracy ${(result.accuracy * 100).toFixed(1)}% on ${datasetType}.`
    )
    setIsRunning(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />
      <div className="flex">
        <Sidebar />
        
        <main className="flex-1 p-6 md:p-8">
          <div className="max-w-7xl mx-auto">
            <motion.h1
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-4xl font-bold gradient-text mb-8"
            >
              👁️ Visualizations & Analysis
            </motion.h1>

            <Card className="mb-6">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                <div>
                  <label className="block text-sm font-medium mb-2">Dataset</label>
                  <select
                    value={datasetType}
                    onChange={(e) => setDatasetType(e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2"
                  >
                    <option>Linearly Separable</option>
                    <option>XOR</option>
                    <option>Noisy Ring</option>
                    <option>Logic Gate: AND</option>
                    <option>Logic Gate: OR</option>
                    <option>Logic Gate: NAND</option>
                    <option>Logic Gate: NOR</option>
                    <option>Logic Gate: XOR</option>
                    <option>Logic Gate: XNOR</option>
                    <option>Logic Gate: NOT</option>
                    <option>Logic Gate: BUFFER</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Epochs</label>
                  <input
                    type="number"
                    min="10"
                    max="250"
                    value={epochs}
                    onChange={(e) => setEpochs(Number(e.target.value))}
                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Learning Rate</label>
                  <input
                    type="range"
                    min="0.001"
                    max="0.2"
                    step="0.001"
                    value={learningRate}
                    onChange={(e) => setLearningRate(Number(e.target.value))}
                    className="w-full"
                  />
                  <p className="text-sm text-slate-400 mt-1">{learningRate.toFixed(3)}</p>
                </div>

                <Button onClick={handleRunAnalysis} className="w-full">
                  {isRunning ? '⏳ Running...' : 'Run Analysis'}
                </Button>
              </div>

              <p className="text-sm text-slate-400 mt-4">{status}</p>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              <GraphContainer title="Gradient Flow">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analysis.gradientFlow}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis
                      dataKey="name"
                      stroke="#94a3b8"
                      label={{ value: 'Network Region', position: 'insideBottom', offset: -4, fill: '#94a3b8' }}
                    />
                    <YAxis
                      stroke="#94a3b8"
                      label={{ value: 'Normalized Gradient', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                      labelStyle={{ color: '#e2e8f0' }}
                    />
                    <Bar dataKey="grad" fill="#a855f7" radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </GraphContainer>

              <GraphContainer title="Feature Importance">
                <div className="space-y-3">
                  {analysis.featureImportance.map((feat, i) => (
                    <div key={feat.name}>
                      <div className="flex justify-between text-sm mb-1">
                        <span>{feat.name}</span>
                        <span className="text-cyan-400">{feat.value}%</span>
                      </div>
                      <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${feat.value}%` }}
                          transition={{ delay: i * 0.1, duration: 0.8 }}
                          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </GraphContainer>

              <Card className="md:col-span-2">
                <h3 className="text-xl font-bold mb-4">Confusion Matrix</h3>
                <div className="grid grid-cols-2 gap-4 text-center">
                  {[
                    {
                      label: 'True Positive',
                      value: analysis.confusion.tp,
                      color: 'bg-green-500/20'
                    },
                    {
                      label: 'False Positive',
                      value: analysis.confusion.fp,
                      color: 'bg-red-500/20'
                    },
                    {
                      label: 'False Negative',
                      value: analysis.confusion.fn,
                      color: 'bg-red-500/20'
                    },
                    {
                      label: 'True Negative',
                      value: analysis.confusion.tn,
                      color: 'bg-green-500/20'
                    }
                  ].map((item, i) => (
                    <motion.div
                      key={i}
                      whileHover={{ scale: 1.05 }}
                      className={`p-4 rounded-lg border ${item.color} border-opacity-30`}
                    >
                      <p className="text-sm text-slate-400">{item.label}</p>
                      <p className="text-3xl font-bold mt-2">{item.value}</p>
                    </motion.div>
                  ))}
                </div>

                <div className="mt-4 p-3 rounded-lg bg-slate-800 border border-slate-700">
                  <p className="text-sm text-slate-400">Overall Accuracy</p>
                  <p className="text-xl font-semibold text-cyan-300">
                    {(analysis.accuracy * 100).toFixed(1)}%
                  </p>
                </div>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
