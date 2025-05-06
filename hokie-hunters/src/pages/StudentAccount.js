// src/pages/StudentAccount.js
import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody
} from '@mui/material';

const StudentAccount = () => {
  const studentId = localStorage.getItem('user_id');

  const [leaseTransfers, setLeaseTransfers] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [roommateSearch, setRoommateSearch] = useState('');
  const [newLease, setNewLease] = useState({ PropertyID: '', LeaseEndDate: '', TransferStatus: '' });
  const [newReview, setNewReview] = useState({ PropertyID: '', Rating: '', Comments: '' });
  const [newFavorite, setNewFavorite] = useState({ PropertyID: '', Comments: '' });

  useEffect(() => {
    fetch(`/student/${studentId}/lease_transfers`).then(res => res.json()).then(setLeaseTransfers);
    fetch(`/student/${studentId}/reviews`).then(res => res.json()).then(setReviews);
    fetch(`/student/${studentId}/favorites`).then(res => res.json()).then(setFavorites);
    fetch(`/student/${studentId}/roommate_search`).then(res => res.json()).then(data => setRoommateSearch(data.Preferences || ''));
  }, [studentId]);

  const handleLeaseCreate = async () => {
    await fetch('/lease_transfers', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newLease, StudentID: studentId })
    });
    setNewLease({ PropertyID: '', LeaseEndDate: '', TransferStatus: '' });
    fetch(`/student/${studentId}/lease_transfers`).then(res => res.json()).then(setLeaseTransfers);
  };

  const handleReviewCreate = async () => {
    await fetch('/reviews', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newReview, StudentID: studentId })
    });
    setNewReview({ PropertyID: '', Rating: '', Comments: '' });
    fetch(`/student/${studentId}/reviews`).then(res => res.json()).then(setReviews);
  };

  const handleFavoriteCreate = async () => {
    await fetch('/favorites', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newFavorite, StudentID: studentId })
    });
    setNewFavorite({ PropertyID: '', Comments: '' });
    fetch(`/student/${studentId}/favorites`).then(res => res.json()).then(setFavorites);
  };

  const handleRoommateUpdate = async () => {
    await fetch(`/student/${studentId}/roommate_search`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Preferences: roommateSearch })
    });
  };

  return (
    <Container sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>Student Dashboard</Typography>

      <Box mt={4}>
        <Typography variant="h6">Roommate Preferences</Typography>
        <TextField
          fullWidth
          label="Preferences"
          value={roommateSearch}
          onChange={(e) => setRoommateSearch(e.target.value)}
          onBlur={handleRoommateUpdate}
        />
      </Box>

      <Box mt={4}>
        <Typography variant="h6">Lease Transfers</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField label="Property ID" value={newLease.PropertyID} onChange={(e) => setNewLease({ ...newLease, PropertyID: e.target.value })} />
          <TextField label="Lease End Date" value={newLease.LeaseEndDate} onChange={(e) => setNewLease({ ...newLease, LeaseEndDate: e.target.value })} />
          <TextField label="Status" value={newLease.TransferStatus} onChange={(e) => setNewLease({ ...newLease, TransferStatus: e.target.value })} />
          <Button onClick={handleLeaseCreate} variant="contained">Add</Button>
        </Box>
        <Table><TableHead><TableRow><TableCell>Property ID</TableCell><TableCell>End Date</TableCell><TableCell>Status</TableCell></TableRow></TableHead><TableBody>{leaseTransfers.map(l => (<TableRow key={l.TransferID}><TableCell>{l.PropertyID}</TableCell><TableCell>{l.LeaseEndDate}</TableCell><TableCell>{l.TransferStatus}</TableCell></TableRow>))}</TableBody></Table>
      </Box>

      <Box mt={4}>
        <Typography variant="h6">Reviews</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField label="Property ID" value={newReview.PropertyID} onChange={(e) => setNewReview({ ...newReview, PropertyID: e.target.value })} />
          <TextField label="Rating" value={newReview.Rating} onChange={(e) => setNewReview({ ...newReview, Rating: e.target.value })} />
          <TextField label="Comments" value={newReview.Comments} onChange={(e) => setNewReview({ ...newReview, Comments: e.target.value })} />
          <Button onClick={handleReviewCreate} variant="contained">Add</Button>
        </Box>
        <Table><TableHead><TableRow><TableCell>Property ID</TableCell><TableCell>Rating</TableCell><TableCell>Comments</TableCell></TableRow></TableHead><TableBody>{reviews.map(r => (<TableRow key={r.ReviewID}><TableCell>{r.PropertyID}</TableCell><TableCell>{r.Rating}</TableCell><TableCell>{r.Comments}</TableCell></TableRow>))}</TableBody></Table>
      </Box>

      <Box mt={4}>
        <Typography variant="h6">Favorites</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField label="Property ID" value={newFavorite.PropertyID} onChange={(e) => setNewFavorite({ ...newFavorite, PropertyID: e.target.value })} />
          <TextField label="Comments" value={newFavorite.Comments} onChange={(e) => setNewFavorite({ ...newFavorite, Comments: e.target.value })} />
          <Button onClick={handleFavoriteCreate} variant="contained">Add</Button>
        </Box>
        <Table><TableHead><TableRow><TableCell>Property ID</TableCell><TableCell>Comments</TableCell></TableRow></TableHead><TableBody>{favorites.map(f => (<TableRow key={f.FavoriteID}><TableCell>{f.PropertyID}</TableCell><TableCell>{f.Comments}</TableCell></TableRow>))}</TableBody></Table>
      </Box>
    </Container>
  );
};

export default StudentAccount;
