import { useState, useEffect } from 'react'
import { FileText, Copy, Download, Eye, Calendar } from 'lucide-react'
import { contentAPI } from '../services/api'
import toast from 'react-hot-toast'

const Results = () => {
  const [contentSources, setContentSources] = useState([])
  const [selectedContent, setSelectedContent] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadContentSources()
  }, [])

  const loadContentSources = async () => {
    try {
      const response = await contentAPI.list()
      setContentSources(response.data.sources || [])
    } catch (error) {
      console.error('Error loading content sources:', error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  const downloadContent = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${filename}_${Date.now()}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Generated Results</h1>
        <p className="text-gray-600 mt-2">View and manage your generated content</p>
      </div>

      {contentSources.length === 0 ? (
        <div className="card text-center py-12">
          <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No content available</h3>
          <p className="text-gray-500 mb-4">
            Upload some content and generate posts to see results here.
          </p>
          <a href="/upload" className="btn-primary">
            Upload Content
          </a>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Content List */}
          <div className="lg:col-span-1">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Content Sources</h3>
              <div className="space-y-3">
                {contentSources.map((source) => (
                  <div
                    key={source.id}
                    onClick={() => setSelectedContent(source)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors duration-200 ${
                      selectedContent?.id === source.id
                        ? 'bg-primary-50 border border-primary-200'
                        : 'bg-gray-50 hover:bg-gray-100'
                    }`}
                  >
                    <div className="flex items-start">
                      <FileText className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {source.title}
                        </p>
                        <p className="text-xs text-gray-500">
                          {source.source_type} • {source.file_size} bytes
                        </p>
                        <div className="flex items-center text-xs text-gray-400 mt-1">
                          <Calendar className="h-3 w-3 mr-1" />
                          {new Date(source.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Content Details */}
          <div className="lg:col-span-2">
            {selectedContent ? (
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {selectedContent.title}
                  </h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => copyToClipboard(selectedContent.transcript || 'No content available')}
                      className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                      title="Copy content"
                    >
                      <Copy className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => downloadContent(
                        selectedContent.transcript || 'No content available',
                        selectedContent.title
                      )}
                      className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                      title="Download content"
                    >
                      <Download className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="font-medium text-gray-700">Type:</span>
                      <span className="ml-2 text-gray-600">{selectedContent.source_type}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Size:</span>
                      <span className="ml-2 text-gray-600">{selectedContent.file_size} bytes</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Status:</span>
                      <span className="ml-2 text-gray-600 capitalize">{selectedContent.status}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-700">Uploaded:</span>
                      <span className="ml-2 text-gray-600">
                        {new Date(selectedContent.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Content Preview</h4>
                    <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                      {selectedContent.transcript ? (
                        <pre className="whitespace-pre-wrap text-sm text-gray-700">
                          {selectedContent.transcript}
                        </pre>
                      ) : (
                        <p className="text-gray-500 italic">No transcript available</p>
                      )}
                    </div>
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">Generate Content</h4>
                    <p className="text-blue-700 text-sm mb-3">
                      Use this content to generate AI-powered social media posts.
                    </p>
                    <a
                      href="/generate"
                      className="btn-primary text-sm"
                    >
                      Generate Posts
                    </a>
                  </div>
                </div>
              </div>
            ) : (
              <div className="card text-center py-12">
                <Eye className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select content to view</h3>
                <p className="text-gray-500">
                  Choose a content source from the list to view details and generate posts.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Results
