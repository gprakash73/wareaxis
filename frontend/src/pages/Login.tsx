import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { TruckIcon } from '@heroicons/react/24/outline'

import { Button, Input, Card, CardBody } from '@/components/ui'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/store/authStore'
import type { LoginRequest } from '@/types'

export function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuthStore()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>({
    defaultValues: {
      username: '',
      password: '',
      tenant_slug: '',
    },
  })

  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: async (tokens, variables) => {
      // Set tokens first
      useAuthStore.getState().setTokens(tokens.access_token, tokens.refresh_token)
      useAuthStore.getState().setTenantSlug(variables.tenant_slug)

      // Fetch user data
      try {
        const user = await authApi.getCurrentUser()
        login(user, tokens.access_token, tokens.refresh_token, variables.tenant_slug)
        toast.success('Welcome back!')
        navigate('/')
      } catch (error) {
        toast.error('Failed to fetch user data')
      }
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || 'Login failed'
      toast.error(message)
    },
  })

  const onSubmit = (data: LoginRequest) => {
    loginMutation.mutate(data)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="flex items-center">
            <TruckIcon className="h-12 w-12 text-primary-600" />
            <span className="ml-2 text-3xl font-bold text-gray-900">WMS Pro</span>
          </div>
          <p className="mt-2 text-gray-600">Warehouse Management System</p>
        </div>

        <Card>
          <CardBody className="p-8">
            <h2 className="text-2xl font-bold text-gray-900 text-center mb-6">
              Sign in to your account
            </h2>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
              <Input
                label="Organization"
                placeholder="your-company"
                {...register('tenant_slug', {
                  required: 'Organization is required',
                })}
                error={errors.tenant_slug?.message}
                helpText="Enter your organization's identifier"
              />

              <Input
                label="Username or Email"
                placeholder="Enter your username or email"
                {...register('username', {
                  required: 'Username is required',
                })}
                error={errors.username?.message}
              />

              <Input
                label="Password"
                type="password"
                placeholder="Enter your password"
                {...register('password', {
                  required: 'Password is required',
                })}
                error={errors.password?.message}
              />

              <Button
                type="submit"
                className="w-full"
                loading={loginMutation.isPending}
              >
                Sign in
              </Button>
            </form>

            <div className="mt-6 text-center">
              <Link
                to="/forgot-password"
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Forgot your password?
              </Link>
            </div>
          </CardBody>
        </Card>

        <p className="mt-6 text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <Link
            to="/register"
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Register your organization
          </Link>
        </p>
      </div>
    </div>
  )
}
