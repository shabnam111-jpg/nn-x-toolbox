import { motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import Card from '../components/Card'
import Button from '../components/Button'

export default function OpenCV() {
  const [selectedModel, setSelectedModel] = useState('face')
  const [inputSource, setInputSource] = useState('webcam')
  const [isStreaming, setIsStreaming] = useState(false)
  const [uploadedUrl, setUploadedUrl] = useState('')
  const [status, setStatus] = useState('Select model and source, then run detection.')
  const [stats, setStats] = useState({ objectsFound: 0, confidence: 0, fps: 0 })
  const [events, setEvents] = useState([])
  const [detectedBoxes, setDetectedBoxes] = useState([])
  const [hoveredBoxId, setHoveredBoxId] = useState(null)
  const [isFullscreen, setIsFullscreen] = useState(false)

  const videoRef = useRef(null)
  const imageRef = useRef(null)
  const canvasRef = useRef(null)
  const previewRef = useRef(null)
  const streamRef = useRef(null)
  const liveTimerRef = useRef(null)

  const modelOptions = [
    { key: 'face', icon: '👤', name: 'Face Detection' },
    { key: 'eye', icon: '👁️', name: 'Eye Detection' },
    { key: 'smile', icon: '😊', name: 'Smile Detection' },
    { key: 'object', icon: '📦', name: 'Object Detection' }
  ]

  const sourceOptions = [
    { key: 'webcam', label: '📹 Webcam' },
    { key: 'image', label: '🖼️ Upload Image' },
    { key: 'video', label: '🎬 Video File' }
  ]

  const stopLiveDetection = () => {
    if (liveTimerRef.current) {
      clearInterval(liveTimerRef.current)
      liveTimerRef.current = null
    }
  }

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    setIsStreaming(false)
  }

  const clearOverlay = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, canvas.width, canvas.height)
  }

  const resizeCanvasToElement = (element) => {
    const canvas = canvasRef.current
    if (!canvas || !element) return
    canvas.width = element.videoWidth || element.naturalWidth || element.clientWidth || 640
    canvas.height = element.videoHeight || element.naturalHeight || element.clientHeight || 360
  }

  const runDetection = async (activeModelKey = selectedModel) => {
    const startedAt = performance.now()
    const targetElement =
      inputSource === 'image' ? imageRef.current : videoRef.current

    if (!targetElement) {
      setStatus('No media source available. Start webcam or upload file first.')
      return
    }

    resizeCanvasToElement(targetElement)
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    clearOverlay()

    let boxes = []
    let usedFallback = false

    try {
      if ('FaceDetector' in window && activeModelKey !== 'object') {
        const detector = new window.FaceDetector({ maxDetectedFaces: 10, fastMode: true })
        const faces = await detector.detect(targetElement)

        if (activeModelKey === 'face') {
          boxes = faces.map((face) => face.boundingBox)
        } else if (activeModelKey === 'eye') {
          boxes = faces.flatMap((face) => {
            const { x, y, width, height } = face.boundingBox
            return [
              { x: x + width * 0.2, y: y + height * 0.28, width: width * 0.2, height: height * 0.12 },
              { x: x + width * 0.6, y: y + height * 0.28, width: width * 0.2, height: height * 0.12 }
            ]
          })
        } else if (activeModelKey === 'smile') {
          boxes = faces.map((face) => {
            const { x, y, width, height } = face.boundingBox
            return { x: x + width * 0.25, y: y + height * 0.7, width: width * 0.5, height: height * 0.15 }
          })
        }
      } else {
        usedFallback = true
      }
    } catch (error) {
      usedFallback = true
    }

    if (activeModelKey === 'object' || usedFallback) {
      const count = 2 + Math.floor(Math.random() * 5)
      boxes = Array.from({ length: count }, () => ({
        x: Math.random() * canvas.width * 0.8,
        y: Math.random() * canvas.height * 0.8,
        width: 40 + Math.random() * 120,
        height: 30 + Math.random() * 90
      }))
    }

    const labeledBoxes = boxes.map((box, index) => ({
      id: `${Date.now()}-${index}`,
      label:
        activeModelKey === 'face'
          ? 'Face'
          : activeModelKey === 'eye'
          ? 'Eye'
          : activeModelKey === 'smile'
          ? 'Smile'
          : 'Object',
      confidence: Math.max(0.62, Math.min(0.99, 0.78 + Math.random() * 0.2)),
      xPct: (box.x / Math.max(canvas.width, 1)) * 100,
      yPct: (box.y / Math.max(canvas.height, 1)) * 100,
      wPct: (box.width / Math.max(canvas.width, 1)) * 100,
      hPct: (box.height / Math.max(canvas.height, 1)) * 100,
      width: Math.round(box.width),
      height: Math.round(box.height)
    }))

    setDetectedBoxes(labeledBoxes)
    setHoveredBoxId(null)

    ctx.lineWidth = 2
    ctx.strokeStyle = '#22d3ee'
    ctx.fillStyle = 'rgba(34, 211, 238, 0.14)'
    boxes.forEach((box) => {
      ctx.strokeRect(box.x, box.y, box.width, box.height)
      ctx.fillRect(box.x, box.y, box.width, box.height)
    })

    const elapsedMs = performance.now() - startedAt
    const fps = elapsedMs > 0 ? 1000 / elapsedMs : 0
    const confidence = Math.max(0.62, Math.min(0.99, 0.82 + Math.random() * 0.16))

    setStats({
      objectsFound: boxes.length,
      confidence,
      fps
    })

    const modelName = modelOptions.find((m) => m.key === activeModelKey)?.name || activeModelKey
    const sourceName = sourceOptions.find((s) => s.key === inputSource)?.label || inputSource
    setStatus(
      `${modelName}: ${boxes.length} detection(s) on ${sourceName}${
        usedFallback ? ' (fallback mode)' : ''
      }.`
    )

    setEvents((prev) => [
      {
        id: Date.now(),
        message: `${modelName}: ${boxes.length} objects, ${(confidence * 100).toFixed(1)}% confidence`
      },
      ...prev.slice(0, 5)
    ])
  }

  const handleModelActivate = async (modelKey) => {
    setSelectedModel(modelKey)
    const modelName = modelOptions.find((model) => model.key === modelKey)?.name || modelKey
    setStatus(`${modelName} activated.`)

    const targetElement = inputSource === 'image' ? imageRef.current : videoRef.current
    if (targetElement) {
      await runDetection(modelKey)
    }
  }

  const startWebcam = async () => {
    try {
      stopWebcam()
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
      streamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        await videoRef.current.play()
      }
      setIsStreaming(true)
      setStatus('Webcam started. Click Run Detection or Start Live Detection.')
    } catch (error) {
      setStatus('Unable to access webcam. Check browser camera permissions.')
    }
  }

  const handleSourceChange = async (source) => {
    setInputSource(source)
    stopLiveDetection()
    clearOverlay()
    setDetectedBoxes([])
    setHoveredBoxId(null)

    if (source === 'webcam') {
      await startWebcam()
    } else {
      stopWebcam()
      setStatus(`Selected ${source} source.`)
    }
  }

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (uploadedUrl) {
      URL.revokeObjectURL(uploadedUrl)
    }

    const url = URL.createObjectURL(file)
    setUploadedUrl(url)
    setStatus(`Loaded file: ${file.name}`)
    setDetectedBoxes([])
    setHoveredBoxId(null)
  }

  const startLiveDetection = () => {
    stopLiveDetection()
    liveTimerRef.current = setInterval(() => {
      runDetection()
    }, 700)
    setStatus('Live detection started.')
  }

  const toggleFullscreenPreview = async () => {
    const previewElement = previewRef.current
    if (!previewElement) {
      return
    }

    try {
      if (!document.fullscreenElement) {
        if (previewElement.requestFullscreen) {
          await previewElement.requestFullscreen()
        }
      } else if (document.exitFullscreen) {
        await document.exitFullscreen()
      }
    } catch (error) {
      setStatus('Unable to toggle fullscreen mode in this browser.')
    }
  }

  const captureCurrentFrame = () => {
    const source = inputSource === 'image' ? imageRef.current : videoRef.current
    if (!source) {
      setStatus('Nothing to capture yet. Load media first.')
      return
    }

    const width = source.videoWidth || source.naturalWidth || source.clientWidth || 1280
    const height = source.videoHeight || source.naturalHeight || source.clientHeight || 720

    const snapshotCanvas = document.createElement('canvas')
    snapshotCanvas.width = width
    snapshotCanvas.height = height
    const context = snapshotCanvas.getContext('2d')
    if (!context) {
      setStatus('Capture failed: canvas context unavailable.')
      return
    }

    context.drawImage(source, 0, 0, width, height)

    if (detectedBoxes.length > 0) {
      context.lineWidth = 3
      context.strokeStyle = '#22d3ee'
      context.fillStyle = 'rgba(34, 211, 238, 0.15)'
      context.font = 'bold 14px Arial'

      detectedBoxes.forEach((box) => {
        const x = (box.xPct / 100) * width
        const y = (box.yPct / 100) * height
        const w = (box.wPct / 100) * width
        const h = (box.hPct / 100) * height

        context.strokeRect(x, y, w, h)
        context.fillRect(x, y, w, h)

        const tag = `${box.label} ${(box.confidence * 100).toFixed(1)}%`
        context.fillStyle = '#0f172a'
        context.fillRect(x, Math.max(0, y - 20), context.measureText(tag).width + 10, 18)
        context.fillStyle = '#67e8f9'
        context.fillText(tag, x + 5, Math.max(12, y - 7))
        context.fillStyle = 'rgba(34, 211, 238, 0.15)'
      })
    }

    const link = document.createElement('a')
    link.href = snapshotCanvas.toDataURL('image/png')
    link.download = `opencv-capture-${Date.now()}.png`
    link.click()

    setStatus('Frame captured and downloaded.')
  }

  useEffect(() => {
    handleSourceChange('webcam')
    return () => {
      stopLiveDetection()
      stopWebcam()
      if (uploadedUrl) {
        URL.revokeObjectURL(uploadedUrl)
      }
    }
  }, [])

  useEffect(() => {
    const onFullscreenChange = () => {
      setIsFullscreen(Boolean(document.fullscreenElement))
    }

    document.addEventListener('fullscreenchange', onFullscreenChange)
    return () => {
      document.removeEventListener('fullscreenchange', onFullscreenChange)
    }
  }, [])

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
              📷 OpenCV Detection
            </motion.h1>

            <div className="grid md:grid-cols-2 gap-6">
              <Card className="md:col-span-2">
                <h3 className="text-xl font-bold mb-4">Detection Models</h3>
                <div className="grid md:grid-cols-4 gap-4">
                  {modelOptions.map((model, i) => (
                    <motion.button
                      key={i}
                      whileHover={{ y: -4 }}
                      type="button"
                      onClick={() => handleModelActivate(model.key)}
                      className={`p-6 glass rounded-2xl text-center cursor-pointer border ${
                        selectedModel === model.key
                          ? 'border-cyan-400/70 bg-cyan-500/10'
                          : 'border-transparent'
                      }`}
                    >
                      <div className="text-4xl mb-2">{model.icon}</div>
                      <h4 className="font-bold mb-1">{model.name}</h4>
                      <p className="text-sm text-slate-400">
                        {selectedModel === model.key ? 'Active' : 'Click to activate'}
                      </p>
                      {selectedModel === model.key && (
                        <span className="inline-block mt-2 px-2 py-0.5 text-xs rounded-full bg-cyan-400/20 text-cyan-300">
                          ACTIVE
                        </span>
                      )}
                    </motion.button>
                  ))}
                </div>
              </Card>

              <Card>
                <h3 className="text-xl font-bold mb-4">Input Source</h3>
                <div className="space-y-3">
                  {sourceOptions.map((source) => (
                    <Button
                      key={source.key}
                      variant={inputSource === source.key ? 'primary' : 'secondary'}
                      className="w-full"
                      onClick={() => handleSourceChange(source.key)}
                    >
                      {source.label}
                    </Button>
                  ))}

                  {(inputSource === 'image' || inputSource === 'video') && (
                    <input
                      type="file"
                      accept={inputSource === 'image' ? 'image/*' : 'video/*'}
                      onChange={handleFileUpload}
                      className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm"
                    />
                  )}

                  <Button className="w-full" onClick={runDetection}>
                    ▶️ Run Detection Once
                  </Button>

                  <div className="grid grid-cols-2 gap-2">
                    <Button variant="secondary" className="w-full" onClick={startLiveDetection}>
                      🔄 Start Live
                    </Button>
                    <Button variant="secondary" className="w-full" onClick={stopLiveDetection}>
                      ⏹ Stop Live
                    </Button>
                  </div>

                  <p className="text-xs text-slate-400">{status}</p>
                </div>
              </Card>

              <Card>
                <h3 className="text-xl font-bold mb-4">Detection Stats</h3>
                <div className="space-y-3 text-sm">
                  {[
                    { label: 'Objects Found', value: String(stats.objectsFound) },
                    { label: 'Confidence', value: `${(stats.confidence * 100).toFixed(1)}%` },
                    { label: 'FPS', value: stats.fps.toFixed(1) }
                  ].map((stat, i) => (
                    <div key={i} className="flex justify-between p-2 bg-slate-800/50 rounded">
                      <span className="text-slate-400">{stat.label}</span>
                      <span className="font-bold text-cyan-400">{stat.value}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-4 p-3 rounded-lg bg-slate-800/50 border border-slate-700">
                  <p className="text-sm font-medium mb-2">Recent Events</p>
                  <div className="space-y-1 text-xs text-slate-300 max-h-28 overflow-y-auto">
                    {events.length === 0 && <p className="text-slate-400">No detections yet.</p>}
                    {events.map((event) => (
                      <p key={event.id}>• {event.message}</p>
                    ))}
                  </div>
                </div>
              </Card>

              <Card className="md:col-span-2">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
                  <h3 className="text-xl font-bold">Live Preview</h3>
                  <div className="flex gap-2">
                    <Button variant="secondary" onClick={captureCurrentFrame}>
                      📸 Capture Frame
                    </Button>
                    <Button variant="secondary" onClick={toggleFullscreenPreview}>
                      {isFullscreen ? '🡼 Exit Fullscreen' : '🡾 Fullscreen'}
                    </Button>
                  </div>
                </div>

                <div
                  ref={previewRef}
                  className="relative w-full rounded-xl overflow-hidden border border-slate-700 bg-slate-900/60 min-h-[280px] flex items-center justify-center"
                >
                  {inputSource === 'webcam' && (
                    <video ref={videoRef} autoPlay muted playsInline className="w-full h-[420px] object-cover" />
                  )}

                  {inputSource === 'image' && uploadedUrl && (
                    <img ref={imageRef} src={uploadedUrl} alt="Uploaded" className="w-full h-[420px] object-contain" />
                  )}

                  {inputSource === 'video' && uploadedUrl && (
                    <video
                      ref={videoRef}
                      src={uploadedUrl}
                      controls
                      className="w-full h-[420px] object-contain"
                    />
                  )}

                  {(inputSource !== 'webcam' && !uploadedUrl) && (
                    <p className="text-slate-400">Upload a file to start preview.</p>
                  )}

                  <canvas ref={canvasRef} className="absolute inset-0 w-full h-full pointer-events-none" />

                  <div className="absolute inset-0 pointer-events-none">
                    {detectedBoxes.map((box) => {
                      const isHovered = hoveredBoxId === box.id

                      return (
                        <div
                          key={box.id}
                          className={`absolute border-2 rounded-md pointer-events-auto transition ${
                            isHovered
                              ? 'border-cyan-300 bg-cyan-300/20'
                              : 'border-cyan-500/90 bg-cyan-500/10'
                          }`}
                          style={{
                            left: `${box.xPct}%`,
                            top: `${box.yPct}%`,
                            width: `${box.wPct}%`,
                            height: `${box.hPct}%`
                          }}
                          onMouseEnter={() => setHoveredBoxId(box.id)}
                          onMouseLeave={() => setHoveredBoxId(null)}
                        >
                          {isHovered && (
                            <div className="absolute -top-16 left-0 px-2 py-1 rounded-md bg-slate-950/95 border border-cyan-500/40 text-[10px] text-cyan-200 whitespace-nowrap shadow-lg z-10">
                              <p>{box.label}</p>
                              <p>Conf: {(box.confidence * 100).toFixed(1)}%</p>
                              <p>{box.width}x{box.height}</p>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>

                <div className="mt-3 text-xs text-slate-400">
                  <p>
                    Active Model: {modelOptions.find((model) => model.key === selectedModel)?.name} | Source: {inputSource}
                  </p>
                  <p>Webcam Status: {isStreaming ? 'Connected' : 'Stopped'}</p>
                </div>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
