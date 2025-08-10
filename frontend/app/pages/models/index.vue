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
  <div class="space-y-6">
    
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">ModelHub</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-1">Manage your machine learning models</p>
      </div>

      <NuxtLink
        v-if="auth.isLoggedIn"
        to="/models/new-model"
        :class="`inline-flex items-center px-4 py-2 bg-${theme.colorClasses.primary} text-white font-semibold rounded-lg shadow hover:bg-${theme.colorClasses.primaryHover} transition`"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        New Model
      </NuxtLink>
    </div>

    
    <div v-if="pending" class="flex items-center justify-center py-12">
      <div :class="`animate-spin rounded-full h-8 w-8 border-b-2 border-${theme.colorClasses.primary}`"></div>
      <span class="ml-3 text-gray-500 dark:text-gray-400">Loading models...</span>
    </div>

    
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-red-700 dark:text-red-300">Failed to load models</span>
      </div>
    </div>

    
    <div v-else-if="modelGroups.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No models yet</h3>
      <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Get started by creating your first model.</p>
      <div class="mt-6" v-if="auth.isLoggedIn">
        <NuxtLink
          to="/models/new-model"
          :class="`inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-${theme.colorClasses.primary} hover:bg-${theme.colorClasses.primaryHover}`"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          New Model
        </NuxtLink>
      </div>
    </div>

    
    <div v-else class="block md:hidden space-y-4">
      <div
        v-for="group in modelGroups"
        :key="group.group_name"
        class="bg-white dark:bg-gray-800 shadow-sm border dark:border-gray-700 rounded-lg p-4 transition-colors"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="flex items-center space-x-3">
            <div :class="`h-10 w-10 bg-${theme.colorClasses.bg} rounded-lg flex items-center justify-center`">
              <svg :class="`h-6 w-6 text-${theme.colorClasses.text}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ group.group_name }}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ group.variants.length }} variant{{ group.variants.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-900 dark:text-white">{{ getTotalVersions(group) }}</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">versions</div>
          </div>
        </div>

        <div class="mb-3">
          <div class="flex flex-wrap gap-1">
            <span
              v-for="variant in group.variants"
              :key="variant.id"
              class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
            >
              {{ variant.variant }}
            </span>
          </div>
        </div>

        <div class="flex items-center justify-between text-sm">
          <div class="text-gray-500 dark:text-gray-400">
            {{ getLatestActivity(group) }} • {{ getLatestActivityDate(group) }}
          </div>
        </div>

        <div class="mt-3 flex items-center justify-between">
          <NuxtLink
            :to="`/models/group/${encodeURIComponent(group.group_name)}`"
            :class="`text-${theme.colorClasses.text} hover:text-${theme.colorClasses.textHover} font-medium`"
          >
            View Versions →
          </NuxtLink>
          <button
            v-if="auth.isLoggedIn"
            @click="deleteModelGroup(group)"
            class="text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 text-sm font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    
    <div v-else class="hidden md:block bg-white dark:bg-gray-800 shadow-sm border dark:border-gray-700 rounded-lg overflow-hidden transition-colors">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Model Group
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Variants
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Total Versions
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Latest Activity
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="group in modelGroups" :key="group.group_name" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div :class="`h-10 w-10 bg-${theme.colorClasses.bg} rounded-lg flex items-center justify-center`">
                      <svg :class="`h-6 w-6 text-${theme.colorClasses.text}`" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                      </svg>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ group.group_name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ group.variants.length }} variant{{ group.variants.length !== 1 ? 's' : '' }}</div>
                  </div>
                </div>
              </td>

              
              <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="variant in group.variants"
                    :key="variant.id"
                    class="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
                  >
                    {{ variant.variant }}
                  </span>
                </div>
              </td>

              
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ getTotalVersions(group) }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">versions</div>
              </td>

              
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 dark:text-white">{{ getLatestActivity(group) }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">{{ getLatestActivityDate(group) }}</div>
              </td>

              
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <NuxtLink
                  :to="`/models/group/${encodeURIComponent(group.group_name)}`"
                  :class="`text-${theme.colorClasses.text} hover:text-${theme.colorClasses.textHover}`"
                >
                  View Versions
                </NuxtLink>
                <span v-if="auth.isLoggedIn" class="text-gray-300 dark:text-gray-600">|</span>
                <button
                  v-if="auth.isLoggedIn"
                  @click="deleteModelGroup(group)"
                  class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
                >
                  Delete Group
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const auth = useAuthStore()
const theme = useThemeStore()
const notifications = useNotificationStore()
const modals = useModalStore()

type ModelVariant = {
  id: number
  name: string
  variant: string
  description: string
  latest_alias: string | null
  version_count: number
  created_at: string | null
}

type ModelGroup = {
  group_name: string
  variants: ModelVariant[]
}

const {
  data: modelGroups = ref<ModelGroup[]>([]),
  pending,
  error,
  refresh,
} = await useFetch<ModelGroup[]>(`${config.public.apiBase}/models/groups`, {
  credentials: "include",
  transform: (res) => res || [],
})


const getTotalVersions = (group: ModelGroup) => {
  return group.variants.reduce((total, variant) => total + variant.version_count, 0)
}

const getLatestActivity = (group: ModelGroup) => {
  const latestVariant = group.variants.reduce((latest, variant) => {
    if (!latest.created_at || !variant.created_at) return latest
    return new Date(variant.created_at) > new Date(latest.created_at) ? variant : latest
  })
  return `${latestVariant.variant} variant`
}

const getLatestActivityDate = (group: ModelGroup) => {
  const latestVariant = group.variants.reduce((latest, variant) => {
    if (!latest.created_at || !variant.created_at) return latest
    return new Date(variant.created_at) > new Date(latest.created_at) ? variant : latest
  })
  return formatDate(latestVariant.created_at)
}

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return "Unknown"
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return "Today"
  if (diffDays <= 7) return `${diffDays} days ago`
  return date.toLocaleDateString()
}

const deleteModelGroup = async (group: ModelGroup) => {
  if (!auth.isLoggedIn) return
  
  modals.confirm(
    'Delete Model Group',
    `Are you sure you want to delete the entire "${group.group_name}" model group?\n\nThis will permanently delete:\n• All ${group.variants.length} variants\n• All versions across all variants\n• All aliases and tags\n• All associated files\n\nThis action cannot be undone.`,
    async () => {
      try {
        await $fetch(`${config.public.apiBase}/models/groups/${encodeURIComponent(group.group_name)}`, {
          method: "DELETE",
          credentials: "include",
        })
        
        await refresh()
        notifications.success('Model Group Deleted', `Successfully deleted model group "${group.group_name}" with ${group.variants.length} variants`)
      } catch (error: any) {
        console.error("Delete error:", error)
        notifications.error(
          'Failed to Delete Model Group',
          error?.data?.detail || error?.message || "Unknown error"
        )
      }
    }
  )
}


useHead({
  title: 'ModelHub - VaultML'
})
</script>