import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
    persist(
        (set, get) => ({
            user: null,
            token: null,
            githubToken: null,
            isAuthenticated: false,
            _hasHydrated: false,

            setHasHydrated: (state) => {
                set({ _hasHydrated: state });
            },

            login: (userData, jwtToken, ghToken) => {
                console.log('🔐 Auth Store - Setting login state:', {
                    user: userData?.login || userData?.username,
                    hasToken: !!jwtToken,
                    hasGhToken: !!ghToken
                });

                const newState = {
                    user: userData,
                    token: jwtToken,
                    githubToken: ghToken,
                    isAuthenticated: true
                };

                set(newState);

                // Force save to localStorage immediately
                try {
                    const storageData = {
                        state: newState,
                        version: 0
                    };
                    localStorage.setItem('auth-storage', JSON.stringify(storageData));
                    console.log('💾 Forced save to localStorage');
                } catch (e) {
                    console.error('Failed to save to localStorage:', e);
                }

                // Verify the state was set
                setTimeout(() => {
                    const state = get();
                    console.log('🔐 Auth Store - State after login:', {
                        isAuthenticated: state.isAuthenticated,
                        hasUser: !!state.user
                    });
                }, 50);
            },

            logout: () => {
                set({
                    user: null,
                    token: null,
                    githubToken: null,
                    isAuthenticated: false
                });
            },

            updateUser: (userData) => {
                set({ user: { ...get().user, ...userData } });
            }
        }),
        {
            name: 'auth-storage',
            onRehydrateStorage: () => (state) => {
                console.log('💧 Zustand hydration complete:', {
                    isAuthenticated: state?.isAuthenticated,
                    hasUser: !!state?.user
                });
                state?.setHasHydrated(true);
            }
        }
    )
);

export default useAuthStore;
