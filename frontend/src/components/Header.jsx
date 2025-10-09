import { useAuth } from '../contexts/AuthContext'
import { Bell, User } from 'lucide-react'

const Header = () => {
  const { user } = useAuth()

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-gray-800">Welcome back, {user?.username}!</h2>
            <p className="text-gray-600">Ready to create amazing content?</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
              <Bell className="h-6 w-6" />
            </button>
            
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <User className="h-5 w-5 text-white" />
              </div>
              <span className="text-sm font-medium text-gray-700">{user?.username}</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
