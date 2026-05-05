import { create } from 'zustand'

export const useAppStore = create((set) => ({
  sidebarOpen: true,
  activeModule: 'dashboard',
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setActiveModule: (module) => set({ activeModule: module })
}))
