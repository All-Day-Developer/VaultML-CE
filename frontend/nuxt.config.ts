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

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  ssr: false,
  nitro: {
    prerender: {
      routes: ['/']
    },
    devProxy: {
      "/api": {
        target: "http://localhost:8000/api", // FastAPI backend
        changeOrigin: true,
        prependPath: true,
      },
    },
  },

  runtimeConfig: {
    public: {
      apiBase: "/api",
    },
  },
  pinia: { storesDirs: ["./app/stores"] },
  modules: ["@nuxtjs/tailwindcss", "@pinia/nuxt"],
});

