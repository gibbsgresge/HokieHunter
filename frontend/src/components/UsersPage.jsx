import React, { useEffect, useState } from 'react';
import { getUsers, deleteUser } from '../api/users';
import UserCard from './UserCard';

const UsersPage = () => {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const data = await getUsers();
    setUsers(data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleDelete = async (id) => {
    await deleteUser(id);
    fetchUsers();
  };

  return (
    <div>
      <h2>Users</h2>
      <button onClick={() => alert("Insert form coming soon!")}>Insert User</button>
      <div>
        {users.map(user => (
          <UserCard key={user.id} user={user} onDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
};

export default UsersPage;
