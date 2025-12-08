import {
  CubeIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  ClipboardDocumentListIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline'
import { Card, CardBody, CardHeader } from '@/components/ui'
import { useAuthStore } from '@/store/authStore'

const stats = [
  {
    name: 'Total SKUs',
    value: '2,345',
    change: '+12%',
    changeType: 'increase',
    icon: CubeIcon,
  },
  {
    name: 'Inbound Today',
    value: '48',
    change: '+5%',
    changeType: 'increase',
    icon: ArrowDownTrayIcon,
  },
  {
    name: 'Outbound Today',
    value: '156',
    change: '-3%',
    changeType: 'decrease',
    icon: ArrowUpTrayIcon,
  },
  {
    name: 'Open Tasks',
    value: '23',
    change: '-8%',
    changeType: 'decrease',
    icon: ClipboardDocumentListIcon,
  },
]

const alerts = [
  {
    id: 1,
    type: 'warning',
    message: 'Low stock alert: SKU-1234 (Widget A) - 5 units remaining',
    time: '10 minutes ago',
  },
  {
    id: 2,
    type: 'error',
    message: 'Inbound delivery #IB-2024-001 delayed by 2 hours',
    time: '25 minutes ago',
  },
  {
    id: 3,
    type: 'success',
    message: 'Wave #W-2024-015 completed - 45 orders shipped',
    time: '1 hour ago',
  },
]

const recentTasks = [
  { id: 1, type: 'Pick', location: 'A-01-02-03', status: 'In Progress', user: 'John D.' },
  { id: 2, type: 'Putaway', location: 'B-03-01-05', status: 'Pending', user: 'Jane S.' },
  { id: 3, type: 'Count', location: 'C-02-04-01', status: 'Completed', user: 'Mike R.' },
  { id: 4, type: 'Pick', location: 'A-02-03-02', status: 'In Progress', user: 'Sarah L.' },
]

export function DashboardPage() {
  const { user } = useAuthStore()

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.first_name}!
        </h1>
        <p className="text-gray-600">Here's what's happening in your warehouse today.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardBody className="flex items-center">
              <div className="p-3 bg-primary-100 rounded-lg">
                <stat.icon className="h-6 w-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{stat.name}</p>
                <div className="flex items-baseline">
                  <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
                  <span
                    className={`ml-2 text-sm font-medium ${
                      stat.changeType === 'increase'
                        ? 'text-green-600'
                        : 'text-red-600'
                    }`}
                  >
                    {stat.change}
                  </span>
                </div>
              </div>
            </CardBody>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Alerts */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-gray-900">Recent Alerts</h2>
          </CardHeader>
          <CardBody className="divide-y divide-gray-100">
            {alerts.map((alert) => (
              <div key={alert.id} className="py-3 flex items-start">
                <div className="flex-shrink-0">
                  {alert.type === 'warning' && (
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
                  )}
                  {alert.type === 'error' && (
                    <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />
                  )}
                  {alert.type === 'success' && (
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  )}
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm text-gray-900">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{alert.time}</p>
                </div>
              </div>
            ))}
          </CardBody>
        </Card>

        {/* Recent Tasks */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-semibold text-gray-900">Recent Tasks</h2>
          </CardHeader>
          <CardBody className="p-0">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    User
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentTasks.map((task) => (
                  <tr key={task.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {task.type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {task.location}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          task.status === 'Completed'
                            ? 'bg-green-100 text-green-800'
                            : task.status === 'In Progress'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {task.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {task.user}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
