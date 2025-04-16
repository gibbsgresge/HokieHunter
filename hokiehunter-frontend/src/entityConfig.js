export const entityConfig = {
  users: {
    fields: ['Email', 'Role'],
    idKey: 'UserID',
  },
  students: {
    fields: ['Major', 'GraduationYear'],
    idKey: 'StudentID',
  },
  landlords: {
    fields: [],
    idKey: 'LandlordID',
  },
  admin: {
    fields: ['Permissions'],
    idKey: 'AdminID',
  },
  property: {
    fields: ['Name', 'Location', 'Price', 'RoomType'],
    idKey: 'PropertyID',
  },
  review: {
    fields: ['StudentID', 'PropertyID', 'Rating', 'Comments'],
    idKey: 'ReviewID',
  },
  favorite: {
    fields: ['StudentID', 'PropertyID', 'DateSaved', 'Comments'],
    idKey: 'FavoriteID',
  },
  leasetransfer: {
    fields: ['StudentID', 'PropertyID', 'LeaseEndDate', 'TransferStatus'],
    idKey: 'TransferID',
  },
  lease_transfer: {
    fields: ['transfer_details', 'student_id', 'property_id'],
    idKey: 'lease_transfer_id',
  },
  list: {
    fields: ['PropertyID', 'AvailableFrom', 'Status'],
    idKey: 'ListID',
  },
  amenities: {
    fields: ['ListID', 'Type'],
    idKey: 'AmenityID',
  },
  roommatesearch: {
    fields: ['StudentID', 'Preferences'],
    idKey: 'SearchID',
  },
  roommate_search: {
    fields: ['preferences', 'student_id'],
    idKey: 'roommate_search_id',
  },
  commute: {
    fields: ['PropertyID', 'Time', 'Distance', 'ServiceID'],
    idKey: 'CommuteID',
  },
  movingservices: {
    fields: ['PropertyID', 'CompanyName', 'ContactInfo'],
    idKey: 'ServiceID',
  },
  safetyfeatures: {
    fields: ['PropertyID', 'FeatureDescription'],
    idKey: 'FeatureID',
  },
  safety_features: {
    fields: ['feature_name', 'property_id'],
    idKey: 'safety_feature_id',
  },
  message: {
    fields: ['SenderID', 'Content', 'Timestamp'],
    idKey: 'MessageID',
  },
}
