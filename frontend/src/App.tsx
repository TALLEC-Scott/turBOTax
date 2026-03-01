import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import GraphView from './GraphView'
import './App.css'

const API_URL = `http://${window.location.hostname}:8888`

const generateId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return 'id-' + Math.random().toString(36).substr(2, 9) + '-' + Date.now()
}

interface ToolCall {
  id: string
  name: string
  args: Record<string, unknown>
  result?: string
  status: 'pending' | 'done'
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  toolCalls?: ToolCall[]
}

interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
}

interface GraphData {
  nodes: { id: string; data: Record<string, unknown> }[]
  edges: { id: string; source: string; target: string }[]
  positions?: Record<string, { x: number; y: number }>
}

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [graphData, setGraphData] = useState<GraphData | null>(null)
  const [highlightedNodes, setHighlightedNodes] = useState<string[]>([])
  const [openInObsidian, setOpenInObsidian] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const currentConversation = conversations.find(c => c.id === currentConversationId)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [currentConversation?.messages])

  // Auto-create conversation if needed

  // Extract file paths from tool calls and highlight them
  const extractFilePaths = (toolName: string, args: Record<string, unknown>, result?: string): string[] => {
    const paths: string[] = []

    if (toolName === 'read_note' && args.path) {
      paths.push(String(args.path))
    } else if (toolName === 'search_notes' && result) {
      // Extract paths from search results
      try {
        const parsed = JSON.parse(result)
        if (Array.isArray(parsed)) {
          parsed.forEach((item: { path?: string }) => {
            if (item.path) paths.push(item.path)
          })
        }
      } catch { /* ignore */ }
    } else if (toolName === 'list_directory' && args.path) {
      paths.push(String(args.path))
    } else if (toolName === 'get_indices' && result) {
      // Highlight all index files
      try {
        const parsed = JSON.parse(result)
        if (parsed.indices && Array.isArray(parsed.indices)) {
          parsed.indices.forEach((idx: { path?: string }) => {
            if (idx.path) paths.push(idx.path)
          })
        }
      } catch { /* ignore */ }
    } else if (toolName === 'crawl_from_index') {
      // Highlight the index being crawled
      if (args.path) paths.push(String(args.path))
      // Also highlight all crawled notes from result
      if (result) {
        try {
          const parsed = JSON.parse(result)
          if (parsed.notes && Array.isArray(parsed.notes)) {
            parsed.notes.forEach((note: { path?: string }) => {
              if (note.path) paths.push(note.path)
            })
          }
        } catch { /* ignore */ }
      }
    } else if (toolName === 'get_backlinks' && result) {
      // Highlight backlinked notes
      try {
        const parsed = JSON.parse(result)
        if (parsed.backlinks && Array.isArray(parsed.backlinks)) {
          parsed.backlinks.forEach((bl: { path?: string }) => {
            if (bl.path) paths.push(bl.path)
          })
        }
        if (parsed.source) paths.push(parsed.source)
      } catch { /* ignore */ }
    } else if (toolName === 'get_outlinks' && result) {
      // Highlight outlinked notes
      try {
        const parsed = JSON.parse(result)
        if (parsed.outlinks && Array.isArray(parsed.outlinks)) {
          parsed.outlinks.forEach((ol: { path?: string }) => {
            if (ol.path) paths.push(ol.path)
          })
        }
        if (parsed.source) paths.push(parsed.source)
      } catch { /* ignore */ }
    } else if (toolName === 'explore_note_graph' && result) {
      // Highlight all nodes in explored graph
      try {
        const parsed = JSON.parse(result)
        if (parsed.nodes && Array.isArray(parsed.nodes)) {
          parsed.nodes.forEach((node: { path?: string }) => {
            if (node.path) paths.push(node.path)
          })
        }
      } catch { /* ignore */ }
    }

    return paths
  }

  // Convert file path to node ID (matching backend logic)
  const pathToNodeId = (path: string): string | null => {
    if (!graphData?.nodes) return null

    // Try exact match first
    const exactMatch = graphData.nodes.find(n => n.data?.path === path)
    if (exactMatch) {
      console.log(`✅ Exact match: ${path} -> ${exactMatch.id}`)
      return exactMatch.id
    }

    // Try matching by filename
    const filename = path.split('/').pop()?.replace('.md', '') || ''
    const nameMatch = graphData.nodes.find(n => {
      const nodeLabel = String(n.data?.label || '').toLowerCase()
      const nodePath = String(n.data?.path || '').toLowerCase()
      return nodeLabel.includes(filename.toLowerCase()) || 
             filename.toLowerCase().includes(nodeLabel) ||
             nodePath.includes(filename.toLowerCase())
    })

    if (nameMatch) {
      console.log(`✅ Name match: ${path} -> ${nameMatch.id}`)
      return nameMatch.id
    }
    
    console.log(`❌ No match for: ${path}`)
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    let convId = currentConversationId
    if (!convId) {
      const newConv: Conversation = {
        id: generateId(),
        title: input.slice(0, 30) + (input.length > 30 ? '...' : ''),
        messages: [],
        createdAt: new Date(),
      }
      setConversations(prev => [newConv, ...prev])
      convId = newConv.id
      setCurrentConversationId(convId)
    }

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setConversations(prev => prev.map(c =>
      c.id === convId
        ? {
            ...c,
            messages: [...c.messages, userMessage],
            title: c.messages.length === 0 ? input.slice(0, 30) + (input.length > 30 ? '...' : '') : c.title
          }
        : c
    ))
    setInput('')
    setIsLoading(true)

    // Create assistant message placeholder
    const assistantId = generateId()
    setConversations(prev => prev.map(c =>
      c.id === convId
        ? {
            ...c,
            messages: [...c.messages, {
              id: assistantId,
              role: 'assistant' as const,
              content: '',
              timestamp: new Date(),
              toolCalls: []
            }]
          }
        : c
    ))

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      })

      if (!response.ok) throw new Error('Failed to get response')

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (reader) {
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })

          const events = buffer.split('\n\n')
          buffer = events.pop() || ''

          for (const event of events) {
            const line = event.trim()
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))

                if (data.type === 'tool_call') {
                  const toolCall: ToolCall = {
                    id: data.id || generateId(),
                    name: data.name,
                    args: data.args,
                    status: 'pending'
                  }

                  setConversations(prev => prev.map(c => {
                    if (c.id !== convId) return c
                    return {
                      ...c,
                      messages: c.messages.map(m =>
                        m.id === assistantId
                          ? { ...m, toolCalls: [...(m.toolCalls || []), toolCall] }
                          : m
                      )
                    }
                  }))

                  // Highlight node when tool is called
                  console.log('🔧 Tool call:', data.name, 'args:', data.args)
                  const paths = extractFilePaths(data.name, data.args)
                  console.log('📁 Extracted paths:', paths)
                  console.log('📊 Graph data available:', !!graphData?.nodes, graphData?.nodes?.length, 'nodes')
                  const nodeIds = paths.map(pathToNodeId).filter(Boolean) as string[]
                  console.log('🎯 Node IDs to highlight:', nodeIds)
                  if (nodeIds.length > 0) {
                    setHighlightedNodes(prev => [...new Set([...prev, ...nodeIds])])
                  }

                } else if (data.type === 'tool_result') {
                  setConversations(prev => prev.map(c => {
                    if (c.id !== convId) return c
                    return {
                      ...c,
                      messages: c.messages.map(m =>
                        m.id === assistantId
                          ? {
                              ...m,
                              toolCalls: (m.toolCalls || []).map(tc =>
                                tc.id === data.id
                                  ? { ...tc, result: data.result, status: 'done' }
                                  : tc
                              )
                            }
                          : m
                      )
                    }
                  }))

                  // Highlight from paths sent by backend
                  if (data.paths && Array.isArray(data.paths) && data.paths.length > 0) {
                    console.log('📁 Paths from backend:', data.paths)
                    console.log('📊 Graph data available:', !!graphData?.nodes, graphData?.nodes?.length, 'nodes')
                    const nodeIds = data.paths.map(pathToNodeId).filter(Boolean) as string[]
                    console.log('🎯 Node IDs to highlight:', nodeIds)
                    if (nodeIds.length > 0) {
                      setHighlightedNodes(prev => [...new Set([...prev, ...nodeIds])])
                    }
                  }

                } else if (data.type === 'content') {
                  setConversations(prev => prev.map(c => {
                    if (c.id !== convId) return c
                    return {
                      ...c,
                      messages: c.messages.map(m =>
                        m.id === assistantId
                          ? { ...m, content: m.content + data.content }
                          : m
                      )
                    }
                  }))
                  await new Promise(r => setTimeout(r, 10))
                } else if (data.type === 'error') {
                  setConversations(prev => prev.map(c => {
                    if (c.id !== convId) return c
                    return {
                      ...c,
                      messages: c.messages.map(m =>
                        m.id === assistantId
                          ? { ...m, content: `Error: ${data.content}` }
                          : m
                      )
                    }
                  }))
                }
              } catch {
                // Skip invalid JSON
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error)
      setConversations(prev => prev.map(c => {
        if (c.id !== convId) return c
        return {
          ...c,
          messages: c.messages.map(m =>
            m.id === assistantId
              ? { ...m, content: 'Sorry, I encountered an error connecting to the server.' }
              : m
          )
        }
      }))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <main className="chat-container">
        <header className="header">
          <h1>🧾 Tax Assistant</h1>
          <p>Powered by IRS Document Intelligence</p>
        </header>

        <div className="main-content">
          <div className="chat-area">
            <div className="messages">
              {!currentConversation || currentConversation.messages.length === 0 ? (
                <div className="welcome">
                  <h2>Welcome to Tax Assistant</h2>
                  <p>Ask me anything about tax forms, deductions, credits, or filing requirements.</p>
                  <div className="suggestions">
                    <button onClick={() => setInput('What is Form 1040?')}>What is Form 1040?</button>
                    <button onClick={() => setInput('Compare Traditional vs Roth IRA')}>Traditional vs Roth IRA</button>
                    <button onClick={() => setInput('What are the filing deadlines?')}>Filing deadlines</button>
                  </div>
                </div>
              ) : (
                currentConversation.messages.map(msg => (
                  <div key={msg.id} className={`message ${msg.role}`}>
                    {msg.toolCalls && msg.toolCalls.length > 0 && (
                      <details className="tool-calls-summary">
                        <summary>
                          <span className="tool-count">
                            🔧 {msg.toolCalls.length} tool call{msg.toolCalls.length > 1 ? 's' : ''}
                          </span>
                          <span className="tool-names">
                            {msg.toolCalls.map(tc => tc.name).join(', ')}
                          </span>
                          {msg.toolCalls.every(tc => tc.status === 'done') && (
                            <span className="all-done">✓</span>
                          )}
                        </summary>
                        <div className="tool-calls">
                          {msg.toolCalls.map((tc, idx) => (
                            <div key={tc.id || idx} className={`tool-call ${tc.status}`}>
                              <div className="tool-header">
                                <span className="tool-icon">🔧</span>
                                <span className="tool-name">{tc.name}</span>
                                {tc.status === 'pending' && <span className="spinner">⏳</span>}
                                {tc.status === 'done' && <span className="check">✓</span>}
                              </div>
                              {tc.args && Object.keys(tc.args).length > 0 && (
                                <div className="tool-args">
                                  {Object.entries(tc.args).map(([k, v]) => (
                                    <span key={k} className="arg">{k}={JSON.stringify(v)}</span>
                                  ))}
                                </div>
                              )}
                              {tc.result && (
                                <div className="tool-result">{tc.result}</div>
                              )}
                            </div>
                          ))}
                        </div>
                      </details>
                    )}
                    {msg.content && (
                      <div className="message-content">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {msg.content}
                        </ReactMarkdown>
                      </div>
                    )}
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            <form className="input-form" onSubmit={handleSubmit}>
              <textarea
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Ask about tax forms, deductions, IRA limits, filing deadlines..."
                rows={2}
                onKeyDown={e => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
              />
              <button type="submit" disabled={isLoading || !input.trim()}>
                {isLoading ? (
                  <>Sending...</>
                ) : (
                  <>
                    <span>Send</span>
                    <span>→</span>
                  </>
                )}
              </button>
            </form>
          </div>

          <aside className="graph-sidebar">
            <div className="graph-sidebar-header">
              <h3>🕸️ Knowledge Graph</h3>
              <div className="graph-header-actions">
                <button 
                  className={`obsidian-toggle ${openInObsidian ? 'active' : ''}`}
                  onClick={() => setOpenInObsidian(!openInObsidian)}
                  title={openInObsidian ? "Click opens Obsidian" : "Click to enable Obsidian opening"}
                >
                  📓
                </button>
                <button 
                  className="clear-highlight-btn"
                  onClick={() => setHighlightedNodes([])}
                  title="Clear highlights"
                >
                  ✕
                </button>
              </div>
            </div>
            <GraphView
              cachedData={graphData}
              onDataLoaded={setGraphData}
              highlightedNodes={highlightedNodes}
              openInObsidian={openInObsidian}
            />
          </aside>
        </div>
      </main>
    </div>
  )
}

export default App
