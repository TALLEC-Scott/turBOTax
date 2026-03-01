import { useEffect, useRef, useState } from 'react'
import cytoscape from 'cytoscape'
import fcose from 'cytoscape-fcose'

cytoscape.use(fcose)

interface DynamicGraphProps {
  openInObsidian?: boolean
}

export default function DynamicGraph({ openInObsidian = false }: DynamicGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [status, setStatus] = useState('Connecting...')
  const [nodeCount, setNodeCount] = useState(0)
  const cyRef = useRef<cytoscape.Core | null>(null)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    const cy = cytoscape({
      container: containerRef.current,
      elements: [],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (ele) => {
              const nodeType = ele.data('nodeType')
              switch (nodeType) {
                case 'form':
                  return '#a78bfa'
                case 'publication':
                  return '#34d399'
                case 'instructions':
                  return '#fbbf24'
                case 'asset':
                  return '#f472b6'
                case 'index':
                  return '#60a5fa'
                default:
                  return '#64748b'
              }
            },
            width: 20,
            height: 20,
            label: 'data(label)',
            'font-size': '8px',
            color: '#e2e8f0',
            'text-opacity': 0,
            'text-margin-x': 8,
          },
        },
        {
          selector: 'node.highlighted',
          style: {
            'text-opacity': 1,
            'text-background-color': '#1e293b',
            'text-background-opacity': 1,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
          },
        },
        {
          selector: 'node.new',
          style: {
            width: 30,
            height: 30,
            'border-width': 3,
            'border-color': '#22d3ee',
            'border-opacity': 1,
          },
        },
        {
          selector: 'edge',
          style: {
            width: 0.5,
            'line-color': 'rgba(148, 163, 184, 0.3)',
            'curve-style': 'bezier',
          },
        },
      ],
      layout: {
        name: 'fcose',
        animate: true,
        animationDuration: 300,
        fit: false,
        gravity: 0.5,
        nodeRepulsion: 6000,
      } as cytoscape.LayoutOptions,
      minZoom: 0.1,
      maxZoom: 4,
      wheelSensitivity: 0.3,
    })

    cyRef.current = cy

    cy.on('mouseover', 'node', (evt) => {
      const node = evt.target
      node.addClass('highlighted')
    })

    cy.on('mouseout', 'node', (evt) => {
      const node = evt.target
      node.removeClass('highlighted')
    })

    cy.on('tap', 'node', (evt) => {
      const node = evt.target
      const path = node.data('path')
      if (path && openInObsidian) {
        const vaultName = 'turbo_tax'
        const encodedPath = encodeURIComponent(path)
        window.location.href = `obsidian://open?vault=${vaultName}&file=${encodedPath}`
      }
    })

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.hostname}:8888/ws/traversal`

    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      setStatus('Ready - ask a question')
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.type === 'node') {
        const existingNode = cy.getElementById(data.id)
        if (existingNode.length === 0) {
          cy.add({
            data: {
              id: data.id,
              label: data.label,
              path: data.path,
              nodeType: data.node_type,
            },
          })

          const newNode = cy.getElementById(data.id)
          newNode.addClass('new')
          setTimeout(() => newNode.removeClass('new'), 1000)

          cy.layout({
            name: 'fcose',
            animate: true,
            animationDuration: 300,
            fit: false,
            gravity: 0.5,
            nodeRepulsion: 6000,
          } as cytoscape.LayoutOptions).run()
          cy.center()

          setNodeCount((c) => c + 1)
          setStatus(`Exploring: ${data.label}`)
        }
      } else if (data.type === 'edge') {
        // Add edge
        const existingEdge = cy.getElementById(data.id)
        if (existingEdge.length === 0) {
          cy.add({
            data: {
              id: data.id,
              source: data.source,
              target: data.target,
            },
          })
          // Re-run layout and center on new edges
          cy.layout({
            name: 'fcose',
            animate: true,
            animationDuration: 300,
            fit: false,
            gravity: 0.5,
            nodeRepulsion: 6000,
          } as cytoscape.LayoutOptions).run()
          cy.center()
        }
      } else if (data.type === 'done') {
        setStatus('Ready - ask a question')
      }
    }

    ws.onerror = () => setStatus('WebSocket error')
    ws.onclose = () => setStatus('Disconnected')

    return () => {
      ws.close()
      cy.destroy()
    }
  }, [openInObsidian])

  return (
    <div className="dynamic-graph-wrapper">
      <div className="dynamic-graph-header">
        <span className="graph-status">{status}</span>
        <span className="graph-node-count">{nodeCount} nodes</span>
      </div>
      <div ref={containerRef} className="dynamic-graph-canvas" />
    </div>
  )
}
