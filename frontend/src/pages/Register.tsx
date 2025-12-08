import { useNavigate, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { TruckIcon } from '@heroicons/react/24/outline'

import { Button, Input, Card, CardBody } from '@/components/ui'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/store/authStore'
import type { TenantRegistration } from '@/types'

export function RegisterPage() {
  const navigate = useNavigate()
  const { login } = useAuthStore()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<TenantRegistration & { confirm_password: string }>({
    defaultValues: {
      tenant_name: '',
      tenant_slug: '',
      contact_email: '',
      admin_email: '',
      admin_username: '',
      admin_password: '',
      confirm_password: '',
      admin_first_name: '',
      admin_last_name: '',
    },
  })

  const password = watch('admin_password')

  const registerMutation = useMutation({
    mutationFn: (data: TenantRegistration) => authApi.register(data),
    onSuccess: (response) => {
      const { tenant, user, tokens } = response
      login(user, tokens.access_token, tokens.refresh_token, tenant.slug)
      toast.success('Organization registered successfully!')
      navigate('/')
    },
    onError: (error: any) => {
      const message = error.response?.data?.detail || 'Registration failed'
      toast.error(message)
    },
  })

  const onSubmit = (data: TenantRegistration & { confirm_password: string }) => {
    const { confirm_password, ...registrationData } = data
    registerMutation.mutate(registrationData)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-lg w-full">
        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
          <div className="flex items-center">
            <TruckIcon className="h-12 w-12 text-primary-600" />
            <span className="ml-2 text-3xl font-bold text-gray-900">WMS Pro</span>
          </div>
          <p className="mt-2 text-gray-600">Register your organization</p>
        </div>

        <Card>
          <CardBody className="p-8">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Organization Info */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Organization Details
                </h3>
                <div className="space-y-4">
                  <Input
                    label="Organization Name"
                    placeholder="Acme Logistics"
                    {...register('tenant_name', {
                      required: 'Organization name is required',
                      minLength: { value: 2, message: 'Min 2 characters' },
                    })}
                    error={errors.tenant_name?.message}
                  />

                  <Input
                    label="Organization ID"
                    placeholder="acme-logistics"
                    {...register('tenant_slug', {
                      required: 'Organization ID is required',
                      pattern: {
                        value: /^[a-z0-9][a-z0-9-]*[a-z0-9]$/,
                        message: 'Lowercase letters, numbers, and hyphens only',
                      },
                    })}
                    error={errors.tenant_slug?.message}
                    helpText="This will be used to identify your organization"
                  />

                  <Input
                    label="Contact Email"
                    type="email"
                    placeholder="contact@acme.com"
                    {...register('contact_email', {
                      required: 'Contact email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address',
                      },
                    })}
                    error={errors.contact_email?.message}
                  />
                </div>
              </div>

              {/* Admin User Info */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Administrator Account
                </h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <Input
                      label="First Name"
                      placeholder="John"
                      {...register('admin_first_name', {
                        required: 'First name is required',
                      })}
                      error={errors.admin_first_name?.message}
                    />

                    <Input
                      label="Last Name"
                      placeholder="Doe"
                      {...register('admin_last_name', {
                        required: 'Last name is required',
                      })}
                      error={errors.admin_last_name?.message}
                    />
                  </div>

                  <Input
                    label="Email"
                    type="email"
                    placeholder="john.doe@acme.com"
                    {...register('admin_email', {
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address',
                      },
                    })}
                    error={errors.admin_email?.message}
                  />

                  <Input
                    label="Username"
                    placeholder="johndoe"
                    {...register('admin_username', {
                      required: 'Username is required',
                      minLength: { value: 3, message: 'Min 3 characters' },
                      pattern: {
                        value: /^[a-zA-Z0-9_]+$/,
                        message: 'Letters, numbers, and underscores only',
                      },
                    })}
                    error={errors.admin_username?.message}
                  />

                  <Input
                    label="Password"
                    type="password"
                    placeholder="********"
                    {...register('admin_password', {
                      required: 'Password is required',
                      minLength: { value: 8, message: 'Min 8 characters' },
                      pattern: {
                        value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                        message: 'Must include uppercase, lowercase, and number',
                      },
                    })}
                    error={errors.admin_password?.message}
                  />

                  <Input
                    label="Confirm Password"
                    type="password"
                    placeholder="********"
                    {...register('confirm_password', {
                      required: 'Please confirm password',
                      validate: (value) =>
                        value === password || 'Passwords do not match',
                    })}
                    error={errors.confirm_password?.message}
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full"
                loading={registerMutation.isPending}
              >
                Create Organization
              </Button>
            </form>
          </CardBody>
        </Card>

        <p className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link
            to="/login"
            className="text-primary-600 hover:text-primary-700 font-medium"
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
