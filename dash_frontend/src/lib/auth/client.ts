'use client';

import type { User } from '@/types/user';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? '';

function ensureApiBaseUrl(): string {
  if (!API_BASE_URL) throw new Error('NEXT_PUBLIC_API_BASE_URL is not set');
  return API_BASE_URL.endsWith('/') ? API_BASE_URL : API_BASE_URL + '/';
}

export interface SignInWithOAuthParams {
  code: string;
}

class AuthClient {
  private async callMe(): Promise<User | null> {
    const base = ensureApiBaseUrl();
    const url = new URL('user/me', base);
    const response = await fetch(url.toString(), {
      method: 'GET',
      credentials: 'include',
    });

    if (response.status === 401) {
      return null;
    }

    if (!response.ok) {
      throw new Error(`Failed to fetch current user: ${response.statusText}`);
    }

    const data = (await response.json()) as { athlete_id: number };
    return {
      id: String(data.athlete_id),
      name: 'Strava athlete',
    };
  }

  async signInWithOAuth({ code }: SignInWithOAuthParams): Promise<{ data?: User | null; error?: string }> {
    try {
      if (!code) {
        return { error: 'No authorization code provided' };
      }

      const base = ensureApiBaseUrl();
      const endpoint = new URL('user/login', base);
      endpoint.searchParams.append('access_code', code);

      const response = await fetch(endpoint.toString(), {
        method: 'GET',
        credentials: 'include',
      });

      if (!response.ok) {
        return { error: `Login request failed: ${response.statusText}` };
      }

      const user = await this.callMe();
      return { data: user };
    } catch (error) {
      console.error('OAuth sign-in failed:', error);
      return { error: error instanceof Error ? error.message : 'Failed to sign in' };
    }
  }

  async getUser(): Promise<{ data?: User | null; error?: string }> {
    try {
      const user = await this.callMe();
      return { data: user };
    } catch (error) {
      console.error('Failed to fetch user:', error);
      return { error: error instanceof Error ? error.message : 'Failed to fetch user' };
    }
  }

  async signOut(): Promise<{ error?: string }> {
    try {
      const base = ensureApiBaseUrl();
      const url = new URL('user/logout', base);
      const response = await fetch(url.toString(), {
        method: 'POST',
        credentials: 'include',
      });

      if (!response.ok) {
        return { error: `Logout failed: ${response.statusText}` };
      }

      return {};
    } catch (error) {
      console.error('Sign out failed:', error);
      return { error: 'Failed to sign out properly' };
    }
  }
}

export const authClient = new AuthClient();