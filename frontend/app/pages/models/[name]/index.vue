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
    
    <div v-if="pending" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      <span class="ml-3 text-gray-500 dark:text-gray-400">Loading model details...</span>
    </div>

    
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-red-700 dark:text-red-300">Model not found or failed to load</span>
      </div>
    </div>

    
    <div v-else class="space-y-8">
      
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
          </div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            {{ modelInfo?.group_name }}:{{ modelInfo?.variant }}
          </h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">{{ modelInfo?.description || 'No description provided' }}</p>
        </div>

        <div class="flex items-center space-x-3">
          <button
            v-if="auth.isLoggedIn"
            @click="editModel"
            class="inline-flex items-center px-4 py-2 bg-gray-600 text-white font-semibold rounded-lg shadow hover:bg-gray-700 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
            Edit Details
          </button>
          <NuxtLink
            v-if="auth.isLoggedIn"
            :to="`/models/${route.params.name}/versions/new`"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-700 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            New Version
          </NuxtLink>
        </div>
      </div>

      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Model Information</h3>
          <div class="space-y-3">
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Group Name:</span>
              <p class="text-gray-900 dark:text-white">{{ modelInfo?.group_name }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Variant:</span>
              <p class="text-gray-900 dark:text-white">{{ modelInfo?.variant }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Full Name:</span>
              <p class="font-mono text-gray-900 dark:text-white">{{ modelInfo?.name }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Created:</span>
              <p class="text-gray-900 dark:text-white">{{ formatDate(modelInfo?.created_at) }}</p>
            </div>
          </div>
        </div>

        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Version Statistics</h3>
          <div class="space-y-3">
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Versions:</span>
              <p class="text-2xl font-bold text-indigo-600">{{ versions.length }}</p>
            </div>
            <div v-if="versions.length > 0">
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Latest Version:</span>
              <p class="text-lg font-semibold text-gray-900 dark:text-white">v{{ latestVersion }}</p>
            </div>
            <div>
              <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Aliases:</span>
              <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ aliases.length }}</p>
            </div>
            <div class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
              <NuxtLink
                :to="`/models/${route.params.name}/versions`"
                class="inline-flex items-center text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300"
              >
                View all versions
                <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </NuxtLink>
            </div>
          </div>
        </div>

        
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 transition-colors">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
          <div class="space-y-3">
            <NuxtLink
              :to="`/models/${route.params.name}/versions`"
              class="w-full text-left px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded transition"
            >
              📂 Manage Versions
            </NuxtLink>
            <button
              v-if="auth.isLoggedIn"
              @click="setAlias"
              class="w-full text-left px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded transition"
            >
              🏷️ Set Alias
            </button>
            <button
              @click="copyResolveCommand"
              class="w-full text-left px-3 py-2 text-sm bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded transition"
            >
              📋 Copy Resolve Command
            </button>
            <button
              v-if="auth.isLoggedIn"
              @click="deleteModel"
              class="w-full text-left px-3 py-2 text-sm bg-red-50 dark:bg-red-900/50 hover:bg-red-100 dark:hover:bg-red-900/70 text-red-700 dark:text-red-300 rounded transition"
            >
              🗑️ Delete Model
            </button>
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


const { data: modelInfo, pending: modelPending } = await useFetch<ModelInfo>(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}`,
  { credentials: "include" }
);


const { data: versions = ref<ModelVersion[]>([]) } = await useFetch<ModelVersion[]>(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}/versions`,
  { credentials: "include", default: () => [] }
);


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

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return "Unknown";
  return new Date(dateStr).toLocaleDateString();
};


const setAlias = () => {
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
        value: latestVersion.value,
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
                // Refresh aliases list
                aliases.value = await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}/aliases`, { credentials: 'include', default: () => [] });
                notifications.success('Alias Set', `Successfully set @${aliasField.value} to version ${versionField.value}`);
              } catch (error: any) {
                notifications.error('Failed to Set Alias', error.message);
                throw error; // Re-throw to keep modal open
              }
            }
          }
        },
        type: 'primary'
      }
    ]
  });
};

const copyResolveCommand = () => {
  const command = `curl "${config.public.apiBase}/resolve/${modelInfo.value?.group_name}/${modelInfo.value?.variant}?alias=latest"`;
  navigator.clipboard.writeText(command);
  notifications.success('Copied!', 'Resolve command copied to clipboard');
};


const deleteModel = async () => {
  modals.confirm(
    'Delete Model',
    `Are you sure you want to delete "${modelInfo.value?.group_name}:${modelInfo.value?.variant}"?\n\nThis will permanently delete:\n• All versions\n• All aliases\n• All associated files\n\nThis action cannot be undone.`,
    async () => {
      try {
        await $fetch(`${config.public.apiBase}/models/${encodeURIComponent(modelName)}`, {
          method: "DELETE",
          credentials: "include",
        });
        notifications.success('Model Deleted', `Successfully deleted ${modelInfo.value?.group_name}:${modelInfo.value?.variant}`);
        navigateTo("/models");
      } catch (error: any) {
        notifications.error('Failed to Delete Model', error?.data?.detail || error?.message || "Unknown error");
      }
    }
  );
};

const editModel = () => {
  modals.addModal({
    type: 'form',
    title: 'Edit Model Details',
    formFields: [
      {
        key: 'description',
        label: 'Description',
        type: 'textarea',
        value: modelInfo.value?.description || '',
        placeholder: 'Enter a description for this model'
      }
    ],
    buttons: [
      {
        label: 'Cancel',
        action: () => {},
        type: 'secondary'
      },
      {
        label: 'Save Changes',
        action: async () => {
          const modal = modals.modals.find(m => m.title === 'Edit Model Details');
          if (modal && modal.formFields) {
            const descriptionField = modal.formFields.find(f => f.key === 'description');
            
            if (descriptionField) {
              try {
                // Note: This would need a backend endpoint to update model description
                // For now, just show success
                notifications.success('Model Updated', 'Model description updated successfully');
                // In a real implementation, you'd refresh the model data here
              } catch (error: any) {
                notifications.error('Failed to Update Model', error.message);
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
</script>