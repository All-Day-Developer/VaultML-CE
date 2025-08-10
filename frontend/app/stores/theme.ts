
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

export type ThemeMode = 'light' | 'dark' | 'auto'
export type PrimaryColor = 'indigo' | 'blue' | 'purple' | 'green' | 'orange' | 'red'

export interface ThemeConfig {
  mode: ThemeMode
  primaryColor: PrimaryColor
}

export const useThemeStore = defineStore('theme', {
  state: (): ThemeConfig => ({
    mode: 'auto',
    primaryColor: 'indigo',
  }),

  getters: {
    isDark: (state) => {
      if (state.mode === 'dark') return true
      if (state.mode === 'light') return false
      
      if (process.client) {
        return window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      return false
    },

    colorClasses() {
      const colors = {
        indigo: {
          primary: 'indigo-600',
          primaryHover: 'indigo-700',
          primaryLight: 'indigo-50',
          primaryDark: 'indigo-800',
          text: 'indigo-600',
          textHover: 'indigo-700',
          bg: 'indigo-100',
          border: 'indigo-200',
        },
        blue: {
          primary: 'blue-600',
          primaryHover: 'blue-700',
          primaryLight: 'blue-50',
          primaryDark: 'blue-800',
          text: 'blue-600',
          textHover: 'blue-700',
          bg: 'blue-100',
          border: 'blue-200',
        },
        purple: {
          primary: 'purple-600',
          primaryHover: 'purple-700',
          primaryLight: 'purple-50',
          primaryDark: 'purple-800',
          text: 'purple-600',
          textHover: 'purple-700',
          bg: 'purple-100',
          border: 'purple-200',
        },
        green: {
          primary: 'green-600',
          primaryHover: 'green-700',
          primaryLight: 'green-50',
          primaryDark: 'green-800',
          text: 'green-600',
          textHover: 'green-700',
          bg: 'green-100',
          border: 'green-200',
        },
        orange: {
          primary: 'orange-600',
          primaryHover: 'orange-700',
          primaryLight: 'orange-50',
          primaryDark: 'orange-800',
          text: 'orange-600',
          textHover: 'orange-700',
          bg: 'orange-100',
          border: 'orange-200',
        },
        red: {
          primary: 'red-600',
          primaryHover: 'red-700',
          primaryLight: 'red-50',
          primaryDark: 'red-800',
          text: 'red-600',
          textHover: 'red-700',
          bg: 'red-100',
          border: 'red-200',
        },
      }
      return colors[this.primaryColor]
    }
  },

  actions: {
    setMode(mode: ThemeMode) {
      this.mode = mode
      this.applyTheme()
      this.saveToStorage()
    },

    setPrimaryColor(color: PrimaryColor) {
      this.primaryColor = color
      this.applyTheme()
      this.saveToStorage()
    },

    applyTheme() {
      if (!process.client) return

      const html = document.documentElement
      const isDark = this.isDark

      if (isDark) {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }

      
      const root = html.style
      const colors = this.colorClasses
      root.setProperty('--color-primary', `var(--color-${colors.primary.replace('-', '-')})`)
      root.setProperty('--color-primary-hover', `var(--color-${colors.primaryHover.replace('-', '-')})`)
    },

    loadFromStorage() {
      if (!process.client) return

      const saved = localStorage.getItem('vaultml-theme')
      if (saved) {
        try {
          const config = JSON.parse(saved) as ThemeConfig
          this.mode = config.mode || 'auto'
          this.primaryColor = config.primaryColor || 'indigo'
        } catch (e) {
          console.warn('Failed to load theme from storage:', e)
        }
      }
      this.applyTheme()
    },

    saveToStorage() {
      if (!process.client) return

      const config: ThemeConfig = {
        mode: this.mode,
        primaryColor: this.primaryColor,
      }
      localStorage.setItem('vaultml-theme', JSON.stringify(config))
    },

    initializeTheme() {
      this.loadFromStorage()
      
      
      if (process.client) {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        mediaQuery.addEventListener('change', () => {
          if (this.mode === 'auto') {
            this.applyTheme()
          }
        })
      }
    }
  }
})