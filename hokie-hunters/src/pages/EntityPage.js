// src/pages/EntityPage.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  CircularProgress,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Box
} from '@mui/material';

function EntityPage() {
  const { entityName } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const endpointMap = {
            property: 'property',
            leasetransfer: 'leasetransfer',
            review: 'review',
            favorite: 'favorite',
            roommatesearch: 'roommatesearch',
            commute: 'commute',
            movingservices: 'movingservices',
            safetyfeatures: 'safetyfeatures'
          };
          
          const res = await fetch(`http://localhost:5000/${endpointMap[entityName]}`);
          
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [entityName]);

  if (loading) return <CircularProgress sx={{ mt: 10 }} />;
  if (!data || data.length === 0) return <Typography>No data found.</Typography>;

  const headers = Object.keys(data[0]);

  return (
    <Container maxWidth="lg" sx={{ mt: 8 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 600 }}>
        {entityName.charAt(0).toUpperCase() + entityName.slice(1)} Entries
      </Typography>
      <Paper elevation={3}>
        <Box sx={{ overflowX: 'auto' }}>
          <Table>
            <TableHead>
              <TableRow>
                {headers.map((header) => (
                  <TableCell key={header}>{header}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((entry, idx) => (
                <TableRow key={idx}>
                  {headers.map((field) => (
                    <TableCell key={field}>{entry[field]}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </Paper>
    </Container>
  );
}

export default EntityPage;
