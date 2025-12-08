import { NavLink } from 'react-router-dom'
import {
  HomeIcon,
  CubeIcon,
  TruckIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  ClipboardDocumentListIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  UsersIcon,
} from '@heroicons/react/24/outline'
import clsx from 'clsx'
import { useAuthStore } from '@/store/authStore'

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Inventory', href: '/inventory', icon: CubeIcon },
  { name: 'Inbound', href: '/inbound', icon: ArrowDownTrayIcon },
  { name: 'Outbound', href: '/outbound', icon: ArrowUpTrayIcon },
  { name: 'Tasks', href: '/tasks', icon: ClipboardDocumentListIcon },
  { name: 'Reports', href: '/reports', icon: ChartBarIcon },
]

const adminNavigation = [
  { name: 'Users', href: '/admin/users', icon: UsersIcon },
  { name: 'Settings', href: '/admin/settings', icon: Cog6ToothIcon },
]

export function Sidebar() {
  const { hasRole } = useAuthStore()
  const isAdmin = hasRole('admin')

  return (
    <div className="flex flex-col w-64 bg-secondary-900 min-h-screen">
      {/* Logo */}
      <div className="flex items-center h-16 px-6 bg-secondary-950">
        <TruckIcon className="h-8 w-8 text-primary-500" />
        <span className="ml-2 text-xl font-bold text-white">WMS Pro</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              clsx(
                'flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-secondary-800 text-white'
                  : 'text-secondary-300 hover:bg-secondary-800 hover:text-white'
              )
            }
          >
            <item.icon className="h-5 w-5 mr-3" />
            {item.name}
          </NavLink>
        ))}

        {/* Admin Section */}
        {isAdmin && (
          <>
            <div className="pt-6 pb-2">
              <p className="px-3 text-xs font-semibold text-secondary-400 uppercase tracking-wider">
                Administration
              </p>
            </div>
            {adminNavigation.map((item) => (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-secondary-800 text-white'
                      : 'text-secondary-300 hover:bg-secondary-800 hover:text-white'
                  )
                }
              >
                <item.icon className="h-5 w-5 mr-3" />
                {item.name}
              </NavLink>
            ))}
          </>
        )}
      </nav>

      {/* Version */}
      <div className="px-6 py-4 border-t border-secondary-800">
        <p className="text-xs text-secondary-500">WMS Pro v1.0.0</p>
      </div>
    </div>
  )
}
