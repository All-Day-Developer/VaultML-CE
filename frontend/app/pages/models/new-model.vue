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
  <div class="max-w-3xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Create New Model Group</h1>
      <p class="mt-2 text-gray-600">
        Create a new model group with variants. Example: "Bielik" group with
        "7b" variant.
      </p>
    </div>

    <form
      @submit.prevent="handleCreate"
      class="space-y-8 bg-white p-8 rounded-xl shadow-sm border border-gray-200"
    >
      <div class="space-y-6">
        <h2
          class="text-xl font-semibold text-gray-900 border-b border-gray-200 pb-2"
        >
          Model Group Information
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Group Name *
            </label>
            <input
              v-model="groupName"
              type="text"
              required
              placeholder="e.g., Bielik, Llama, GPT"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
            <p class="mt-1 text-sm text-gray-500">
              The name of the model family or group
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Variant *
            </label>
            <input
              v-model="variant"
              type="text"
              required
              placeholder="e.g., 7b, 13b, base, small"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            />
            <p class="mt-1 text-sm text-gray-500">
              Size or type variant (7b, 13b, etc.)
            </p>
          </div>
        </div>

        <div class="bg-gray-50 rounded-lg p-4">
          <h3 class="text-sm font-medium text-gray-700 mb-2">
            Generated Model Name:
          </h3>
          <div class="font-mono text-lg text-indigo-600">
            {{ generatedModelName || "Group_name:variant" }}
          </div>
          <p class="text-sm text-gray-500 mt-1">
            This will be the unique identifier for this model variant
          </p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            v-model="description"
            rows="3"
            placeholder="Describe this model..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
          />
        </div>
      </div>

      <div class="space-y-6">
        <h2
          class="text-xl font-semibold text-gray-900 border-b border-gray-200 pb-2"
        >
          Initial Version (Optional)
        </h2>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Upload Model Files
          </label>
          <input
            ref="folderInput"
            type="file"
            webkitdirectory
            directory
            multiple
            @change="onFilesSelected"
            class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 transition-colors"
          />

          <div v-if="files.length" class="mt-4 bg-green-50 rounded-lg p-4">
            <div class="flex items-start">
              <svg
                class="w-5 h-5 text-green-500 mt-0.5 mr-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
              <div>
                <p class="text-sm font-medium text-green-800">
                  {{ files.length }} file(s) selected
                </p>
                <p class="text-sm text-green-600 mt-1">
                  Ready to upload as version 1
                </p>
              </div>
            </div>
          </div>

          <div v-else class="mt-2 text-sm text-gray-500 space-y-1">
            <p>
              • Click "Choose Files" and select a
              <strong>folder</strong> containing your model files
            </p>
            <p>
              • You can also create an empty model group and add versions later
            </p>
            <p>• Folder structure will be preserved in the model repository</p>
          </div>
        </div>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex items-center">
          <svg
            class="w-5 h-5 text-red-500 mr-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            ></path>
          </svg>
          <span class="text-red-700 text-sm">{{ error }}</span>
        </div>
      </div>

      <div
        class="flex items-center justify-between pt-6 border-t border-gray-200"
      >
        <NuxtLink
          to="/models"
          class="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <svg
            class="w-4 h-4 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            ></path>
          </svg>
          Back to ModelHub
        </NuxtLink>

        <button
          type="submit"
          :disabled="loading || !groupName || !variant"
          class="inline-flex items-center px-6 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow-sm hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          <svg
            v-if="loading"
            class="animate-spin -ml-1 mr-3 h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          {{ loading ? "Creating..." : "Create Model Group" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig();

const groupName = ref("");
const variant = ref("");
const description = ref("");
const files = ref<File[]>([]);
const error = ref("");
const loading = ref(false);
const folderInput = ref<HTMLInputElement | null>(null);

const generatedModelName = computed(() => {
  if (groupName.value && variant.value) {
    return `${groupName.value}:${variant.value}`;
  }
  return "";
});

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

const handleCreate = async () => {
  error.value = "";
  loading.value = true;

  try {
    if (!groupName.value || !variant.value) {
      throw new Error("Group name and variant are required");
    }

    await $fetch(`${config.public.apiBase}/models`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: {
        name: generatedModelName.value,
        group_name: groupName.value,
        variant: variant.value,
        description: description.value,
      },
      credentials: "include",
    });

    if (files.value.length > 0) {
      const relPaths = files.value.map(
        (f) => (f as any).webkitRelativePath as string,
      );

      const versionRes = await $fetch<{
        version: number;
        uploads: { key: string; url: string }[];
      }>(
        `${config.public.apiBase}/models/${encodeURIComponent(generatedModelName.value)}/versions/new`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: { files: relPaths },
          credentials: "include",
        },
      );

      const urlBySuffix = new Map(
        versionRes.uploads.map((u) => [u.key, u.url]),
      );

      for (const f of files.value) {
        const rel = (f as any).webkitRelativePath as string;

        let uploadUrl = urlBySuffix.get(rel);
        if (!uploadUrl) {
          uploadUrl = versionRes.uploads.find((u) => u.key.endsWith(rel))?.url;
        }
        if (!uploadUrl) {
          throw new Error(`No upload URL for ${rel}`);
        }

        await fetch(uploadUrl, {
          method: "PUT",
          body: f,
          headers: f.type ? { "Content-Type": f.type } : undefined,
        });
      }
    }

    navigateTo("/models");
  } catch (err: any) {
    console.error("Model creation error:", err);
    error.value =
      err?.data?.detail || err?.message || "Failed to create model group";
  } finally {
    loading.value = false;
  }
};
</script>
