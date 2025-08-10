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
  <div v-if="modals.modals.length > 0">
    <TransitionGroup
      name="modal"
      tag="div"
    >
      <div
        v-for="modal in modals.modals"
        :key="modal.id"
        class="fixed inset-0 z-50 overflow-y-auto"
        @click.self="modals.removeModal(modal.id)"
      >
        <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div>
        
        <div class="flex items-center justify-center min-h-screen p-4">
          <div
            class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full transition-colors"
            @click.stop
          >
            <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  {{ modal.title }}
                </h3>
                <button
                  @click="modals.removeModal(modal.id)"
                  class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
            </div>

            <div class="px-6 py-4">
              <p v-if="modal.message" class="text-gray-700 dark:text-gray-300 mb-4">
                {{ modal.message }}
              </p>

              <div v-if="modal.type === 'prompt'" class="mb-4">
                <label v-if="modal.inputLabel" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {{ modal.inputLabel }}
                </label>
                <input
                  v-model="modal.inputValue"
                  :type="modal.inputType || 'text'"
                  :placeholder="modal.inputPlaceholder"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  @keydown.enter="handlePrimaryAction(modal)"
                />
              </div>

              <div v-if="modal.type === 'form' && modal.formFields" class="space-y-4 mb-4">
                <div v-for="field in modal.formFields" :key="field.key">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    {{ field.label }}
                    <span v-if="field.required" class="text-red-500">*</span>
                  </label>
                  
                  <input
                    v-if="field.type === 'text' || field.type === 'number'"
                    v-model="field.value"
                    :type="field.type"
                    :placeholder="field.placeholder"
                    :required="field.required"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  
                  <textarea
                    v-else-if="field.type === 'textarea'"
                    v-model="field.value"
                    :placeholder="field.placeholder"
                    :required="field.required"
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  ></textarea>
                  
                  <select
                    v-else-if="field.type === 'select'"
                    v-model="field.value"
                    :required="field.required"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option v-for="option in field.options" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>
            </div>

            <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700 rounded-b-lg">
              <div class="flex justify-end space-x-3">
                <button
                  v-for="button in modal.buttons"
                  :key="button.label"
                  @click="handleButtonClick(modal, button)"
                  :disabled="button.loading"
                  :class="getButtonClasses(button.type)"
                  class="px-4 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg v-if="button.loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ button.label }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { useModalStore, type Modal, type ModalButton } from '~/stores/modals'

const modals = useModalStore()

const handleButtonClick = async (modal: Modal, button: ModalButton) => {
  try {
    button.loading = true
    await button.action()
    modals.removeModal(modal.id)
  } catch (error) {
    console.error('Modal action failed:', error)
  } finally {
    button.loading = false
  }
}

const handlePrimaryAction = (modal: Modal) => {
  const primaryButton = modal.buttons.find(b => b.type === 'primary')
  if (primaryButton) {
    handleButtonClick(modal, primaryButton)
  }
}

const getButtonClasses = (type?: string) => {
  switch (type) {
    case 'primary':
      return 'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500'
    case 'danger':
      return 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
    case 'secondary':
    default:
      return 'bg-white dark:bg-gray-600 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-500 hover:bg-gray-50 dark:hover:bg-gray-500 focus:ring-indigo-500'
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>