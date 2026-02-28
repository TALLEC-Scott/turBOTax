import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
}

function App() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [showDocUpload, setShowDocUpload] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const currentConversation = conversations.find(c => c.id === currentConversationId)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [currentConversation?.messages])

  const createNewConversation = () => {
    const newConv: Conversation = {
      id: crypto.randomUUID(),
      title: 'New conversation',
      messages: [],
      createdAt: new Date(),
    }
    setConversations(prev => [newConv, ...prev])
    setCurrentConversationId(newConv.id)
  }

  const deleteConversation = (id: string) => {
    setConversations(prev => prev.filter(c => c.id !== id))
    if (currentConversationId === id) {
      setCurrentConversationId(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    let convId = currentConversationId
    if (!convId) {
      const newConv: Conversation = {
        id: crypto.randomUUID(),
        title: input.slice(0, 30) + (input.length > 30 ? '...' : ''),
        messages: [],
        createdAt: new Date(),
      }
      setConversations(prev => [newConv, ...prev])
      convId = newConv.id
      setCurrentConversationId(convId)
    }

    const userMessage: Message = {
      id: crypto.randomUUID(),
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

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      })

      if (!response.ok) throw new Error('Failed to get response')

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let assistantContent = ''

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          const chunk = decoder.decode(value)
          assistantContent += chunk
          setConversations(prev => prev.map(c => {
            if (c.id !== convId) return c
            const newMessages = [...c.messages]
            const lastMessage = newMessages[newMessages.length - 1]
            if (lastMessage?.role === 'assistant') {
              lastMessage.content = assistantContent
            } else {
              newMessages.push({
                id: crypto.randomUUID(),
                role: 'assistant',
                content: assistantContent,
                timestamp: new Date()
              })
            }
            return { ...c, messages: newMessages }
          }))
        }
      }
    } catch (error) {
      console.error('Error:', error)
      setConversations(prev => prev.map(c => {
        if (c.id !== convId) return c
        return {
          ...c,
          messages: [...c.messages, {
            id: crypto.randomUUID(),
            role: 'assistant' as const,
            content: 'Sorry, I encountered an error connecting to the server. Please make sure the backend is running on port 8000.',
            timestamp: new Date()
          }]
        }
      }))
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Upload failed')

      const result = await response.json()
      setInput(prev => prev + `\n\n[Uploaded: ${file.name}]\n${result.summary || 'Document processed successfully'}`)
    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload document. Please check if the backend is running.')
    }

    setShowDocUpload(false)
  }

  return (
    <div className="app">
      <button
        className="sidebar-toggle"
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? '◀' : '▶'}
      </button>

      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <button className="new-chat-btn" onClick={createNewConversation}>
          + New Chat
        </button>

        <div className="conversations-list">
          {conversations.map(conv => (
            <div
              key={conv.id}
              className={`conversation-item ${conv.id === currentConversationId ? 'active' : ''}`}
              onClick={() => setCurrentConversationId(conv.id)}
            >
              <span className="conv-title">{conv.title}</span>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation()
                  deleteConversation(conv.id)
                }}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </aside>

      <main className="chat-container">
        <header className="header">
          <h1>🧾 Tax Assistant</h1>
          <p>Powered by IRS Document Intelligence</p>
        </header>

        <div className="messages">
          {!currentConversation || currentConversation.messages.length === 0 ? (
            <div className="welcome">
              <h2>Welcome to Tax Assistant</h2>
              <p>Ask me anything about tax forms, deductions, credits, or filing requirements.</p>
              <div className="suggestions">
                <button onClick={() => setInput('What is Form 1040?')}>What is Form 1040?</button>
                <button onClick={() => setInput('Explain itemized deductions')}>Explain itemized deductions</button>
                <button onClick={() => setInput('What are the filing deadlines?')}>Filing deadlines</button>
              </div>
            </div>
          ) : (
            currentConversation.messages.map(msg => (
              <div key={msg.id} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
          {isLoading && currentConversation?.messages[currentConversation.messages.length - 1]?.role !== 'assistant' && (
            <div className="message assistant">
              <div className="message-content typing">Thinking...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-form" onSubmit={handleSubmit}>
          <div className="input-wrapper">
            <button
              type="button"
              className="upload-btn"
              onClick={() => setShowDocUpload(!showDocUpload)}
              title="Upload document"
            >
              📎
            </button>
            {showDocUpload && (
              <input
                type="file"
                className="file-input"
                onChange={handleFileUpload}
                accept=".pdf,.doc,.docx,.txt"
              />
            )}
          </div>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Ask a tax question..."
            rows={2}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </main>
    </div>
  )
}

export default App
