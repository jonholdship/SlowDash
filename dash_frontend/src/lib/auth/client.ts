'use client';

import type { User } from '@/types/user';
import { getTokenFromCode } from '@/api/api-call';
import { BehaviorSubject } from 'rxjs';

// Define Session interface
export interface Session {
  accessToken: string;
  expiresAt?: number; // Unix timestamp in seconds
  refreshToken?: string;
  user?: User;
}

export interface SignUpParams {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
}

export interface SignInWithOAuthParams {
  code: string;
}

export interface SignInWithPasswordParams {
  email: string;
  password: string;
}

export interface ResetPasswordParams {
  email: string;
}

const STORAGE_KEY = 'auth-session';

class AuthClient {
  private session$ = new BehaviorSubject<Session | null>(null);
  private refreshTokenTimeout: NodeJS.Timeout | null = null;

  constructor() {
    // Initialize on client side only
    if (typeof window !== 'undefined') {
      this.loadSession();
    }
  }

  private loadSession(): void {
    const sessionStr = localStorage.getItem(STORAGE_KEY);
    if (sessionStr) {
      try {
        const session = JSON.parse(sessionStr) as Session;
        
        // Check if session is expired
        if (session.expiresAt && session.expiresAt < Math.floor(Date.now() / 1000)) {
          this.clearSession();
        } else {
          this.session$.next(session);
        }
      } catch (error) {
        console.error('Failed to parse session from storage:', error);
        this.clearSession();
      }
    }
  }

  private saveSession(session: Session): void {
    // Store in localStorage for client-side access
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    
    // Also store token in cookie for server-side access
    document.cookie = `auth-token=${session.accessToken}; path=/; max-age=${
      session.expiresAt ? session.expiresAt - Math.floor(Date.now() / 1000) : 3600
    }; SameSite=Strict; Secure`;
    
    this.session$.next(session);
  }

  private clearSession(): void {
    localStorage.removeItem(STORAGE_KEY);
    
    // Clear the cookie too
    document.cookie = 'auth-token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict; Secure';
    
    this.session$.next(null);
    if (this.refreshTokenTimeout) {
      clearTimeout(this.refreshTokenTimeout);
      this.refreshTokenTimeout = null;
    }
  }



  async signInWithOAuth({ code }: SignInWithOAuthParams): Promise<{ data?: Session; error?: string }> {
    try {
      if (!code) {
        return { error: 'No authorization code provided' };
      }
      const tokenResponse = await getTokenFromCode(code);
      
      // Assuming getTokenFromCode returns at minimum an access token
      // and potentially refresh_token, expires_in, etc.
      const session: Session = {
        accessToken: tokenResponse,
        expiresAt: Date.now() + 3600 * 1000, // Assuming token is valid for 1 hour
      };

      this.saveSession(session);
      return { data: session };
    } catch (error) {
      console.error('OAuth sign-in failed:', error);
      return { error: error instanceof Error ? error.message : 'Failed to sign in' };
    }
  }



  async getSession(): Promise<{ data: { session: Session | null }; error?: string }> {
    return { data: { session: this.session$.value } };
  }

  onSessionChange(callback: (session: Session | null) => void): { unsubscribe: () => void } {
    const subscription = this.session$.subscribe(callback);
    return {
      unsubscribe: () => subscription.unsubscribe()
    };
  }

  async getUser(): Promise<{ data?: User | null; error?: string }> {
    const session = this.session$.value;
    if (!session || !session.accessToken) {
      return { data: null };
    }

    // If we have the user in the session
    if (session.user) {
      return { data: session.user };
    }
    
    // Create a minimal user object if we have a token but no user
    return { 
      data: { 
        id: 'authenticated-user',  // Placeholder ID
        name: 'authenticated-user', // Placeholder name
      } 
    };
  }

  async getToken(): Promise<string | null> {
    const session = this.session$.value;
    return session?.accessToken || null;
  }

  async signOut(): Promise<{ error?: string }> {
    try {
 
      this.clearSession();
      return {};
    } catch (error) {
      console.error('Sign out failed:', error);
      return { error: 'Failed to sign out properly' };
    }
  }
}

export const authClient = new AuthClient();