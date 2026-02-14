'use client'

import React from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth/client';
import { useEffect, useState } from 'react';

export default function LoginSuccessClient(): JSX.Element {
  const params = useSearchParams();
  const code = params.get('code');
  const router = useRouter();
  const [isProcessing, setIsProcessing] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function handleAuth() {
      if (!code) {
        setError('No authorization code found in URL');
        setIsProcessing(false);
        return;
      }

      try {
        const result = await authClient.signInWithOAuth({ code });
        if (result.error) {
          setError(result.error);
          setIsProcessing(false);
          return;
        }

        // Navigate to dashboard after sign in
        setTimeout(() => {
          void router.push('/dashboard');
          setTimeout(() => setIsProcessing(false), 500);
        }, 100);
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err));
        setIsProcessing(false);
      }
    }

    void handleAuth();
  }, [code, router]);

  if (isProcessing) return <div>Authenticating...</div>;

  if (error) {
    return (
      <div>
        <h2>Authentication Error</h2>
        <p>{error}</p>
        <button type="button" onClick={() => { void router.push('/auth/sign-in'); }}>
          Return to Sign In
        </button>
      </div>
    );
  }

  return <div>Redirecting to dashboard...</div>;
}
