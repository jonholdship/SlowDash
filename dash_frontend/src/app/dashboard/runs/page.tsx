import * as React from 'react';
import type { Metadata } from 'next';
import { config } from '@/config';

import  RunsTablePage from '@/components/dashboard/runs/runs-table';

export const metadata = { title: `Runs | Dashboard | ${config.site.name}` } satisfies Metadata;





export default function Page(): React.JSX.Element {

  return (
    <React.Suspense>
      <RunsTablePage/>
    </React.Suspense>
  );
}

