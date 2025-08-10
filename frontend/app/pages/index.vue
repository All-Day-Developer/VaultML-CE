<!--
Copyright (C) 2025 All-Day Developer Marcin Wawrzków
contributor: Marcin Wawrzków

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
-->

<template>
  <div>
    
    <div v-if="!auth.isLoggedIn" :class="`min-h-screen bg-gradient-to-br from-${theme.colorClasses.primaryLight} via-white dark:via-gray-900 to-cyan-50 dark:to-gray-800 transition-colors`">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            Welcome to <span :class="`text-${theme.colorClasses.primary}`">VaultML</span>
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-3xl mx-auto">
            A powerful model repository system for managing your machine learning models with versioning, 
            aliasing, and S3-compatible storage. Organize your models by groups and variants with ease.
          </p>
          
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <NuxtLink
              to="/login"
              :class="`inline-flex items-center px-6 py-3 bg-${theme.colorClasses.primary} text-white font-semibold rounded-lg shadow-lg hover:bg-${theme.colorClasses.primaryHover} transition-all transform hover:scale-105`"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
              </svg>
              Sign In
            </NuxtLink>
            <NuxtLink
              to="/models"
              class="inline-flex items-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-all"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
              Browse Models
            </NuxtLink>
          </div>
        </div>

        
        <div class="mt-24">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Key Features</h2>
            <p class="text-lg text-gray-600 dark:text-gray-400">Everything you need to manage your ML models effectively</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 text-center transition-colors">
              <div :class="`w-12 h-12 bg-${theme.colorClasses.bg} rounded-lg flex items-center justify-center mx-auto mb-4`">
                <svg :class="`w-6 h-6 text-${theme.colorClasses.text}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Model Groups</h3>
              <p class="text-gray-600 dark:text-gray-400">Organize models by families (e.g., Bielik, Llama) with variants (7b, 13b)</p>
            </div>

            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 text-center transition-colors">
              <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Version & Tags</h3>
              <p class="text-gray-600 dark:text-gray-400">Track versions and use aliases like @prod, @latest for easy deployment</p>
            </div>

            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 text-center transition-colors">
              <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">S3 Storage</h3>
              <p class="text-gray-600 dark:text-gray-400">Scalable object storage with MinIO/S3 compatibility for your models</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    <div v-else class="space-y-6 sm:space-y-8">
      
      <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
              <p class="mt-1 text-gray-600 dark:text-gray-400">Welcome back! Here's your ModelHub overview.</p>
            </div>
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              <NuxtLink
                to="/models/new-model"
                :class="`inline-flex items-center justify-center px-4 py-2 bg-${theme.colorClasses.primary} text-white font-semibold rounded-lg shadow hover:bg-${theme.colorClasses.primaryHover} transition`"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                New Model
              </NuxtLink>
              <NuxtLink
                to="/models"
                class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                ModelHub
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      
      <div v-if="pending" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-center py-12">
          <div :class="`animate-spin rounded-full h-8 w-8 border-b-2 border-${theme.colorClasses.primary}`"></div>
          <span class="ml-3 text-gray-500 dark:text-gray-400">Loading dashboard...</span>
        </div>
      </div>

      
      <div v-else-if="error" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-red-700 dark:text-red-300">Failed to load dashboard data</span>
          </div>
        </div>
      </div>

      
      <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6 sm:space-y-8">
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div :class="`w-10 h-10 bg-${theme.colorClasses.bg} rounded-lg flex items-center justify-center`">
                  <svg :class="`w-6 h-6 text-${theme.colorClasses.text}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Models</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats?.totals.models || 0 }}</p>
              </div>
            </div>
            <div class="mt-4">
              <div class="flex items-center text-sm">
                <span class="text-green-600 dark:text-green-400 font-medium">+{{ stats?.recent.models || 0 }}</span>
                <span class="text-gray-500 dark:text-gray-400 ml-1">last 7 days</span>
              </div>
            </div>
          </div>

          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Model Groups</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats?.totals.groups || 0 }}</p>
              </div>
            </div>
            <div class="mt-4">
              <div class="text-sm text-gray-500 dark:text-gray-400">
                Unique model families
              </div>
            </div>
          </div>

          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Versions</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats?.totals.versions || 0 }}</p>
              </div>
            </div>
            <div class="mt-4">
              <div class="flex items-center text-sm">
                <span class="text-green-600 dark:text-green-400 font-medium">+{{ stats?.recent.versions || 0 }}</span>
                <span class="text-gray-500 dark:text-gray-400 ml-1">last 7 days</span>
              </div>
            </div>
          </div>

          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                  <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                  </svg>
                </div>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Tags</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats?.totals.aliases || 0 }}</p>
              </div>
            </div>
            <div class="mt-4">
              <div class="text-sm text-gray-500 dark:text-gray-400">
                Model aliases & tags
              </div>
            </div>
          </div>
        </div>

        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
            <div class="px-4 sm:px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Top Model Groups</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">By version count</p>
            </div>
            <div class="p-4 sm:p-6">
              <div v-if="stats?.top_groups.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-8">
                <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                <p class="mt-2 text-sm">No model groups yet</p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="(group, index) in stats?.top_groups"
                  :key="group.group_name"
                  class="flex items-center justify-between"
                >
                  <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                      <div :class="`w-8 h-8 bg-${theme.colorClasses.bg} rounded-lg flex items-center justify-center`">
                        <span :class="`text-sm font-medium text-${theme.colorClasses.text}`">{{ index + 1 }}</span>
                      </div>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">{{ group.group_name }}</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ group.version_count }} versions</p>
                    </div>
                  </div>
                  <div class="flex items-center">
                    <div class="w-20 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        :class="`bg-${theme.colorClasses.primary} h-2 rounded-full transition-all`"
                        :style="{ width: `${(group.version_count / Math.max(...(stats?.top_groups.map(g => g.version_count) || [1]))) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
            <div class="px-4 sm:px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Activity</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">Latest models and versions</p>
            </div>
            <div class="p-4 sm:p-6">
              <div v-if="(stats?.latest_models.length || 0) === 0 && (stats?.latest_versions.length || 0) === 0" class="text-center text-gray-500 dark:text-gray-400 py-8">
                <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <p class="mt-2 text-sm">No recent activity</p>
              </div>
              <div v-else class="space-y-4">
                
                <div v-for="model in stats?.latest_models.slice(0, 3)" :key="model.name">
                  <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                      <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                        <svg class="w-4 h-4 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                        New model: {{ model.group_name }}:{{ model.variant }}
                      </p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(model.created_at) }}</p>
                    </div>
                  </div>
                </div>

                
                <div v-for="version in stats?.latest_versions.slice(0, 2)" :key="`${version.model_name}-${version.version}`">
                  <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                      <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                        <svg class="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                        </svg>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {{ version.group_name }}:{{ version.variant }} v{{ version.version }}
                      </p>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(version.created_at) }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <NuxtLink
              to="/models/new-model"
              :class="`flex items-center p-4 bg-${theme.colorClasses.primaryLight} hover:bg-${theme.colorClasses.bg} dark:bg-${theme.colorClasses.primaryDark} dark:hover:bg-${theme.colorClasses.primaryDark}/80 rounded-lg transition-colors group`"
            >
              <div :class="`w-10 h-10 bg-${theme.colorClasses.bg} group-hover:bg-${theme.colorClasses.primary} dark:bg-${theme.colorClasses.primary} dark:group-hover:bg-${theme.colorClasses.primaryHover} rounded-lg flex items-center justify-center mr-4 transition-colors`">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Create New Model</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Start a new model group</p>
              </div>
            </NuxtLink>

            <NuxtLink
              to="/models"
              class="flex items-center p-4 bg-purple-50 hover:bg-purple-100 dark:bg-purple-900/50 dark:hover:bg-purple-900/70 rounded-lg transition-colors group"
            >
              <div class="w-10 h-10 bg-purple-100 group-hover:bg-purple-200 dark:bg-purple-700 dark:group-hover:bg-purple-600 rounded-lg flex items-center justify-center mr-4 transition-colors">
                <svg class="w-5 h-5 text-purple-600 dark:text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Browse ModelHub</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">View all models</p>
              </div>
            </NuxtLink>

            <button
              @click="refreshData"
              class="flex items-center p-4 bg-green-50 hover:bg-green-100 dark:bg-green-900/50 dark:hover:bg-green-900/70 rounded-lg transition-colors group"
            >
              <div class="w-10 h-10 bg-green-100 group-hover:bg-green-200 dark:bg-green-700 dark:group-hover:bg-green-600 rounded-lg flex items-center justify-center mr-4 transition-colors">
                <svg class="w-5 h-5 text-green-600 dark:text-green-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                </svg>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900 dark:text-white">Refresh Data</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">Update statistics</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const auth = useAuthStore()
const theme = useThemeStore()


type DashboardStats = {
  totals: {
    models: number
    groups: number
    versions: number
    aliases: number
  }
  recent: {
    models: number
    versions: number
  }
  top_groups: Array<{
    group_name: string
    version_count: number
  }>
  latest_models: Array<{
    name: string
    group_name: string
    variant: string
    description: string
    created_at: string
  }>
  latest_versions: Array<{
    model_name: string
    group_name: string
    variant: string
    version: number
    created_at: string
  }>
}


const { data: stats, pending, error, refresh } = await useFetch<DashboardStats>(
  `${config.public.apiBase}/dashboard/stats`,
  {
    credentials: "include",
    default: () => null,
    server: false, 
    lazy: true,
  }
)

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return "Unknown"
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return "Today"
  if (diffDays <= 7) return `${diffDays} days ago`
  return date.toLocaleDateString()
}

const refreshData = async () => {
  await refresh()
}


useHead({
  title: 'VaultML - Dashboard'
})
</script>