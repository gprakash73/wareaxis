import { Link } from 'react-router-dom'
import {
  CubeIcon,
  TruckIcon,
  ChartBarIcon,
  DevicePhoneMobileIcon,
  CloudIcon,
  ShieldCheckIcon,
  ArrowPathIcon,
  BoltIcon,
  GlobeAltIcon,
  CheckCircleIcon,
  ArrowRightIcon,
} from '@heroicons/react/24/outline'

const features = [
  {
    name: 'Inventory Management',
    description:
      'Real-time stock tracking across multiple warehouses with batch, serial, and handling unit support.',
    icon: CubeIcon,
  },
  {
    name: 'Inbound & Outbound',
    description:
      'Streamlined receiving, put-away, picking, packing, and shipping workflows with barcode scanning.',
    icon: TruckIcon,
  },
  {
    name: 'Task Management',
    description:
      'Intelligent task assignment based on skills, proximity, and workload with real-time tracking.',
    icon: ArrowPathIcon,
  },
  {
    name: 'Mobile & RF Ready',
    description:
      'Native mobile apps and RF scanner support with offline mode for uninterrupted operations.',
    icon: DevicePhoneMobileIcon,
  },
  {
    name: 'ERP Integration',
    description:
      'Seamless integration with SAP, Oracle, Dynamics and other ERPs via configurable middleware.',
    icon: CloudIcon,
  },
  {
    name: 'Analytics & AI',
    description:
      'Predictive analytics, demand forecasting, and AI-powered optimization for smarter decisions.',
    icon: ChartBarIcon,
  },
]

const benefits = [
  'Multi-tenant SaaS architecture',
  'Schema-based data isolation',
  'Role-based access control',
  'SSO with SAML2, OAuth2, Azure AD',
  'Real-time inventory visibility',
  'Configurable movement types',
  'Wave & batch picking',
  'Carrier integration (DHL, UPS, FedEx)',
  '99.9% uptime SLA',
  '24/7 support available',
]

const pricingPlans = [
  {
    name: 'Starter',
    price: '499',
    description: 'Perfect for small warehouses getting started',
    features: [
      'Up to 5,000 SKUs',
      '3 user accounts',
      '1 warehouse',
      'Basic reporting',
      'Email support',
      'Mobile app access',
    ],
    cta: 'Start Free Trial',
    highlighted: false,
  },
  {
    name: 'Professional',
    price: '1,299',
    description: 'For growing businesses with complex needs',
    features: [
      'Up to 50,000 SKUs',
      '15 user accounts',
      '3 warehouses',
      'Advanced analytics',
      'ERP integration',
      'Priority support',
      'Custom fields',
      'API access',
    ],
    cta: 'Start Free Trial',
    highlighted: true,
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'For large operations requiring full customization',
    features: [
      'Unlimited SKUs',
      'Unlimited users',
      'Unlimited warehouses',
      'AI-powered optimization',
      'Dedicated middleware',
      '24/7 phone support',
      'Custom integrations',
      'On-premise option',
      'SLA guarantee',
    ],
    cta: 'Contact Sales',
    highlighted: false,
  },
]

export function LandingPage() {
  return (
    <div className="bg-white">
      {/* Navigation */}
      <nav className="fixed w-full bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <TruckIcon className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">WMS Pro</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900">
                Features
              </a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900">
                Pricing
              </a>
              <a href="#contact" className="text-gray-600 hover:text-gray-900">
                Contact
              </a>
              <Link
                to="/login"
                className="text-gray-600 hover:text-gray-900 font-medium"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 bg-gradient-to-br from-primary-50 via-white to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center px-3 py-1 rounded-full bg-primary-100 text-primary-700 text-sm font-medium mb-6">
                <BoltIcon className="h-4 w-4 mr-2" />
                Now with AI-Powered Optimization
              </div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Modern Warehouse Management,{' '}
                <span className="text-primary-600">Simplified</span>
              </h1>
              <p className="mt-6 text-xl text-gray-600 leading-relaxed">
                Streamline your warehouse operations with our cloud-native WMS.
                Real-time inventory, smart task management, and seamless ERP
                integration — all in one powerful platform.
              </p>
              <div className="mt-8 flex flex-col sm:flex-row gap-4">
                <Link
                  to="/register"
                  className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Start Free Trial
                  <ArrowRightIcon className="ml-2 h-5 w-5" />
                </Link>
                <a
                  href="#demo"
                  className="inline-flex items-center justify-center px-6 py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:border-gray-400 transition-colors"
                >
                  Watch Demo
                </a>
              </div>
              <div className="mt-8 flex items-center gap-6 text-sm text-gray-500">
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                  14-day free trial
                </div>
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                  No credit card required
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-white rounded-2xl shadow-2xl p-4 border border-gray-200">
                <div className="bg-gray-100 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="font-semibold text-gray-900">Dashboard</h3>
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 rounded-full bg-red-400"></div>
                      <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                      <div className="w-3 h-3 rounded-full bg-green-400"></div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-xs text-gray-500">Total SKUs</p>
                      <p className="text-2xl font-bold text-gray-900">12,458</p>
                      <p className="text-xs text-green-600">+12% this month</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-xs text-gray-500">Orders Today</p>
                      <p className="text-2xl font-bold text-gray-900">847</p>
                      <p className="text-xs text-green-600">+8% vs yesterday</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-xs text-gray-500">Pick Rate</p>
                      <p className="text-2xl font-bold text-gray-900">98.2%</p>
                      <p className="text-xs text-green-600">Above target</p>
                    </div>
                    <div className="bg-white p-4 rounded-lg shadow-sm">
                      <p className="text-xs text-gray-500">Active Tasks</p>
                      <p className="text-2xl font-bold text-gray-900">156</p>
                      <p className="text-xs text-blue-600">23 in progress</p>
                    </div>
                  </div>
                </div>
              </div>
              {/* Decorative elements */}
              <div className="absolute -z-10 -top-4 -right-4 w-72 h-72 bg-primary-200 rounded-full opacity-20 blur-3xl"></div>
              <div className="absolute -z-10 -bottom-4 -left-4 w-72 h-72 bg-blue-200 rounded-full opacity-20 blur-3xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Logos Section */}
      <section className="py-12 bg-gray-50 border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500 mb-8">
            Trusted by leading companies worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-12 opacity-50">
            <div className="text-2xl font-bold text-gray-400">SAP</div>
            <div className="text-2xl font-bold text-gray-400">Oracle</div>
            <div className="text-2xl font-bold text-gray-400">Microsoft</div>
            <div className="text-2xl font-bold text-gray-400">Shopify</div>
            <div className="text-2xl font-bold text-gray-400">DHL</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Everything you need to run your warehouse
            </h2>
            <p className="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
              From receiving to shipping, WMS Pro handles every aspect of your
              warehouse operations with powerful automation and real-time visibility.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature) => (
              <div
                key={feature.name}
                className="bg-white p-6 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-lg transition-all"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.name}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-secondary-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
                Built for enterprise, priced for everyone
              </h2>
              <p className="text-lg text-secondary-300 mb-8">
                WMS Pro combines enterprise-grade features with an intuitive
                interface that your team will actually want to use. No lengthy
                implementations, no complex training required.
              </p>
              <div className="grid sm:grid-cols-2 gap-4">
                {benefits.map((benefit) => (
                  <div key={benefit} className="flex items-center">
                    <CheckCircleIcon className="h-5 w-5 text-green-400 mr-3 flex-shrink-0" />
                    <span className="text-secondary-200">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-secondary-800 rounded-2xl p-8">
                <div className="flex items-center mb-6">
                  <GlobeAltIcon className="h-10 w-10 text-primary-400" />
                  <div className="ml-4">
                    <h3 className="text-white font-semibold">Global Ready</h3>
                    <p className="text-secondary-400">Multi-region deployment</p>
                  </div>
                </div>
                <div className="flex items-center mb-6">
                  <ShieldCheckIcon className="h-10 w-10 text-green-400" />
                  <div className="ml-4">
                    <h3 className="text-white font-semibold">Enterprise Security</h3>
                    <p className="text-secondary-400">SOC 2 Type II compliant</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <BoltIcon className="h-10 w-10 text-yellow-400" />
                  <div className="ml-4">
                    <h3 className="text-white font-semibold">Lightning Fast</h3>
                    <p className="text-secondary-400">&lt;100ms response time</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Simple, transparent pricing
            </h2>
            <p className="mt-4 text-xl text-gray-600">
              Choose the plan that fits your warehouse size and needs
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {pricingPlans.map((plan) => (
              <div
                key={plan.name}
                className={`bg-white rounded-2xl p-8 ${
                  plan.highlighted
                    ? 'border-2 border-primary-500 shadow-xl scale-105'
                    : 'border border-gray-200'
                }`}
              >
                {plan.highlighted && (
                  <div className="text-center mb-4">
                    <span className="bg-primary-100 text-primary-700 text-sm font-medium px-3 py-1 rounded-full">
                      Most Popular
                    </span>
                  </div>
                )}
                <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                <p className="text-gray-500 mt-2">{plan.description}</p>
                <div className="mt-6 mb-8">
                  {plan.price === 'Custom' ? (
                    <span className="text-4xl font-bold text-gray-900">Custom</span>
                  ) : (
                    <>
                      <span className="text-4xl font-bold text-gray-900">
                        ${plan.price}
                      </span>
                      <span className="text-gray-500">/month</span>
                    </>
                  )}
                </div>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Link
                  to={plan.price === 'Custom' ? '#contact' : '/register'}
                  className={`block text-center py-3 rounded-lg font-semibold transition-colors ${
                    plan.highlighted
                      ? 'bg-primary-600 text-white hover:bg-primary-700'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {plan.cta}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6">
            Ready to transform your warehouse operations?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of warehouses already using WMS Pro to streamline
            their operations and boost productivity.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-primary-50 transition-colors"
            >
              Start Your Free Trial
              <ArrowRightIcon className="ml-2 h-5 w-5" />
            </Link>
            <a
              href="#contact"
              className="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors"
            >
              Talk to Sales
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="bg-secondary-900 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <TruckIcon className="h-8 w-8 text-primary-500" />
                <span className="ml-2 text-xl font-bold text-white">WMS Pro</span>
              </div>
              <p className="text-secondary-400">
                Modern warehouse management for the modern enterprise.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#features" className="text-secondary-400 hover:text-white">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#pricing" className="text-secondary-400 hover:text-white">
                    Pricing
                  </a>
                </li>
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    Integrations
                  </a>
                </li>
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    API Docs
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    About
                  </a>
                </li>
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    Blog
                  </a>
                </li>
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    Careers
                  </a>
                </li>
                <li>
                  <a href="#" className="text-secondary-400 hover:text-white">
                    Contact
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Contact Us</h4>
              <ul className="space-y-2 text-secondary-400">
                <li>sales@wmspro.io</li>
                <li>support@wmspro.io</li>
                <li>+1 (555) 123-4567</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-secondary-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-secondary-400">
              &copy; 2024 WMS Pro. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-secondary-400 hover:text-white">
                Privacy Policy
              </a>
              <a href="#" className="text-secondary-400 hover:text-white">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
