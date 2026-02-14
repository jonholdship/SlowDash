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
import { getRuns } from '@/api/api-call';
import { RunDetail } from '@/components/dashboard/runs/run-detail';
import { authClient } from '@/lib/auth/client';
import { ArrowsClockwise as SyncIcon } from '@phosphor-icons/react/dist/ssr/ArrowsClockwise';

function noop(): void {
  // do nothing
}

interface CustomersTableProps {
  count?: number;
  rows: Run[];
  page?: number;
  rowsPerPage?: number;
  pageSetter: Function;
  rowsPerPageSetter: Function;
  runId: number;
  runSetter: Function;
}

// Client component wrapper for data fetching
export default function RunsTableWrapper(): React.JSX.Element {
  const [runId, setRun] = React.useState<number>(1);
  const [page, setPage] = React.useState<number>(0);
  const [rowsPerPage, setRowsPerPage] = React.useState<number>(20);
  const [runs, setRuns] = React.useState<Run[]>([]);
  const [isLoading, setIsLoading] = React.useState<boolean>(true);

  // Handle sync button click - refresh data
  const handleSync = React.useCallback(() => {
    setIsLoading(true);
    fetchRuns();
  }, []);

  // Function to fetch runs with authentication
  const fetchRuns = React.useCallback(async () => {
    try {
      const token = await authClient.getToken();
      const runsData = await getRuns(token);
      setRuns(runsData);
    } catch (error) {
      console.error("Failed to fetch runs:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Fetch data on component mount
  React.useEffect(() => {
    fetchRuns();
  }, [fetchRuns]);

  // Apply pagination to the runs data
  const paginatedRuns = React.useMemo(() => {
    return runs.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);
  }, [runs, page, rowsPerPage]);

  if (isLoading) {
    return <div>Loading runs data...</div>;
  }

  return (
    <Stack spacing={3}>
      <Stack direction="row" spacing={3}>
        <Stack spacing={1} sx={{ flex: '1 1 auto' }}>
          <Typography variant="h4">Runs</Typography>
        </Stack>
        <div>
          <Button 
            startIcon={<SyncIcon fontSize="var(--icon-fontSize-md)" />} 
            variant="contained"
            onClick={handleSync}
          >
            Sync
          </Button>
        </div>
      </Stack>
      <RunsTable
        count={runs.length}
        page={page}
        rows={paginatedRuns}
        rowsPerPage={rowsPerPage}
        pageSetter={setPage}
        rowsPerPageSetter={setRowsPerPage}
        runId={runId}
        runSetter={setRun}
      />
      <RunDetail runId={runId} />
    </Stack>
  );
}

// Stateless component to display the runs table
export function RunsTable({
  count = 0,
  rows,
  page = 0,
  rowsPerPage = 0,
  pageSetter,
  rowsPerPageSetter,
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
              <TableCell>Run Date</TableCell>
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
                  <TableCell>{row.start_date}</TableCell>
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
        onRowsPerPageChange={(event) => rowsPerPageSetter(event.target.value)}
        page={page}
        rowsPerPage={rowsPerPage}
        rowsPerPageOptions={[5, 10, 25]}
      />
    </Card>
  );
}
