// Copyright (C) 2025 All-Day Developer Marcin Wawrzków
// contributor: Marcin Wawrzków
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

import { defineStore } from 'pinia'

export interface ModalButton {
  label: string
  action: () => void | Promise<void>
  type?: 'primary' | 'secondary' | 'danger'
  loading?: boolean
}

export interface Modal {
  id: string
  type: 'confirm' | 'prompt' | 'form' | 'info'
  title: string
  message?: string
  buttons: ModalButton[]
  onClose?: () => void
  inputValue?: string
  inputLabel?: string
  inputPlaceholder?: string
  inputType?: string
  formFields?: Array<{
    key: string
    label: string
    type: 'text' | 'textarea' | 'select' | 'number'
    value: any
    placeholder?: string
    required?: boolean
    options?: Array<{ label: string; value: any }>
  }>
}

export const useModalStore = defineStore('modals', () => {
  const modals = ref<Modal[]>([])

  const addModal = (modal: Omit<Modal, 'id'>) => {
    const id = Date.now().toString() + Math.random().toString(36).substr(2, 9)
    const newModal: Modal = { id, ...modal }
    modals.value.push(newModal)
    return id
  }

  const removeModal = (id: string) => {
    const index = modals.value.findIndex(m => m.id === id)
    if (index > -1) {
      const modal = modals.value[index]
      if (modal.onClose) {
        modal.onClose()
      }
      modals.value.splice(index, 1)
    }
  }

  const clearAll = () => {
    modals.value.forEach(modal => {
      if (modal.onClose) {
        modal.onClose()
      }
    })
    modals.value.length = 0
  }

  const confirm = (
    title: string,
    message: string,
    onConfirm: () => void | Promise<void>,
    onCancel?: () => void
  ) => {
    return addModal({
      type: 'confirm',
      title,
      message,
      buttons: [
        {
          label: 'Cancel',
          action: () => {
            if (onCancel) onCancel()
          },
          type: 'secondary'
        },
        {
          label: 'Confirm',
          action: onConfirm,
          type: 'danger'
        }
      ]
    })
  }

  const prompt = (
    title: string,
    inputLabel: string,
    onSubmit: (value: string) => void | Promise<void>,
    options: {
      placeholder?: string
      defaultValue?: string
      inputType?: string
    } = {}
  ) => {
    return addModal({
      type: 'prompt',
      title,
      inputLabel,
      inputValue: options.defaultValue || '',
      inputPlaceholder: options.placeholder,
      inputType: options.inputType || 'text',
      buttons: [
        {
          label: 'Cancel',
          action: () => {},
          type: 'secondary'
        },
        {
          label: 'Submit',
          action: () => {
            const modal = modals.value.find(m => m.inputLabel === inputLabel)
            if (modal && modal.inputValue) {
              onSubmit(modal.inputValue)
            }
          },
          type: 'primary'
        }
      ]
    })
  }

  const info = (title: string, message: string, onClose?: () => void) => {
    return addModal({
      type: 'info',
      title,
      message,
      buttons: [
        {
          label: 'OK',
          action: () => {
            if (onClose) onClose()
          },
          type: 'primary'
        }
      ]
    })
  }

  return {
    modals: readonly(modals),
    addModal,
    removeModal,
    clearAll,
    confirm,
    prompt,
    info,
  }
})