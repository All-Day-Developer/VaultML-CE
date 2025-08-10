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
  <div
    class="flex flex-col min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors"
  >
    <NavBar />

    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <slot />
    </main>

    <footer
      class="bg-white dark:bg-gray-800 border-t dark:border-gray-700 mt-8 transition-colors"
    >
      <div
        class="container mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-gray-500 dark:text-gray-400 text-sm space-y-1"
      >
        <p>© 2025 VaultML CE — All Rights Reserved.</p>
        <p class="text-gray-400 dark:text-gray-500">
          developed and maintained by
          <a
            href="https://alldaydev.com"
            target="_blank"
            :class="`${theme.colorClasses.text} hover:underline`"
          >
            All-Day Developer
          </a>
        </p>
      </div>
    </footer>

    <!-- Global UI Components -->
    <NotificationContainer />
    <ModalContainer />
  </div>
</template>

<script setup lang="ts">
const theme = useThemeStore();

onMounted(() => {
  theme.initializeTheme();
});
</script>
