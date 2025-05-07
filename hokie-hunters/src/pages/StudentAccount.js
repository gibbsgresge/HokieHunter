import React, { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  TextField,
  MenuItem,
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
  const [properties, setProperties] = useState([]);
  const [roommateSearch, setRoommateSearch] = useState('');

  const [newLease, setNewLease] = useState({ PropertyID: '', LeaseEndDate: '', TransferStatus: '' });
  const [newReview, setNewReview] = useState({ PropertyID: '', Rating: '', Comments: '' });
  const [newFavorite, setNewFavorite] = useState({ PropertyID: '', Comments: '' });

  const [editingLease, setEditingLease] = useState(null);
  const [editingReview, setEditingReview] = useState(null);
  const [editingFavorite, setEditingFavorite] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/student/${studentId}/lease_transfers`).then(res => res.json()).then(setLeaseTransfers);
    fetch(`http://localhost:5000/student/${studentId}/reviews`).then(res => res.json()).then(setReviews);
    fetch(`http://localhost:5000/student/${studentId}/favorites`).then(res => res.json()).then(setFavorites);
    fetch(`http://localhost:5000/student/${studentId}/roommate_search`).then(res => res.json()).then(data => setRoommateSearch(data.Preferences || ''));
    fetch('http://localhost:5000/property').then(res => res.json()).then(setProperties);
  }, [studentId]);

  const refreshData = () => {
    fetch(`http://localhost:5000/student/${studentId}/lease_transfers`).then(res => res.json()).then(setLeaseTransfers);
    fetch(`http://localhost:5000/student/${studentId}/reviews`).then(res => res.json()).then(setReviews);
    fetch(`http://localhost:5000/student/${studentId}/favorites`).then(res => res.json()).then(setFavorites);
  };

  const handleLeaseCreate = async () => {
    await fetch('http://localhost:5000/lease_transfers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newLease, StudentID: studentId })
    });
    setNewLease({ PropertyID: '', LeaseEndDate: '', TransferStatus: '' });
    refreshData();
  };

  const handleLeaseDelete = async (id) => {
    await fetch(`http://localhost:5000/lease_transfers/${id}`, { method: 'DELETE' });
    refreshData();
  };

  const handleLeaseUpdate = async () => {
    await fetch(`http://localhost:5000/lease_transfers/${editingLease.TransferID}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        LeaseEndDate: editingLease.LeaseEndDate,
        TransferStatus: editingLease.TransferStatus
      })
    });
    setEditingLease(null);
    refreshData();
  };

  const handleReviewCreate = async () => {
    await fetch('http://localhost:5000/reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newReview, StudentID: studentId })
    });
    setNewReview({ PropertyID: '', Rating: '', Comments: '' });
    refreshData();
  };

  const handleReviewDelete = async (id) => {
    await fetch(`http://localhost:5000/reviews/${id}`, { method: 'DELETE' });
    refreshData();
  };

  const handleReviewUpdate = async () => {
    await fetch(`http://localhost:5000/reviews/${editingReview.ReviewID}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Rating: editingReview.Rating,
        Comments: editingReview.Comments
      })
    });
    setEditingReview(null);
    refreshData();
  };

  const handleFavoriteCreate = async () => {
    await fetch('http://localhost:5000/favorites', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newFavorite, StudentID: studentId })
    });
    setNewFavorite({ PropertyID: '', Comments: '' });
    refreshData();
  };

  const handleFavoriteDelete = async (id) => {
    await fetch(`http://localhost:5000/favorites/${id}`, { method: 'DELETE' });
    refreshData();
  };

  const handleFavoriteUpdate = async () => {
    await fetch(`http://localhost:5000/favorites/${editingFavorite.FavoriteID}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        Comments: editingFavorite.Comments
      })
    });
    setEditingFavorite(null);
    refreshData();
  };

  const handleRoommateUpdate = async () => {
    await fetch(`http://localhost:5000/student/${studentId}/roommate_search`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ Preferences: roommateSearch })
    });
  };

  return (
    <Container sx={{ mt: 10 }}>
      <Typography variant="h4" gutterBottom>Student Dashboard</Typography>

      {/* Roommate Preferences */}
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

      {/* Lease Transfers */}
      <Box mt={4}>
        <Typography variant="h6">Lease Transfers</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField
            select label="Property" value={newLease.PropertyID}
            onChange={(e) => setNewLease({ ...newLease, PropertyID: e.target.value })}
            fullWidth>
            <MenuItem value="">Select Property</MenuItem>
            {properties.map((p) => (
              <MenuItem key={p.PropertyID} value={p.PropertyID}>{p.Name}</MenuItem>
            ))}
          </TextField>
          <TextField label="Lease End Date" value={newLease.LeaseEndDate} onChange={(e) => setNewLease({ ...newLease, LeaseEndDate: e.target.value })} />
          <TextField label="Status" value={newLease.TransferStatus} onChange={(e) => setNewLease({ ...newLease, TransferStatus: e.target.value })} />
          <Button onClick={handleLeaseCreate} variant="contained">Add</Button>
        </Box>

        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Property</TableCell>
              <TableCell>End Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leaseTransfers.map(l => (
              <TableRow key={l.TransferID}>
                <TableCell>{l.PropertyName}</TableCell>
                <TableCell>
                  {editingLease?.TransferID === l.TransferID ? (
                    <TextField value={editingLease.LeaseEndDate} onChange={(e) => setEditingLease({ ...editingLease, LeaseEndDate: e.target.value })} />
                  ) : l.LeaseEndDate}
                </TableCell>
                <TableCell>
                  {editingLease?.TransferID === l.TransferID ? (
                    <TextField value={editingLease.TransferStatus} onChange={(e) => setEditingLease({ ...editingLease, TransferStatus: e.target.value })} />
                  ) : l.TransferStatus}
                </TableCell>
                <TableCell>
                  {editingLease?.TransferID === l.TransferID ? (
                    <Button size="small" onClick={handleLeaseUpdate}>Save</Button>
                  ) : (
                    <Button size="small" onClick={() => setEditingLease(l)}>Edit</Button>
                  )}
                  <Button size="small" color="error" onClick={() => handleLeaseDelete(l.TransferID)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
                 {/* Reviews */}
      <Box mt={4}>
        <Typography variant="h6">Reviews</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField select label="Property" value={newReview.PropertyID}
            onChange={(e) => setNewReview({ ...newReview, PropertyID: e.target.value })}
            fullWidth>
            <MenuItem value="">Select Property</MenuItem>
            {properties.map((p) => (
              <MenuItem key={p.PropertyID} value={p.PropertyID}>{p.Name}</MenuItem>
            ))}
          </TextField>
          <TextField label="Rating" value={newReview.Rating} onChange={(e) => setNewReview({ ...newReview, Rating: e.target.value })} />
          <TextField label="Comments" value={newReview.Comments} onChange={(e) => setNewReview({ ...newReview, Comments: e.target.value })} />
          <Button onClick={handleReviewCreate} variant="contained">Add</Button>
        </Box>
        <Table>
          <TableHead>
            <TableRow><TableCell>Property</TableCell><TableCell>Rating</TableCell><TableCell>Comments</TableCell><TableCell>Actions</TableCell></TableRow>
          </TableHead>
          <TableBody>
            {reviews.map(r => (
              <TableRow key={r.ReviewID}>
                <TableCell>{r.PropertyName}</TableCell>
                <TableCell>
                  {editingReview?.ReviewID === r.ReviewID ? (
                    <TextField value={editingReview.Rating} onChange={(e) => setEditingReview({ ...editingReview, Rating: e.target.value })} />
                  ) : r.Rating}
                </TableCell>
                <TableCell>
                  {editingReview?.ReviewID === r.ReviewID ? (
                    <TextField value={editingReview.Comments} onChange={(e) => setEditingReview({ ...editingReview, Comments: e.target.value })} />
                  ) : r.Comments}
                </TableCell>
                <TableCell>
                  {editingReview?.ReviewID === r.ReviewID ? (
                    <Button size="small" onClick={handleReviewUpdate}>Save</Button>
                  ) : (
                    <Button size="small" onClick={() => setEditingReview(r)}>Edit</Button>
                  )}
                  <Button size="small" color="error" onClick={() => handleReviewDelete(r.ReviewID)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>

      {/* Favorites */}
      <Box mt={4}>
        <Typography variant="h6">Favorites</Typography>
        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
          <TextField select label="Property" value={newFavorite.PropertyID}
            onChange={(e) => setNewFavorite({ ...newFavorite, PropertyID: e.target.value })}
            fullWidth>
            <MenuItem value="">Select Property</MenuItem>
            {properties.map((p) => (
              <MenuItem key={p.PropertyID} value={p.PropertyID}>{p.Name}</MenuItem>
            ))}
          </TextField>
          <TextField label="Comments" value={newFavorite.Comments} onChange={(e) => setNewFavorite({ ...newFavorite, Comments: e.target.value })} />
          <Button onClick={handleFavoriteCreate} variant="contained">Add</Button>
        </Box>
        <Table>
          <TableHead>
            <TableRow><TableCell>Property</TableCell><TableCell>Comments</TableCell><TableCell>Actions</TableCell></TableRow>
          </TableHead>
          <TableBody>
            {favorites.map(f => (
              <TableRow key={f.FavoriteID}>
                <TableCell>{f.PropertyName}</TableCell>
                <TableCell>
                  {editingFavorite?.FavoriteID === f.FavoriteID ? (
                    <TextField value={editingFavorite.Comments} onChange={(e) => setEditingFavorite({ ...editingFavorite, Comments: e.target.value })} />
                  ) : f.Comments}
                </TableCell>
                <TableCell>
                  {editingFavorite?.FavoriteID === f.FavoriteID ? (
                    <Button size="small" onClick={handleFavoriteUpdate}>Save</Button>
                  ) : (
                    <Button size="small" onClick={() => setEditingFavorite(f)}>Edit</Button>
                  )}
                  <Button size="small" color="error" onClick={() => handleFavoriteDelete(f.FavoriteID)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
      
    </Container>
  );
};

export default StudentAccount;
