import * as React from 'react';
import type { Metadata } from 'next';

import { config } from '@/config';
import { Layout } from '@/components/auth/layout';
import { SignInForm } from '@/components/auth/sign-in-form';

export const metadata = { title: `Sign in | ${config.site.name}` } satisfies Metadata;

export default function Page(): React.JSX.Element {
  console.log("I triggered")
  const { REACT_APP_CLIENT_ID } = process.env;

  const redirectUrl = "http://localhost:3000/auth/login-success";
  const scope = "read,activity:read";

  const stravaUrl=`http://www.strava.com/oauth/authorize?client_id=${REACT_APP_CLIENT_ID}&response_type=code&redirect_uri=${redirectUrl}&approval_prompt=force&scope=${scope}`;
  console.log(stravaUrl)  
  return (
    <Layout>
        <SignInForm stravaAuth={stravaUrl}/>
    </Layout>
  );
}
