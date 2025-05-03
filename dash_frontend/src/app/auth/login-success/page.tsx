'use client'

import { useSearchParams } from 'next/navigation';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth/client';
import { useEffect, useState } from 'react';

export default function Page() {
  const params = useSearchParams();
  const code = params.get("code");
  const router = useRouter();
  const [isProcessing, setIsProcessing] = useState(true);
  const [error, setError] = useState<string | null>(null);
  console.log("error", error);
  useEffect(() => {
    async function handleAuth() {
      // Check if code is missing and exit early
      console.log("handinglin auth");
      if (!code) {
        console.error("No code provided in URL parameters.");
        setError("No authorization code found in URL");
        setIsProcessing(false);
        return;
      }
      
      try {
        console.log("Starting authentication with code:", code);
        
        // Sign in and get session data
        const result = await authClient.signInWithOAuth({
          code: code,
        });
        
        if (result.error) {
          console.error("Auth error:", result.error);
          setError(result.error);
          setIsProcessing(false);
          return;
        }

        console.log("Authentication successful, session:", result.data);
        
        // Force a small delay to ensure the session is saved properly
        setTimeout(() => {
          // After successful authentication
          router.push('/dashboard');
          // In case router.push doesn't trigger immediately, set processing to false
          setTimeout(() => setIsProcessing(false), 500);
        }, 100);
        
      } catch (err) {
        console.error("Failed to authenticate:", err);
        setError(err instanceof Error ? err.message : String(err));
        setIsProcessing(false);
      }
    }
    
    handleAuth();
  }, [code, router]);

  // Show loading state
  if (isProcessing) {
    return <div>Authenticating...</div>;
  }
  
  if (error) {
    return (
      <div>
        <h2>Authentication Error</h2>
        <p>{error}</p>
        <button onClick={() => router.push('/auth/sign-in')}>
          Return to Sign In
        </button>
      </div>
    );
  }

  return <div>Redirecting to dashboard...</div>;
}
