import React, { Suspense } from 'react';
import LoginSuccessClient from './LoginSuccessClient';

export default function Page() {
  return (
    <Suspense fallback={<div>Authenticating...</div>}>
      <LoginSuccessClient />
    </Suspense>
  );
}
