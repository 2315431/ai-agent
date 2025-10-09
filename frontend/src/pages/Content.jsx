import { useState, useEffect } from 'react'
import { FileText, Trash2, Download, Calendar, HardDrive } from 'lucide-react'
import { contentAPI } from '../services/api'
import toast from 'react-hot-toast'

const Content = () => {
  const [contentSources, setContentSources] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    loadContentSources()
  }, [])

  const loadContentSources = async () => {
    try {
      const response = await contentAPI.list()
      setContentSources(response.data.sources || [])
    } catch (error) {
      console.error('Error loading content sources:', error)
      toast.error('Failed to load content')
    } finally {
      setLoading(false)
    }
  }

  const filteredContent = contentSources.filter(source => {
    if (filter === 'all') return true
    return source.source_type === filter
  })

  const totalSize = contentSources.reduce((sum, source) => sum + (source.file_size || 0), 0)

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const downloadContent = (source) => {
    if (!source.transcript) {
      toast.error('No content available for download')
      return
    }

    const blob = new Blob([source.transcript], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${source.title}_content.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    toast.success('Content downloaded')
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
        <h1 className="text-3xl font-bold text-gray-900">Content Library</h1>
        <p className="text-gray-600 mt-2">Manage your uploaded content and files</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-50 rounded-lg">
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Files</p>
              <p className="text-2xl font-semibold text-gray-900">{contentSources.length}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-50 rounded-lg">
              <HardDrive className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Size</p>
              <p className="text-2xl font-semibold text-gray-900">{formatFileSize(totalSize)}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-purple-50 rounded-lg">
              <Calendar className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Latest Upload</p>
              <p className="text-2xl font-semibold text-gray-900">
                {contentSources.length > 0 
                  ? new Date(contentSources[0].created_at).toLocaleDateString()
                  : 'None'
                }
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Filter and Actions */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-4">
            <h3 className="text-lg font-semibold text-gray-900">Content Files</h3>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="input-field w-auto"
            >
              <option value="all">All Types</option>
              <option value="text">Text Files</option>
              <option value="video">Video Files</option>
              <option value="audio">Audio Files</option>
              <option value="document">Documents</option>
            </select>
          </div>
          <a href="/upload" className="btn-primary">
            Upload New Content
          </a>
        </div>

        {filteredContent.length === 0 ? (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 mb-4">
              {filter === 'all' ? 'No content uploaded yet' : `No ${filter} files found`}
            </p>
            <a href="/upload" className="btn-primary">
              Upload Content
            </a>
          </div>
        ) : (
          <div className="space-y-3">
            {filteredContent.map((source) => (
              <div key={source.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className="p-2 bg-white rounded-lg mr-4">
                    <FileText className="h-5 w-5 text-gray-400" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{source.title}</p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span className="capitalize">{source.source_type}</span>
                      <span>{formatFileSize(source.file_size)}</span>
                      <span className="flex items-center">
                        <Calendar className="h-3 w-3 mr-1" />
                        {new Date(source.created_at).toLocaleDateString()}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        source.status === 'uploaded' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {source.status}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => downloadContent(source)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg"
                    title="Download content"
                  >
                    <Download className="h-4 w-4" />
                  </button>
                  <button
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg"
                    title="Delete content"
                    onClick={() => toast.error('Delete functionality not implemented yet')}
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Content
