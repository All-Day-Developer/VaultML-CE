<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          {{ isUploading ? 'Uploading Large File' : 'Upload Large File' }}
        </h3>
        <button
          @click="handleCancel"
          :disabled="isUploading"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 disabled:opacity-50"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div v-if="!selectedFile" class="space-y-4">
        <div class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            class="hidden"
          >
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <div class="mt-4">
              <button
                @click="$refs.fileInput.click()"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
              >
                Select File
              </button>
              <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Choose files larger than 100MB for multipart upload
              </p>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!isUploading" class="space-y-4">
        <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
                {{ selectedFile.name }}
              </p>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ formatFileSize(selectedFile.size) }}
              </p>
            </div>
            <button
              @click="selectedFile = null"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div class="flex space-x-3">
          <button
            @click="handleCancel"
            class="flex-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 px-4 py-2 rounded-md hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="startUpload"
            class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            Start Upload
          </button>
        </div>
      </div>

      <div v-else class="space-y-4">
        <!-- Upload Progress -->
        <div class="space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-600 dark:text-gray-400">Progress</span>
            <span class="text-gray-900 dark:text-white">{{ progress.percentage.toFixed(1) }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${progress.percentage}%` }"
            ></div>
          </div>
        </div>

        <!-- Upload Stats -->
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="text-gray-600 dark:text-gray-400">Speed:</span>
            <span class="text-gray-900 dark:text-white ml-1">{{ formatSpeed(progress.speed) }}</span>
          </div>
          <div>
            <span class="text-gray-600 dark:text-gray-400">Remaining:</span>
            <span class="text-gray-900 dark:text-white ml-1">{{ formatTime(progress.remainingTime) }}</span>
          </div>
          <div>
            <span class="text-gray-600 dark:text-gray-400">Part:</span>
            <span class="text-gray-900 dark:text-white ml-1">{{ progress.currentPart }} / {{ progress.totalParts }}</span>
          </div>
          <div>
            <span class="text-gray-600 dark:text-gray-400">Size:</span>
            <span class="text-gray-900 dark:text-white ml-1">{{ formatFileSize(progress.uploadedBytes) }} / {{ formatFileSize(progress.totalBytes) }}</span>
          </div>
        </div>

        <!-- Upload Controls -->
        <div class="flex space-x-3">
          <button
            @click="abortUpload"
            class="flex-1 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
          >
            Cancel Upload
          </button>
          <button
            v-if="uploadManager && !uploadManager.isPaused"
            @click="pauseUpload"
            class="flex-1 bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700 transition-colors"
          >
            Pause
          </button>
          <button
            v-else-if="uploadManager && uploadManager.isPaused"
            @click="resumeUpload"
            class="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
          >
            Resume
          </button>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="mt-4 p-3 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 rounded-md">
        <p class="text-sm text-red-700 dark:text-red-200">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useChunkedUpload, type ChunkedUploadOptions, type UploadProgress, ChunkedUploadManager } from '~/composables/useMultipartUpload'

interface Props {
  isOpen: boolean
  modelName: string
}

interface Emits {
  (e: 'close'): void
  (e: 'success', result: any): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const { createUpload, formatFileSize, formatSpeed, formatTime } = useChunkedUpload()

const fileInput = ref<HTMLInputElement>()
const selectedFile = ref<File | null>(null)
const isUploading = ref(false)
const error = ref<string | null>(null)
const uploadManager = ref<ChunkedUploadManager | null>(null)

const progress = reactive<UploadProgress>({
  uploadedBytes: 0,
  totalBytes: 0,
  percentage: 0,
  currentPart: 0,
  totalParts: 0,
  speed: 0,
  remainingTime: 0
})

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0]
    error.value = null
  }
}

async function startUpload() {
  if (!selectedFile.value) return
  
  isUploading.value = true
  error.value = null
  
  const options: ChunkedUploadOptions = {
    modelName: props.modelName,
    filename: selectedFile.value.name,
    file: selectedFile.value,
    chunkSize: 100 * 1024 * 1024, // 100MB chunks
    onProgress: (p) => {
      Object.assign(progress, p)
    },
    onError: (err) => {
      error.value = err.message
      isUploading.value = false
    },
    onComplete: (result) => {
      isUploading.value = false
      emit('success', result)
      emit('close')
    }
  }
  
  uploadManager.value = createUpload(options)
  await uploadManager.value.start()
}

async function pauseUpload() {
  if (uploadManager.value) {
    await uploadManager.value.pause()
  }
}

async function resumeUpload() {
  if (uploadManager.value) {
    await uploadManager.value.resume()
  }
}

async function abortUpload() {
  if (uploadManager.value) {
    await uploadManager.value.abort()
  }
  isUploading.value = false
  error.value = null
}

function handleCancel() {
  if (isUploading.value && uploadManager.value) {
    abortUpload()
  } else {
    emit('close')
  }
}

// Reset state when dialog closes
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    selectedFile.value = null
    isUploading.value = false
    error.value = null
    uploadManager.value = null
    Object.assign(progress, {
      uploadedBytes: 0,
      totalBytes: 0,
      percentage: 0,
      currentPart: 0,
      totalParts: 0,
      speed: 0,
      remainingTime: 0
    })
  }
})
</script>