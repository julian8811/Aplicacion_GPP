import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface EvaluationDraft {
  pa: Record<string, Record<string, number>>
  po: Record<string, Record<string, number>>
  lastSaved: string | null
}

interface DraftStore {
  paDraft: EvaluationDraft['pa']
  poDraft: EvaluationDraft['po']
  lastSaved: string | null
  setPADraft: (draft: Record<string, Record<string, number>>) => void
  setPODraft: (draft: Record<string, Record<string, number>>) => void
  clearDrafts: () => void
}

export const useDraftStore = create<DraftStore>()(
  persist(
    (set) => ({
      paDraft: {},
      poDraft: {},
      lastSaved: null,
      setPADraft: (draft) => set({ 
        paDraft: draft, 
        lastSaved: new Date().toISOString() 
      }),
      setPODraft: (draft) => set({ 
        poDraft: draft, 
        lastSaved: new Date().toISOString() 
      }),
      clearDrafts: () => set({ 
        paDraft: {}, 
        poDraft: {}, 
        lastSaved: null 
      }),
    }),
    {
      name: 'gpp-evaluation-draft',
    }
  )
)