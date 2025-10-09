import { useState, useEffect } from 'react'
import { 
  Upload, 
  Zap, 
  FileText, 
  TrendingUp, 
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'
import { contentAPI, generationAPI } from '../services/api'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalContent: 0,
    generatedContent: 0,
    aiStatus: 'loading'
  })
  const [recentContent, setRecentContent] = useState([])

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      // Load content sources
      const contentResponse = await contentAPI.list()
      const totalContent = contentResponse.data.count || 0

      // Check AI status
      const aiResponse = await generationAPI.getStatus()
      const aiStatus = aiResponse.data.status || 'unknown'

      setStats({
        totalContent,
        generatedContent: totalContent * 3, // Estimate based on typical usage
        aiStatus
      })

      // Set recent content
      setRecentContent(contentResponse.data.sources?.slice(0, 5) || [])
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    }
  }

  const statCards = [
    {
      title: 'Total Content',
      value: stats.totalContent,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Generated Posts',
      value: stats.generatedContent,
      icon: Zap,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'AI Status',
      value: stats.aiStatus === 'ai_ready' ? 'Active' : 'Loading',
      icon: stats.aiStatus === 'ai_ready' ? CheckCircle : AlertCircle,
      color: stats.aiStatus === 'ai_ready' ? 'text-green-600' : 'text-yellow-600',
      bgColor: stats.aiStatus === 'ai_ready' ? 'bg-green-50' : 'bg-yellow-50'
    }
  ]

  const quickActions = [
    {
      title: 'Upload Content',
      description: 'Upload your blog, video, or audio content',
      icon: Upload,
      href: '/upload',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Generate Content',
      description: 'Create AI-powered social media posts',
      icon: Zap,
      href: '/generate',
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'View Results',
      description: 'Browse your generated content',
      icon: FileText,
      href: '/results',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50'
    }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Overview of your content repurposing activities</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="card">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {quickActions.map((action, index) => {
          const Icon = action.icon
          return (
            <Link
              key={index}
              to={action.href}
              className="card hover:shadow-lg transition-shadow duration-200 cursor-pointer"
            >
              <div className="flex items-center mb-4">
                <div className={`p-3 rounded-lg ${action.bgColor}`}>
                  <Icon className={`h-6 w-6 ${action.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 ml-3">{action.title}</h3>
              </div>
              <p className="text-gray-600">{action.description}</p>
            </Link>
          )
        })}
      </div>

      {/* Recent Content */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Recent Content</h3>
          <Link to="/content" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
            View all
          </Link>
        </div>
        
        {recentContent.length > 0 ? (
          <div className="space-y-3">
            {recentContent.map((content) => (
              <div key={content.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <FileText className="h-5 w-5 text-gray-400 mr-3" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{content.title}</p>
                    <p className="text-xs text-gray-500">{content.source_type} • {content.file_size} bytes</p>
                  </div>
                </div>
                <div className="flex items-center text-xs text-gray-500">
                  <Clock className="h-4 w-4 mr-1" />
                  {new Date(content.created_at).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No content uploaded yet</p>
            <Link to="/upload" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
              Upload your first content
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
