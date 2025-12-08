import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import {
  BellIcon,
  UserCircleIcon,
  ArrowRightOnRectangleIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline'
import { useNavigate } from 'react-router-dom'
import clsx from 'clsx'
import { useAuthStore } from '@/store/authStore'

export function Header() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="flex items-center justify-between h-16 px-6">
        {/* Page Title / Breadcrumb area */}
        <div>
          {/* Breadcrumbs can be added here */}
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-full">
            <BellIcon className="h-6 w-6" />
          </button>

          {/* User Menu */}
          <Menu as="div" className="relative">
            <Menu.Button className="flex items-center space-x-3 p-2 hover:bg-gray-100 rounded-lg">
              <div className="text-right hidden sm:block">
                <p className="text-sm font-medium text-gray-700">
                  {user?.full_name || user?.username}
                </p>
                <p className="text-xs text-gray-500">{user?.email}</p>
              </div>
              <UserCircleIcon className="h-8 w-8 text-gray-400" />
            </Menu.Button>

            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 mt-2 w-56 origin-top-right bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="py-1">
                  <div className="px-4 py-2 border-b border-gray-100">
                    <p className="text-sm font-medium text-gray-900">
                      {user?.full_name}
                    </p>
                    <p className="text-xs text-gray-500">{user?.email}</p>
                  </div>

                  <Menu.Item>
                    {({ active }) => (
                      <button
                        onClick={() => navigate('/profile')}
                        className={clsx(
                          'flex items-center w-full px-4 py-2 text-sm',
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700'
                        )}
                      >
                        <UserCircleIcon className="h-5 w-5 mr-3" />
                        Profile
                      </button>
                    )}
                  </Menu.Item>

                  <Menu.Item>
                    {({ active }) => (
                      <button
                        onClick={() => navigate('/settings')}
                        className={clsx(
                          'flex items-center w-full px-4 py-2 text-sm',
                          active ? 'bg-gray-100 text-gray-900' : 'text-gray-700'
                        )}
                      >
                        <Cog6ToothIcon className="h-5 w-5 mr-3" />
                        Settings
                      </button>
                    )}
                  </Menu.Item>

                  <div className="border-t border-gray-100">
                    <Menu.Item>
                      {({ active }) => (
                        <button
                          onClick={handleLogout}
                          className={clsx(
                            'flex items-center w-full px-4 py-2 text-sm',
                            active ? 'bg-gray-100 text-red-600' : 'text-red-600'
                          )}
                        >
                          <ArrowRightOnRectangleIcon className="h-5 w-5 mr-3" />
                          Sign out
                        </button>
                      )}
                    </Menu.Item>
                  </div>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </header>
  )
}
