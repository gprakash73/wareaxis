import { useEffect } from 'react'
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { MainLayout } from '@/components/layout'
import { LoginPage, RegisterPage, DashboardPage } from '@/pages'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/store/authStore'

// Protected route wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const location = useLocation()
  const { isAuthenticated, accessToken, setUser } = useAuthStore()

  // Fetch user data if authenticated but user is null
  const { data: user, isLoading } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
    enabled: isAuthenticated && !!accessToken,
    retry: false,
  })

  useEffect(() => {
    if (user) {
      setUser(user)
    }
  }, [user, setUser])

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return <>{children}</>
}

// Public route wrapper (redirects to dashboard if already logged in)
function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return <>{children}</>
}

// Placeholder pages
function PlaceholderPage({ title }: { title: string }) {
  return (
    <div className="flex items-center justify-center h-64">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        <p className="text-gray-500 mt-2">This page is coming soon</p>
      </div>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Protected routes */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<DashboardPage />} />
          <Route path="/inventory" element={<PlaceholderPage title="Inventory" />} />
          <Route path="/inbound" element={<PlaceholderPage title="Inbound" />} />
          <Route path="/outbound" element={<PlaceholderPage title="Outbound" />} />
          <Route path="/tasks" element={<PlaceholderPage title="Tasks" />} />
          <Route path="/reports" element={<PlaceholderPage title="Reports" />} />
          <Route path="/profile" element={<PlaceholderPage title="Profile" />} />
          <Route path="/settings" element={<PlaceholderPage title="Settings" />} />

          {/* Admin routes */}
          <Route path="/admin/users" element={<PlaceholderPage title="User Management" />} />
          <Route path="/admin/settings" element={<PlaceholderPage title="System Settings" />} />
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
