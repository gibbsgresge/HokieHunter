import React from 'react';

const UserCard = ({ user, onDelete }) => (
  <div className="user-card">
    <p><strong>Name:</strong> {user.name}</p>
    <p><strong>Email:</strong> {user.email}</p>
    <button onClick={() => alert("Update form coming soon!")}>✏️</button>
    <button onClick={() => onDelete(user.id)}>🗑️</button>
  </div>
);

export default UserCard;
