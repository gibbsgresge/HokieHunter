// src/entityConfig.js
export const entityConfig = {
    users: {
      fields: ['Email', 'Role'], // fields used in CrudDialog
      idKey: 'UserID'
    },
    properties: {
      fields: ['Name', 'Location', 'Price', 'RoomType'],
      idKey: 'PropertyID'
    },
    // For future expansions: reviews, favorites, etc.
  }
  