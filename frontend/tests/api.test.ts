/**
 * React Query integration tests.
 * Tests API hooks with mocked responses.
 *
 * Note: Full integration testing requires MSW (Mock Service Worker)
 * or a similar API mocking library. This file provides the test structure.
 */
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useEvaluations } from '../src/hooks/useApi'

// Create wrapper for React Query hooks
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        // Short timeout for tests
        staleTime: 1000,
      },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('useEvaluations hook', () => {
  test('hook exists and can be rendered', () => {
    const { result } = renderHook(() => useEvaluations(), {
      wrapper: createWrapper(),
    })

    // Hook should return an object with data, isLoading, error
    expect(result.current).toHaveProperty('data')
    expect(result.current).toHaveProperty('isLoading')
    expect(result.current).toHaveProperty('error')
  })

  test('initial state has no data', () => {
    const { result } = renderHook(() => useEvaluations(), {
      wrapper: createWrapper(),
    })

    // Initially data should be undefined (not yet fetched)
    expect(result.current.data).toBeUndefined()
  })
})

// Example of how MSW would be set up (requires additional deps):
/*
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

const server = setupServer(
  http.get('/api/evaluations', () => {
    return HttpResponse.json([
      {
        id: '1',
        nombre_establecimiento: 'Test Restaurant',
        fecha: '2026-05-01',
        general_pct: 75.5,
        pa_pct: 78.0,
        po_pct: 73.0,
      }
    ])
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

test('useEvaluations returns data', async () => {
  const { result } = renderHook(() => useEvaluations(), {
    wrapper: createWrapper(),
  })

  await waitFor(() => expect(result.current.isSuccess).toBe(true))

  expect(result.current.data).toHaveLength(1)
  expect(result.current.data[0].nombre_establecimiento).toBe('Test Restaurant')
})
*/