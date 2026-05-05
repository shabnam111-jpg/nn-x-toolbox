import { motion } from 'framer-motion'
import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import Card from '../components/Card'
import GraphContainer from '../components/GraphContainer'
import Button from '../components/Button'

function step(value) {
  return value >= 0 ? 1 : 0
}

function generateLinearlySeparableData(size = 120) {
  return Array.from({ length: size }, () => {
    const x1 = Math.random()
    const x2 = Math.random()
    const noise = (Math.random() - 0.5) * 0.15
    const label = x1 + x2 + noise > 1 ? 1 : 0
    return { x1, x2, label }
  })
}

function generateXorData(size = 120) {
  return Array.from({ length: size }, () => {
    const x1 = Math.random()
    const x2 = Math.random()
    const label = (x1 > 0.5) !== (x2 > 0.5) ? 1 : 0
    return { x1, x2, label }
  })
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

function generateLogicGateData(gate, size = 160) {
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

function getDataset(datasetType) {
  if (datasetType.startsWith('Logic Gate: ')) {
    const gate = datasetType.replace('Logic Gate: ', '')
    return generateLogicGateData(gate)
  }

  if (datasetType === 'XOR Problem') {
    return generateXorData()
  }

  if (datasetType === 'Custom Data') {
    return generateLinearlySeparableData(150).map((sample) => ({
      ...sample,
      x1: Math.min(1, Math.max(0, sample.x1 + (Math.random() - 0.5) * 0.1)),
      x2: Math.min(1, Math.max(0, sample.x2 + (Math.random() - 0.5) * 0.1))
    }))
  }

  return generateLinearlySeparableData()
}

function trainPerceptron(samples, learningRate, epochs) {
  let w1 = Math.random() * 0.4 - 0.2
  let w2 = Math.random() * 0.4 - 0.2
  let bias = Math.random() * 0.2 - 0.1
  const history = []

  for (let epoch = 1; epoch <= epochs; epoch += 1) {
    let errors = 0

    samples.forEach(({ x1, x2, label }) => {
      const prediction = step(w1 * x1 + w2 * x2 + bias)
      const error = label - prediction

      if (error !== 0) {
        w1 += learningRate * error * x1
        w2 += learningRate * error * x2
        bias += learningRate * error
        errors += 1
      }
    })

    history.push({ epoch, loss: errors / samples.length })
  }

  const correct = samples.reduce((acc, { x1, x2, label }) => {
    const prediction = step(w1 * x1 + w2 * x2 + bias)
    return acc + (prediction === label ? 1 : 0)
  }, 0)

  return {
    model: { w1, w2, bias },
    history,
    accuracy: correct / samples.length
  }
}

export default function Perceptron() {
  const [learningRate, setLearningRate] = useState(0.01)
  const [epochs, setEpochs] = useState(100)
  const [datasetType, setDatasetType] = useState('Linearly Separable')
  const [trainingData, setTrainingData] = useState([])
  const [samples, setSamples] = useState([])
  const [model, setModel] = useState({ w1: 0.5, w2: 0.5, bias: -0.5 })
  const [accuracy, setAccuracy] = useState(null)
  const [isTraining, setIsTraining] = useState(false)
  const [status, setStatus] = useState('Select parameters and click Train Model.')

  const handleTrain = () => {
    setIsTraining(true)
    setStatus('Training in progress...')

    const nextSamples = getDataset(datasetType)
    const result = trainPerceptron(nextSamples, Number(learningRate), Number(epochs))

    setSamples(nextSamples)
    setTrainingData(result.history)
    setModel(result.model)
    setAccuracy(result.accuracy)
    setStatus(`Training complete on ${datasetType}.`)
    setIsTraining(false)
  }

  const decisionLine = (() => {
    const { w1, w2, bias } = model
    const eps = 1e-6

    if (Math.abs(w2) < eps) {
      const x = Math.min(1, Math.max(0, -bias / (w1 || eps)))
      return { x1: x, y1: 0, x2: x, y2: 1, vertical: true }
    }

    const yAt0 = -bias / w2
    const yAt1 = -(w1 + bias) / w2
    return {
      x1: 0,
      y1: Math.min(1, Math.max(0, yAt0)),
      x2: 1,
      y2: Math.min(1, Math.max(0, yAt1)),
      vertical: false
    }
  })()

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
              ⚡ Perceptron Trainer
            </motion.h1>

            <div className="grid md:grid-cols-3 gap-6">
              {/* Control Panel */}
              <Card className="md:col-span-1">
                <h3 className="text-xl font-bold mb-6">Configuration</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Learning Rate</label>
                    <input
                      type="range"
                      min="0.001"
                      max="0.5"
                      step="0.01"
                      value={learningRate}
                      onChange={(e) => setLearningRate(Number(e.target.value))}
                      className="w-full"
                    />
                    <p className="text-sm text-slate-400 mt-1">{learningRate}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Epochs</label>
                    <input
                      type="number"
                      value={epochs}
                      onChange={(e) => setEpochs(Math.max(1, Number(e.target.value) || 1))}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Dataset</label>
                    <select
                      value={datasetType}
                      onChange={(e) => setDatasetType(e.target.value)}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white"
                    >
                      <option>Linearly Separable</option>
                      <option>XOR Problem</option>
                      <option>Custom Data</option>
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

                  <Button className="w-full mt-4" onClick={handleTrain}>
                    {isTraining ? '⏳ Training...' : '🚀 Train Model'}
                  </Button>

                  <p className="text-sm text-slate-400 mt-3">{status}</p>

                  {accuracy !== null && (
                    <div className="mt-3 p-3 rounded-lg bg-slate-800 border border-slate-700">
                      <p className="text-sm text-slate-400">Final Accuracy</p>
                      <p className="text-xl font-semibold text-cyan-300">
                        {(accuracy * 100).toFixed(1)}%
                      </p>
                    </div>
                  )}
                </div>
              </Card>

              {/* Visualization */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="md:col-span-2"
              >
                <GraphContainer title="Decision Boundary">
                  <div className="w-full h-96 bg-slate-800 rounded-lg relative overflow-hidden border border-slate-700">
                    <div className="absolute left-1/2 bottom-2 -translate-x-1/2 text-xs text-slate-300 pointer-events-none">
                      X1 Feature
                    </div>
                    <div className="absolute left-2 top-1/2 -translate-y-1/2 -rotate-90 origin-left text-xs text-slate-300 pointer-events-none">
                      X2 Feature
                    </div>
                    <svg viewBox="0 0 100 100" className="absolute inset-0 w-full h-full">
                      <defs>
                        <linearGradient id="boundary" x1="0" y1="0" x2="1" y2="1">
                          <stop offset="0%" stopColor="#22d3ee" />
                          <stop offset="100%" stopColor="#3b82f6" />
                        </linearGradient>
                      </defs>

                      {!decisionLine.vertical && (
                        <line
                          x1={decisionLine.x1 * 100}
                          y1={(1 - decisionLine.y1) * 100}
                          x2={decisionLine.x2 * 100}
                          y2={(1 - decisionLine.y2) * 100}
                          stroke="url(#boundary)"
                          strokeWidth="1"
                        />
                      )}

                      {decisionLine.vertical && (
                        <line
                          x1={decisionLine.x1 * 100}
                          y1="0"
                          x2={decisionLine.x2 * 100}
                          y2="100"
                          stroke="url(#boundary)"
                          strokeWidth="1"
                        />
                      )}

                      {samples.map((sample, index) => (
                        <circle
                          key={`${sample.x1}-${sample.x2}-${index}`}
                          cx={sample.x1 * 100}
                          cy={(1 - sample.x2) * 100}
                          r="1.2"
                          fill={sample.label === 1 ? '#22d3ee' : '#f59e0b'}
                          opacity="0.85"
                        />
                      ))}
                    </svg>

                    {samples.length === 0 && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <p className="text-slate-400">Click Train Model to generate data and boundary.</p>
                      </div>
                    )}
                  </div>
                </GraphContainer>

                <div className="mt-6">
                  <GraphContainer title="Training Progress">
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={trainingData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                      <XAxis
                        dataKey="epoch"
                        stroke="#94a3b8"
                        label={{
                          value: 'Epoch',
                          position: 'insideBottom',
                          offset: -4,
                          fill: '#94a3b8'
                        }}
                      />
                      <YAxis
                        stroke="#94a3b8"
                        label={{
                          value: 'Loss',
                          angle: -90,
                          position: 'insideLeft',
                          fill: '#94a3b8'
                        }}
                      />
                      <Tooltip
                        contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                        labelStyle={{ color: '#e2e8f0' }}
                      />
                      <Line
                        type="monotone"
                        dataKey="loss"
                        stroke="#f59e0b"
                        strokeWidth={2}
                        dot={{ fill: '#f59e0b' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                  </GraphContainer>
                </div>
              </motion.div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
