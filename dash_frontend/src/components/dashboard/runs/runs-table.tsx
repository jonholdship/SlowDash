'use client';

import * as React from 'react';
import { Box, Divider } from '@mui/material';
import Card from '@mui/material/Card';
import {Run} from '@/types/run'
import Stack from '@mui/material/Stack';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { getRuns } from '@/api/api_call';
import { RunDetail } from '@/components/dashboard/runs/run-detail';
function noop(): void {
  // do nothing
}
import { ArrowsClockwise as SyncIcon } from '@phosphor-icons/react/dist/ssr/ArrowsClockwise';

import { CustomersFilters } from '@/components/dashboard/runs/customers-filters';

interface CustomersTableProps {
  count?: number;
  rows: Run[];
  page?: number;
  rowsPerPage?: number;
  pageSetter: Function;
  runId: number;
  runSetter: Function;

}


export default async function RunsTablePage(): Promise<React.JSX.Element> {
	const [runId, setRun] = React.useState(1);
  const [page, setPage] = React.useState(1);
  const rowsPerPage = 5;
  const runs = await getRuns();

  const paginatedRuns = applyPagination(runs, page, rowsPerPage);
  return (
    <Stack spacing={3}>
      <Stack direction="row" spacing={3}>
        <Stack spacing={1} sx={{ flex: '1 1 auto' }}>
          <Typography variant="h4">Runs</Typography>
        </Stack>
        <div>
          <Button startIcon={<SyncIcon fontSize="var(--icon-fontSize-md)" />} variant="contained">
            Sync
          </Button>
        </div>
      </Stack>
      <CustomersFilters />
      <RunsTable
        count={runs.length}
        page={page}
        rows={paginatedRuns}
        rowsPerPage={rowsPerPage}
        pageSetter={setPage}
        runId={runId}
        runSetter={setRun}
      />
      <RunDetail runId={runId} />
    </Stack>
  );
}

function applyPagination(rows: Run[], page: number, rowsPerPage: number): Run[] {
  return rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
}



export function RunsTable({
  count = 0,
  rows,
  page = 0,
  rowsPerPage = 0,
  pageSetter,
  runId,
  runSetter,
}: CustomersTableProps): React.JSX.Element {

  const rowIds = React.useMemo(() => {
    return rows.map((run) => run.id);
  }, [rows]);


  return (
    <Card>
      <Box sx={{ overflowX: 'auto' }}>
        <Table sx={{ minWidth: '800px' }}>
          <TableHead>
            <TableRow>

              <TableCell>Name</TableCell>
              <TableCell>Distance</TableCell>
              <TableCell>Pace</TableCell>
              <TableCell>Average HR</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => {
              const isSelected = (String(runId)==row.id);

              return (
                <TableRow hover key={row.id} selected={isSelected} onClick={(event) => runSetter(row.id)}>
                  <TableCell>
                    <Stack sx={{ alignItems: 'center' }} direction="row" spacing={2}>
                      <Typography variant="subtitle2">{row.name}</Typography>
                    </Stack>
                  </TableCell>
                  <TableCell>{row.distance}</TableCell>
                  <TableCell>
                    {row.pace}
                  </TableCell>
                  <TableCell>{row.average_hr}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Box>
      <Divider />
      <TablePagination
        component="div"
        count={count}
        onPageChange={(event,page) => pageSetter(page)}
        onRowsPerPageChange={noop}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
}
