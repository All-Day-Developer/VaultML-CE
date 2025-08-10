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
  <div class="max-w-4xl mx-auto space-y-8">
    
    <div v-if="modelPending" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      <span class="ml-3 text-gray-500 dark:text-gray-400">Loading model information...</span>
    </div>

    
    <div v-else-if="modelError" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span class="text-red-700 dark:text-red-300">Model not found or failed to load: {{ modelError }}</span>
      </div>
    </div>

    
    <div v-else class="space-y-8">
      
      <div>
        <div class="flex items-center space-x-3 mb-4">
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
          <span class="text-gray-300 dark:text-gray-600">/</span>
          <NuxtLink
            :to="`/models/${route.params.name}/versions`"
            class="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
          >
            Versions
          </NuxtLink>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Create New Version</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Upload files for a new version of <span class="font-semibold">{{ modelInfo?.group_name }}:{{ modelInfo?.variant }}</span>
        </p>
      </div>

      
      <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 transition-colors">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Model</h3>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ modelInfo?.group_name }}:{{ modelInfo?.variant }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Latest Version</h3>
            <p class="text-lg font-semibold text-gray-900 dark:text-white">v{{ latestVersion || 0 }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">Next Version</h3>
            <p class="text-lg font-semibold text-indigo-600">v{{ nextVersion }}</p>
          </div>
        </div>
      </div>

      
      <form @submit.prevent="handleUpload" class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8 space-y-8 transition-colors">
        <div>
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">Upload Model Files</h2>

          <div class="space-y-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Select Model Files *
            </label>
            <input
              ref="folderInput"
              type="file"
              webkitdirectory
              directory
              multiple
              @change="onFilesSelected"
              :disabled="loading"
              class="block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 dark:file:bg-indigo-900 file:text-indigo-700 dark:file:text-indigo-300 hover:file:bg-indigo-100 dark:hover:file:bg-indigo-800 transition-colors disabled:opacity-50"
            />

            
            <div v-if="files.length > 0" class="bg-green-50 dark:bg-green-900/50 rounded-lg p-4">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-green-500 dark:text-green-400 mt-0.5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <div class="flex-1">
                  <p class="text-sm font-medium text-green-800 dark:text-green-200">
                    {{ files.length }} file(s) selected
                  </p>
                  <p class="text-sm text-green-600 dark:text-green-300 mt-1">
                    Ready to upload as version {{ nextVersion }}
                  </p>
                  <details class="mt-2">
                    <summary class="text-sm text-green-700 dark:text-green-300 cursor-pointer hover:text-green-800 dark:hover:text-green-200">
                      View selected files ({{ files.length }} files)
                    </summary>
                    <div class="mt-2 max-h-40 overflow-y-auto">
                      <ul class="text-sm text-green-600 dark:text-green-400 space-y-1">
                        <li v-for="file in files.slice(0, 20)" :key="file.name" class="font-mono text-xs">
                          {{ (file as any).webkitRelativePath || file.name }}
                        </li>
                        <li v-if="files.length > 20" class="italic">
                          ... and {{ files.length - 20 }} more files
                        </li>
                      </ul>
                    </div>
                  </details>
                </div>
              </div>
            </div>

            <div v-else class="text-sm text-gray-500 dark:text-gray-400 space-y-2">
              <p>• Click "Choose Files" and select a <strong>folder</strong> containing your model files</p>
              <p>• All files and subdirectories will be uploaded</p>
              <p>• Folder structure will be preserved in the model repository</p>
              <p>• Supported formats: All file types (models, configs, tokenizers, etc.)</p>
            </div>
          </div>

          
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Version Notes (Optional)
            </label>
            <textarea
              v-model="versionNotes"
              rows="3"
              placeholder="Describe what's new in this version..."
              :disabled="loading"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none disabled:opacity-50 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
            />
          </div>
        </div>

        
        <div v-if="uploadProgress.show" class="space-y-4">
          <div class="bg-blue-50 dark:bg-blue-900/50 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-blue-800 dark:text-blue-200">
                {{ uploadProgress.status }}
              </span>
              <span class="text-sm text-blue-600 dark:text-blue-300">
                {{ uploadProgress.current }} / {{ uploadProgress.total }}
              </span>
            </div>
            <div class="w-full bg-blue-200 dark:bg-blue-800 rounded-full h-2">
              <div 
                class="bg-blue-600 dark:bg-blue-400 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${(uploadProgress.current / uploadProgress.total) * 100}%` }"
              ></div>
            </div>
          </div>
        </div>

        
        <div v-if="error" class="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <div class="flex items-center">
            <svg class="w-5 h-5 text-red-500 dark:text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-red-700 dark:text-red-300 text-sm">{{ error }}</span>
          </div>
        </div>

        
        <div class="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
          <NuxtLink
            :to="`/models/${route.params.name}/versions`"
            class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            Cancel
          </NuxtLink>

          <button
            type="submit"
            :disabled="loading || files.length === 0"
            class="inline-flex items-center px-6 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Uploading...' : `Create Version ${nextVersion}` }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { encodeModelName, decodeModelName } from '~/utils/model-utils';

const config = useRuntimeConfig();
const route = useRoute();
const theme = useThemeStore();

const modelName = decodeModelName(route.params.name);
console.log('Creating version for model:', modelName);


const files = ref<File[]>([]);
const versionNotes = ref("");
const error = ref("");
const loading = ref(false);
const folderInput = ref<HTMLInputElement | null>(null);


const uploadProgress = ref({
  show: false,
  status: "",
  current: 0,
  total: 0,
});


const { data: modelInfo, pending: modelPending, error: modelError } = await useFetch(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}`,
  { 
    credentials: "include",
    server: false,
    transform: (data: any) => {
      console.log('Model data:', data);
      return data;
    }
  }
);

const { data: versions = ref([]) } = await useFetch(
  `${config.public.apiBase}/models/${encodeURIComponent(modelName)}/versions`,
  { 
    credentials: "include", 
    default: () => [],
    server: false,
    transform: (data: any) => {
      console.log('Versions data:', data);
      return data;
    }
  }
);


const latestVersion = computed(() => {
  if (!versions.value?.length) return 0;
  return Math.max(...versions.value.map((v: any) => v.version));
});

const nextVersion = computed(() => latestVersion.value + 1);


const isDirectorySelection = (list: File[]) =>
  list.length > 0 &&
  list.every((f) => "webkitRelativePath" in f && (f as any).webkitRelativePath);

const onFilesSelected = (e: Event) => {
  error.value = "";
  const target = e.target as HTMLInputElement;
  const picked = target.files ? Array.from(target.files) : [];

  if (picked.length === 0) {
    files.value = [];
    return;
  }

  if (!isDirectorySelection(picked)) {
    files.value = [];
    error.value = "Please select a folder (directory), not individual files.";
    target.value = "";
    return;
  }

  files.value = picked;
};


const handleUpload = async () => {
  error.value = "";
  loading.value = true;
  
  try {
    if (files.value.length === 0) {
      throw new Error("Please select files to upload");
    }

    
    uploadProgress.value = {
      show: true,
      status: "Uploading files to server...",
      current: 0,
      total: files.value.length,
    };

    
    const formData = new FormData();
    for (const file of files.value) {
      formData.append('files', file);
    }

    
    const versionRes = await $fetch<{
      version: number;
      s3_prefix: string;
      uploaded_files: Array<{
        filename: string;
        size: number;
        s3_key: string;
        s3_url: string;
        content_type: string;
      }>;
      message: string;
    }>(
      `${config.public.apiBase}/models/${encodeURIComponent(modelName)}/versions/new`,
      {
        method: "POST",
        body: formData,
        credentials: "include",
      },
    );

    uploadProgress.value.current = files.value.length;
    uploadProgress.value.status = "Upload completed successfully!";

    
    await new Promise(resolve => setTimeout(resolve, 1000));
    navigateTo(`/models/${route.params.name}/versions`);
    
  } catch (err: any) {
    console.error("Version creation error:", err);
    error.value = err?.data?.detail || err?.message || "Failed to create version";
  } finally {
    loading.value = false;
    uploadProgress.value.show = false;
  }
};
</script>