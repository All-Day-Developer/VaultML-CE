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
  <div class="max-w-6xl mx-auto space-y-8">
    <!-- Loading State -->
    <div v-if="pending" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      <span class="ml-3 text-gray-500 dark:text-gray-400">Loading versions...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-red-700 dark:text-red-300">Model not found or failed to load</span>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-8">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <div class="flex items-center space-x-3 mb-2">
            <NuxtLink
              to="/models"
              class="inline-flex items-center text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            >
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Back to ModelHub
            </NuxtLink>
            <span class="text-gray-300 dark:text-gray-600">/</span>
            <NuxtLink
              :to="`/models/${route.params.name}`"
              class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
            >
              {{ modelInfo?.group_name }}:{{ modelInfo?.variant }}
            </NuxtLink>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Versions for {{ modelInfo?.group_name }}:{{ modelInfo?.variant }}
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">
            Manage and view all versions of this model
          </p>
        </div>

        <div class="flex items-center space-x-3">
          <NuxtLink
            v-if="auth.isLoggedIn"
            :to="`/models/${route.params.name}/versions/new`"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-700 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Add New Version
          </NuxtLink>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Versions</h3>
          <p class="text-2xl font-bold text-indigo-600">{{ versions.length }}</p>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Latest Version</h3>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ versions.length > 0 ? `v${latestVersion}` : 'None' }}
          </p>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Aliases</h3>
          <p class="text-2xl font-bold text-green-600">{{ aliases.length }}</p>
        </div>
      </div>

      <!-- Versions List -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">All Versions</h2>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            {{ versions.length }} version{{ versions.length !== 1 ? 's' : '' }} total
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-if="versions.length === 0" class="p-12 text-center text-gray-500 dark:text-gray-400">
          <svg class="mx-auto h-16 w-16 text-gray-400 dark:text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
          </svg>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No versions yet</h3>
          <p class="text-gray-500 dark:text-gray-400 mb-6">Create your first version to get started with this model.</p>
          <div v-if="auth.isLoggedIn">
            <NuxtLink
              :to="`/models/${route.params.name}/versions/new`"
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              Create First Version
            </NuxtLink>
          </div>
        </div>

        <!-- Versions List -->
        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="version in sortedVersions"
            :key="version.id"
            class="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-lg flex items-center justify-center">
                    <span class="text-lg font-bold text-indigo-600 dark:text-indigo-300">v{{ version.version }}</span>
                  </div>
                </div>
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white">Version {{ version.version }}</h3>
                    <span v-if="version.version === latestVersion" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200">
                      Latest
                    </span>
                  </div>
                  <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                    Created {{ formatDate(version.created_at) }}
                  </p>
                  <p class="text-xs text-gray-400 dark:text-gray-500 font-mono mt-1">
                    S3: {{ version.s3_prefix }}
                  </p>
                  
                  <!-- Aliases for this version -->
                  <div v-if="getAliasesForVersion(version.version).length > 0" class="flex flex-wrap gap-1 mt-2">
                    <span
                      v-for="alias in getAliasesForVersion(version.version)"
                      :key="alias.alias"
                      class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200"
                    >
                      @{{ alias.alias }}
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex items-center space-x-3">
                <button
                  @click="resolveVersion(version.version)"
                  class="inline-flex items-center px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                  </svg>
                  Resolve
                </button>
                
                <button
                  v-if="auth.isLoggedIn"
                  @click="setAlias(version.version)"
                  class="inline-flex items-center px-3 py-2 text-sm bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-lg hover:bg-green-200 dark:hover:bg-green-800 transition"
                >
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                  </svg>
                  Set Alias
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Aliases Section -->
      <div v-if="aliases.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Active Aliases</h2>
        </div>
        <div class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="alias in aliases"
            :key="alias.alias"
            class="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-between transition-colors"
          >
            <div class="flex items-center space-x-4">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                  <span class="text-sm font-bold text-green-600 dark:text-green-200">@</span>
                </div>
              </div>
              <div>
                <p class="text-lg font-medium text-gray-900 dark:text-white">@{{ alias.alias }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">Points to version {{ alias.version }}</p>
                <p class="text-xs text-gray-400 dark:text-gray-500">Updated {{ formatDate(alias.updated_at) }}</p>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <button
                @click="resolveAlias(alias.alias)"
                class="text-sm px-3 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition"
              >
                Resolve
              </button>
              <button
                v-if="auth.isLoggedIn"
                @click="deleteAlias(alias.alias)"
                class="text-sm px-3 py-2 bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/70 transition"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { encodeModelName, decodeModelName } from '~/utils/model-utils';

const config = useRuntimeConfig();
const route = useRoute();
const auth = useAuthStore();
const notifications = useNotificationStore();
const modals = useModalStore();

const modelName = decodeModelName(route.params.name as string);

type ModelInfo = {
  id: number;
  name: string;
  group_name: string;
  variant: string;
  description: string;
  created_by: number;
  created_at: string;
};

type ModelVersion = {
  id: number;
  version: number;
  s3_prefix: string;
  created_at: string;
};

type ModelAlias = {
  alias: string;
  version: number;
  updated_at: string;
};

// Fetch model info
const { data: modelInfo, pending: modelPending } = await useFetch<ModelInfo>(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}`,
  { credentials: "include" }
);

// Fetch versions
const { data: versions = ref<ModelVersion[]>([]) } = await useFetch<ModelVersion[]>(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}/versions`,
  { credentials: "include", default: () => [] }
);

// Fetch aliases
const { data: aliases = ref<ModelAlias[]>([]) } = await useFetch<ModelAlias[]>(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}/aliases`,
  { credentials: "include", default: () => [] }
);

const pending = computed(() => modelPending.value);
const error = computed(() => !modelInfo.value && !pending.value);

const latestVersion = computed(() => {
  if (versions.value.length === 0) return 0;
  return Math.max(...versions.value.map(v => v.version));
});

const sortedVersions = computed(() => {
  return [...versions.value].sort((a, b) => b.version - a.version);
});

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return "Unknown";
  return new Date(dateStr).toLocaleDateString();
};

const getAliasesForVersion = (version: number) => {
  return aliases.value.filter(alias => alias.version === version);
};

const resolveVersion = async (version: number) => {
  try {
    const result = await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/resolve?version=${version}`, {
      credentials: "include"
    });
    console.log("Resolve result:", result);
    notifications.success(
      'Version Resolved',
      `Successfully resolved ${result.display_name}`,
      {
        actions: [
          {
            label: 'Copy S3 Path',
            action: () => {
              navigator.clipboard.writeText(result.s3_prefix);
              notifications.success('Copied!', 'S3 path copied to clipboard');
            }
          }
        ]
      }
    );
  } catch (error: any) {
    notifications.error('Resolution Failed', `Failed to resolve version ${version}: ${error.message}`);
  }
};

const resolveAlias = async (alias: string) => {
  try {
    const result = await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/resolve?alias=${alias}`, {
      credentials: "include"
    });
    console.log("Resolve result:", result);
    notifications.success(
      'Alias Resolved',
      `Successfully resolved @${alias} to ${result.display_name}`,
      {
        actions: [
          {
            label: 'Copy S3 Path',
            action: () => {
              navigator.clipboard.writeText(result.s3_prefix);
              notifications.success('Copied!', 'S3 path copied to clipboard');
            }
          }
        ]
      }
    );
  } catch (error: any) {
    notifications.error('Resolution Failed', `Failed to resolve alias @${alias}: ${error.message}`);
  }
};

const setAlias = (versionNumber?: number) => {
  modals.addModal({
    type: 'form',
    title: 'Set Model Alias',
    formFields: [
      {
        key: 'alias',
        label: 'Alias Name',
        type: 'text',
        value: '',
        placeholder: 'e.g., prod, latest, stable',
        required: true
      },
      {
        key: 'version',
        label: 'Version Number',
        type: 'number',
        value: versionNumber || latestVersion.value,
        required: true
      }
    ],
    buttons: [
      {
        label: 'Cancel',
        action: () => {},
        type: 'secondary'
      },
      {
        label: 'Set Alias',
        action: async () => {
          const modal = modals.modals.find(m => m.title === 'Set Model Alias');
          if (modal && modal.formFields) {
            const aliasField = modal.formFields.find(f => f.key === 'alias');
            const versionField = modal.formFields.find(f => f.key === 'version');
            
            if (aliasField?.value && versionField?.value) {
              try {
                await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/aliases/${aliasField.value}?version=${versionField.value}`, {
                  method: 'POST',
                  credentials: 'include'
                });
                await refreshCookie(aliases);
                notifications.success('Alias Set', `Successfully set @${aliasField.value} to version ${versionField.value}`);
              } catch (error: any) {
                notifications.error('Failed to Set Alias', error.message);
                throw error;
              }
            }
          }
        },
        type: 'primary'
      }
    ]
  });
};

const deleteAlias = async (aliasName: string) => {
  modals.confirm(
    'Delete Alias',
    `Are you sure you want to delete the alias "@${aliasName}"? This action cannot be undone.`,
    async () => {
      try {
        await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/aliases/${aliasName}`, {
          method: "DELETE",
          credentials: "include"
        });
        await refreshCookie(aliases);
        notifications.success('Alias Deleted', `Successfully deleted alias @${aliasName}`);
      } catch (error: any) {
        notifications.error('Failed to Delete Alias', error.message);
      }
    }
  );
};
</script>