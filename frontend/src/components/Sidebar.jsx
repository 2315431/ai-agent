import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Upload, 
  Zap, 
  FileText, 
  FolderOpen, 
  Settings, 
  BookOpen,
  LogOut
} from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Sidebar = () => {
  const { logout } = useAuth()

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload Content', href: '/upload', icon: Upload },
    { name: 'Generate Content', href: '/generate', icon: Zap },
    { name: 'View Results', href: '/results', icon: FileText },
    { name: 'Content Library', href: '/content', icon: FolderOpen },
    { name: 'Settings', href: '/settings', icon: Settings },
    { name: 'API Docs', href: '/docs', icon: BookOpen },
  ]

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <h1 className="text-xl font-bold text-gray-800">Content Agent</h1>
        <p className="text-sm text-gray-500 mt-1">AI Repurposing Platform</p>
      </div>
      
      <nav className="mt-6">
        {navigation.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-sm font-medium transition-colors duration-200 ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }`
              }
            >
              <Icon className="mr-3 h-5 w-5" />
              {item.name}
            </NavLink>
          )
        })}
      </nav>
      
      <div className="absolute bottom-0 w-64 p-6">
        <button
          onClick={logout}
          className="flex items-center w-full px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition-colors duration-200"
        >
          <LogOut className="mr-3 h-5 w-5" />
          Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar
