import { useEffect, useRef, useState } from 'react'
import cytoscape from 'cytoscape'
import fcose from 'cytoscape-fcose'
import type { NodeSingular } from 'cytoscape'

cytoscape.use(fcose)

interface GraphData {
  nodes: { id: string; data: Record<string, unknown> }[]
  edges: { id: string; source: string; target: string }[]
  positions?: Record<string, { x: number; y: number }>
}

interface GraphViewProps {
  cachedData: GraphData | null
  onDataLoaded: (data: GraphData) => void
  highlightedNodes: string[]
  openInObsidian?: boolean
}

export default function GraphView({ cachedData, onDataLoaded, highlightedNodes, openInObsidian = false }: GraphViewProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [status, setStatus] = useState('Initializing...')
  const [error, setError] = useState<string | null>(null)
  const cyRef = useRef<cytoscape.Core | null>(null)
  const isInitializedRef = useRef(false)

  // Update highlights when highlightedNodes changes
  useEffect(() => {
    const cy = cyRef.current
    if (!cy) return

    cy.nodes().removeClass('active')
    highlightedNodes.forEach(nodeId => {
      cy.getElementById(nodeId).addClass('active')
    })

    if (highlightedNodes.length > 0) {
      const highlightedCollection = cy.nodes().filter(n => highlightedNodes.includes(n.id()))
      if (highlightedCollection.length > 0) {
        cy.animate({
          fit: { eles: highlightedCollection, padding: 50 },
          duration: 300
        })
      }
    }
  }, [highlightedNodes])

  // Initialize graph
  useEffect(() => {
    if (!containerRef.current || isInitializedRef.current) return

    const buildGraph = (data: GraphData) => {
      try {
        setStatus('Building graph...')

        const degreeMap = new Map<string, number>()
        data.nodes.forEach(n => degreeMap.set(n.id, 0))
        data.edges.forEach(e => {
          degreeMap.set(e.source, (degreeMap.get(e.source) || 0) + 1)
          degreeMap.set(e.target, (degreeMap.get(e.target) || 0) + 1)
        })

        const maxDegree = Math.max(...Array.from(degreeMap.values()), 1)

        const elements: cytoscape.ElementDefinition[] = [
          ...data.nodes.map(node => {
            const degree = degreeMap.get(node.id) || 0
            const size = 4 + (degree / maxDegree) * 16

            return {
              data: {
                id: node.id,
                label: String(node.data?.label || '').slice(0, 20),
                path: node.data?.path || '',
                type: node.data?.type || 'note',
                degree,
                size,
              },
            }
          }),
          ...data.edges.map(edge => ({
            data: {
              id: edge.id,
              source: edge.source,
              target: edge.target,
            },
          })),
        ]

        const cy = cytoscape({
          container: containerRef.current,
          elements,
          style: [
            {
              selector: 'node',
              style: {
                'background-color': (ele: NodeSingular) => {
                  const degree = ele.data('degree') || 0
                  const intensity = Math.min(degree / 50, 1)
                  const type = ele.data('type')

                  let baseColor: [number, number, number]
                  switch (type) {
                    case 'form': baseColor = [167, 139, 250]; break
                    case 'publication': baseColor = [52, 211, 153]; break
                    case 'instructions': baseColor = [251, 191, 36]; break
                    default: baseColor = [100, 116, 139]
                  }

                  const r = Math.round(baseColor[0] + (255 - baseColor[0]) * intensity * 0.5)
                  const g = Math.round(baseColor[1] + (255 - baseColor[1]) * intensity * 0.5)
                  const b = Math.round(baseColor[2] + (255 - baseColor[2]) * intensity * 0.5)

                  return `rgb(${r}, ${g}, ${b})`
                },
                'width': 'data(size)',
                'height': 'data(size)',
                'label': 'data(label)',
                'font-size': 8,
                'color': '#e2e8f0',
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
                'border-width': 2,
                'border-color': '#fff',
              },
            },
            {
              selector: 'node.active',
              style: {
                'width': 'data(size) * 2',
                'height': 'data(size) * 2',
                'text-opacity': 1,
                'text-background-color': '#1e293b',
                'text-background-opacity': 1,
                'text-background-padding': '3px',
                'text-background-shape': 'roundrectangle',
                'border-width': 3,
                'border-color': '#6366f1',
                'z-index': 999,
              },
            },
            {
              selector: 'edge',
              style: {
                'width': 0.5,
                'line-color': 'rgba(148, 163, 184, 0.12)',
                'curve-style': 'bezier',
                'haystack-radius': 0,
              },
            },
            {
              selector: 'edge.highlighted',
              style: {
                'width': 1.5,
                'line-color': 'rgba(99, 102, 241, 0.5)',
              },
            },
            {
              selector: 'edge.active',
              style: {
                'width': 2,
                'line-color': 'rgba(99, 102, 241, 0.7)',
              },
            },
          ],
          layout: {
            name: 'fcose',
            idealEdgeLength: 50,
            nodeRepulsion: 8000,
            gravity: 1,
            gravityRange: 3.8,
            animate: true,
            animationDuration: 1000,
            fit: true,
            padding: 30,
            randomize: true,
          } as cytoscape.LayoutOptions,
          minZoom: 0.1,
          maxZoom: 4,
          wheelSensitivity: 0.3,
        })

        cyRef.current = cy
        isInitializedRef.current = true

        cy.on('mouseover', 'node', (evt) => {
          const node = evt.target
          if (!node.hasClass('active')) {
            node.addClass('highlighted')
            node.connectedEdges().addClass('highlighted')
            node.neighborhood('node').addClass('highlighted')
          }
        })

        cy.on('mouseout', 'node', (evt) => {
          const node = evt.target
          if (!node.hasClass('active')) {
            node.removeClass('highlighted')
            node.connectedEdges().removeClass('highlighted')
            node.neighborhood('node').removeClass('highlighted')
          }
        })

        cy.on('tap', 'node', (evt) => {
          const node = evt.target
          const path = node.data('path')
          console.log('Node clicked, path:', path, 'openInObsidian:', openInObsidian)

          if (path && openInObsidian) {
            // Open in Obsidian using URI scheme
            // Format: obsidian://open?vault=VAULT_NAME&file=PATH
            const vaultName = 'turbo_tax'
            const encodedPath = encodeURIComponent(path)
            const obsidianUrl = `obsidian://open?vault=${vaultName}&file=${encodedPath}`
            console.log('Opening Obsidian URL:', obsidianUrl)
            window.location.href = obsidianUrl
          }
        })

        setStatus('Ready')
      } catch (err) {
        console.error('Graph error:', err)
        setError(err instanceof Error ? err.message : String(err))
      }
    }

    const fetchData = async () => {
      if (cachedData && cachedData.nodes && cachedData.nodes.length > 0) {
        buildGraph(cachedData)
        return
      }

      try {
        setStatus('Fetching data...')
        const apiUrl = `http://${window.location.hostname}:8888/graph`
        const response = await fetch(apiUrl)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)

        const data = await response.json()
        if (!data.nodes || data.nodes.length === 0) {
          throw new Error('No nodes')
        }

        onDataLoaded(data)
        buildGraph(data)
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err instanceof Error ? err.message : String(err))
      }
    }

    fetchData()
  }, [])

  if (error) {
    return (
      <div className="graph-loading">
        <span style={{ color: '#ef4444' }}>Error: {error}</span>
      </div>
    )
  }

  return (
    <div className="graph-wrapper-interactive">
      {status !== 'Ready' && (
        <div className="graph-loading">
          <div className="graph-spinner"></div>
          <span>{status}</span>
        </div>
      )}
      <div
        ref={containerRef}
        className="graph-cytoscape"
        style={{ opacity: status === 'Ready' ? 1 : 0 }}
      />
    </div>
  )
}
