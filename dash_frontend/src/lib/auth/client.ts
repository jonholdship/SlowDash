'use client';

import type { User } from '@/types/user';
import { getTokenFromCode } from '@/api/api_call';


const user = {
  id: 'USR-000',
  avatar: '/assets/avatar.png',
  firstName: 'Sofia',
  lastName: 'Rivers',
  email: 'sofia@devias.io',
} satisfies User;

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

class AuthClient {
  
  async signInWithOAuth({code}: SignInWithOAuthParams): Promise<{ error?: string }> {
    if (code){
      let token = await getTokenFromCode(code)
      localStorage.setItem('custom-auth-token',token)
    };
    return {};
  }


  async getUser(): Promise<{ data?: User | null; error?: string }> {
    // Make API request

    // We do not handle the API, so just check if we have a token in localStorage.
    const token = localStorage.getItem('custom-auth-token');

    if (!token) {
      return { data: null };
    }

    return { data: user };
  }

  async getToken(): Promise<string>{
    const token = localStorage.getItem('custom-auth-token');
    return token
  }

  async signOut(): Promise<{ error?: string }> {
    localStorage.removeItem('custom-auth-token');

    return {};
  }
}

export const authClient = new AuthClient();