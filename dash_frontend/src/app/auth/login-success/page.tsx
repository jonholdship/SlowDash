'use client'

import { useSearchParams} from 'next/navigation';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth/client';

export default function Page(): void {
  let params = useSearchParams();
  let code = params.get("code");
  authClient.signInWithOAuth({code: code});
  const router = useRouter();
  router.push('/dashboard');
}
