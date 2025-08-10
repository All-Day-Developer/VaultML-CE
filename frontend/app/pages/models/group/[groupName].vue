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
    
    <div class="flex items-center justify-between">
      <div>
        <nav class="flex items-center space-x-2 text-sm text-gray-500 mb-2">
          <NuxtLink to="/models" class="hover:text-gray-700">ModelHub</NuxtLink>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
          </svg>
          <span class="text-gray-900">{{ groupName }}</span>
        </nav>
        <h1 class="text-3xl font-bold text-gray-900">{{ groupName }} Models</h1>
        <p class="text-gray-600 mt-1">All variants and versions for {{ groupName }}</p>
      </div>

      <div class="flex items-center space-x-3">
        <NuxtLink
          v-if="auth.isLoggedIn"
          to="/models/new-model"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Add Variant
        </NuxtLink>
      </div>
    </div>

    
    <div v-if="pending" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      <span class="ml-3 text-gray-500">Loading models...</span>
    </div>

    
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-red-700">Failed to load model variants</span>
      </div>
    </div>

    
    <div v-else-if="!displayModels || displayModels.length === 0" class="text-center py-12">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No variants found</h3>
      <p class="mt-1 text-sm text-gray-500">This model group doesn't exist or has no variants.</p>
      <div class="mt-6">
        <NuxtLink
          to="/models"
          class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          Back to ModelHub
        </NuxtLink>
      </div>
    </div>

    
    <div v-else class="space-y-8">
      <div
        v-for="model in displayModels"
        :key="model.id"
        class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors"
      >
        
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ groupName }}:{{ model.variant }}
              </h2>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ model.description || 'No description' }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">
                {{ model.versions?.length || 0 }} versions
              </span>
              <span v-if="model.latest_alias" class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200">
                @{{ model.latest_alias }}
              </span>
            </div>
          </div>
        </div>

        
        <div class="overflow-hidden">
          <div v-if="!model.versions || model.versions.length === 0" class="px-6 py-8 text-center text-gray-500">
            <svg class="mx-auto h-8 w-8 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
            </svg>
            <p class="text-sm">No versions uploaded yet</p>
            <NuxtLink
              v-if="auth.isLoggedIn"
              :to="`/models/${encodeModelName(model.name)}/versions/new`"
              class="inline-flex items-center mt-3 text-sm text-indigo-600 hover:text-indigo-800"
            >
              Upload first version
            </NuxtLink>
          </div>

          <table v-else class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Version
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Aliases
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  S3 Path
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Created
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="version in model.versions" :key="version.id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-8 w-8">
                      <div class="h-8 w-8 bg-indigo-100 rounded-full flex items-center justify-center">
                        <span class="text-xs font-medium text-indigo-600">v{{ version.version }}</span>
                      </div>
                    </div>
                    <div class="ml-3">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">Version {{ version.version }}</div>
                      <div class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(version.created_at) }}</div>
                    </div>
                  </div>
                </td>

                
                <td class="px-6 py-4">
                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="alias in getAliasesForVersion(version.id)"
                      :key="alias"
                      class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200"
                    >
                      @{{ alias }}
                    </span>
                    <span v-if="getAliasesForVersion(version.id).length === 0" class="text-xs text-gray-400 dark:text-gray-500">
                      No aliases
                    </span>
                  </div>
                </td>

                
                <td class="px-6 py-4">
                  <div class="text-xs font-mono text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700 rounded px-2 py-1">
                    {{ version.s3_prefix }}
                  </div>
                </td>

                
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(version.created_at) }}
                </td>

                
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    @click="resolveVersion(model.name, version.version)"
                    class="text-indigo-600 hover:text-indigo-800 mr-3"
                  >
                    Resolve
                  </button>
                  <button
                    v-if="auth.isLoggedIn"
                    @click="setAlias(model.name, version.version)"
                    class="text-blue-600 dark:text-blue-400 hover:text-blue-900 dark:hover:text-blue-300 mr-3"
                  >
                    Set Alias
                  </button>
                  <button
                    v-if="auth.isLoggedIn"
                    @click="deleteVersion(model.name, version.version)"
                    class="text-red-600 dark:text-red-400 hover:text-red-900 dark:hover:text-red-300"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        
        <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-500 dark:text-gray-400">
              Created {{ formatDate(model.created_at) }}
            </div>
            <div class="flex items-center space-x-3">
              <NuxtLink
                :to="`/models/${encodeModelName(model.name)}`"
                class="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white"
              >
                View Details
              </NuxtLink>
              <NuxtLink
                v-if="auth.isLoggedIn"
                :to="`/models/${encodeModelName(model.name)}/versions/new`"
                class="inline-flex items-center px-3 py-1.5 text-sm bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition"
              >
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                New Version
              </NuxtLink>
              <button
                v-if="auth.isLoggedIn"
                @click="deleteModel(model)"
                class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300"
              >
                Delete Variant
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
const theme = useThemeStore();
const notifications = useNotificationStore();
const modals = useModalStore();


const groupName = route.params.groupName as string;

type ModelVersion = {
  id: number;
  version: number;
  s3_prefix: string;
  created_at: string;
};

type ModelInfo = {
  id: number;
  name: string;
  group_name: string;
  variant: string;
  description: string;
  created_at: string;
  latest_alias?: string;
  versions?: ModelVersion[];
};


const { data: allModels, pending, error, refresh } = await useFetch<ModelInfo[]>(
  `${config.public.apiBase}/models`,
  { credentials: "include" }
);


const groupModels = computed(() => {
  if (!allModels.value) return [];
  return allModels.value.filter(m => m.group_name === groupName);
});


const modelsWithVersions = ref<ModelInfo[]>([]);

watch(groupModels, async (models) => {
  if (models.length === 0) return;
  
  try {
    const modelsWithVersionsData = await Promise.all(
      models.map(async (model) => {
        const versions = await $fetch<ModelVersion[]>(
          `${config.public.apiBase}/models/${encodeURIComponent(model.name)}/versions`,
          { credentials: "include" }
        );
        return { ...model, versions };
      })
    );
    modelsWithVersions.value = modelsWithVersionsData;
  } catch (err) {
    console.error("Failed to fetch versions:", err);
  }
}, { immediate: true });


const displayModels = computed(() => modelsWithVersions.value);


const groupModelsDisplay = computed(() => displayModels.value);

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return "Unknown";
  const date = new Date(dateStr);
  const now = new Date();
  const diffTime = Math.abs(now.getTime() - date.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 1) return "Today";
  if (diffDays <= 7) return `${diffDays} days ago`;
  return date.toLocaleDateString();
};


const getAliasesForVersion = (versionId: number): string[] => {
  
  return [];
};

const resolveVersion = async (modelName: string, version: number) => {
  try {
    const result = await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/resolve?version=${version}`, {
      credentials: "include"
    });
    notifications.success(
      'Model Resolved',
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

const setAlias = async (modelName: string, version: number) => {
  modals.prompt(
    'Set Alias',
    'Alias Name',
    async (aliasName: string) => {
      try {
        await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/aliases/${aliasName}?version=${version}`, {
          method: "POST",
          credentials: "include"
        });
        await refresh();
        notifications.success('Alias Set', `Successfully set @${aliasName} for version ${version}`);
      } catch (error: any) {
        notifications.error('Failed to Set Alias', error.message);
      }
    },
    {
      placeholder: "e.g., 'prod', 'latest', 'stable'"
    }
  );
};

const deleteVersion = async (modelName: string, version: number) => {
  modals.confirm(
    'Delete Version',
    `Are you sure you want to delete version ${version}? This action cannot be undone.`,
    async () => {
      try {
        // Note: This would need a backend endpoint to delete specific versions
        notifications.warning('Not Implemented', 'Version deletion is not yet implemented');
      } catch (error: any) {
        notifications.error('Failed to Delete Version', error.message);
      }
    }
  );
};

const deleteModel = async (model: ModelInfo) => {
  modals.confirm(
    'Delete Model Variant',
    `Are you sure you want to delete "${model.group_name}:${model.variant}"?\n\nThis will permanently delete:\n• All versions\n• All aliases\n• All associated files\n\nThis action cannot be undone.`,
    async () => {
      try {
        await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(model.name)}`, {
          method: "DELETE",
          credentials: "include",
        });
        await refresh();
        notifications.success('Model Deleted', `Successfully deleted ${model.group_name}:${model.variant}`);
      } catch (error: any) {
        notifications.error('Failed to Delete Model', error?.data?.detail || error?.message || "Unknown error");
      }
    }
  );
};
</script>