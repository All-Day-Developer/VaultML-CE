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
  <div class="max-w-4xl mx-auto">

    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
      <p class="text-gray-600 dark:text-gray-400 mt-2">
        Customize your VaultML experience with themes and personalization options.
      </p>
    </div>


    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border dark:border-gray-700 p-6 transition-colors">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-600 dark:text-indigo-400" fill="none" stroke="currentColor"
              viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4h4a2 2 0 002-2V5z">
              </path>
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Appearance</h2>
            <p class="text-sm text-gray-600 dark:text-gray-400">Customize how VaultML looks and feels</p>
          </div>
        </div>


        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Theme Mode
            </label>
            <div class="grid grid-cols-3 gap-3">

              <button @click="theme.setMode('light')" :class="[
                'relative flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all',
                theme.mode === 'light'
                  ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/50'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600'
              ]">
                <div class="w-8 h-8 mb-2 flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z">
                    </path>
                  </svg>
                </div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">Light</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Bright theme</div>
                <div v-if="theme.mode === 'light'"
                  class="absolute top-2 right-2 w-4 h-4 bg-indigo-500 rounded-full flex items-center justify-center">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setMode('dark')" :class="[
                'relative flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all',
                theme.mode === 'dark'
                  ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/50'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600'
              ]">
                <div class="w-8 h-8 mb-2 flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                  </svg>
                </div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">Dark</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Dark theme</div>
                <div v-if="theme.mode === 'dark'"
                  class="absolute top-2 right-2 w-4 h-4 bg-indigo-500 rounded-full flex items-center justify-center">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setMode('auto')" :class="[
                'relative flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all',
                theme.mode === 'auto'
                  ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/50'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600'
              ]">
                <div class="w-8 h-8 mb-2 flex items-center justify-center">
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z">
                    </path>
                  </svg>
                </div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">System</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">Follow OS</div>
                <div v-if="theme.mode === 'auto'"
                  class="absolute top-2 right-2 w-4 h-4 bg-indigo-500 rounded-full flex items-center justify-center">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>
            </div>
          </div>


          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Primary Color
            </label>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-3">

              <button @click="theme.setPrimaryColor('indigo')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-indigo-500',
                theme.primaryColor === 'indigo'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Indigo">
                <div v-if="theme.primaryColor === 'indigo'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setPrimaryColor('blue')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-blue-500',
                theme.primaryColor === 'blue'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Blue">
                <div v-if="theme.primaryColor === 'blue'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setPrimaryColor('purple')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-purple-500',
                theme.primaryColor === 'purple'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Purple">
                <div v-if="theme.primaryColor === 'purple'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setPrimaryColor('green')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-green-500',
                theme.primaryColor === 'green'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Green">
                <div v-if="theme.primaryColor === 'green'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setPrimaryColor('orange')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-orange-500',
                theme.primaryColor === 'orange'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Orange">
                <div v-if="theme.primaryColor === 'orange'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>


              <button @click="theme.setPrimaryColor('red')" :class="[
                'relative w-12 h-12 rounded-lg border-2 transition-all bg-red-500',
                theme.primaryColor === 'red'
                  ? 'border-gray-800 dark:border-white scale-110'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 hover:scale-105'
              ]" title="Red">
                <div v-if="theme.primaryColor === 'red'" class="absolute inset-0 flex items-center justify-center">
                  <svg class="w-6 h-6 text-white drop-shadow-lg" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      clip-rule="evenodd"></path>
                  </svg>
                </div>
              </button>
            </div>
          </div>


          <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Preview</h4>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <div :class="getPreviewColorClass()" class="w-4 h-4 rounded"></div>
                <span class="text-sm text-gray-600 dark:text-gray-400">Primary color</span>
              </div>
              <div class="flex items-center space-x-3">
                <button :class="getPreviewButtonClass()"
                  class="px-3 py-1.5 text-sm font-medium text-white rounded-md transition-colors">
                  Sample Button
                </button>
                <span class="text-sm text-gray-600 dark:text-gray-400">Button style</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="text-sm">
                  <span class="font-medium text-gray-900 dark:text-white">Current mode:</span>
                  <span :class="getPreviewTextClass()" class="ml-1 font-semibold">{{ theme.mode }}</span>
                  <span class="text-gray-500 dark:text-gray-400 ml-1">({{ theme.isDark ? 'dark' : 'light' }})</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border dark:border-gray-700 p-6 transition-colors">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 bg-gray-500 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Account</h2>
            <p class="text-sm text-gray-600 dark:text-gray-400">Manage your account settings</p>
          </div>
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <h3 class="font-medium text-gray-900 dark:text-white">User ID</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Your unique identifier</p>
            </div>
            <div class="text-sm font-mono text-gray-500 dark:text-gray-400">
              {{ auth.isLoggedIn ? 'Logged in' : 'Not logged in' }}
            </div>
          </div>

          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div>
              <h3 class="font-medium text-gray-900 dark:text-white">Session</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Your login session status</p>
            </div>
            <div class="flex items-center space-x-2">
              <div :class="auth.isLoggedIn ? 'bg-green-500' : 'bg-red-500'" class="w-2 h-2 rounded-full"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">
                {{ auth.isLoggedIn ? 'Active' : 'Inactive' }}
              </span>
            </div>
          </div>
        </div>
      </div>


      <div
        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border dark:border-gray-700 p-6 transition-colors lg:col-span-2">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 bg-gray-600 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">About VaultML</h2>
            <p class="text-sm text-gray-600 dark:text-gray-400">Information about your VaultML installation</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div>
              <h4 class="font-medium text-gray-900 dark:text-white mb-2">Version Info</h4>
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">VaultML CE</span>
                  <span class="text-sm font-mono text-gray-900 dark:text-white">2025.1.0</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Frontend</span>
                  <span class="text-sm font-mono text-gray-900 dark:text-white">Nuxt 4.0</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600 dark:text-gray-400">Backend</span>
                  <span class="text-sm font-mono text-gray-900 dark:text-white">FastAPI</span>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <h4 class="font-medium text-gray-900 dark:text-white mb-2">Resources</h4>
              <div class="space-y-2">
                <a href="https://github.com/vaultml/vaultml" target="_blank"
                  class="flex items-center space-x-2 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path
                      d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                  <span>GitHub Repository</span>
                </a>
                <a href="https://docs.vaultml.com" target="_blank"
                  class="flex items-center space-x-2 text-sm text-indigo-600 dark:text-indigo-400 hover:underline">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253">
                    </path>
                  </svg>
                  <span>Documentation</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Require authentication
definePageMeta({
  middleware: 'auth'
})

const theme = useThemeStore()
const auth = useAuthStore()

// Helper methods for preview section
const getPreviewColorClass = () => {
  const colorMap = {
    indigo: 'bg-indigo-500',
    blue: 'bg-blue-500',
    purple: 'bg-purple-500',
    green: 'bg-green-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500'
  }
  return colorMap[theme.primaryColor] || 'bg-indigo-500'
}

const getPreviewButtonClass = () => {
  const colorMap = {
    indigo: 'bg-indigo-500 hover:bg-indigo-600',
    blue: 'bg-blue-500 hover:bg-blue-600',
    purple: 'bg-purple-500 hover:bg-purple-600',
    green: 'bg-green-500 hover:bg-green-600',
    orange: 'bg-orange-500 hover:bg-orange-600',
    red: 'bg-red-500 hover:bg-red-600'
  }
  return colorMap[theme.primaryColor] || 'bg-indigo-500 hover:bg-indigo-600'
}

const getPreviewTextClass = () => {
  const colorMap = {
    indigo: 'text-indigo-600 dark:text-indigo-400',
    blue: 'text-blue-600 dark:text-blue-400',
    purple: 'text-purple-600 dark:text-purple-400',
    green: 'text-green-600 dark:text-green-400',
    orange: 'text-orange-600 dark:text-orange-400',
    red: 'text-red-600 dark:text-red-400'
  }
  return colorMap[theme.primaryColor] || 'text-indigo-600 dark:text-indigo-400'
}

// Set page title
useHead({
  title: 'Settings - VaultML'
})
</script>