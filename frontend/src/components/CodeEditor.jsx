import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'

const CodeEditor = ({ value, onChange, language = 'python', readOnly = false }) => {
  const textareaRef = useRef(null)
  const [lineCount, setLineCount] = useState(1)

  useEffect(() => {
    const lines = (value || '').split('\n').length
    setLineCount(Math.max(lines, 20))
  }, [value])

  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      const start = e.target.selectionStart
      const end = e.target.selectionEnd
      const newValue = value.substring(0, start) + '  ' + value.substring(end)
      onChange(newValue)
      setTimeout(() => {
        e.target.selectionStart = e.target.selectionEnd = start + 2
      }, 0)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="relative glass rounded-xl overflow-hidden"
    >
      {/* Editor Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500" />
          </div>
          <span className="text-sm text-gray-500 ml-3">code.{language}</span>
        </div>
        <span className="text-xs text-gray-500 font-mono">
          {language.toUpperCase()}
        </span>
      </div>

      {/* Editor Body */}
      <div className="flex relative">
        {/* Line Numbers */}
        <div className="flex flex-col items-end py-4 px-3 bg-black/20 text-gray-600 font-mono text-sm select-none border-r border-white/5">
          {Array.from({ length: lineCount }, (_, i) => (
            <div key={i + 1} className="leading-6 h-6">
              {i + 1}
            </div>
          ))}
        </div>

        {/* Code Area */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            readOnly={readOnly}
            placeholder="// Paste your code here for security analysis..."
            spellCheck={false}
            className={`
              w-full h-96 p-4 bg-transparent text-gray-200
              font-mono text-sm leading-6 resize-none
              focus:outline-none placeholder:text-gray-600
              ${readOnly ? 'cursor-default' : ''}
            `}
            style={{ tabSize: 2 }}
          />
          
          {/* Scan Line Animation (shown when analyzing) */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden opacity-0 group-data-[scanning=true]:opacity-100">
            <motion.div
              className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent"
              animate={{ top: ['0%', '100%'] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
            />
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default CodeEditor
