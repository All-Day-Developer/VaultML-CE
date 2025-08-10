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
  <div class="fixed inset-0 z-50 pointer-events-none">
    <div class="flex flex-col items-end justify-start min-h-screen p-4 sm:p-6 space-y-4">
      <TransitionGroup
        name="notification"
        tag="div"
        class="space-y-4"
        enter-active-class="transition duration-500 ease-out"
        enter-from-class="transform translate-x-full scale-95 opacity-0"
        enter-to-class="transform translate-x-0 scale-100 opacity-100"
        leave-active-class="transition duration-300 ease-in"
        leave-from-class="transform translate-x-0 scale-100 opacity-100"
        leave-to-class="transform translate-x-full scale-95 opacity-0"
      >
        <div
          v-for="notification in notifications.notifications"
          :key="notification.id"
          class="pointer-events-auto w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl"
          style="max-width: min(40vw, 672px); min-width: 320px;"
        >
          <div
            :class="[
              'rounded-xl shadow-xl border p-6 transition-all duration-200 backdrop-blur-sm',
              notificationClasses(notification.type)
            ]"
          >
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <svg v-if="notification.type === 'success'" :class="iconClasses(notification.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <svg v-else-if="notification.type === 'error'" :class="iconClasses(notification.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <svg v-else-if="notification.type === 'warning'" :class="iconClasses(notification.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <svg v-else :class="iconClasses(notification.type)" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-3 w-0 flex-1">
                <p :class="['text-base font-semibold', textClasses(notification.type)]">
                  {{ notification.title }}
                </p>
                <p v-if="notification.message" :class="['mt-2 text-sm leading-relaxed', subtextClasses(notification.type)]">
                  {{ notification.message }}
                </p>
                <div v-if="notification.actions && notification.actions.length > 0" class="mt-4 flex space-x-3">
                  <button
                    v-for="action in notification.actions"
                    :key="action.label"
                    @click="action.action"
                    :class="[
                      'text-sm font-medium px-4 py-2 rounded-lg transition-all duration-200 hover:scale-105',
                      action.type === 'primary' ? primaryActionClasses(notification.type) : secondaryActionClasses(notification.type)
                    ]"
                  >
                    {{ action.label }}
                  </button>
                </div>
              </div>
              <div class="ml-4 flex-shrink-0 flex">
                <button
                  @click="notifications.removeNotification(notification.id)"
                  :class="['rounded-lg inline-flex p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200']"
                >
                  <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '~/stores/notifications'

const notifications = useNotificationStore()

const notificationClasses = (type: string) => {
  switch (type) {
    case 'success':
      return 'bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/60 dark:to-emerald-900/60 border-green-300 dark:border-green-700 shadow-green-100 dark:shadow-green-900/30'
    case 'error':
      return 'bg-gradient-to-r from-red-50 to-rose-50 dark:from-red-900/60 dark:to-rose-900/60 border-red-300 dark:border-red-700 shadow-red-100 dark:shadow-red-900/30'
    case 'warning':
      return 'bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/60 dark:to-amber-900/60 border-yellow-300 dark:border-yellow-700 shadow-yellow-100 dark:shadow-yellow-900/30'
    case 'info':
      return 'bg-gradient-to-r from-blue-50 to-sky-50 dark:from-blue-900/60 dark:to-sky-900/60 border-blue-300 dark:border-blue-700 shadow-blue-100 dark:shadow-blue-900/30'
    default:
      return 'bg-gradient-to-r from-white to-gray-50 dark:from-gray-800 dark:to-gray-700 border-gray-300 dark:border-gray-600 shadow-gray-100 dark:shadow-gray-900/30'
  }
}

const iconClasses = (type: string) => {
  const base = 'h-6 w-6'
  switch (type) {
    case 'success':
      return `${base} text-green-500 dark:text-green-400`
    case 'error':
      return `${base} text-red-500 dark:text-red-400`
    case 'warning':
      return `${base} text-yellow-500 dark:text-yellow-400`
    case 'info':
      return `${base} text-blue-500 dark:text-blue-400`
    default:
      return `${base} text-gray-500 dark:text-gray-400`
  }
}

const textClasses = (type: string) => {
  switch (type) {
    case 'success':
      return 'text-green-800 dark:text-green-200'
    case 'error':
      return 'text-red-800 dark:text-red-200'
    case 'warning':
      return 'text-yellow-800 dark:text-yellow-200'
    case 'info':
      return 'text-blue-800 dark:text-blue-200'
    default:
      return 'text-gray-800 dark:text-gray-200'
  }
}

const subtextClasses = (type: string) => {
  switch (type) {
    case 'success':
      return 'text-green-700 dark:text-green-300'
    case 'error':
      return 'text-red-700 dark:text-red-300'
    case 'warning':
      return 'text-yellow-700 dark:text-yellow-300'
    case 'info':
      return 'text-blue-700 dark:text-blue-300'
    default:
      return 'text-gray-700 dark:text-gray-300'
  }
}

const primaryActionClasses = (type: string) => {
  switch (type) {
    case 'success':
      return 'bg-green-600 dark:bg-green-500 text-white shadow-lg hover:bg-green-700 dark:hover:bg-green-600 hover:shadow-xl'
    case 'error':
      return 'bg-red-600 dark:bg-red-500 text-white shadow-lg hover:bg-red-700 dark:hover:bg-red-600 hover:shadow-xl'
    case 'warning':
      return 'bg-yellow-600 dark:bg-yellow-500 text-white shadow-lg hover:bg-yellow-700 dark:hover:bg-yellow-600 hover:shadow-xl'
    case 'info':
      return 'bg-blue-600 dark:bg-blue-500 text-white shadow-lg hover:bg-blue-700 dark:hover:bg-blue-600 hover:shadow-xl'
    default:
      return 'bg-gray-600 dark:bg-gray-500 text-white shadow-lg hover:bg-gray-700 dark:hover:bg-gray-600 hover:shadow-xl'
  }
}

const secondaryActionClasses = (type: string) => {
  return 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 hover:text-gray-900 dark:hover:text-white'
}
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>